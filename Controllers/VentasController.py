import sys
import os


myDir = os.getcwd()
sys.path.append(myDir)

from PyQt5.QtCore import QDate
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox,QInputDialog, QLineEdit
from DataBase.Connection import connection
from Models.Ventas import Ventas
from Models.DetalleVenta import DetalleVenta
from Models.Stock import Stock
from Models.Productos import Productos


class VentasController():

    #-----------------Constructor----------------------
    def __init__(self,view):
        self.ventas = Ventas(connection())
        self.detalleVenta = DetalleVenta(connection())
        self.stock = Stock(connection())
        self.productos= Productos(connection())

        self.ventas_view = view
    

    #Mostrar Registro de Ventas
    def mostrar_ventas(self):
        self.ventas_view.dateEdit_final.setDate(QDate.currentDate())
        self.ventas_view.dateEdit_inicial.setDate(QDate.currentDate())

        datos = self.ventas.getVentas()
        num_filas = len(datos)
        num_columnas = 3 
        
        self.ventas_view.table_ventas.setRowCount(num_filas)
        self.ventas_view.table_ventas.setColumnCount(num_columnas)

        self.ventas_view.label_total.setText("-")

        for fila, registro in enumerate(datos):
            for columna, valor in enumerate(registro):
                item = QtWidgets.QTableWidgetItem(str(valor))
                self.ventas_view.table_ventas.setItem(fila, columna, item)

        tabla= self.ventas_view.table_ventas
        header = tabla.horizontalHeader()
        header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(0,QtWidgets.QHeaderView.Interactive)
        header.setSectionResizeMode(1,QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(2,QtWidgets.QHeaderView.Stretch)

    
    #Mostrar los productos en Stock
    def mostrar_stock(self):
        datos = self.stock.getStockVenta()
        num_filas = len(datos)
        num_columnas = 5     
        
        self.ventas_view.table_venta_prodEnStock.setRowCount(num_filas)
        self.ventas_view.table_venta_prodEnStock.setColumnCount(num_columnas)

        for fila, registro in enumerate(datos):
            for columna, valor in enumerate(registro):
                item = QtWidgets.QTableWidgetItem(str(valor))
                self.ventas_view.table_venta_prodEnStock.setItem(fila, columna, item)

        tabla= self.ventas_view.table_venta_prodEnStock
        header = tabla.horizontalHeader()
        header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(0,QtWidgets.QHeaderView.Interactive)
        header.setSectionResizeMode(1,QtWidgets.QHeaderView.Interactive)
        header.setSectionResizeMode(2,QtWidgets.QHeaderView.Interactive)
        header.setSectionResizeMode(3,QtWidgets.QHeaderView.Interactive)
        header.setSectionResizeMode(4,QtWidgets.QHeaderView.Stretch)


    #Ingresar Nueva Venta
    def nueva_venta(self,date):
        total= 0
        self.codVenta = self.ventas.insertVenta(date,total)
        self.mostrar_detalleVenta(self.codVenta)
        self.ventas_view.label_codVenta.setText(str(self.codVenta))
        self.mostrar_stock()

    #Cancelar la Venta
    def cancelar_venta(self):
        self.ventas.deleteVenta(self.codVenta)
        self.detalleVenta.deleteDetalle(self.codVenta)

    # Eliminar Venta
    def eliminar_venta_seleccionada(self):
        current_row = self.ventas_view.table_ventas.currentRow()
        if current_row != -1:
            codVen = self.ventas_view.table_ventas.item(current_row, 0).text()
            if codVen:
                reply = QMessageBox.question(self.ventas_view, 'Confirmar Eliminación',
                    f"¿Estás seguro de que deseas eliminar la venta?",
                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                if reply == QMessageBox.Yes:
                    # Pedir la contraseña de administrador
                    password, ok = QInputDialog.getText(self.ventas_view, 'Contraseña',
                        'Introduce la contraseña de administrador:',
                        QLineEdit.Password)
                    if ok and password == 'admin': 
                        self.ventas.deleteVenta(codVen)
                        self.detalleVenta.deleteDetalle(codVen)
                        self.mostrar_ventas()
                    else:
                        mensaje = "Contraseña incorrecta. No se eliminó la venta."
                        self.mensaje_advertencia(mensaje)
        else:
            mensaje = "Debes seleccionar una Venta"
            self.mensaje_advertencia(mensaje)


    #Agregar un Producto al Detalle de la Venta
    def cargar_producto(self):
        current_row = self.ventas_view.table_venta_prodEnStock.currentRow()

        if current_row != -1:
            codItem = self.ventas_view.table_venta_prodEnStock.item(current_row, 0).text()

            if codItem:
                self.producto = self.productos.getProductoCod(codItem)

                if self.producto:
                    en_stock = self.stock.getStockCantidad(codItem)[0]  
                    cantidad_a_agregar = self.ventas_view.spinBox_agregarDetalle.value()

                    if en_stock >= cantidad_a_agregar:
                        en_stock_actualizado = en_stock - cantidad_a_agregar
                        self.stock.updateStock(codItem, en_stock_actualizado)

                        self.en_detalle = self.detalleVenta.getInDetalle(self.codVenta, codItem)

                        if self.en_detalle:
                            cantidad_actual = int(self.en_detalle[0]) 
                            nueva_cantidad = cantidad_actual + cantidad_a_agregar
                            subtotal = self.productos.getPrecioVentaProducto(codItem)[0] * nueva_cantidad
                            self.detalleVenta.updateDetalle(self.codVenta, codItem, nueva_cantidad, subtotal)
                        else:
                            nombre_producto = self.productos.getProductoCod(codItem)[1] #Nombre del Producto
                            subtotal = self.productos.getPrecioVentaProducto(codItem)[0] * cantidad_a_agregar
                            self.detalleVenta.insertDetalle(self.codVenta, codItem, nombre_producto, cantidad_a_agregar, subtotal)

                        total = self.detalleVenta.getDetalleTotal(self.codVenta)[0]
                        self.ventas.updateVentaTotal(self.codVenta, total)
                        self.ventas_view.label_total.setText(str(total))
                        self.mostrar_detalleVenta(self.codVenta)
                    else:
                        mensaje = "Producto insuficiente en Stock"
                        self.mensaje_advertencia(mensaje)


    #Restar Producto de Detalle
    def restar_producto(self):
        current_row = self.ventas_view.table_detalleVenta.currentRow()

        if current_row != -1:
            codProd_item = self.ventas_view.table_detalleVenta.item(current_row, 0)

            if codProd_item:
                codProd = codProd_item.text()
                cantidadDetalle = self.detalleVenta.getDetalleCantidad(self.codVenta, codProd)
                cantidadDetalle = cantidadDetalle[0] if cantidadDetalle else 0
                resta = int(self.ventas_view.spinBox_restarDetalle.value())

                if cantidadDetalle >= resta:
                    nuevaCantidad = cantidadDetalle - resta
                    subtotal = self.productos.getPrecioVentaProducto(codProd)[0] * nuevaCantidad

                    self.detalleVenta.updateDetalle(self.codVenta, codProd, nuevaCantidad, subtotal)
                    self.mostrar_detalleVenta(self.codVenta)

                    en_stock = self.stock.getStockCantidad(codProd)[0]
                    nuevo_en_stock = en_stock + resta  
                    self.stock.updateStock(codProd, nuevo_en_stock)
                else:
                    mensaje = "La cantidad ingresada es superior a la disponible en el Detalle"
                    self.mensaje_advertencia(mensaje)
        else:
            mensaje = "Debes seleccionar un Producto en Detalle de Venta"
            self.mensaje_advertencia(mensaje)


    #Mostrar Detalle de la Venta en proceso
    def mostrar_detalleVenta(self,codVen):
        
        datos = self.detalleVenta.getDetalle(codVen)

        num_filas = len(datos)
        num_columnas = 4
        
        self.ventas_view.table_detalleVenta.setRowCount(num_filas)
        self.ventas_view.table_detalleVenta.setColumnCount(num_columnas)


        for fila, registro in enumerate(datos):
            for columna, valor in enumerate(registro):
                item = QtWidgets.QTableWidgetItem(str(valor))
                self.ventas_view.table_detalleVenta.setItem(fila, columna, item)

        tabla= self.ventas_view.table_detalleVenta
        header = tabla.horizontalHeader()
        header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(0,QtWidgets.QHeaderView.Interactive)
        header.setSectionResizeMode(1,QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(2,QtWidgets.QHeaderView.Interactive)
        header.setSectionResizeMode(3,QtWidgets.QHeaderView.Interactive)


    #Mostrar Detalle de la Venta seleccionada
    def mostrar_detalleVentaSeleccionada(self):
        
        codVen = self.ventas_view.table_ventas.item(self.ventas_view.table_ventas.currentRow(), 0).text()

        datos = self.detalleVenta.getDetalle(codVen)

        num_filas = len(datos)
        num_columnas = 4
        
        self.ventas_view.table_detalleVentaSelec.setRowCount(num_filas)
        self.ventas_view.table_detalleVentaSelec.setColumnCount(num_columnas)

        for fila, registro in enumerate(datos):
            for columna, valor in enumerate(registro):
                item = QtWidgets.QTableWidgetItem(str(valor))
                self.ventas_view.table_detalleVentaSelec.setItem(fila, columna, item)

        tabla= self.ventas_view.table_detalleVentaSelec
        header = tabla.horizontalHeader()
        header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(0,QtWidgets.QHeaderView.Interactive)
        header.setSectionResizeMode(1,QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(2,QtWidgets.QHeaderView.Interactive)
        header.setSectionResizeMode(3,QtWidgets.QHeaderView.Interactive)


    #Buscar Stock por nombre
    def buscar_producto_por_nombre(self):
        nombre_producto = self.ventas_view.input_nombre_detalleVenta.text().lower()
        
        if not nombre_producto:
            self.mostrar_stock()
            return
        
        resultados_tabla = []
        for fila in range(self.ventas_view.table_venta_prodEnStock.rowCount()):
            nombre_fila = self.ventas_view.table_venta_prodEnStock.item(fila, 1).text().lower()
            if nombre_producto in nombre_fila:
                resultados_tabla.append([self.ventas_view.table_venta_prodEnStock.item(fila, columna).text() 
                for columna in range(self.ventas_view.table_venta_prodEnStock.columnCount())])
            

        self.mostrar_resultados_busqueda(resultados_tabla)
        
        self.ventas_view.input_nombre_detalleVenta.clear()


    #Mostrar Resultados
    def mostrar_resultados_busqueda(self, resultados_tabla,):

        self.ventas_view.table_venta_prodEnStock.setRowCount(len(resultados_tabla))

        for fila, resultado in enumerate(resultados_tabla):
            for columna, valor in enumerate(resultado):
                item = QtWidgets.QTableWidgetItem(valor)
                self.ventas_view.table_venta_prodEnStock.setItem(fila, columna, item)

        tabla= self.ventas_view.table_venta_prodEnStock



    #Filtrar Ventas por entre Fechas
    def buscar_ventas_por_rango_de_fechas(self):
    
        fecha_inicial = self.ventas_view.dateEdit_inicial.date()
        fecha_final = self.ventas_view.dateEdit_final.date()
        
        if fecha_inicial < fecha_final:
            fecha_inicial_str = fecha_inicial.toString('yyyy-MM-dd')
            fecha_final_str = fecha_final.toString('yyyy-MM-dd')

            datos = self.ventas.getVentasEntreFechas(fecha_inicial_str,fecha_final_str)

            num_filas = len(datos)
            num_columnas = 3 
            
            self.ventas_view.table_ventas.setRowCount(num_filas)
            self.ventas_view.table_ventas.setColumnCount(num_columnas)

            self.ventas_view.label_total.setText("-")

            for fila, registro in enumerate(datos):
                for columna, valor in enumerate(registro):
                    item = QtWidgets.QTableWidgetItem(str(valor))
                    self.ventas_view.table_ventas.setItem(fila, columna, item)

            tabla= self.ventas_view.table_ventas
            


        else:
            mensaje= "La fecha inicial es mayor a la fecha final"
            self.mensaje_advertencia(mensaje)




    #Caja de Mensajes
    def mensaje_advertencia(self,mensaje):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowTitle("Advertencia")
        msg.setText(mensaje)
        msg.exec_()
                