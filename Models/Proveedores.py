import sys
import os
myDir = os.getcwd()
sys.path.append(myDir)

import sqlite3

class Proveedores():


    #-----------Constructor----------------
    def __init__(self,connection):
        self.control = connection

        
        #-------------CREAR LA TABLA ---------------
        cursor = self.control.cursor()
        sql = """ CREATE TABLE IF NOT EXISTS "Tabla_Proveedores" (
	    "Codigo"	INTEGER,
	    "Nombre"	TEXT,
	    "Telefono"	INTEGER,
	    "Mail"	TEXT,
	    "Direccion"	TEXT,
	    "Descripcion"	TEXT,
	    PRIMARY KEY("Codigo" AUTOINCREMENT)
        );"""


        cursor.execute(sql)
        self.control.commit()
        


