import sys
import os
myDir = os.getcwd()
sys.path.append(myDir)


from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox
from DataBase.Connection import connection
from Models.Productos import Productos
from Models.Proveedores import Proveedores
from Models.Stock import Stock



class StockController():

    #------------------Constructor----------------
    def __init__(self,view):
        self.productos = Productos(connection())
        self.proveedores = Proveedores(connection())
        self.stock = Stock(connection())
        self.stock_view = view


    #Mostrar lista de los productos en Stock
    def mostrar_stock(self):
        datos = self.stock.getStock()
        num_filas = len(datos)
        num_columnas = 5
        
        self.stock_view.table_stock.setRowCount(num_filas)
        self.stock_view.table_stock.setColumnCount(num_columnas)

        for fila, registro in enumerate(datos):
            for columna, valor in enumerate(registro):
                item = QtWidgets.QTableWidgetItem(str(valor))
                self.stock_view.table_stock.setItem(fila, columna, item)
        
        
    #Mostrar lista de Productos
    def mostrar_productos(self):
        datos = self.stock.getProductos()
        num_filas = len(datos)
        num_columnas = 4
        
        self.stock_view.table_stock_listaProductos.setRowCount(num_filas)
        self.stock_view.table_stock_listaProductos.setColumnCount(num_columnas)

        for fila, registro in enumerate(datos):
            for columna, valor in enumerate(registro):
                item = QtWidgets.QTableWidgetItem(str(valor))
                self.stock_view.table_stock_listaProductos.setItem(fila, columna, item)
        
    
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
                        self.mostrar_productos()
                    else:
                        cantidad = int(self.stock_view.spinBox_Agregar.value())
                        self.stock.insertProducto(codItem,cantidad)
                        self.mostrar_stock()
                        self.mostrar_productos()
        else:
            mensaje= "Debe seleccionar un Producto en la Lista de Productos"
            self.mensaje_advertencia(mensaje)

    #Restar Producto del Stock
    def restar_cantidad_producto(self):

        if self.stock_view.table_stock.currentRow() != -1:
            item = self.stock_view.table_stock.item(self.stock_view.table_stock.currentRow(), 0).text()
        
            if self.stock_view.spinBox_Restar.value() > 0:
                self.producto = self.stock.getInStock(item)
                
                if self.producto:
                    cantidad_actual = int(self.producto[2])
                    cantidad_a_restar = int(self.stock_view.spinBox_Restar.value())
                    
                    nueva_cantidad = cantidad_actual - cantidad_a_restar

                    self.stock.updateStock(item, nueva_cantidad)
                    self.mostrar_stock()
                    self.mostrar_productos()
        else:
            mensaje= "Debe seleccionar un Producto en Stock"
            self.mensaje_advertencia(mensaje)

                
    #Buscar en Stock y Productos por nombre
    def buscar_producto_por_nombre(self):
        nombre_producto = self.stock_view.input_nombre_producto_buscar_stock.text().lower()
        
        resultados_tabla_1 = []
        for fila in range(self.stock_view.table_stock_listaProductos.rowCount()):
            nombre_fila = self.stock_view.table_stock_listaProductos.item(fila, 1).text().lower()
            if nombre_producto in nombre_fila:
                resultados_tabla_1.append([self.stock_view.table_stock_listaProductos.item(fila, columna).text() 
                                        for columna in range(self.stock_view.table_stock_listaProductos.columnCount())])
        
        resultados_tabla_2 = []
        for fila in range(self.stock_view.table_stock.rowCount()):
            nombre_fila = self.stock_view.table_stock.item(fila, 1).text().lower()
            if nombre_producto in nombre_fila:
                resultados_tabla_2.append([self.stock_view.table_stock.item(fila, columna).text() 
                                        for columna in range(self.stock_view.table_stock.columnCount())])
        
        self.mostrar_resultados_busqueda(resultados_tabla_1, resultados_tabla_2)
        self.stock_view.input_nombre_producto_buscar_stock.clear()


    #Mostrar resultado de busqueda
    def mostrar_resultados_busqueda(self, resultados_tabla_1, resultados_tabla_2):

        self.stock_view.table_stock_listaProductos.setRowCount(len(resultados_tabla_1))

        for fila, resultado in enumerate(resultados_tabla_1):
            for columna, valor in enumerate(resultado):
                item = QtWidgets.QTableWidgetItem(valor)
                self.stock_view.table_stock_listaProductos.setItem(fila, columna, item)
        
        self.stock_view.table_stock.setRowCount(len(resultados_tabla_2))
        for fila, resultado in enumerate(resultados_tabla_2):
            for columna, valor in enumerate(resultado):
                item = QtWidgets.QTableWidgetItem(valor)
                self.stock_view.table_stock.setItem(fila, columna, item)

    #Caja de Mensajes
    def mensaje_advertencia(self,mensaje):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowTitle("Advertencia")
        msg.setText(mensaje)
        msg.exec_()

                    
                    
                    
        

    
   
   