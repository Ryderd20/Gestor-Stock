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
        num_columnas = 4     #podria obtenerlo solo con self.stock_view.table_articulos.rowCount  //probar
        
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
        num_columnas = 3    #podria obtenerlo solo con self.stock_view.table_productos.rowCount  //probar
        
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



    
            
    def cargar_producto_stock(self):
        
    
        if self.stock_view.table_stock_listaProductos.currentRow() != -1:
            item = self.stock_view.table_stock_listaProductos.item(self.stock_view.table_stock_listaProductos.currentRow(), 0).text()
            
            if item is not None:
                self.producto = self.productos.getProductoCod(item)
                

                if self.producto:
                    self.en_stock = self.stock.getInStock(item)
                    if self.en_stock:
                        cantidad = int(self.en_stock[2]) + int(self.stock_view.spinBox_Agregar.value())
                        self.stock.updateStock(item, cantidad)
                        print (self.en_stock[2])
                        self.mostrar_stock()
                    else:
                        nombre = self.stock_view.table_stock_listaProductos.item(self.stock_view.table_stock_listaProductos.currentRow(), 1).text()
                        cantidad = int(self.stock_view.spinBox_Agregar.value())
                        descripcion = self.stock_view.table_stock_listaProductos.item(self.stock_view.table_stock_listaProductos.currentRow(), 2).text()
                        self.stock.insertProducto(item,nombre,cantidad,descripcion)
                        self.mostrar_stock()



    def restar_cantidad_producto(self):
    # Verificar si se ha seleccionado una fila en la tabla de productos
        if self.stock_view.table_stock.currentRow() != -1:
            item = self.stock_view.table_stock.item(self.stock_view.table_stock.currentRow(), 0).text()
        
        # Verificar si se ha proporcionado una cantidad a restar
            if self.stock_view.spinBox_Restar.value() > 0:
                self.producto = self.stock.getInStock(item)
                
                # Verificar si el producto está en stock
                if self.producto:
                    # Obtener la cantidad actual en stock y la cantidad a restar
                    cantidad_actual = int(self.producto[2])
                    cantidad_a_restar = self.stock_view.spinBox_Restar.value()
                    
                    # Calcular la nueva cantidad después de restar
                    nueva_cantidad = cantidad_actual - cantidad_a_restar
                    
                    # Verificar si la cantidad después de restar es positiva
                    if nueva_cantidad >= 0:
                        # Actualizar la cantidad en el stock
                        self.stock.updateStock(item, nueva_cantidad)
                        # Actualizar la vista del stock
                        self.mostrar_stock()
                    else:
                        # Mostrar un mensaje de error si la cantidad a restar es mayor que la cantidad en stock
                        print("Error: La cantidad a restar es mayor que la cantidad en stock")
                else:
                    # Mostrar un mensaje de error si el producto no está en stock
                    print("Error: El producto seleccionado no está en stock")
            else:
                # Mostrar un mensaje de error si no se ha proporcionado una cantidad válida a restar
                print("Error: Debe ingresar una cantidad válida para restar")

                


    def buscar_producto_por_nombre(self):
    # Paso 1: Obtener el texto ingresado en el campo de búsqueda
        nombre_producto = self.stock_view.input_nombre_producto_buscar_stock.text().lower()
        
        # Paso 2: Realizar la búsqueda en la tabla "table_stock_listaProductos"
        resultados_tabla_1 = []
        for fila in range(self.stock_view.table_stock_listaProductos.rowCount()):
            nombre_fila = self.stock_view.table_stock_listaProductos.item(fila, 1).text().lower()
            if nombre_producto in nombre_fila:
                resultados_tabla_1.append([self.stock_view.table_stock_listaProductos.item(fila, columna).text() 
                                        for columna in range(self.stock_view.table_stock_listaProductos.columnCount())])
        
        # Paso 3: Realizar la búsqueda en la tabla "table_stock"
        resultados_tabla_2 = []
        for fila in range(self.stock_view.table_stock.rowCount()):
            nombre_fila = self.stock_view.table_stock.item(fila, 1).text().lower()
            if nombre_producto in nombre_fila:
                resultados_tabla_2.append([self.stock_view.table_stock.item(fila, columna).text() 
                                        for columna in range(self.stock_view.table_stock.columnCount())])
        
        # Paso 4: Mostrar los resultados de la búsqueda en ambas tablas
        self.mostrar_resultados_busqueda(resultados_tabla_1, resultados_tabla_2)


    def mostrar_resultados_busqueda(self, resultados_tabla_1, resultados_tabla_2):

        
        # Mostrar resultados en la tabla "table_stock_listaProductos"
        self.stock_view.table_stock_listaProductos.setRowCount(len(resultados_tabla_1))
        for fila, resultado in enumerate(resultados_tabla_1):
            for columna, valor in enumerate(resultado):
                item = QtWidgets.QTableWidgetItem(valor)
                self.stock_view.table_stock_listaProductos.setItem(fila, columna, item)
        
        # Mostrar resultados en la tabla "table_stock"
        self.stock_view.table_stock.setRowCount(len(resultados_tabla_2))
        for fila, resultado in enumerate(resultados_tabla_2):
            for columna, valor in enumerate(resultado):
                item = QtWidgets.QTableWidgetItem(valor)
                self.stock_view.table_stock.setItem(fila, columna, item)

                    
                    
                    
        

    
   
   