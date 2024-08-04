import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam
import Get_Data
import os


class Sort():
    def __init__(self):
        pass

    def add_arr(self, arr1, arr2):
        for i in range(len(arr2)):
            arr1.append(arr2[i])
        return arr1

    def generate_y(self, l, value):
        y = []
        for i in range(l):
            y.append([value])
        return y

    def sort_data(self):
        Data_X_Normal = []
        for file_name in os.listdir("Normal"):
            Data_X_Normal = self.add_arr(Data_X_Normal, Get_Data.Data("Normal/" + file_name, [1920, 1080],
                                                                 "Drag-GameStudio").get_player_input())
        Data_Y_Normal = self.generate_y(len(Data_X_Normal), 0)

        Data_X_Cheat = []
        for file_name in os.listdir("Cheat"):
            Data_X_Cheat = self.add_arr(Data_X_Cheat, Get_Data.Data("Cheat/" + file_name, [1920, 1080],
                                                               "Drag-GameStudio").get_player_input())
        Data_Y_Cheat = self.generate_y(len(Data_X_Cheat), 1)

        return self.add_arr(Data_X_Normal, Data_X_Cheat), self.add_arr(Data_Y_Normal, Data_Y_Cheat)

class NN():
    def __init__(self, input_dim, output_dim, activation="relu"):
        self.input_size = input_dim
        self.output_size = output_dim
        self.activation = activation


    def create_model(self):
        self.model = Sequential([
            Dense(90, input_dim=self.input_size, activation=self.activation),
            Dense(45, activation=self.activation),
            Dense(22, activation=self.activation),
            Dense(11, activation=self.activation),
            Dense(5, activation=self.activation),
            Dense(2, activation=self.activation),
            Dense(self.output_size, activation="sigmoid")
        ])
        self.model.compile(optimizer=Adam(learning_rate=0.01), loss='mse')

    def fit_network(self, X, y, epochs):
        self.model.fit(X, y, epochs=epochs)

    def predict(self, data):
        return self.model.predict(data)

    def save(self):
        self.model.save('model.h5')

if __name__ == '__main__':
    input_dim = 90
    output_dim = 1

    Anti_Cheat = NN(input_dim, output_dim)
    Anti_Cheat.create_model()

    x, y = Sort().sort_data()
    Anti_Cheat.fit_network(np.array(x), np.array(y), 1000)