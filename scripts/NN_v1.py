
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.python.keras.layers.core import Dropout
from keras.callbacks import EarlyStopping

def create_network(in_dim):
    model = Sequential()
    model.add(Dense(128, input_dim=in_dim, activation="relu"))
    model.add(Dropout(0.2))
    model.add(Dense(256, activation="relu"))
    model.add(Dropout(0.2))
    model.add(Dense(128, activation="relu"))
    model.add(Dropout(0.2))
    model.add(Dense(64, activation="relu"))
    model.add(Dense(1, activation="linear"))
    model.compile(optimizer="adam", loss="mse", metrics=["mae"])
    return model



