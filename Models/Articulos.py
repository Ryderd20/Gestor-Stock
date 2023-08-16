
import sys
import os
myDir = os.getcwd()
sys.path.append(myDir)

import sqlite3

class Articulos():


    #-----------Constructor----------------
    def __init__(self,connection):
        self.control = connection

        """
        -------------CREAR LA TABLA - AGREGAR DESPUES--------------
        cursor = self.control.cursor()
        sql = CREATE TABLE IF NOT EXISTS "Tabla_Articulos"
        ("Codigo" VARCHAR(45) NO NULL,
        "Nombre" VARCHAR(45) NO NULL,
        "Precio" VARCHAR(45) NO NULL,
        "Descripcion" VARCHAR(45) NO NULL,
        "Proveedor" VARCHAR(45) NO NULL)

        cursor.execute(sql)
        self.control.commit()
        """
        





    def getArticulos(self):
        cursor = self.control.cursor()
        sql = """SELECT * FROM Tabla_Articulos"""
        cursor.execute(sql)
        registro = cursor.fetchall()
        cursor.close()
        return registro
    
    def getArticuloCod(self,cod):
        cursor = self.control.cursor()
        sql = """SELECT * FROM Tabla_Articulos WHERE Codigo = {}""".format(cod)
        cursor.execute(sql)
        registro = cursor.fetchone()
        cursor.close()
        if registro:
            return registro
    
    def updateArticulos(self,cod,nombre,precio,descripcion,proveedor):
        cursor = self.control.cursor()
        sql = """UPDATE Tabla_Articulos SET Nombre = %s , Precio = %s , Descripcion = %s, Proveedor = %s WHERE Codigo = %s """
        cursor.execute(sql,(nombre,precio,descripcion,proveedor,cod))
        self.control.commit()

    def insertArticulo(self,cod,nombre,precio,descripcion,proveedor):
        cursor = self.control.cursor()
        sql = """INSERT INTO Tabla_Articulos (Codigo,Nombre,Precio,Descripcion,Proveedor) VALUES ("{}","{}","{}","{}","{}")""".format(cod,nombre,precio,descripcion,proveedor)
        cursor.execute(sql)
        self.control.commit()


    def deleteArticulo(self,cod):
        cursor = self.control.cursor()
        sql = """DELETE FROM Tabla_Articulos WHERE Codigo = {}""".format(cod)
        cursor.execute(sql)
        self.control.commit()
    
    def getArticuloNom(self,nom):
        cursor = self.control.cursor()
        sql = """SELECT * FROM Tabla_Articulos WHERE Nombre = {}""".format(nom)
        cursor.execute(sql)
        registro = cursor.fetchone()
        cursor.close()
        if registro:
            return registro



#
    

