import sys
import os
myDir = os.getcwd()
sys.path.append(myDir)


class DetalleCompra():


    #-----------Constructor----------------
    def __init__(self,connection):
        self.control = connection


        #-------------CREAR LA TABLA--------------
        cursor = self.control.cursor()
        sql = """CREATE TABLE IF NOT EXISTS "Tabla_DetalleCompra" (
	    "CodCompra"	INTEGER,
	    "CodProd"	INTEGER,
        "Producto" TEXT,
	    "Cantidad"	INTEGER,
	    "SubTotal"	REAL,
	    PRIMARY KEY("CodCompra","CodProd")
        );"""

        cursor.execute(sql)
        self.control.commit()




    #Obtener Detalle de una Compra
    def getDetalle(self, codCompra):
        cursor = self.control.cursor()
        sql = """SELECT CodProd,Producto,Cantidad,SubTotal FROM Tabla_DetalleCompra WHERE CodCompra = {} AND Cantidad > 0""".format(codCompra)
        cursor.execute(sql)
        registro = cursor.fetchall()
        cursor.close()
        return registro
    

    #Agregar Producto al DetalleCompra
    def insertDetalle(self,codCompra,codProd,producto,cantidad,subtotal):
        cursor = self.control.cursor()
        sql = """INSERT INTO Tabla_DetalleCompra (CodCompra,CodProd,Producto,Cantidad,SubTotal) VALUES ("{}", "{}", "{}","{}", "{}")""".format(codCompra,codProd,producto,cantidad,subtotal)
        cursor.execute(sql)
        self.control.commit()


    #Obtener Producto en Detalle
    def getInDetalle(self,codCompra, codProd):
        cursor = self.control.cursor()
        sql = """SELECT Cantidad FROM Tabla_DetalleCompra WHERE CodCompra = {} AND CodProd = {}""".format(codCompra, codProd)
        cursor.execute(sql)
        registro = cursor.fetchone()
        cursor.close()
        return registro
    
    
    #Actualizar Producto en Detalle
    def updateDetalle(self,codCompra, codProd, cantidad, subtotal):
        cursor = self.control.cursor()
        sql = """UPDATE Tabla_DetalleCompra SET Cantidad = "{}", SubTotal = "{}" WHERE CodCompra = {} AND CodProd = {} """.format(cantidad,subtotal,codCompra,codProd)
        cursor.execute(sql)
        self.control.commit()
        cursor.close()

    #Eliminar Detalle de Compra
    def deleteDetalle(self,cod):
        cursor = self.control.cursor()
        sql = """DELETE FROM Tabla_DetalleCompra WHERE CodCompra = {}""".format(cod)
        cursor.execute(sql)
        self.control.commit()

    #Obtener Total
    def getDetalleTotal(self,codCompra):
        cursor = self.control.cursor()
        sql = """SELECT Sum(SubTotal) FROM Tabla_DetalleCompra WHERE CodCompra = {}""".format(codCompra)
        cursor.execute(sql)
        registro = cursor.fetchone()
        cursor.close()
        return registro
    
    #Obtener cantidad en Detalle
    def getDetalleCantidad(self,codCompra,codProd):
        cursor = self.control.cursor()
        sql = """SELECT Cantidad FROM Tabla_DetalleCompra WHERE CodCompra = {} AND CodProd = {}""".format(codCompra,codProd)
        cursor.execute(sql)
        registro = cursor.fetchone()
        cursor.close()
        return registro
    
    
    # Obtener detalle por compra
    def getDetallePorCompra(self, codCompra):
        cursor = self.control.cursor()
        sql = """SELECT CodProd, Cantidad FROM Tabla_DetalleCompra WHERE CodCompra = ?"""
        cursor.execute(sql, (codCompra,))
        registro = cursor.fetchall()
        cursor.close()
        return registro