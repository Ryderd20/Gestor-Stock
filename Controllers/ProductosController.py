import sys
import os
myDir = os.getcwd()
sys.path.append(myDir)

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox
from DataBase.Connection import connection
from Models.Productos import Productos
from Models.Proveedores import Proveedores


class ProductosController():
    

    #------Constructor---------------
    def __init__(self,view):
        self.productos = Productos(connection())
        self.proveedores = Proveedores(connection())
        self.prod_view = view
        

    #Mostrar la lista de Productos
    def mostrar_productos(self):
        datos = self.productos.getProductos()
        num_filas = len(datos)
        num_columnas = 5  
        
        self.prod_view.table_productos.setRowCount(num_filas)
        self.prod_view.table_productos.setColumnCount(num_columnas)

        for fila, registro in enumerate(datos):
            for columna, valor in enumerate(registro):
                item = QtWidgets.QTableWidgetItem(str(valor))
                self.prod_view.table_productos.setItem(fila, columna, item)
        
        self.prod_view.comboBox_nuevo_producto_listaProv.clear()
        self.prod_view.comboBox_modificar_producto_listaProv.clear()


    #Agregar nuevo Producto
    def agregar_producto(self):
        self.prod_view.signal_nuevo_producto.setText("Espacios obligatorios*")

        nombre = self.prod_view.input_nombre_producto_nuevo.text()
        proveedor = self.prod_view.comboBox_nuevo_producto_listaProv.currentText()
        precio = self.prod_view.input_precio_producto_nuevo.text()
        descripcion = self.prod_view.input_descripcion_producto_nuevo.text()

        if nombre !="" and precio !="":
            try:
                precio_float = float(precio)

                self.productos.insertProducto(nombre,proveedor,precio_float,descripcion)
                self.limpiar_producto_nuevo()
                self.prod_view.signal_nuevo_producto.setText("Registrado con exito")
            except ValueError:
                self.prod_view.signal_nuevo_producto.setText("El espacio Precio debe ser numeral")
        else:
            self.prod_view.signal_nuevo_producto.setText("Hay espacios obligatorios vacios")


    #Eliminar el Producto seleccionado
    def eliminar_producto(self):
        current_row = self.prod_view.table_productos.currentRow()
        if current_row != -1:
            item = self.prod_view.table_productos.item(current_row, 0).text()
            if item:
                producto = self.productos.getProductoCod(item)
                if producto:
                    self.productos.deleteProducto(item)
                    self.mostrar_productos()
        else:
            mensaje = "Debes seleccionar un Producto"
            self.mensaje_advertencia(mensaje)


    #Guardar Producto
    def modificar_producto(self):
            
        nombre = self.prod_view.input_nombre_producto_modificar.text()
        proveedor = self.prod_view.comboBox_modificar_producto_listaProv.currentText()
        precio = self.prod_view.input_precio_producto_modificar.text()
        descripcion = self.prod_view.input_descripcion_producto_modificar.text()

        if nombre !="" and precio != "":
            try:
                precio_float = float(precio)
                cod = self.producto[0]
                self.productos.updateProducto(cod,nombre,proveedor,precio_float,descripcion)
                self.mostrar_productos()
            except ValueError:
                self.prod_view.signal_modificar_producto.setText("El espacio Precio debe ser numeral")

            return True
        else:
            return False
    
    
    #Cargar Producto para Modificar
    def cargar_producto(self):

        self.prod_view.signal_producto_modificado.setText("Espacios obligatorios*")
        self.cargarListaProveedores()

        if self.prod_view.table_productos.currentRow() != -1:
            item = self.prod_view.table_productos.item(self.prod_view.table_productos.currentRow(), 0).text()

            if item is not None:
                self.producto = self.productos.getProductoCod(item)

                if self.producto:
                    self.prod_view.input_nombre_producto_modificar.setText(self.producto[1])
                    self.prod_view.input_precio_producto_modificar.setText(str(self.producto[3]))
                    self.prod_view.input_descripcion_producto_modificar.setText(str(self.producto[4]))


    #Limpiar espacios para agregar un nuevo Producto
    def limpiar_producto_nuevo(self):
            self.prod_view.input_nombre_producto_nuevo.clear()
            self.prod_view.input_precio_producto_nuevo.clear()
            self.prod_view.input_descripcion_producto_nuevo.clear()


    #Cargar Lista de Proveedores en ComboBox
    def cargarListaProveedores(self):
        self.prod_view.comboBox_nuevo_producto_listaProv.clear()
        lista = self.proveedores.getListProveevores()
        self.prod_view.comboBox_nuevo_producto_listaProv.addItem("Ninguno")
        self.prod_view.comboBox_modificar_producto_listaProv.addItem("Ninguno")
        for prov in lista:
            texto_proveedor = str(prov).replace("(", "").replace(")", "").replace("'", "").replace('"', '').replace(',', '')
            self.prod_view.comboBox_nuevo_producto_listaProv.addItem(texto_proveedor)
            self.prod_view.comboBox_modificar_producto_listaProv.addItem(texto_proveedor)


    #Buscar Producto por Nombre
    def buscarProductoPorNombre(self):
        nombre = self.prod_view.input_nombre_producto_buscar.text()
        datos = self.productos.getProductoNom(nombre)

        if datos is not None:
            num_filas = len(datos)
        else:
            num_filas = 0

        num_columnas = self.prod_view.table_productos.columnCount()

        self.prod_view.table_productos.setRowCount(num_filas)
        self.prod_view.table_productos.setColumnCount(num_columnas)

        if datos:
            for fila, registro in enumerate(datos):
                for columna, valor in enumerate(registro):
                    item = QtWidgets.QTableWidgetItem(str(valor))
                    self.prod_view.table_productos.setItem(fila, columna, item)
            self.prod_view.input_nombre_producto_buscar.clear()
        else:
            self.mostrar_productos
            self.prod_view.input_nombre_producto_buscar.clear()


    #Caja de Mensajes
    def mensaje_advertencia(self,mensaje):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowTitle("Advertencia")
        msg.setText(mensaje)
        msg.exec_()

    








        

        
        




    




        




    

