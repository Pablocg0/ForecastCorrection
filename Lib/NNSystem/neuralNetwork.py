import keras
import tensorflow as tf
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation
from keras.layers import LSTM
from keras.optimizers import SGD
from keras.callbacks import TensorBoard
from keras.callbacks import EarlyStopping
from keras.layers import Lambda, concatenate
from keras import Model
from keras.utils import multi_gpu_model
from keras import backend as K
import numpy as np


def train(x_data, y_data, estacion, variable, dirTrain):

    name = 'train_'+estacion+'_'+variable

    model = Sequential()

    model.add(Dense(256, activation= 'sigmoid', input_dim = 1))
    model.add(Dropout(0.2))
    model.add(Dense(512, activation= 'sigmoid'))
    model.add(Dropout(0.2))
    model.add(Dense(1, activation='sigmoid'))

    model = multi_gpu_model(model, gpus=4)

    model.compile(loss='mean_squared_error', optimizer='adam')
    tensorboard = TensorBoard(log_dir="logs/train_drop/"+estacion+'_'+variable )
    stop_callback = EarlyStopping(monitor='val_loss',min_delta=0.0001,patience=150, mode='auto')
    model.fit(x_data, y_data, epochs=300,  batch_size=64*16, validation_split= 0.05 ,callbacks=[tensorboard,stop_callback])
    model.save(dirTrain + name + '_drop.h5')


def train_recurrent(x_data, y_data, estacion, variable, dirTrain):

    name = 'train_'+estacion+'_'+variable
    look_back = 1

    model = Sequential()
    model.add(LSTM(10, input_shape=(1, look_back)))
    model.add(Dense(1))

    model = multi_gpu_model(model, gpus=4)


    model.compile(loss='mean_squared_error', optimizer='adam')
    tensorboard = TensorBoard(log_dir="logs/recurrent/"+estacion+'_'+variable )
    stop_callback = EarlyStopping(monitor='val_loss',min_delta=0.0001,patience=150, mode='auto')
    model.fit(x_data, y_data, epochs= 300,  batch_size=64*16, verbose=2, validation_split=0.05, callbacks=[tensorboard,stop_callback])
    model.save(dirTrain + name + '_recurrent.h5')



def train_baseline(x_data, y_data, estacion, variable, dirTrain):
    name = 'train_'+estacion+'_'+variable
    model = Sequential()
    model.add(Dense(13, input_dim=1, kernel_initializer='normal', activation = 'relu'))
    model.add(Dense(128, kernel_initializer = 'normal', activation = 'relu'))
    model.add(Dense(1, kernel_initializer='normal'))

    model = multi_gpu_model(model, gpus=4)

    model.compile(loss='mean_squared_error', optimizer='adam')
    tensorboard = TensorBoard(log_dir="logs/baseline2/"+estacion+'_'+variable)
    stop_callback = EarlyStopping(monitor='val_loss',min_delta=0.0001,patience=150, mode='auto')
    model.fit(x_data, y_data, epochs=300,  batch_size=64*16, verbose=1, validation_split=0.05, callbacks=[tensorboard,stop_callback])
    model.save(dirTrain + name + '_baseline.h5')


def main_train(x_data, y_data, estacion, variable, dirTrain, option):
    if option == 1:
        train(x_data, y_data, estacion, variable, dirTrain)
    elif option == 2:
        train_recurrent(x_data, y_data, estacion, variable, dirTrain)
    elif option == 3:
        train_baseline(x_data, y_data, estacion, variable, dirTrain)
    else:
        print('No existe esa opcion')


def multi_gpu_model(model, gpus):
  if isinstance(gpus, (list, tuple)):
    num_gpus = len(gpus)
    target_gpu_ids = gpus
  else:
    num_gpus = gpus
    target_gpu_ids = range(num_gpus)

  def get_slice(data, i, parts):
    shape = tf.shape(data)
    batch_size = shape[:1]
    input_shape = shape[1:]
    step = batch_size // parts
    if i == num_gpus - 1:
      size = batch_size - step * i
    else:
      size = step
    size = tf.concat([size, input_shape], axis=0)
    stride = tf.concat([step, input_shape * 0], axis=0)
    start = stride * i
    return tf.slice(data, start, size)

  all_outputs = []
  for i in range(len(model.outputs)):
    all_outputs.append([])

  # Place a copy of the model on each GPU,
  # each getting a slice of the inputs.
  for i, gpu_id in enumerate(target_gpu_ids):
    with tf.device('/gpu:%d' % gpu_id):
      with tf.name_scope('replica_%d' % gpu_id):
        inputs = []
        # Retrieve a slice of the input.
        for x in model.inputs:
          input_shape = tuple(x.get_shape().as_list())[1:]
          slice_i = Lambda(get_slice,
                           output_shape=input_shape,
                           arguments={'i': i,
                                      'parts': num_gpus})(x)
          inputs.append(slice_i)

        # Apply model on slice
        # (creating a model replica on the target device).
        outputs = model(inputs)
        if not isinstance(outputs, list):
          outputs = [outputs]

        # Save the outputs for merging back together later.
        for o in range(len(outputs)):
          all_outputs[o].append(outputs[o])

  # Merge outputs on CPU.
  with tf.device('/cpu:0'):
    merged = []
    for name, outputs in zip(model.output_names, all_outputs):
      merged.append(concatenate(outputs,
                                axis=0, name=name))
    return Model(model.inputs, merged)
