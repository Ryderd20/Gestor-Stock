import sys
import os
myDir = os.getcwd()
sys.path.append(myDir)

from PyQt5 import QtWidgets
from DataBase.Connection import connection
from Models.Articulos import Articulos




class ArticulosController():
    

    #------Constructor---------------
    def __init__(self,view):
        self.articulos = Articulos(connection())
        self.art_view = view


    def mostrar_articulos(self):
        datos = self.articulos.getArticulos()
        num_filas = len(datos)
        num_columnas = 6     #podria obtenerlo solo con self.art_view.table_articulos.rowCount  //probar
        

        self.art_view.table_articulos.setRowCount(num_filas)
        self.art_view.table_articulos.setColumnCount(num_columnas)

        for fila, registro in enumerate(datos):
            for columna, valor in enumerate(registro):
                item = QtWidgets.QTableWidgetItem(str(valor))
                self.art_view.table_articulos.setItem(fila, columna, item)




    def eliminar_articulo(self):
        table = self.art_view.table_articulos
        if table.currentItem() != None:
            cod = table.currentItem().text()
            articulo = self.articulos.getArticuloCod(cod)
            if articulo:
                self.articulos.deleteArticulo(cod)
                self.mostrar_articulos()

        
        




    




        




    

