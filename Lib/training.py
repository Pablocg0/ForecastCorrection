from NNSystem.neuralNetwork import main_train as nn
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
from sklearn import preprocessing
from datetime import datetime, timedelta
import configparser
import prediction as pre
import numpy as np
import pandas as pd
import os

def training(estacion, startDate, endDate,dirData, dirTraining, variable, option):
    name_file = estacion +'_complete.csv'
    if os.path.exists(dirData + name_file):
        data = pd.read_csv(dirData + name_file)
        data_pred = data
        #data = data.sort_values(['fecha'])
        data = data[data['fecha'] < endDate]
        if option == 2:
            non_data = data.drop(['fecha'], axis=1)
            #non_data = non_data.values
            #look_back = 1
            #trainX, trainY = create_dataset(non_data, look_back)
            trainY = create_data(non_data)
            trainY = np.array(trainY)
            trainY2 = trainY.reshape((1,len(trainY)))

            #trainX, trainY = create_terc(data, estacion, 'T2_0')

            trainX = exp(data, estacion, 'T2_0')
            #print(data_set)
            #return 0
            #print(non_data)
            #print(trainX)
            #print(trainY)
            #return 0
            #trainX = normalize(trainX)
            #trainY = normalize(trainY)
            #trainX = np.reshape(trainX, (trainX.shape[0], 1, trainX.shape[1]))
            nn(trainX, trainY, estacion,variable,dirTraining, option)
            #nn(data_set, trainY, estacion,variable,dirTraining, option)
            test(data_pred, estacion, '2017-11-01', '2017-12-31', dirTraining, variable, option)
        else:
            complete_data = data.drop(['fecha','val_met_tmp'], axis=1)
            complete_data = complete_data.reset_index(drop=True)
            #x_train = normalize(data['T2_0'])
            x_train = normalize(complete_data)
            y_target = normalize1(data['val_met_tmp'])
            nn(x_train, y_target, estacion,variable,dirTraining,option)
            test(data_pred, estacion, '2017-11-01', '2017-12-31', dirTraining, variable, option)



def normalize(data):
    #data = data.fillna(value=-1)
    data_array = data.as_matrix()
    #data_array = data_array.reshape(len(data_array),-1)
    min_max_scaler = preprocessing.MinMaxScaler()
    data_normalize = min_max_scaler.fit_transform(np.array(data_array))
    return data_normalize


def normalize1(data):
    #data_array = data.values
    data_array = data
    data_array = data_array.reshape(len(data_array),-1)
    min_max_scaler = preprocessing.MinMaxScaler(feature_range=(0, 1))
    data_normalize = min_max_scaler.fit_transform(np.array(data_array))
    return data_normalize

def exp(data, estacion, variable):
    data_temp = data.drop(['fecha','val_met_tmp'], axis =1)
    data_temp = data_temp.values
    data_array = normalize1(data_temp)
    data_3d = data_array.reshape((data_array.shape[0],1,7))
    return data_3d


def create_terc(data, estacion,variable):
    #print(data)
    data = data.reset_index(drop=True)
    array_date = []
    fecha = data['fecha']
    # data_variable = data[variable] #valor de las estaciones  [samples, time steps, features],
    # data_temp = data.drop(['fecha', 'val_met_tmp'], axis=1)
    for xs in np.asarray(fecha):
        datef = datetime.strptime(xs, '%Y-%m-%d %H:%M:%S')
        array_date.append(datef.hour)
    frame_hours = pd.DataFrame(array_date, columns=['hora'])
    data = pd.concat([data,frame_hours], axis=1)

    data_meta = []
    total_data = np.zeros((24,500,5))
    for xs in range(24):
        data_hours = data[data['hora']==xs]
        data_hours = data_hours.drop_duplicates(subset='fecha', keep='first')
        data_hours = data_hours.reset_index(drop=True)
        data_hours = data_hours.drop(['hora'], axis =1)
        data_meta_temp = normalize1(data_hours['val_met_tmp'].values)
        print(data_meta_temp.shape)
        data_meta.append(convert(data_meta_temp[:500]))
        data_hours = data_hours.drop(['fecha','val_met_tmp'], axis =1)
        data_temp = normalize(data_hours)
        data_temp = data_temp[:500]
        data_3d = data_temp.reshape(data_temp.shape[0],5)
        total_data[xs] = data_3d

    print(total_data.shape)
    data_y = np.array(data_meta)
    #data_y = data_meta
    print(data_y.shape)
    data_y = data_y.reshape((500*24,1))
    data_x = total_data


    return data_x, data_y
    # array_date = normalize1(np.array(array_date))
    # array_date = array_date.reshape(len(array_date),1)
    # data_variable = normalize1(data_variable)
    # data_variable = data_variable.reshape(len(data_variable),1)
    # other_data = normalize(data_temp)
    # return np.array([data_temp, len(array_date), 5])

