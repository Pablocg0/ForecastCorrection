import keras
from keras.models import Sequential, load_model
from keras.layers import Dense, Dropout, Activation
from keras.utils import multi_gpu_model
import tensorflow as tf
import numpy as np


def prediction_normal(estacion, arrayPred, variable, dirTrain):
    result = []
    name = 'train_'+estacion+'_'+variable

    model = Sequential()

    model = load_model(dirTrain + name + '_drop.h5', {'tf': tf})

    for xs in arrayPred:
        pred = model.predict(xs)
        result.append(pred[0,0])
    return result


def prediction_recurrent(estacion, arrayPred, variable, dirTrain):
    result = []
    name = 'train_'+estacion+'_'+variable

    model = Sequential()

    model = load_model(dirTrain + name + '_recurrent.h5', {'tf': tf})

    for xs in arrayPred:
        xs = np.reshape(xs, (xs.shape[0], 1, xs.shape[1]))
        pred = model.predict(xs)
        result.append(pred[0,0])
    return result


def prediction_baseline(estacion, arrayPred, variable, dirTrain):
    result = []
    name = 'train_'+estacion+'_'+variable

    model = Sequential()

    model = load_model(dirTrain + name + '_baseline.h5', {'tf': tf})

    for xs in arrayPred:
        pred = model.predict(xs)
        result.append(pred[0,0])
    return result

def main_prediction(estacion, arrayPred, variable, dirTrain,option):
    if option == 1:
        return prediction_normal(estacion, arrayPred, variable, dirTrain)
    elif option == 2:
        return prediction_recurrent(estacion, arrayPred, variable, dirTrain)
    elif option == 3:
         return prediction_baseline(estacion, arrayPred, variable, dirTrain)
    else:
         print('No existe esa opcion')
