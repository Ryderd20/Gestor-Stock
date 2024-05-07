import sys
import os
myDir = os.getcwd()
sys.path.append(myDir)


from PyQt5 import QtWidgets
from DataBase.Connection import connection
from Models.Productos import Productos
from Models.Proveedores import Proveedores
from Models.Stock import Stock



class StockController():

    def __init__(self,view):
        self.productos = Productos(connection())
        self.proveedores = Proveedores(connection())
        self.stock = Stock(connection())
        self.stock_view = view



    #Muestra la lista de los productos en Stock
    def mostrar_stock(self):
        datos = self.stock.getStock()
        num_filas = len(datos)
        num_columnas = 5     #podria obtenerlo solo con self.stock_view.table_articulos.rowCount  //probar
        
        self.stock_view.table_stock.setRowCount(num_filas)
        self.stock_view.table_stock.setColumnCount(num_columnas)

        for fila, registro in enumerate(datos):
            for columna, valor in enumerate(registro):
                item = QtWidgets.QTableWidgetItem(str(valor))
                self.stock_view.table_stock.setItem(fila, columna, item)
        
        


    #Muestra la lista de Productos
    def mostrar_productos(self):
        datos = self.stock.getProductos()
        num_filas = len(datos)
        num_columnas = 4    #podria obtenerlo solo con self.stock_view.table_productos.rowCount  //probar
        
        self.stock_view.table_stock_listaProductos.setRowCount(num_filas)
        self.stock_view.table_stock_listaProductos.setColumnCount(num_columnas)

        for fila, registro in enumerate(datos):
            for columna, valor in enumerate(registro):
                item = QtWidgets.QTableWidgetItem(str(valor))
                self.stock_view.table_stock_listaProductos.setItem(fila, columna, item)
        
       


    def cargarListaProveedores_Stock(self):
        self.stock_view.comboBox_nuevo_artStock_listaProv.clear()
        lista = self.proveedores.getListProveevores()
        self.stock_view.comboBox_nuevo_articulo_listaProv.addItem("Ninguno")
        for prov in lista:
            texto_proveedor = str(prov).replace("(", "").replace(")", "").replace("'", "").replace('"', '').replace(',', '')
            self.stock_view.comboBox_nuevo_artStock_listaProv.addItem(texto_proveedor)



    
    #Agregar Producto al Stock
    def cargar_producto_stock(self):
        
        if self.stock_view.table_stock_listaProductos.currentRow() != -1:
            codItem = self.stock_view.table_stock_listaProductos.item(self.stock_view.table_stock_listaProductos.currentRow(), 0).text()
            
            if codItem is not None:
                self.producto = self.productos.getProductoCod(codItem)
                
                if self.producto:
                    self.en_stock = self.stock.getInStock(codItem)
                    if self.en_stock:
                        cantidad = int(self.en_stock[2]) + int(self.stock_view.spinBox_Agregar.value())
                        self.stock.updateStock(codItem, cantidad)
                        self.mostrar_stock()
                    else:
                        cantidad = int(self.stock_view.spinBox_Agregar.value())
                        self.stock.insertProducto(codItem,cantidad)
                        self.mostrar_stock()



                    
                    
                    
        

    
   
   