def convert(data):
    list =[]
    for xs in data:
        list.append(xs[0])
    return np.array(list)



def create_data(data):
    y_target = normalize1(data['val_met_tmp'])
    y_data = []
    for xs in y_target:
        y_data.append(xs[0])
    return y_data


def create_dataset(dataset, look_back=1):
	dataX, dataY = [], []
	for i in range(len(dataset)-look_back-1):
		a = dataset[i:(i+look_back), 0]
		dataX.append(a)
		dataY.append(dataset[i + look_back, 0])
	return np.array(dataX), np.array(dataY)

def desNorm(data,estacion):
    real = []
    data_minMax= pd.read_csv('/ServerData/DataForecastCorrection/DataTraining/valoresMaxMin.csv')
    valores = data_minMax[(data_minMax['estacion']==estacion)]
    maxx = valores['maximo'].values[0]
    minn = valores['minimo'].values[0]
    for xs in data:
        realVal = (xs * (maxx - minn)) + minn
        real.append(realVal)
    return real


def nombreEst(station):
    """
    function that returns from the full name of a station

    :param station: abbreviation of the name of the station
    :type station: String
    :return: full name of the station
    :type return: String
    """
    if station == 'AJM':
        return 'Ajusco Medio'
    elif station == 'MGH':
        return 'Miguel Hidalgo'
    elif station == 'CCA':
        return 'Centro de Ciencias de la Atmosfera'
    elif station == 'SFE':
        return 'Santa Fe'
    elif station == 'UAX':
        return 'UAM Xochimilco'
    elif station == 'CUA':
        return 'Cuajimalpa'
    elif station == 'NEZ':
        return 'Nezahualcóyotl'
    elif station == 'CAM':
        return 'Camarones'
    elif station == 'LPR':
        return 'La Presa'
    elif station == 'SJA':
        return 'San Juan Aragón'
    elif station == 'CHO':
        return 'Chalco'
    elif station == 'IZT':
        return 'Iztacalco'
    elif station == 'SAG':
        return 'San Agustín'
    elif station == 'TAH':
        return 'Tlahuac'
    elif station == 'ATI':
        return 'Atizapan'
    elif station == 'FAC':
        return 'FES Acatlán'
    elif station == 'UIZ':
        return 'UAM Iztapalapa'
    elif station == 'MER':
        return 'Merced'
    elif station == 'PED':
        return 'Pedregal'
    elif station == 'TLA':
        return 'tlalnepantla'
    elif station == 'BJU':
        return 'Benito Juárez'
    elif station == 'XAL':
        return 'Xalostoc'
    elif station =='ACO':
        return 'Acolman'
    elif station == 'MON':
        return 'Montecillo'
    elif station == 'CUT':
        return 'Cuautitlán'
    elif station == 'HGM':
        return 'Hospital General de México'
    elif station == 'VIF':
        return 'Villa de las Flores'
    elif station == 'AJU':
        return 'Ajusco'


