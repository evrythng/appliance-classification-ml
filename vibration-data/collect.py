from keras import models
from keras import layers
from keras import preprocessing

import matplotlib.pyplot as plt
import sklearn.utils
import numpy as np
import requests
import json
import os.path

x_train_file = 'x_train.json'
y_train_file = 'y_train.json'


def get_training_data():
    evrythng_url = 'https://api.evrythng.com'
    collection_id = 'U4dp2qmYBD8wQpRwwE7y7Epa'
    property_name = 'magnitude'
    trusted_api_key = ''

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": trusted_api_key}
    resp = requests.get('{}/collections/{}/thngs'.format(evrythng_url, collection_id), headers=headers)
    if resp.status_code != 200:
        raise SystemExit('failed to get collection thngs')

    threshold = 3
    permutations = 100
    initial_training_data = []
    x_training = []
    y_training = []
    max_len = 0

    for thng in resp.json():
        r = requests.get('{}/thngs/{}/properties/{}'.format(
            evrythng_url, thng['id'], property_name), headers=headers)
        if r.status_code != 200:
            continue

        m_props = r.json()
        for prop in m_props:
            m_hist = np.array(json.loads(prop['value']))
            initial_training_data.append(m_hist[:, 1:])
            if len(initial_training_data[-1]) > max_len:
                max_len = len(initial_training_data[-1])
            y_training.append((np.max(m_hist) - np.min(m_hist)) > threshold)


    x_training = preprocessing.sequence.pad_sequences(initial_training_data,
               maxlen=max_len, dtype='float32', padding='post')

    for arr in x_training:
        seq_amp = np.max(arr) - np.min(arr)
        for x in np.nditer(np.arange(permutations)):
            x_training = (np.vstack([x_training, [np.random.permutation(arr)]]))
            y_training.append(seq_amp > 3)

        print('{} {}'.format(np.shape(x_training), np.shape(y_training)))

    y_training = np.asarray(y_training).astype('float32')

    x_training, y_training = sklearn.utils.shuffle(x_training, y_training, random_state=0)

    return x_training, y_training


def get_untrained_model(len):
    model = models.Sequential()

    model.add(layers.Dense(16, activation='relu', input_shape=(len, 3)))
    model.add(layers.Dense(16, activation='relu'))
    model.add(layers.Dense(8, activation='relu'))
    model.add(layers.Flatten())
    model.add(layers.Dense(1, activation='sigmoid'))

    model.compile(optimizer='rmsprop',
                  #loss='binary_crossentropy',
                  loss='mse',
                  metrics=['accuracy'])
    model.summary()
    return model


if not os.path.isfile(x_train_file) or not os.path.isfile(y_train_file):
    x_training, y_training = get_training_data()
    json.dump(x_training.tolist(), open(x_train_file, 'w'))
    json.dump(y_training.tolist(), open(y_train_file, 'w'))
else:
    x_training = np.array(json.load(open(x_train_file)))
    y_training = np.array(json.load(open(y_train_file)))


'''
# normalizing
mean = x_training.mean()
std = x_training.std()

x_training -= mean
x_training /= std
'''


'''
# training model using K-folding algo
k = 5
num_val_samples = len(x_training) // k
num_epochs = 50
all_scores = []

for i in range(k):
    print('processing fold #', i)

    x_val = x_training[i * num_val_samples: (i + 1) * num_val_samples]
    y_val = y_training[i * num_val_samples: (i + 1) * num_val_samples]

    x_train = np.concatenate(
        [x_training[:i * num_val_samples],
         x_training[(i + 1) * num_val_samples:]],
        axis=0)

    y_train = np.concatenate(
        [y_training[:i * num_val_samples],
         y_training[(i + 1) * num_val_samples:]],
        axis=0)

    model = get_model(np.shape(x_train)[1])
    model.fit(x_train, y_train,
          epochs=num_epochs, batch_size=128, verbose=1)
    val_mse, val_mae = model.evaluate(x_val, y_val, verbose=0)
    all_scores.append(val_mae)

print('{} mean: {}'.format(all_scores, np.mean(all_scores)))
'''

total_num = np.shape(y_training)[0]
train_ratio = .85
val_ratio = .1

train_num = int(total_num * .85)
val_num = int(total_num * .1)
test_num = total_num - (train_num + val_num)

x_train = x_training[:train_num]
y_train = y_training[:train_num]
x_val = x_training[train_num:(train_num+val_num)]
y_val = y_training[train_num:(train_num+val_num)]
x_test = x_training[(train_num+val_num):]
y_test = y_training[(train_num+val_num):]

print('x_train: {}, y_train: {}'.format(np.shape(x_train), np.shape(y_train)))
print('x_val: {}, y_val: {}'.format(np.shape(x_val), np.shape(y_val)))
print('x_test: {}, y_test: {}'.format(np.shape(x_test), np.shape(y_test)))

model = get_untrained_model(np.shape(x_training)[1])
history = model.fit(x_train, y_train,
                    epochs=20,
                    batch_size=128,
                    validation_data=(x_val, y_val))

test_results = model.evaluate(x_test, y_test)
print('evaluating test samples: {}'.format(test_results))

model.save('trained_model.h5')

loss = history.history['loss']
val_loss = history.history['val_loss']
epochs = range(1, len(loss) + 1)

plt.figure(1)
plt.plot(epochs, loss, 'bo', label='Training loss')
plt.plot(epochs, val_loss, 'b', label='Validation loss')
plt.title('Training and validation loss')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()

plt.figure(2)
acc = history.history['acc']
val_acc = history.history['val_acc']
plt.plot(epochs, acc, 'bo', label='Training accuracy')
plt.plot(epochs, val_acc, 'b', label='Validation accuracy')
plt.title('Training and validation accuracy')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()

plt.show()
