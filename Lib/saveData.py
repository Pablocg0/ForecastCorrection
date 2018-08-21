from datetime import datetime, timedelta
from DB.output import output as out
import pandas as pd
import os
import numpy as np
import configparser
import matplotlib.pyplot as plt


def saveData(estacion, variable, startDate, endDate, dirNetcdf, dirSave):
    data_obs = out(startDate, endDate, estacion)
    data_obs = convertCtoK(data_obs)
    data_for =  pd.read_csv(dirNetcdf + variable +'_'+estacion+'_total.csv')
    data_for = convertDates(data_for)
    data_for =  data_for.drop_duplicates(keep='first')
    total_data =  data_for.merge(data_obs, how='left', on='fecha')
    total_data = total_data.dropna(axis=0, how='any')
    total_data = total_data.reset_index(drop = True)
    print('save')
    total_data.to_csv(dirSave+estacion+'_'+variable+'.csv',encoding='utf-8',index=False)
    #graph(total_data)



def convertDates(data):
    """
    function to convert a string into a date and save it in a dataframe

    :param data: dataframe with the dates to convert
    :type data : DataFrame
    :return: DataFrame
    """
    fecha = data['fecha']
    data = data.drop(labels='fecha', axis=1)
    date = []
    for i in fecha:
        datef = datetime.strptime(i, '%Y-%m-%d %H:%M:%S')
        correct_date = datef - timedelta(hours=6)
        date.append(correct_date)
    dataTemp = pd.DataFrame(date, columns=['fecha'])
    data = pd.concat([dataTemp,data], axis=1)
    return data

def convertCtoK (data):
    data_cel =  data['val_met_tmp'].values
    data = data.drop(['val_met_tmp'], axis=1)
    data_convert = []
    for xs in data_cel:
        k = xs + 273.15
        data_convert.append(k)
    data_ke = pd.DataFrame(data_convert, columns=['val_met_tmp'])
    data = pd.concat([data,data_ke], axis=1)
    return data

def graph(data):
    plt.figure(figsize=(22.2,11.4))
    plt.plot(data['val_met_tmp'].values ,color='tomato', linestyle="solid", marker='o', label='Valor observado.')
    plt.plot(data['T2_0'].values, color='darkgreen', linestyle='solid', marker='o', label='Pronóstico')
    plt.title('Diferencia entre temperatura ' ,fontsize=25, y=1.1 )
    plt.xlabel('Fecha', fontsize=22)
    plt.ylabel('Grados K', fontsize=22)
    plt.legend(loc='best')
    plt.grid(True, axis='both', alpha= 0.3, linestyle="--", which="both")
    plt.xlim(0, 0+120)
    plt.show()

def init():
    config = configparser.ConfigParser()
    config.read('/home/pablo/ForecastCorrection/ForecastCorrection/Modulos/Preprocesamiento/confSaveData.conf')
    estaciones = config.get('saveData','estaciones')
    variables = config.get('saveData', 'variables')
    startDate =  config.get('saveData', 'startDate')
    endDate = config.get('saveData', 'endDate')
    dirNetcdf = config.get('saveData', 'pathNetCDF')
    dirSave =  config.get('saveData', 'pathSave')
    estaciones = estaciones.split()
    print(estaciones)
    for xs in estaciones:
        print(xs)
        saveData(xs, variables, startDate, endDate, dirNetcdf,dirSave)

init()
