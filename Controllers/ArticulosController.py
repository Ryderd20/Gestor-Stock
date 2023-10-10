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




    def modificar_articulo(self):
        table = self.art_view.table_articulos
        articulo = []
        fila = []

        for row_number in range(table.rowCount()):
            for column_number in range(table.columnCount()):
                if table.item(row_number,column_number) != None:
                    fila.append(table.item(row_number,column_number).text())
            if len(fila)>0:
                articulo.append(fila)
            fila= []

        if len(articulo) >0:
            for arts in articulo:
                self.articulos.updateArticulos(arts[0],arts[1],arts[2],arts[3],arts[4],arts[5])

        self.mostrar_articulos()

    def crear_articulo(self,cod,nombre,precio,descripcion,proveedor):
        if cod and nombre and precio and descripcion and proveedor:
            self.articulos.insertArticulo(cod,nombre,precio,descripcion,proveedor)
        
        self.mostrar_articulos()

    def eliminar_articulo(self):
        table = self.art_view.table_articulos
        if table.currentItem() != None:
            cod = table.currentItem().text()
            articulo = self.articulos.getArticuloCod(cod)
            if articulo:
                self.articulos.deleteArticulo(cod)
                self.mostrar_articulos()

    def buscar_Articulo(self,nombre):
        self.articulos.getArticuloNom(nombre)
        
        




    




        




    

