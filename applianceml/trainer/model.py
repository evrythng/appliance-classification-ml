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

np.random.seed(42)
import tensorflow as tf
from keras import backend as K
from keras.layers import Dense, GRU, Conv1D, MaxPool1D, GlobalMaxPool1D, MaxPooling1D,Dropout,Flatten
from keras.models import Sequential
from tensorflow.python.saved_model import builder as saved_model_builder
from tensorflow.python.saved_model import tag_constants, signature_constants
from tensorflow.python.saved_model.signature_def_utils_impl import predict_signature_def

LOOKBACK = 96
CLASSES = 3
FEATURES = 4
INPUT_SHAPE = [LOOKBACK, FEATURES]


def compile_model(model):
    model.compile(optimizer='rmsprop',
                  loss='categorical_crossentropy',
                  metrics=['accuracy'])
    return model


def model_fn(input_shape, classes):
    model = Sequential()
    model.add(Conv1D(32, 3, input_shape=input_shape, activation='relu'))
    model.add(MaxPooling1D(3))
    model.add(Conv1D(32, 3, activation='relu'))
    model.add(MaxPooling1D(3))
    model.add(Conv1D(32, 3, activation='relu'))
    # model.add(GRU(128, dropout=0.1, recurrent_dropout=0.5, return_sequences=True))
    # model.add(GlobalMaxPool1D())
    model.add(GRU(24, dropout=0.1, recurrent_dropout=0.5, return_sequences=False))
    model.add(Dense(classes, activation='softmax'))
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


def generator_input(input_file, batch_size=32):
    """Generator function to produce features and labels
       needed by keras fit_generator.
    """

    while True:
        with tf.gfile.Open(input_file[0], 'rb') as fd:
            data = ujson.load(fd)
        input_data, labels = data
        input_data, labels = np.array(input_data), np.array(labels)
        for i in range(0, len(input_data), batch_size):
            x = input_data[i:min(i + batch_size, len(input_data))]
            y = labels[i:min(i + batch_size, len(input_data))]
            yield x, y
