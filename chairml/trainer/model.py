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
from keras.layers import Input, Conv1D
from keras.models import Model
from tensorflow.python.saved_model import builder as saved_model_builder
from tensorflow.python.saved_model import tag_constants, signature_constants
from tensorflow.python.saved_model.signature_def_utils_impl import predict_signature_def


# Python2/3 compatibility imports
# from builtins import range


# # csv columns in the input file
# CSV_COLUMNS = ('age', 'workclass', 'fnlwgt', 'education', 'education_num',
#                'marital_status', 'occupation', 'relationship', 'race',
#                'gender', 'capital_gain', 'capital_loss', 'hours_per_week',
#                'native_country', 'income_bracket')
#
# CSV_COLUMN_DEFAULTS = [[0], [''], [0], [''], [0], [''], [''], [''], [''],
#                        [''], [0], [0], [0], [''], ['']]
#
# # Categorical columns with vocab size
# # native_country and fnlwgt are ignored
# CATEGORICAL_COLS = (('education', 16), ('marital_status', 7),
#                     ('relationship', 6), ('workclass', 9), ('occupation', 15),
#                     ('gender', [' Male', ' Female']), ('race', 5))
#
# CONTINUOUS_COLS = ('age', 'education_num', 'capital_gain', 'capital_loss',
#                    'hours_per_week')
#
# LABELS = [' <=50K', ' >50K']
# LABEL_COLUMN = 'income_bracket'
#
# UNUSED_COLUMNS = set(CSV_COLUMNS) - set(
#     list(zip(*CATEGORICAL_COLS))[0] + CONTINUOUS_COLS + (LABEL_COLUMN,))
#





def compile_model(model):
    model.compile(optimizer='adadelta', loss='mse',metrics=['accuracy'])
    return model


def model_fn(input_shape, hidden_dim):
    input_layer = Input(shape=input_shape)
    encoded = Conv1D(hidden_dim,1,activation='tanh')(input_layer)
    encoded = Conv1D(hidden_dim,1,activation='relu')(encoded)
    decoded = Conv1D(input_shape[-1],1,activation='relu')(encoded)
    return compile_model(Model(inputs=input_layer, outputs=decoded))


def to_savedmodel(model, export_path):
    """Convert the Keras HDF5 model into TensorFlow SavedModel."""

    builder = saved_model_builder.SavedModelBuilder(export_path)

    # https://cloud.google.com/ml-engine/docs/v1/predict-request#multiple-input-tensors
    signature = predict_signature_def(inputs={'inputs': model.inputs[0]},
                                      outputs={'predictions': model.outputs[0]})
    print(signature)

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
        input_data = np.array(ujson.load(tf.gfile.Open(input_file[0], 'rb')))


        for i in range(0,len(input_data),batch_size):
            x = input_data[i:min(i+batch_size, len(input_data))]
            yield x, x


