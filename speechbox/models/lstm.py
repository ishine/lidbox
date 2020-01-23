from tensorflow.keras.layers import (
    Activation,
    Dense,
    Input,
    LSTM,
)
from tensorflow.keras.models import Model
import tensorflow as tf
import numpy as np


def loader(input_shape, num_outputs, output_activation="softmax", num_units=1024):
    inputs = Input(shape=input_shape, name="input")
    lstm = LSTM(num_units, name="lstm")(inputs)
    outputs = Dense(num_outputs, name="output", activation=None)(lstm)
    if output_activation:
        outputs = Activation(getattr(tf.nn, output_activation), name=str(output_activation))(outputs)
    return Model(inputs=inputs, outputs=outputs)

def predict(model, utterances):
    return np.stack([model.predict(frames).mean(axis=0) for frames in utterances.unbatch()])
