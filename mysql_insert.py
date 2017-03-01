from __future__ import print_function
from datetime import date, datetime, timedelta
import mysql.connector

import auth_data

#name,open,max,min,close,data,percent_change,volume,transactions,value_of_trading
def insert_to_database(name,open_value,max,min,close,date,percent_change,volume,transactions,value_of_trading):

    data_for_auth = auth_data.data_for_auth()
    config = {
        'user': data_for_auth[0],
        'password': data_for_auth[1],
        'host': data_for_auth[2],
        'database': data_for_auth[3],
        'raise_on_warnings': True,
        'use_pure': False,
    }

    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    try:
        cursor.execute("CREATE TABLE IF NOT EXISTS "  + str(name) + " (`id` int(11) NOT NULL AUTO_INCREMENT,`open` decimal(10,2) NOT NULL,`close` decimal(10,2) NOT NULL,`max` decimal(10,2) NOT NULL,`min` decimal(10,2) NOT NULL,`date` date NOT NULL,`percent_change` decimal(10,2) NOT NULL,`volume` decimal(10,2) NOT NULL,`transactions` decimal(10,2) NOT NULL,`value_of_trading` decimal(10,2) NOT NULL,PRIMARY KEY (`id`)) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_polish_ci AUTO_INCREMENT=1 ;")
    except mysql.connector.errors.DatabaseError:
        print("ERROR")


    print("INSERT INTO `"+str(name)+"` (`id` ,`open` ,`close` ,`max` ,`min` ,`date` ,`percent_change` ,`volume` ,`transactions` ,`value_of_trading`) VALUES (NULL , '"+str(open_value)+"', '"+str(close)+"', '"+str(max)+"', '"+str(min)+"', '"+str(date)+"', '"+str(percent_change)+"', '"+str(volume)+"', '"+str(transactions)+"', '"+str(value_of_trading)+"');")


    cursor.execute("INSERT INTO `"+str(name)+"` (`id` ,`open` ,`close` ,`max` ,`min` ,`date` ,`percent_change` ,`volume` ,`transactions` ,`value_of_trading`)VALUES (NULL, '"+str(open_value)+"', '"+str(close)+"', '"+str(max)+"', '"+str(min)+"', '"+str(date)+"', '"+str(percent_change)+"', '"+str(volume)+"', '"+str(transactions)+"', '"+str(value_of_trading)+"');")

    cnx.commit()

    cursor.close()
    cnx.close()