from NNSystem.neuralNetwork import main_train as nn
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
from sklearn import preprocessing
import configparser
import prediction as pre
import numpy as np
import pandas as pd
import os

def training(estacion, startDate, endDate,dirData, dirTraining, variable, option):
    name_file = estacion +'_'+variable+'.csv'
    if os.path.exists(dirData + name_file):
        data = pd.read_csv(dirData + name_file)
        data_pred = data
        data = data[data['fecha'] < endDate]
        if option == 2:
            non_data = data.drop(['fecha'], axis=1)
            #non_data = non_data.values
            #look_back = 1
            #trainX, trainY = create_dataset(non_data, look_back)
            trainX, trainY = create_data(non_data)
            #print(non_data)
            #print(trainX)
            #print(trainY)
            #return 0
            #trainX = normalize(trainX)
            #trainY = normalize(trainY)
            trainX = np.reshape(trainX, (trainX.shape[0], 1, trainX.shape[1]))
            nn(trainX, trainY, estacion,variable,dirTraining, option)
            test(data_pred, estacion, '2017-01-01', '2017-05-01', dirTraining, variable, option)
        else:
            x_train = normalize(data['T2_0'])
            y_target = normalize(data['val_met_tmp'])
            nn(x_train, y_target, estacion,variable,dirTraining,option)
            test(data_pred, estacion, '2017-01-01', '2017-05-01', dirTraining, variable, option)



def normalize(data):
    min_max_scaler = preprocessing.MinMaxScaler()
    #data = data.fillna(value=-1)
    data_array = np.asarray(data)
    data_array = data_array.reshape(len(data_array),-1)
    data_normalize = min_max_scaler.fit_transform(data_array)
    return data_normalize


def convert_array(data):
    data_array = []
    for xs in data:
        data_array.append(xs[0])
    return data_array


def create_data(data):
    x_train = normalize(data['T2_0'])
    x_data = x_train.reshape((len(x_train),1))
    y_target = normalize(data['val_met_tmp'])
    y_data = []
    for xs in y_target:
        y_data.append(xs[0])
    return x_data, y_data


def create_dataset(dataset, look_back=1):
	dataX, dataY = [], []
	for i in range(len(dataset)-look_back-1):
		a = dataset[i:(i+look_back), 0]
		dataX.append(a)
		dataY.append(dataset[i + look_back, 0])
	return np.array(dataX), np.array(dataY)


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
    data = data[(data['fecha']>= startDate) & (data['fecha'] <= endDate)]
    if option == 2:
        #non_data = data.drop(['fecha'], axis=1)
        #non_data = non_data.values
        look_back = 1
        #trainX, trainY = create_dataset(non_data, look_back)
        trainX, trainY = create_data(data)
        data_red = normalize(trainX)
        nondata_red = np.reshape(data_red, (data_red.shape[0], 1, data_red.shape[1]))
        #print(nondata_red)
        data_correction = pre.main_prediction(estacion, nondata_red, variable, dirTraining, option)
    elif option == 1:
        data_prediccion = normalize(data['T2_0'])
        data_correction = pre.main_prediction(estacion, data_prediccion, variable, dirTraining, option)
    data_prediccion = normalize(data['T2_0'])
    data_estacion = normalize(data['val_met_tmp'])
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
        return 'drop'
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
    for xs in estaciones:
        training(xs, startDate, endDate, dirData, dirTraining, variables, 1)
    #for xs in estaciones:
    #    training(xs, startDate, endDate, dirData, dirTraining, variables, 2)
    #for xs in estaciones:
    #    training(xs, startDate, endDate, dirData, dirTraining, variables, 3)


init()
#training('ACO', '2016-01-01', '2016-12-21', '/home/pablo/Documentos/Estaciones_EMAS/Data/Data_complete/', '/home/pablo/Documentos/Estaciones_EMAS/Data/Training/', 'T2')
