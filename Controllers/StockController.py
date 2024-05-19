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
        num_columnas = 7
        
        self.stock_view.table_stock.setRowCount(num_filas)
        self.stock_view.table_stock.setColumnCount(num_columnas)

        for fila, registro in enumerate(datos):
            for columna, valor in enumerate(registro):
                item = QtWidgets.QTableWidgetItem(str(valor))
                self.stock_view.table_stock.setItem(fila, columna, item)

        tabla= self.stock_view.table_stock
        header = tabla.horizontalHeader()
        header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(0,QtWidgets.QHeaderView.Interactive)
        header.setSectionResizeMode(1,QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(2,QtWidgets.QHeaderView.Interactive)
        header.setSectionResizeMode(3,QtWidgets.QHeaderView.Interactive)
        header.setSectionResizeMode(4,QtWidgets.QHeaderView.Interactive)
        header.setSectionResizeMode(5,QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(6,QtWidgets.QHeaderView.Stretch)



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
        
        if not nombre_producto:
            self.mostrar_productos()
            self.mostrar_stock()
            return
        
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
        
        # Limpiar el campo de búsqueda después de mostrar resultados
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

        tabla= self.stock_view.table_stock
        self.redimensionar_tabla(tabla)
        tabla= self.stock_view.table_stock_listaProductos
        self.redimensionar_tabla(tabla)


    #Alertar la falta de Stock
    def mostrar_alerta_stock_bajo(self):
        productos_stock_bajo = []
        for stock in self.stock.getStock():
            if stock[2] < 10:  # La cantidad está en el segundo índice
                productos_stock_bajo.append(stock)

        if productos_stock_bajo:
            mensaje = "Los siguientes Productos estan escasos en Stock\n"
            for stock in productos_stock_bajo:
                mensaje += f"Código: {stock[0]} | Cantidad: {stock[2]} | Nombre: {stock[1]} \n"
            self.mensaje_advertencia(mensaje)



    #Caja de Mensajes
    def mensaje_advertencia(self,mensaje):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowTitle("Advertencia")
        msg.setText(mensaje)
        msg.exec_()

                    
                    
                    
        

    
   
   