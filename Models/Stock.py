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
	    "Codigo"	INTEGER NOT NULL,
	    "Producto"	TEXT NOT NULL,
	    "Cantidad"	REAL NOT NULL,
	    "Descripcion"	TEXT NOT NULL,
	    PRIMARY KEY("Codigo"));"""

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
    

    def getInStock(self, cod):
        cursor = self.control.cursor()
        sql = """SELECT * FROM Tabla_Stock WHERE Codigo = {}""".format(cod)
        cursor.execute(sql)
        registro = cursor.fetchone()
        cursor.close()
        return registro


    #Agregar Nuevo Producto al Stock
    def insertProducto(self,codigo,producto,cantidad,descripcion):
        cursor = self.control.cursor()
        sql = """INSERT INTO Tabla_Stock (Codigo, Producto, Cantidad, Descripcion) VALUES ("{}","{}","{}","{}")""".format(codigo,producto,cantidad,descripcion)
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
        


    def getProductos(self):
        cursor = self.control.cursor()
        sql = """SELECT Codigo, Nombre, Descripcion FROM Tabla_Productos"""
        cursor.execute(sql)
        registro = cursor.fetchall()
        cursor.close()
        return registro
    


    def updateStock(self,cod,cantidad):
        cursor = self.control.cursor()
        sql = """UPDATE Tabla_Stock SET Cantidad = "{}" WHERE Codigo = "{}" """.format(cantidad,cod)
        cursor.execute(sql)
        self.control.commit()
        cursor.close()