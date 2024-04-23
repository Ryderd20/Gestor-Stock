import sys
import os
myDir = os.getcwd()
sys.path.append(myDir)


from PyQt5 import QtWidgets
from DataBase.Connection import connection
from Models.Articulos import Articulos
from Models.Proveedores import Proveedores
from Models.Stock import Stock



class StockController():

    def __init__(self,view):
        self.articulos = Articulos(connection())
        self.proveedores = Proveedores(connection())
        self.stock = Stock(connection())
        self.stock_view = view



    #Muestra la lista del Stock
    def mostrar_stock(self):
        datos = self.stock.getStock()
        num_filas = len(datos)
        num_columnas = 3     #podria obtenerlo solo con self.art_view.table_articulos.rowCount  //probar
        
        self.art_view.table_stock.setRowCount(num_filas)
        self.art_view.table_stock.setColumnCount(num_columnas)

        for fila, registro in enumerate(datos):
            for columna, valor in enumerate(registro):
                item = QtWidgets.QTableWidgetItem(str(valor))
                self.art_view.table_stock.setItem(fila, columna, item)
        
        self.art_view.comboBox_nuevo_artStock_listaProv.clear()
        self.art_view.comboBox_nuevo_artStock_listaProv.clear()



    def cargarListaProveedores_Stock(self):
        self.stock_view.comboBox_nuevo_artStock_listaProv.clear()
        lista = self.proveedores.getListProveevores()
        self.stock_view.comboBox_nuevo_articulo_listaProv.addItem("Ninguno")
        for prov in lista:
            texto_proveedor = str(prov).replace("(", "").replace(")", "").replace("'", "").replace('"', '').replace(',', '')
            self.stock_view.comboBox_nuevo_artStock_listaProv.addItem(texto_proveedor)



    def cargarListaArticulos_Stock(self):
        self.stock_view.comboBox_listaProd.clear()
        lista = self.articulos.getListArticulos()
        print (lista)
        for art in lista:
            texto_articulo = str(art).replace("(", "").replace(")", "").replace("'", "").replace('"', '').replace(',', '')
            self.stock_view.comboBox_listaProd.addItem(texto_articulo)
            




    def limpiar_stock_nuevo(self):
            self.art_view.input_nombre_articulo_nuevo.clear()
            self.art_view.input_costo_articulo_nuevo.clear()
            self.art_view.input_precio_articulo_nuevo.clear()
            self.art_view.input_descripcion_articulo_nuevo.clear()
    
    #Agregar nuevo Producto al Stock
    def agregar_stock(self):
        self.art_view.signal_nuevo_stock.setText("Espacios obligatorios*")

        producto = self.art_view.comboBox_listaProd.currentText()
        cantidad = self.art_view.cantidadProd.text()
        proveedor = self.art_view.comboBox_nuevo_articulo_listaProv.currentText()
        

        if producto !="" and cantidad !="" and proveedor !="":
            try:
                cantidad_float = float(cantidad)
                
                self.articulos.insertArticulo(producto,proveedor,cantidad_float)
                self.limpiar_articulo_nuevo()
                self.art_view.signal_nuevo_stock.setText("Registrado con exito")
            except ValueError:
                self.art_view.signal_nuevo_stock.setText("Los espacios Costo y Precio deben ser numerales")
        else:
            self.art_view.signal_nuevo_stock.setText("Hay espacios obligatorios vacios")