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

    #Muestra la lista de Articulos
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


    #Agregar nuevo Articulo
    def agregar_articulo(self):
        self.art_view.signal_nuevo_articulo.setText("Espacios obligatorios*")

        nombre = self.art_view.input_nombre_articulo_nuevo.text()
        proveedor = 1 #valor temporal 
        costo = self.art_view.input_costo_articulo_nuevo.text()
        precio = self.art_view.input_precio_articulo_nuevo.text()
        descripcion = self.art_view.input_descripcion_articulo_nuevo.text()

        if nombre !="" and costo !="" and precio !="":
            try:
                costo_float = float(costo)
                precio_float = float(precio)

                self.articulos.insertArticulo(nombre,proveedor,costo_float,precio_float,descripcion)
                self.limpiar_articulo_nuevo()
                self.art_view.signal_nuevo_articulo.setText("Registrado con exito")
            except ValueError:
                self.art_view.signal_nuevo_articulo.setText("Los espacios Costo y Precio deben ser numerales")
        else:
            self.art_view.signal_nuevo_articulo.setText("Hay espacios obligatorios vacios")


    #Elimina el Articulo seleccionado
    def eliminar_articulo(self):
        item = self.art_view.table_articulos.item(self.art_view.table_articulos.currentRow(),0).text()
        if item != None:
            articulo = self.articulos.getArticuloCod(item)
            if articulo:
                self.articulos.deleteArticulo(item)
                self.mostrar_articulos()

    #Limpiar los input para agregar un nuevo articulo
    def limpiar_articulo_nuevo(self):
            self.art_view.input_nombre_articulo_nuevo.clear()
            self.art_view.input_costo_articulo_nuevo.clear()
            self.art_view.input_precio_articulo_nuevo.clear()
            self.art_view.input_descripcion_proveedor_nuevo.clear()






        

        
        




    




        




    

