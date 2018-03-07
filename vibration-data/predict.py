from keras.models import load_model
from keras import preprocessing

import paho.mqtt.client as mqtt
import numpy as np
import json

thng_id = 'UnVeKXbmeg8atKaRw2hmaGgs'
device_api_key = 'MDupaO0IxiEzC0mJ3rPT9LEO1rxsj3iJSFupEyNP9aFPjHcf57K61UL5M67R3U5GxJq6FEoxFLqTRnTQ'

model = load_model('trained_model.h5')


def on_connect(client, userdata, flags, rc):
    print("Connected with result code: " + str(rc))
    client.subscribe('/thngs/{}/properties/magnitude'.format(thng_id))


def on_log(client, userdata, level, buf):
    print('{}: {}'.format(level, buf))


def on_message(client, userdata, msg):
    js = json.loads(msg.payload.decode('utf-8'))
    print('{}'.format(js))


def on_magnitude(client, userdata, msg):
    js = json.loads(msg.payload.decode('utf-8'))
    values = np.array([json.loads(js[0]['value'])])
    values = values[:,:,1:]

    values = preprocessing.sequence.pad_sequences(
        values, maxlen=model.input_shape[1], dtype='float32', padding='post')

    print('original: {}'.format(values))

    '''
    # normalizing
    mean = values.mean()
    std = values.std()
    values -= mean
    values /= std
    '''
    prediction_value = model.predict([values]).flatten()[0]
    print('normalised: {}'.format(values))
    print('prediction: {}'.format(prediction_value))
    client.publish('/thngs/{}/properties/warning_level'.format(thng_id),
                   payload='[ {{"value": {} }} ]'.format(prediction_value))

client = mqtt.Client(client_id='anomally-predictor')
client.on_connect = on_connect
client.on_message = on_message
client.message_callback_add('/thngs/{}/properties/magnitude'.format(thng_id), on_magnitude)
client.on_log = on_log
client.tls_set('cert.pem')
client.username_pw_set('authorization', device_api_key)
client.connect("mqtt.evrythng.com", 443, 60)
client.loop_forever()
