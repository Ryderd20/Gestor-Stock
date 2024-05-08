import sys
import os
myDir = os.getcwd()
sys.path.append(myDir)


from PyQt5 import QtWidgets
from DataBase.Connection import connection
from Models.Ventas import Ventas
from Models.DetalleVenta import DetalleVenta
from Models.Stock import Stock


class DetalleVentaController():

    #-------------Constructor------------
    def __init__(self,view):
        self.ventas = Ventas(connection())
        self.detalleVenta = DetalleVenta(connection())
        self.stock = Stock(connection())
        self.detalleVenta_view = view

    
    #Mostrar los productos en Stock
    def mostrar_stock(self):
        datos = self.stock.getStock()
        num_filas = len(datos)
        num_columnas = 4     
        
        self.detalleVenta_view.table_venta_prodEnStock.setRowCount(num_filas)
        self.detalleVenta_view.table_venta_prodEnStock.setColumnCount(num_columnas)

        for fila, registro in enumerate(datos):
            for columna, valor in enumerate(registro):
                item = QtWidgets.QTableWidgetItem(str(valor))
                self.detalleVenta_view.table_venta_prodEnStock.setItem(fila, columna, item)

        
