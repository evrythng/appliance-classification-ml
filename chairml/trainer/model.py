# -*- coding: utf-8 -*-

# Copyright 2017 The TensorFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

"""Implements the Keras Sequential model."""

import ujson

import numpy as np
import tensorflow as tf
from keras import backend as K
from keras import regularizers
from keras.layers import Input, Conv1D,GlobalMaxPooling1D,Dense, MaxPool1D,Dropout, LSTM
from keras.models import Model, Sequential
from tensorflow.python.saved_model import builder as saved_model_builder
from tensorflow.python.saved_model import tag_constants, signature_constants
from tensorflow.python.saved_model.signature_def_utils_impl import predict_signature_def, classification_signature_def






def compile_model(model):
    model.compile(optimizer='adam',
                  loss='binary_crossentropy',
                  metrics=['accuracy'])
    return model


def model_fn_conv1d(input_shape, hidden_dim):
    model = Sequential()
    model.add(Conv1D(hidden_dim, 9, activation='relu', input_shape=input_shape))
    model.add(MaxPool1D(3))
    model.add(Conv1D(hidden_dim, 9, activation='relu'))
    model.add(Dropout(0.3))
    model.add(GlobalMaxPooling1D())
    model.add(Dense(1, activation='sigmoid'))  # SGD(lr=0.01, clipvalue=0.5) #adadelta
    return compile_model(model)

def model_fn(input_shape, hidden_dim):
    model = Sequential()
    model.add(LSTM(hidden_dim, input_shape=input_shape, activation='relu', return_sequences=True,
                   activity_regularizer=regularizers.l2(1e-05)))
    model.add(LSTM(hidden_dim, activation='relu', activity_regularizer=regularizers.l2(1e-05)))
    model.add(Dense(1, activation='sigmoid'))
    return compile_model(model)


def to_savedmodel(model, export_path):
    """Convert the Keras HDF5 model into TensorFlow SavedModel."""

    builder = saved_model_builder.SavedModelBuilder(export_path)

    # https://cloud.google.com/ml-engine/docs/v1/predict-request#multiple-input-tensors
    signature = predict_signature_def(inputs={'instances': model.inputs[0]},
                                      outputs={'predictions': model.outputs[0]})


    with K.get_session() as sess:
        builder.add_meta_graph_and_variables(
            sess=sess,
            tags=[tag_constants.SERVING],
            signature_def_map={
                signature_constants.DEFAULT_SERVING_SIGNATURE_DEF_KEY: signature}
        )
        builder.save()


def generator_input(input_file, batch_size=2):
    """Generator function to produce features and labels
       needed by keras fit_generator.
    """

    while True:
        with tf.gfile.Open(input_file[0], 'rb') as fd:
            data = ujson.load(fd)
        input_data, labels = data
        input_data, labels = np.array(input_data), np.array(labels)
        for i in range(0,len(input_data),batch_size):
            x = input_data[i:min(i+batch_size, len(input_data))]
            y = labels[i:min(i+batch_size, len(input_data))]
            yield x, y


