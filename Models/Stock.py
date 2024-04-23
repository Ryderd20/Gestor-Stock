import sys
import os
myDir = os.getcwd()
sys.path.append(myDir)


class Stock():


    #-----------Constructor----------------
    def __init__(self,connection):
        self.control = connection


        #-------------CREAR LA TABLA--------------
        cursor = self.control.cursor()
        sql = """CREATE TABLE IF NOT EXISTS "Tabla_Stock" (
	    "Producto"	TEXT NOT NULL,
	    "Cantidad"	REAL NOT NULL,
	    "Proveedor"	TEXT NOT NULL);"""

        cursor.execute(sql)
        self.control.commit()


    
    #Obtener todo el Stock
    def getStock(self):
        cursor = self.control.cursor()
        sql = """SELECT * FROM Tabla_Stock"""
        cursor.execute(sql)
        registro = cursor.fetchall()
        cursor.close()
        return registro
    

    #Agregar Nuevo Producto al Stock
    def insertArticulo(self,producto,cantidad,proveedor):
        cursor = self.control.cursor()
        sql = """INSERT INTO Tabla_Articulos (Producto, Cantidad, Proveedor) VALUES ("{}","{}","{}")""".format(producto,cantidad,proveedor)
        cursor.execute(sql)
        self.control.commit()



    #Eliminar un Producto del Stock
    def deleteStock(self,cod):
        cursor = self.control.cursor()
        sql = """DELETE FROM Tabla_Stock WHERE Codigo = {}""".format(cod)
        cursor.execute(sql)
        self.control.commit()


    
    #Obetener Stock por Nombre
    def getStockNom(self,nom):
        cursor = self.control.cursor()
        sql = """SELECT * FROM Tabla_Stock WHERE Producto = ?"""
        cursor.execute(sql, (nom,))
        registro = cursor.fetchall()
        if registro:
            return registro