def test(data, estacion, startDate, endDate, dirTraining, variable, option):
    print(estacion)
    data = data[(data['fecha']>= startDate) & (data['fecha'] <= endDate)]
    data = data.drop_duplicates(subset='fecha', keep='first')
    min_max_scaler = preprocessing.MinMaxScaler(feature_range=(0, 1))
    if option == 2:
        #non_data = data.drop(['fecha'], axis=1)
        #non_data = non_data.values
        #look_back = 1
        #trainX, trainY = create_dataset(non_data, look_back)
        #trainX, trainY = create_data(data)
        #data_red = normalize(trainX)
        #nondata_red = np.reshape(data_red, (data_red.shape[0], 1, data_red.shape[1]))
        #print(nondata_red)
        data_temp = data.drop(['fecha','val_met_tmp'], axis =1)
        data_temp = data_temp.values
        data_array = data_temp
        data_array = data_array.reshape(len(data_array),-1)
        data_normalize = min_max_scaler.fit_transform(np.array(data_array))
        data_3d = data_normalize.reshape((data_normalize.shape[0],1,7))
        #trainX = exp(data, estacion, 'T2_0')
        data_correction = pre.main_prediction(estacion, data_3d, variable, dirTraining, option)
    elif option == 1:
        complete_data = data.drop(['fecha','val_met_tmp'], axis=1)
        #data_prediccion = normalize(data['T2_0'])
        data_prediccion = normalize(complete_data)
        #data_prediccion = entr(data_prediccion)
        #print(data_prediccion.shape)
        array_pred = []
        for xs in data_prediccion:
            array_pred.append(convert(xs))
        #print(convert(data_prediccion[0]).shape)
        data_correction = pre.main_prediction(estacion, array_pred, variable, dirTraining, option)
    #data_prediccion = normalize1(data['T2_0'])
    data_prediccion = data['T2_0'].values
    #data_estacion = normalize1(data['val_met_tmp'])
    data_estacion = data['val_met_tmp'].values
    data_correction = desNorm(data_correction, estacion)
    #data_correction = min_max_scaler.inverse_transform(data_correction)
    #print(data_prediccion)
    #print(data_estacion)
    #print(data_correction)
    #data_correction = pre.main_prediction(estacion, data_prediccion, variable, dirTraining, option)
    plt.figure(figsize=(22.2,11.4))
    plt.plot(data_prediccion ,color='tomato', linestyle="solid", marker='o', label='Pronostico')
    plt.plot(data_estacion, color='darkgreen', linestyle='solid', marker='o', label='Estacion')
    plt.plot(data_correction, color= 'magenta', linestyle = 'solid', marker='o', label='RN')
    plt.title('Correccion de temperatura ' + nombreEst(estacion) + ' (' + estacion + ')' ,fontsize=25, y=1.1 )
    plt.xlabel('Fecha', fontsize=22)
    plt.ylabel('Grados °K', fontsize=22)
    plt.legend(loc='best')
    plt.grid(True, axis='both', alpha= 0.3, linestyle="--", which="both")
    plt.grid(True, axis='both', alpha= 0.3, linestyle="--", which="both")
    plt.xlim(0,240)
    plt.gca().spines['bottom'].set_color('dimgray')
    plt.gca().spines['left'].set_visible(False)
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    plt.tight_layout()
    plt.savefig('/home/pablo/ForecastCorrection/ForecastCorrection/Data/' + estacion +'_'+option_name(option)+'.jpg')
    plt.show()
    plt.clf()
    plt.close()


def option_name(option):
    if option == 1:
        return 'normal_sgd'
    elif option == 2:
        return 'recurrent'
    elif option == 3:
        return 'baseline'


def init():
    config = configparser.ConfigParser()
    config.read('/home/pablo/ForecastCorrection/ForecastCorrection/Modulos/Training/confTraining.conf')
    estaciones = config.get('training', 'estaciones')
    startDate = config.get('training', 'startDate')
    endDate = config.get('training', 'endDate')
    dirData = config.get('training', 'dirData')
    dirTraining = config.get('training', 'dirTraining')
    variables = config.get('training', 'variables')
    estaciones = estaciones.split()
    #variables = variables.split()
    #for xs in estaciones:
    #    training(xs, startDate, endDate, dirData, dirTraining, variables, 1)
    for xs in estaciones:
        training(xs, startDate, endDate, dirData, dirTraining, variables, 2)
    #for xs in estaciones:
    #    training(xs, startDate, endDate, dirData, dirTraining, variables, 3)


init()
#training('ACO', '2016-01-01', '2016-12-21', '/home/pablo/Documentos/Estaciones_EMAS/Data/Data_complete/', '/home/pablo/Documentos/Estaciones_EMAS/Data/Training/', 'T2')
