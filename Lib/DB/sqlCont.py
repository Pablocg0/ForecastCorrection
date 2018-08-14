# coding=utf-8
import psycopg2
import netrc

class SqlCont:
    """ This class contains SQL methods to inserte, update and delete inside tables"""

    def __init__(self):
        """Constructor of the class"""

    def getPostgresConn(self):
        secrets = netrc.netrc()
        login, account, passw = secrets.hosts['OWGIS']

        #For Posgresql only
        try:
            #conn =psycopg2.connect(database="contingencia", user=login,host='192.168.1.103', password=passw)
            conn = psycopg2.connect(database="contingencia", user=login, host='132.248.8.238', password=passw)
        except:
            print("Failed to connect to database")

        return conn

    def clearTable(self,conn,table):
        """ Deletes all the rows from the specified table"""
        sql = "DELETE FROM %s WHERE True ;" % (table)
        cur = conn.cursor();
        cur.execute(sql)
        conn.commit()
        cur.close();

    def delFromYear(self,year,tables,conn):
        text = "Are you sure you want to delete from year: %s (Y or N)? " % (year)
        ans = raw_input(text)
        if ans == 'Y':
            cur = conn.cursor();
            for table in tables:
                print("Deleting table %s from year %s" % (table,year))
                sql = "DELETE FROM %s WHERE date_part('year',fecha) >= %s ;" % (table,year)
                cur.execute(sql)
                conn.commit()
            cur.close();
        else:
            print("Not droping tables!")

    def getContaminantes(self,conn):
        cur = conn.cursor();
        cur.execute(""" SELECT table_name FROM information_schema.tables WHERE table_schema='public' AND table_type='BASE TABLE'; """);
        rows = cur.fetchall();
        cur.close();

        return rows

    def insertIntoDBAfter2011(self,fileName, conn, dateFormat, year, sqlCont, oztools):
        "Filling data into Database mode AFTER 2011"
        print("Filling data into Database. Using mode AFTER 2011")
        cur = conn.cursor();
        f = open(fileName)

        firstData = 11
        addMe = -1

        values = f.readlines()[firstData:]
        c_table = ''
        sqlQueries = {}


        contaminantes = sqlCont.getContaminantes(conn)
        for contaminante in contaminantes:
            sqlQueries[contaminante[0]] = ''

        print("Processing file...")
        count = 0
        for line in values:
            count = count + 1
            lineValues = line.split(',')
            fechaValues =  lineValues[0].split(' ')
            fecha =  fechaValues[0]+'/'+str((int(fechaValues[1].split(':')[0])+addMe))
            #print fecha
            id_est =  lineValues[1]
            table =  oztools.findTable(lineValues[2])
            myval =  lineValues[3]

            if myval != '':
                #sql = "SET TimeZone='UTC'; INSERT INTO %s (fecha, val, id_est) VALUES (to_timestamp('%s','%s'), '%s', '%s')\n" % (table, fecha,  dateFormat, myval, id_est)
                #print sql
                #cur.execute(sql)
                if sqlQueries[table] == '':
                    print("Filling rows in table: ",table)
                    sqlQueries[table] = "SET TimeZone='UTC'; INSERT INTO %s (fecha, val, id_est) VALUES (to_timestamp('%s','%s'), '%s', '%s')\n" % (table, fecha,  dateFormat, myval, id_est)
                else:
                    sqlQueries[table] = sqlQueries[table] + " ,(to_timestamp('%s','%s'), '%s', '%s')\n" % (fecha,  dateFormat, myval, id_est)


            if count % 100000 == 0:
                print(count)
                for mykey in sqlQueries.keys():
                    sql = sqlQueries[mykey]
                    if sql != '':
                        #print "Inserting in:",mykey
                        #try:
                        cur.execute(sql)
                        conn.commit()
                        sqlQueries[mykey] = ''
                        #except:
                        #    print sqlQueries[mykey]

        # Last list of inserts
        for mykey in sqlQueries.keys():
            sql = sqlQueries[mykey]
            if sql != '':
                #print "Inserting in:",mykey
                cur.execute(sql)
                conn.commit()
                sqlQueries[mykey] = ''

        cur.close();

    def insertIntoDB(self,fileName, conn, dateFormat, year, oztools):
        "Filling data into Database mode UNTIL 2011"
        print("Filling data into Database. Using mode UNTIL 2011")
        cur = conn.cursor();
        #f = codecs.open(fileName,'r','iso-8859-1')
        f = open(fileName)
        firstData = 11

        addMe = -1

        values = f.readlines()[firstData:]
        sql = ''
        c_table = ''

        for line in values:
            lineValues = line.split(',')
            fechaValues =  lineValues[0].split(' ')
            fecha =  fechaValues[0]+'/'+str((int(fechaValues[1].split(':')[0])+addMe))
            id_est =  lineValues[1]
            table =  oztools.findTable(lineValues[2])
            myval =  lineValues[3]

            if(c_table != table):
                if sql != '':
                    print(c_table)
                    #Run query
                    #try:
                    cur.execute(sql)
                    conn.commit()
                    #except:
                        #print(fecha,id_est,table,myval)
                        ##print(sql)
                        #input("Press Enter to continue...")

                c_table = table
                sql = ''
                firstLine = True

            if myval != '':
                #print myval
                if firstLine:
                    sql =  "SET TimeZone='UTC'; INSERT INTO %s (fecha, val, id_est) VALUES (to_timestamp('%s','%s'), '%s', '%s')\n" % (table, fecha,  dateFormat, myval, id_est)
                    firstLine = False
                else:
                    sql = sql +  " ,(to_timestamp('%s','%s'), '%s', '%s')\n" % (fecha,  dateFormat, myval, id_est)

        # Last table
        if sql != '':
            print(c_table)
            cur.execute(sql)
            conn.commit()

        cur.close();

    def restartSeq(self,table,conn,cur):
        seq = "cont_seq_"+(table.replace("cont_",""))
        print("Setting sequence = 1 for seq %s" % (seq))
        sql = "ALTER SEQUENCE %s RESTART WITH 1" % (seq)
        print(sql)
        cur.execute(sql)
        conn.commit()
        cur.close();

    def restartAllSeq(self,conn,tables):
        cur = conn.cursor()
        for table in tables:
            restartSeq(table,conn,cur)

        cur.close();
