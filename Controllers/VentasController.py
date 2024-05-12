import sys
import os


myDir = os.getcwd()
sys.path.append(myDir)

from PyQt5.QtCore import QDate
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox
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
        self.redimensionar_tabla(tabla)


    #Ingresar Nueva Venta
    def nueva_venta(self,date):
        total= 0
        self.codVenta = self.ventas.insertVenta(date,total)
        self.mostrar_detalleVenta(self.codVenta)
        self.ventas_view.label_codVenta.setText(str(self.codVenta))

    #Cancelar la Venta
    def cancelar_venta(self):
        self.ventas.deleteVenta(self.codVenta)
        self.detalleVenta.deleteDetalle(self.codVenta)

    #Eliminar Venta
    def eliminar_venta_seleccionada(self):
        current_row = self.ventas_view.table_ventas.currentRow()
        if current_row != -1:
            codVen = self.ventas_view.table_ventas.item(current_row, 0).text()
            if codVen:    
                self.ventas.deleteVenta(codVen)
                self.detalleVenta.deleteDetalle(codVen)
                self.mostrar_ventas()
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
                            cantidad_actual = float(self.en_detalle[0]) 
                            nueva_cantidad = cantidad_actual + cantidad_a_agregar
                            subtotal = self.productos.getPrecioProducto(codItem)[0] * nueva_cantidad
                            self.detalleVenta.updateDetalle(self.codVenta, codItem, nueva_cantidad, subtotal)
                        else:
                            nombre_producto = self.productos.getProductoCod(codItem)[1] #Nombre del Producto
                            subtotal = self.productos.getPrecioProducto(codItem)[0] * cantidad_a_agregar
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
                    subtotal = self.productos.getPrecioProducto(codProd)[0] * nuevaCantidad

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
        self.redimensionar_tabla(tabla)


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
        self.redimensionar_tabla(tabla)


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
            self.redimensionar_tabla(tabla)


        else:
            mensaje= "La fecha inicial es mayor a la fecha final"
            self.mensaje_advertencia(mensaje)


    #Redimensionar la Tabla
    def redimensionar_tabla(self,tabla):
        header = tabla.horizontalHeader()
        header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(0,QtWidgets.QHeaderView.Interactive)

    #Caja de Mensajes
    def mensaje_advertencia(self,mensaje):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowTitle("Advertencia")
        msg.setText(mensaje)
        msg.exec_()
                