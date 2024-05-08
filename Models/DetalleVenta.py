import sys
import os
myDir = os.getcwd()
sys.path.append(myDir)


class DetalleVenta():


    #-----------Constructor----------------
    def __init__(self,connection):
        self.control = connection


        #-------------CREAR LA TABLA--------------
        cursor = self.control.cursor()
        sql = """CREATE TABLE IF NOT EXISTS "Tabla_DetalleVenta" (
	    "CodVen"	INTEGER,
	    "CodProd"	INTEGER,
        "Producto" TEXT,
	    "Cantidad"	INTEGER,
	    "SubTotal"	REAL,
	    PRIMARY KEY("CodVen","CodProd")
        );"""

        cursor.execute(sql)
        self.control.commit()




    #Obtener Detalle de una Venta
    def getDetalle(self, codVenta):
        cursor = self.control.cursor()
        sql = """SELECT CodProd,Producto,Cantidad,SubTotal FROM Tabla_DetalleVenta WHERE CodVen = {}""".format(codVenta)
        cursor.execute(sql)
        registro = cursor.fetchall()
        cursor.close()
        return registro
    

    #Agregar Producto al DetalleVenta
    def insertDetalle(self,codVen,codProd,producto,cantidad,subtotal):
        cursor = self.control.cursor()
        sql = """INSERT INTO Tabla_DetalleVenta (CodVen,CodProd,Producto,Cantidad,SubTotal) VALUES ("{}", "{}", "{}","{}", "{}")""".format(codVen,codProd,producto,cantidad,subtotal)
        cursor.execute(sql)
        self.control.commit()


    #Obtener Producto en Detalle
    def getInDetalle(self,codVen, codProd):
        cursor = self.control.cursor()
        sql = """SELECT Cantidad FROM Tabla_DetalleVenta WHERE CodVen = {} AND CodProd = {}""".format(codVen, codProd)
        cursor.execute(sql)
        registro = cursor.fetchone()
        cursor.close()
        return registro
    
    
    #Actualizar Producto en Detalle
    def updateDetalle(self,codVen, codProd, cantidad, subtotal):
        cursor = self.control.cursor()
        sql = """UPDATE Tabla_DetalleVenta SET Cantidad = "{}", SubTotal = "{}" WHERE CodVen = {} AND CodProd = {} """.format(cantidad,subtotal,codVen,codProd)
        cursor.execute(sql)
        self.control.commit()
        cursor.close()

    #Eliminar Detalle de Venta
    def deleteDetalle(self,cod):
        cursor = self.control.cursor()
        sql = """DELETE FROM Tabla_DetalleVenta WHERE CodVen = {}""".format(cod)
        cursor.execute(sql)
        self.control.commit()

    #Obtener Total
    def getDetalleTotal(self,codVen):
        cursor = self.control.cursor()
        sql = """SELECT Sum(SubTotal) FROM Tabla_DetalleVenta WHERE CodVen = {}""".format(codVen)
        cursor.execute(sql)
        registro = cursor.fetchone()
        cursor.close()
        return registro
    
    #Obtener cantidad en Detalle
    def getDetalleCantidad(self,codVen,codProd):
        cursor = self.control.cursor()
        sql = """SELECT Cantidad FROM Tabla_DetalleVenta WHERE CodVen = {} AND CodProd = {}""".format(codVen,codProd)
        cursor.execute(sql)
        registro = cursor.fetchone()
        print(registro)
        cursor.close()
        return registro