import tensorflow as tf
from tensorflow import keras
from keras import layers


model = keras.Sequential(
    [
        layers.Dense(2,activation="relu"),
        layers.Dense(2,activation="relu"),
        layers.Dense(2,activation="relu")
    ]
)

x = tf.ones((3, 3))
y = model(x)
print(y)

