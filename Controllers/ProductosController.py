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
    def __init__(self, view):
        self.productos = Productos(connection())
        self.proveedores = Proveedores(connection())
        self.prod_view = view

    # Mostrar la lista de Productos
    def mostrar_productos(self):
        datos = self.productos.getProductos()
        num_filas = len(datos)
        num_columnas = 7  # Ahora tenemos 7 columnas

        self.prod_view.table_productos.setRowCount(num_filas)
        self.prod_view.table_productos.setColumnCount(num_columnas)

        for fila, registro in enumerate(datos):
            for columna, valor in enumerate(registro):
                item = QtWidgets.QTableWidgetItem(str(valor))
                self.prod_view.table_productos.setItem(fila, columna, item)

        self.prod_view.comboBox_nuevo_producto_listaProv.clear()

        tabla = self.prod_view.table_productos
        self.redimensionar_tabla(tabla)

        self.prod_view.signal_nuevo_producto.setText("Espacios obligatorios*")

    # Agregar nuevo Producto
    def agregar_producto(self):
        

        nombre = self.prod_view.input_nombre_producto_nuevo.text()
        proveedor = self.prod_view.comboBox_nuevo_producto_listaProv.currentText()
        precioCompra = self.prod_view.input_precio_compra_producto_nuevo.text()
        precioVenta = self.prod_view.input_precio_venta_producto_nuevo.text()
        stockMin = self.prod_view.input_stock_min_producto_nuevo.text()
        descripcion = self.prod_view.input_descripcion_producto_nuevo.text()

        if nombre != "" and precioCompra != "" and precioVenta != "" and stockMin != "":
            try:
                precioCompra_float = float(precioCompra)
                precioVenta_float = float(precioVenta)
                stockMin_int = int(stockMin)

                self.productos.insertProducto(nombre, proveedor, precioCompra_float, precioVenta_float, stockMin_int, descripcion)
                self.limpiar_producto_nuevo()
                self.prod_view.signal_nuevo_producto.setText("Registrado con exito")
            except ValueError:
                self.prod_view.signal_nuevo_producto.setText("Los espacios de Precio y Stock Min deben ser numerales")
        else:
            self.prod_view.signal_nuevo_producto.setText("Hay espacios obligatorios vacios")

    # Eliminar el Producto seleccionado
    def eliminar_producto(self):
        current_row = self.prod_view.table_productos.currentRow()
        if current_row != -1:
            item = self.prod_view.table_productos.item(current_row, 0).text()
            if item:
                # Mostrar el mensaje de confirmación
                reply = QMessageBox.question(self.prod_view, 'Confirmar Eliminación',
                                            f"¿Estás seguro de que deseas eliminar este producto?",
                                            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                if reply == QMessageBox.Yes:
                    producto = self.productos.getProductoCod(item)
                    if producto:
                        self.productos.deleteProducto(item)
                        self.mostrar_productos()
        else:
            mensaje = "Debes seleccionar un Producto"
            self.mensaje_advertencia(mensaje)

        # Guardar Producto
    def modificar_producto(self):
        nombre = self.prod_view.input_nombre_producto_modificar.text().strip()
        precioCompra = self.prod_view.input_precio_compra_producto_modificar.text().strip()
        precioVenta = self.prod_view.input_precio_venta_producto_modificar.text().strip()
        stockMin = self.prod_view.input_stock_min_producto_modificar.text().strip()
        descripcion = self.prod_view.input_descripcion_producto_modificar.text().strip()

        if not nombre or not precioCompra or not precioVenta or not stockMin:
            self.prod_view.signal_modificar_producto.setText("Hay espacios obligatorios vacios")
            return False

        try:
            precioCompra_float = float(precioCompra)
        except ValueError:
            self.prod_view.signal_modificar_producto.setText("El espacio de Precio Compra debe ser numeral")
            return False

        try:
            precioVenta_float = float(precioVenta)
        except ValueError:
            self.prod_view.signal_modificar_producto.setText("El espacio de Precio Venta debe ser numeral")
            return False

        try:
            stockMin_int = int(stockMin)
        except ValueError:
            self.prod_view.signal_modificar_producto.setText("El espacio de Stock Min debe ser numeral")
            return False

        cod = self.producto[0]
        self.productos.updateProducto(cod, nombre, precioCompra_float, precioVenta_float, stockMin_int, descripcion)
        self.mostrar_productos()
        return True



    # Cargar Producto para Modificar
    def cargar_producto(self):
        self.prod_view.signal_modificar_producto.setText("Espacios obligatorios*")
        #self.cargarListaProveedores()

        if self.prod_view.table_productos.currentRow() != -1:
            item = self.prod_view.table_productos.item(self.prod_view.table_productos.currentRow(), 0).text()

            if item is not None:
                self.producto = self.productos.getProductoCod(item)

                if self.producto:
                    self.prod_view.input_nombre_producto_modificar.setText(self.producto[1])
                    self.prod_view.input_precio_compra_producto_modificar.setText(str(self.producto[3]))
                    self.prod_view.input_precio_venta_producto_modificar.setText(str(self.producto[4]))
                    self.prod_view.input_stock_min_producto_modificar.setText(str(self.producto[5]))
                    self.prod_view.input_descripcion_producto_modificar.setText(str(self.producto[6]))
                    self.prod_view.lab_proveedor_modificar.setText(str(self.producto[2]))

    # Limpiar espacios para agregar un nuevo Producto
    def limpiar_producto_nuevo(self):
        self.prod_view.input_nombre_producto_nuevo.clear()
        self.prod_view.input_precio_compra_producto_nuevo.clear()
        self.prod_view.input_precio_venta_producto_nuevo.clear()
        self.prod_view.input_stock_min_producto_nuevo.clear()
        self.prod_view.input_descripcion_producto_nuevo.clear()

    # Cargar Lista de Proveedores en ComboBox
    def cargarListaProveedores(self):
        self.prod_view.comboBox_nuevo_producto_listaProv.clear()
        lista = self.proveedores.getListProveevores()
        self.prod_view.comboBox_nuevo_producto_listaProv.addItem("Ninguno")
        for prov in lista:
            texto_proveedor = str(prov).replace("(", "").replace(")", "").replace("'", "").replace('"', '').replace(',', '')
            self.prod_view.comboBox_nuevo_producto_listaProv.addItem(texto_proveedor)

    # Buscar Producto por Nombre
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
            self.prod_view.input_nombre_producto_buscar.clear()

    # Redimensionar la Tabla
    def redimensionar_tabla(self, tabla):
        header = tabla.horizontalHeader()
        header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Interactive)  
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)      
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.Interactive)  
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.Interactive)  
        header.setSectionResizeMode(4, QtWidgets.QHeaderView.Interactive)  
        header.setSectionResizeMode(5, QtWidgets.QHeaderView.Interactive)  
        header.setSectionResizeMode(6, QtWidgets.QHeaderView.Stretch)      

    # Caja de Mensajes
    def mensaje_advertencia(self, mensaje):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowTitle("Advertencia")
        msg.setText(mensaje)
        msg.exec_()


    








        

        
        




    




        




    

