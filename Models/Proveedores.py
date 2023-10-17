import sys
import os
myDir = os.getcwd()
sys.path.append(myDir)

import sqlite3

class Proveedores():


    #-----------Constructor----------------
    def __init__(self,connection):
        self.control = connection

        
        #-------------CREAR TABLA ---------------
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


    def getProveedores(self):
        cursor = self.control.cursor()
        sql = """SELECT * FROM Tabla_Proveedores"""
        cursor.execute(sql)
        registro = cursor.fetchall()
        cursor.close()
        return registro
    

    def getProveedorCod(self,cod):
        cursor = self.control.cursor()
        sql = """SELECT * FROM Tabla_Proveedores WHERE Codigo = {}""".format(cod)
        cursor.execute(sql)
        registro = cursor.fetchone()
        cursor.close()
        if registro:
            return registro




    def updateProveedores(self,cod,nombre,telefono,mail,direccion,descripcion):
        cursor = self.control.cursor()
        sql = """UPDATE Tabla_Proveedores SET Nombre = "{}" , Telefono = "{}" , Mail = "{}", Direccion = "{}", Descripcion = "{}" WHERE Codigo = "{}" """.format(nombre,telefono,mail,direccion,descripcion,cod)
        cursor.execute(sql)
        self.control.commit()
        cursor.close()



    def deleteProveedor(self,cod):
        cursor = self.control.cursor()
        sql = """DELETE FROM Tabla_Proveedores WHERE Codigo = {}""".format(cod)
        cursor.execute(sql)
        self.control.commit()
    
        
        


