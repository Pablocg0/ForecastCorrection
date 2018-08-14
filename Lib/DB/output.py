import numpy as np
import pandas as pd
from DB.sqlCont import SqlCont
from DB.oztools import ContIOTools

def output(startData, endData, estacion):
    oztool = ContIOTools()
    #table_met =  oztool.getMeteoTables()
    table_met = ['met_tmp']
    conexion = SqlCont()
    conn = conexion.getPostgresConn()
    cur = conn.cursor()
    total_data = pd.DataFrame()
    total_data  = pd.read_sql_query("""SELECT fecha FROM {0} WHERE fecha >= '{1}' AND fecha <= '{2}' AND id_est = '{3}' ORDER BY fecha ASC;""".format(table_met[0], startData, endData, estacion),conn)
    total_data = total_data.drop_duplicates(keep='first')
    for xs in table_met:
        temp_data = pd.read_sql_query("""SELECT fecha, val FROM {0} WHERE fecha >= '{1}' AND fecha <= '{2}' AND id_est = '{3}'ORDER BY fecha ASC;""".format(xs, startData, endData, estacion),conn)
        data =  temp_data.drop_duplicates(keep='first')
        data.rename(columns={'fecha':'fecha','val':'val_'+xs}, inplace = True)
        total_data = total_data.merge(data, how='left', on=['fecha'])
    total_data = total_data.dropna(axis=0, how='any')
    total_data = total_data.drop_duplicates(keep='first')
    return total_data


#output('2016-01-01','2016-12-31 23:00:00')
output('2018-08-08','2018-08-12 23:00:00','ACO')
