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

    


        
