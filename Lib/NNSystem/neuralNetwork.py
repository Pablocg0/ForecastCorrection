import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation
from keras.layers import LSTM
from keras.optimizers import SGD
from keras.callbacks import TensorBoard
from keras.callbacks import EarlyStopping
from keras.utils import multi_gpu_model
from keras import backend as K
import numpy as np


def train(x_data, y_data, estacion, variable, dirTrain):

    name = 'train_'+estacion+'_'+variable

    model = Sequential()

    model.add(Dense(256, activation= 'sigmoid', input_dim = 1))
    #model.add(Dropout(0.2))
    model.add(Dense(512, activation= 'sigmoid'))
    #model.add(Dropout(0.2))
    model.add(Dense(1, activation='sigmoid'))

    model.compile(loss='mean_squared_error', optimizer='adam')
    tensorboard = TensorBoard(log_dir="logs/train/"+estacion+'_'+variable )
    stop_callback = EarlyStopping(monitor='val_loss',min_delta=0.0001,patience=150, mode='auto')
    model.fit(x_data, y_data, epochs=1000, validation_split= 0.05 ,callbacks=[tensorboard,stop_callback])
    model.save(dirTrain + name + '_normal.h5')


def train_recurrent(x_data, y_data, estacion, variable, dirTrain):

    name = 'train_'+estacion+'_'+variable
    look_back = 1

    model = Sequential()
    model.add(LSTM(10, input_shape=(1, look_back)))
    model.add(Dense(1))
    model.compile(loss='mean_squared_error', optimizer='adam')
    tensorboard = TensorBoard(log_dir="logs/recurrent/"+estacion+'_'+variable )
    stop_callback = EarlyStopping(monitor='val_loss',min_delta=0.0001,patience=150, mode='auto')
    model.fit(x_data, y_data, epochs= 1000, batch_size=1, verbose=2, validation_split=0.05, callbacks=[tensorboard,stop_callback])
    model.save(dirTrain + name + '_recurrent.h5')



def train_baseline(x_data, y_data, estacion, variable, dirTrain):
    name = 'train_'+estacion+'_'+variable
    model = Sequential()
    model.add(Dense(13, input_dim=1, kernel_initializer='normal', activation = 'relu'))
    model.add(Dense(128, kernel_initializer = 'normal', activation = 'relu'))
    model.add(Dense(1, kernel_initializer='normal'))
    model.compile(loss='mean_squared_error', optimizer='adam')
    tensorboard = TensorBoard(log_dir="logs/baseline2/"+estacion+'_'+variable)
    stop_callback = EarlyStopping(monitor='val_loss',min_delta=0.0001,patience=150, mode='auto')
    model.fit(x_data, y_data, epochs=1000, batch_size= 5, verbose=1, validation_split=0.05, callbacks=[tensorboard,stop_callback])
    model.save(dirTrain + name + '_baseline.h5')


def main_train(x_data, y_data, estacion, variable, dirTrain, option):
    if optio == 1:
        train(x_data, y_data, estacion, variable, dirTrain)
    elif option == 2:
        train_recurrent(x_data, y_data, estacion, variable, dirTrain)
    elif option == 3:
        train_baseline(x_data, y_data, estacion, variable, dirTrain)
    else:
        print('No existe esa opcion')
