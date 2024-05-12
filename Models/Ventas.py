import sys
import os
myDir = os.getcwd()
sys.path.append(myDir)


class Ventas():


    #-----------Constructor----------------
    def __init__(self,connection):
        self.control = connection

        #-------------CREAR LA TABLA--------------
        cursor = self.control.cursor()
        sql = """CREATE TABLE IF NOT EXISTS "Tabla_Ventas" (
	    "CodVenta"	INTEGER NOT NULL,
	    "Fecha"	TEXT,
	    "Total"	REAL,
	    PRIMARY KEY("CodVenta" AUTOINCREMENT)
        );"""

        cursor.execute(sql)
        self.control.commit()

    #Obtener registro de Ventas
    def getVentas(self):
        cursor = self.control.cursor()
        sql = """SELECT * FROM Tabla_Ventas ORDER BY CodVenta DESC"""
        cursor.execute(sql)
        registro = cursor.fetchall()
        cursor.close()
        return registro
    
    #Agregar Nueva Venta
    def insertVenta(self,date,total):
        cursor = self.control.cursor()
        sql = """INSERT INTO Tabla_Ventas (Fecha, Total) VALUES ("{}","{}")""".format(date,total)
        cursor.execute(sql)
        venta_id = cursor.lastrowid
        self.control.commit()
        return venta_id
    
    #Eliminar Venta
    def deleteVenta(self,cod):
        cursor = self.control.cursor()
        sql = """DELETE FROM Tabla_Ventas WHERE CodVenta = {}""".format(cod)
        cursor.execute(sql)
        self.control.commit()


    #Actualizar Total de Venta
    def updateVentaTotal(self,codVen, total):
        cursor = self.control.cursor()
        sql = """UPDATE Tabla_Ventas SET Total = "{}" WHERE CodVenta = {} """.format(total,codVen)
        cursor.execute(sql)
        self.control.commit()
        cursor.close()


    #Obtener Ventas entre Fechas
    def getVentasEntreFechas(self,fecha_inicial,fecha_final):
        cursor = self.control.cursor()
        sql = f""" SELECT * FROM Tabla_Ventas WHERE Fecha BETWEEN '{fecha_inicial}' AND '{fecha_final}' """
        cursor.execute(sql)
        ventas_en_rango = cursor.fetchall()
        cursor.close()

        return ventas_en_rango
