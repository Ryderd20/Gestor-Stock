import sys
import os


myDir = os.getcwd()
sys.path.append(myDir)

from PyQt5.QtCore import QDate
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox,QInputDialog, QLineEdit
from DataBase.Connection import connection
from Models.Compras import Compras
from Models.DetalleCompra import DetalleCompra
from Models.Stock import Stock
from Models.Productos import Productos
from Models.Proveedores import Proveedores


class ComprasController():

    #-----------------Constructor----------------------
    def __init__(self,view):
        self.compras = Compras(connection())
        self.detalleCompra = DetalleCompra(connection())
        self.stock = Stock(connection())
        self.productos= Productos(connection())
        self.proveedores = Proveedores(connection())

        self.compras_view = view
    

    #Mostrar Registro de Compras
    def mostrar_compras(self):

        datos = self.compras.getCompras()
        num_filas = len(datos)
        num_columnas = 4 
        
        self.compras_view.table_compras.setRowCount(num_filas)
        self.compras_view.table_compras.setColumnCount(num_columnas)

        self.compras_view.label_total_compra.setText("-")

        for fila, registro in enumerate(datos):
            for columna, valor in enumerate(registro):
                item = QtWidgets.QTableWidgetItem(str(valor))
                self.compras_view.table_compras.setItem(fila, columna, item)

        tabla= self.compras_view.table_compras
        header = tabla.horizontalHeader()
        header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(0,QtWidgets.QHeaderView.Interactive)
        header.setSectionResizeMode(1,QtWidgets.QHeaderView.Interactive)
        header.setSectionResizeMode(2,QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(3,QtWidgets.QHeaderView.Interactive)



    # Cargar Lista de Proveedores en ComboBox
    def cargarListaProveedores(self):
        self.compras_view.comboBox_nuevaCompra_listaProv.clear()
        lista = self.proveedores.getListProveevores()
        self.compras_view.comboBox_nuevaCompra_listaProv.addItem("Ninguno")
        for prov in lista:
            texto_proveedor = str(prov).replace("(", "").replace(")", "").replace("'", "").replace('"', '').replace(',', '')
            self.compras_view.comboBox_nuevaCompra_listaProv.addItem(texto_proveedor)


    #Mostrar Detalle de la Compra seleccionada
    def mostrar_detalleCompraSeleccionada(self):
        
        codCompra = self.compras_view.table_compras.item(self.compras_view.table_compras.currentRow(), 0).text()

        datos = self.detalleCompra.getDetalle(codCompra)

        num_filas = len(datos)
        num_columnas = 4
        
        self.compras_view.table_detalleCompraSeleccionada.setRowCount(num_filas)
        self.compras_view.table_detalleCompraSeleccionada.setColumnCount(num_columnas)

        for fila, registro in enumerate(datos):
            for columna, valor in enumerate(registro):
                item = QtWidgets.QTableWidgetItem(str(valor))
                self.compras_view.table_detalleCompraSeleccionada.setItem(fila, columna, item)

        tabla =  self.compras_view.table_detalleCompraSeleccionada
        header = tabla.horizontalHeader()
        header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(0,QtWidgets.QHeaderView.Interactive)
        header.setSectionResizeMode(1,QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(2,QtWidgets.QHeaderView.Interactive)
        header.setSectionResizeMode(3,QtWidgets.QHeaderView.Interactive)

    #Ingresar Nueva Compra
    def nueva_compra(self,date):
        total= 0
        self.proveedor = self.compras_view.comboBox_nuevaCompra_listaProv.currentText()
        self.codCompra = self.compras.insertCompra(date,self.proveedor,total)
        self.mostrar_detalleCompra()
        self.compras_view.label_proveedor.setText(str(self.proveedor))
        self.compras_view.label_codCompra.setText(str(self.codCompra))
        self.mostrar_productos_de_proveedor()


    # Eliminar Compra
    def eliminar_compra_seleccionada(self):
        current_row = self.compras_view.table_compras.currentRow()
        if current_row != -1:
            codVen = self.compras_view.table_compras.item(current_row, 0).text()
            if codVen:
                reply = QMessageBox.question(self.compras_view, 'Confirmar Eliminación',
                    f"¿Estás seguro de que deseas eliminar la compra?",
                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                if reply == QMessageBox.Yes:
                    password, ok = QInputDialog.getText(self.compras_view, 'Contraseña',
                        'Introduce la contraseña de administrador:',
                        QLineEdit.Password)
                    if ok and password == 'admin':  
                        self.compras.deleteCompra(codVen)
                        self.detalleCompra.deleteDetalle(codVen)
                        self.mostrar_compras()
                    else:
                        mensaje = "Contraseña incorrecta. No se eliminó la compra."
                        self.mensaje_advertencia(mensaje)
        else:
            mensaje = "Debes seleccionar una Compra"
            self.mensaje_advertencia(mensaje)



    #Cancelar la Compra
    def cancelar_compra(self):
        self.compras.deleteCompra(self.codCompra)
        self.detalleCompra.deleteDetalle(self.codCompra)


    # Mostrar la lista de Productos de dicho Proveedor
    def mostrar_productos_de_proveedor(self):

        if self.proveedor == "Ninguno":
            datos = self.productos.getProductosProveedorNulo()
            num_filas = len(datos)
            num_columnas = 4  

            self.compras_view.table_compra_ProductoxProveedor.setRowCount(num_filas)
            self.compras_view.table_compra_ProductoxProveedor.setColumnCount(num_columnas)

            for fila, registro in enumerate(datos):
                for columna, valor in enumerate(registro):
                    item = QtWidgets.QTableWidgetItem(str(valor))
                    self.compras_view.table_compra_ProductoxProveedor.setItem(fila, columna, item)
        else:
            datos = self.productos.getProductosProveedor(str(self.proveedor))
            num_filas = len(datos)
            num_columnas = 4  

            self.compras_view.table_compra_ProductoxProveedor.setRowCount(num_filas)
            self.compras_view.table_compra_ProductoxProveedor.setColumnCount(num_columnas)

            for fila, registro in enumerate(datos):
                for columna, valor in enumerate(registro):
                    item = QtWidgets.QTableWidgetItem(str(valor))
                    self.compras_view.table_compra_ProductoxProveedor.setItem(fila, columna, item)
        

        tabla = self.compras_view.table_compra_ProductoxProveedor
        header = tabla.horizontalHeader()
        header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(0,QtWidgets.QHeaderView.Interactive)
        header.setSectionResizeMode(1,QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(2,QtWidgets.QHeaderView.Interactive)
        header.setSectionResizeMode(3,QtWidgets.QHeaderView.Interactive)
        

    
    #Mostrar Detalle de la Compra en proceso
    def mostrar_detalleCompra(self):
        
        datos = self.detalleCompra.getDetalle(self.codCompra)

        num_filas = len(datos)
        num_columnas = 4
        
        self.compras_view.table_detalleCompra.setRowCount(num_filas)
        self.compras_view.table_detalleCompra.setColumnCount(num_columnas)


        for fila, registro in enumerate(datos):
            for columna, valor in enumerate(registro):
                item = QtWidgets.QTableWidgetItem(str(valor))
                self.compras_view.table_detalleCompra.setItem(fila, columna, item)

        tabla =  self.compras_view.table_detalleCompra
        header = tabla.horizontalHeader()
        header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(0,QtWidgets.QHeaderView.Interactive)
        header.setSectionResizeMode(1,QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(2,QtWidgets.QHeaderView.Interactive)
        header.setSectionResizeMode(3,QtWidgets.QHeaderView.Interactive)


    # Agregar un Producto al Detalle de la Compra
    def cargar_producto(self):
        current_row = self.compras_view.table_compra_ProductoxProveedor.currentRow()

        if current_row != -1:
            codItem = self.compras_view.table_compra_ProductoxProveedor.item(current_row, 0).text()

            if codItem:
                self.producto = self.productos.getProductoCod(codItem)

                if self.producto:
                    cantidad_a_agregar = self.compras_view.spinBox_agregarDetalleCompra.value()

                    # Verificar si el producto ya está en el detalle de la compra
                    self.en_detalle = self.detalleCompra.getInDetalle(self.codCompra, codItem)

                    if self.en_detalle:
                        cantidad_actual = int(self.en_detalle[0])
                        nueva_cantidad = cantidad_actual + cantidad_a_agregar
                        subtotal = self.productos.getPrecioCompraProducto(codItem)[0] * nueva_cantidad
                        self.detalleCompra.updateDetalle(self.codCompra, codItem, nueva_cantidad, subtotal)
                    else:
                        nombre_producto = self.productos.getProductoCod(codItem)[1]  
                        subtotal = self.productos.getPrecioCompraProducto(codItem)[0] * cantidad_a_agregar
                        self.detalleCompra.insertDetalle(self.codCompra, codItem, nombre_producto, cantidad_a_agregar, subtotal)

                    total = self.detalleCompra.getDetalleTotal(self.codCompra)[0]
                    self.compras.updateCompraTotal(self.codCompra, total)
                    self.compras_view.label_total_compra.setText(str(total))
                    self.mostrar_detalleCompra()
                else:
                    mensaje = "Producto no encontrado"
                    self.mensaje_advertencia(mensaje)
        else:
            mensaje = "Debes seleccionar un Producto"
            self.mensaje_advertencia(mensaje)


    # Restar Producto de Detalle de Compra
    def restar_producto(self):
        current_row = self.compras_view.table_detalleCompra.currentRow()

        if current_row != -1:
            codProd_item = self.compras_view.table_detalleCompra.item(current_row, 0)

            if codProd_item:
                codProd = codProd_item.text()
                cantidadDetalle = self.detalleCompra.getDetalleCantidad(self.codCompra, codProd)
                cantidadDetalle = cantidadDetalle[0] if cantidadDetalle else 0
                resta = int(self.compras_view.spinBox_restarDetalleCompra.value())

                if cantidadDetalle >= resta:
                    nuevaCantidad = cantidadDetalle - resta
                    if nuevaCantidad > 0:
                        subtotal = self.productos.getPrecioCompraProducto(codProd)[0] * nuevaCantidad
                        self.detalleCompra.updateDetalle(self.codCompra, codProd, nuevaCantidad, subtotal)
                    else:
                        self.detalleCompra.deleteDetalle(self.codCompra, codProd)
                    self.mostrar_detalleCompra()

                    # Actualizar el total de la compra
                    total = self.detalleCompra.getDetalleTotal(self.codCompra)[0]
                    self.compras.updateCompraTotal(self.codCompra, total)
                    self.compras_view.label_total_compra.setText(str(total))
                else:
                    mensaje = "La cantidad ingresada es superior a la disponible en el Detalle"
                    self.mensaje_advertencia(mensaje)
        else:
            mensaje = "Debes seleccionar un Producto en Detalle de Compra"
            self.mensaje_advertencia(mensaje)


    def buscar_producto_de_proveedor(self):
        nombre_producto = self.compras_view.input_nombre_detalleCompra.text().lower()
        
        if not nombre_producto:
            self.mostrar_productos_de_proveedor()
            return
        
        if self.proveedor == "Ninguno":
            datos=self.productos.getProductosProveedorNuloNombre(nombre_producto)
        else:
            datos=self.productos.getProductosProveedorNombre(self.proveedor,nombre_producto)

        num_filas = len(datos)
        num_columnas = 4  

        self.compras_view.table_compra_ProductoxProveedor.setRowCount(num_filas)
        self.compras_view.table_compra_ProductoxProveedor.setColumnCount(num_columnas)

        for fila, registro in enumerate(datos):
            for columna, valor in enumerate(registro):
                item = QtWidgets.QTableWidgetItem(str(valor))
                self.compras_view.table_compra_ProductoxProveedor.setItem(fila, columna, item)
        

        tabla = self.compras_view.table_compra_ProductoxProveedor
        header = tabla.horizontalHeader()
        header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(0,QtWidgets.QHeaderView.Interactive)
        header.setSectionResizeMode(1,QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(2,QtWidgets.QHeaderView.Interactive)
        header.setSectionResizeMode(3,QtWidgets.QHeaderView.Interactive)

        self.compras_view.input_nombre_detalleCompra.clear()


    # Actualizar el Stock
    def añadir_compra_a_stock(self):
        detalles = self.detalleCompra.getDetallePorCompra(self.codCompra)

        for detalle in detalles:
            codProd, cantidad = detalle[0], detalle[1]

            # Obtener la cantidad actual en el stock
            cantidad_actual_en_stock = self.stock.getStockCantidad(codProd)

            if cantidad_actual_en_stock is None or cantidad_actual_en_stock[0] == 0:
                # Insertar nuevo registro en el stock si no existe
                self.stock.insertProducto(codProd, cantidad)
            else:
                cantidad_actual_en_stock = cantidad_actual_en_stock[0]
                # Sumar la cantidad comprada al stock actual
                nueva_cantidad_en_stock = cantidad_actual_en_stock + cantidad
                # Actualizar el stock en la base de datos
                self.stock.updateStock(codProd, nueva_cantidad_en_stock)




    



    #Caja de Mensajes
    def mensaje_advertencia(self,mensaje):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowTitle("Advertencia")
        msg.setText(mensaje)
        msg.exec_()