import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation
from keras.layers import LSTM
from keras.optimizers import SGD
from keras.callbacks import TensorBoard
from keras.callbacks import EarlyStopping
from keras.utils import multi_gpu_model
from keras import backend as K
from keras.models import Sequential, load_model
import numpy as np


def prediction_normal(estacion, arrayPred, variable, dirTrain):
    result = []
    name = 'train_'+estacion+'_'+variable

    model = Sequential()

    model = load_model(dirTrain + name + '_normal.h5')

    for xs in arrayPred:
        pred = model.predict(xs)
        result.append(pred[0,0])
    return result


def prediction_recurrent(estacion, arrayPred, variable, dirTrain):
    result = []
    name = 'train_'+estacion+'_'+variable

    model = Sequential()

    model = load_model(dirTrain + name + '_recurrent.h5')

    for xs in arrayPred:
        pred = model.predict(xs)
        result.append(pred[0,0])
    return result


def prediction_baseline(estacion, arrayPred, variable, dirTrain):
    result = []
    name = 'train_'+estacion+'_'+variable

    model = Sequential()

    model = load_model(dirTrain + name + '_baseline.h5')

    for xs in arrayPred:
        pred = model.predict(xs)
        result.append(pred[0,0])
    return result

def main_prediction(estacion, arrayPred, variable, dirTrain,option):
    if option == 1:
        prediction_normal(estacion, arrayPred, variable, dirTrain)
    elif option == 2:
        prediction_recurrent(estacion, arrayPred, variable, dirTrain)
    elif option == 3:
         prediction_baseline(estacion, arrayPred, variable, dirTrain)
     else:
         print('No existe esa opcion')
