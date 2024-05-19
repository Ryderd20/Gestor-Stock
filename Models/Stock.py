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
	    "CodStock"	INTEGER NOT NULL,
	    "Cantidad"	INTEGER NOT NULL,
	    PRIMARY KEY("CodStock"));"""

        cursor.execute(sql)
        self.control.commit()


    #Obtener todos los Productos en Stock
    def getStock(self):
        cursor = self.control.cursor()
        sql = """SELECT s.CodStock, p.Nombre, s.Cantidad, p.PrecioVenta, p.PrecioCompra, p.Proveedor, p.Descripcion, p.StockMin 
             FROM Tabla_Stock s
             INNER JOIN Tabla_Productos p ON s.CodStock = p.CodProd
             ORDER BY p.Nombre"""
        cursor.execute(sql)
        registro = cursor.fetchall()
        cursor.close()
        return registro
    

    #Obtener Producto en Stock
    def getInStock(self, cod):
        cursor = self.control.cursor()
        sql = """SELECT s.CodStock, p.Nombre, s.Cantidad, p.PrecioVenta, p.PrecioVenta, p.Proveedor, p.Descripcion FROM Tabla_Stock s, Tabla_Productos p WHERE s.CodStock = {}""".format(cod)
        cursor.execute(sql)
        registro = cursor.fetchone()
        cursor.close()
        return registro


    #Agregar Nuevo Producto al Stock
    def insertProducto(self,cod,cantidad):
        cursor = self.control.cursor()
        sql = """INSERT INTO Tabla_Stock (CodStock, Cantidad) VALUES ("{}","{}")""".format(cod,cantidad)
        cursor.execute(sql)
        self.control.commit()


    #Eliminar un Producto del Stock
    def deleteStock(self,cod):
        cursor = self.control.cursor()
        sql = """DELETE FROM Tabla_Stock WHERE CodStock = {}""".format(cod)
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
        

    #Obtener Codigo, Nombre y Precio de los Productos
    def getProductos(self):
        cursor = self.control.cursor()
        sql = """SELECT CodProd, Nombre, Precio, Descripcion FROM Tabla_Productos"""
        cursor.execute(sql)
        registro = cursor.fetchall()
        cursor.close()
        return registro
    

    #Actualizar la Cantidad 
    def updateStock(self,cod,cantidad):
        cursor = self.control.cursor()
        sql = """UPDATE Tabla_Stock SET Cantidad = "{}" WHERE CodStock = "{}" """.format(cantidad,cod)
        cursor.execute(sql)
        self.control.commit()
        cursor.close()


    #Obtener Cantidad en Stock
    def getStockCantidad(self,codStock):
        cursor = self.control.cursor()
        sql = """SELECT Cantidad FROM Tabla_Stock WHERE CodStock = "{}" """.format(codStock)
        cursor.execute(sql)
        cantidad = cursor.fetchone()
        self.control.commit()
        cursor.close()
        return cantidad if cantidad else (0,)
