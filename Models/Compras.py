import sys
import os
myDir = os.getcwd()
sys.path.append(myDir)


class Compras():


    #-----------Constructor----------------
    def __init__(self,connection):
        self.control = connection

        #-------------CREAR LA TABLA--------------
        cursor = self.control.cursor()
        sql = """CREATE TABLE IF NOT EXISTS "Tabla_Compras" (
	    "CodCompra"	INTEGER NOT NULL,
	    "Fecha"	TEXT,
        "Proveedor" TEXT,
	    "Total"	REAL,
	    PRIMARY KEY("CodCompra" AUTOINCREMENT)
        );"""

        cursor.execute(sql)
        self.control.commit()

    #Obtener registro de Compras
    def getCompras(self):
        cursor = self.control.cursor()
        sql = """SELECT * FROM Tabla_Compras ORDER BY CodCompra DESC"""
        cursor.execute(sql)
        registro = cursor.fetchall()
        cursor.close()
        return registro
    
    #Agregar Nueva Compra
    def insertCompra(self,date,proveedor,total):
        cursor = self.control.cursor()
        sql = """INSERT INTO Tabla_Compras (Fecha,Proveedor, Total) VALUES ("{}","{}","{}")""".format(date,proveedor,total)
        cursor.execute(sql)
        compra_id = cursor.lastrowid
        self.control.commit()
        return compra_id
    
    #Eliminar Compra
    def deleteCompra(self,codCompra):
        cursor = self.control.cursor()
        sql = """DELETE FROM Tabla_Compras WHERE CodCompra = {}""".format(codCompra)
        cursor.execute(sql)
        self.control.commit()


    #Actualizar Total de Compra
    def updateCompraTotal(self,codVen, total):
        cursor = self.control.cursor()
        sql = """UPDATE Tabla_Compras SET Total = "{}" WHERE CodCompra = {} """.format(total,codVen)
        cursor.execute(sql)
        self.control.commit()
        cursor.close()