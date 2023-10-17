import sys
import os
myDir = os.getcwd()
sys.path.append(myDir)

from PyQt5 import QtWidgets
from DataBase.Connection import connection
from Models.Proveedores import Proveedores




class ProveedoresController():
    

    #------Constructor---------------
    def __init__(self,view):
        self.proveedores = Proveedores(connection())
        self.proveedores_view = view

    
    def mostrar_proveedores(self):
        datos = self.proveedores.getProveedores()
        num_filas = len(datos)
        num_columnas = 6 #self.proveedores_view.table_proveedores.rowCount()    
        

        self.proveedores_view.table_proveedores.setRowCount(num_filas)
        self.proveedores_view.table_proveedores.setColumnCount(num_columnas)

        for fila, registro in enumerate(datos):
            for columna, valor in enumerate(registro):
                item = QtWidgets.QTableWidgetItem(str(valor))
                self.proveedores_view.table_proveedores.setItem(fila, columna, item)

    def cargar_proveedor(self):
        item = self.proveedores_view.table_proveedores.item(self.proveedores_view.table_proveedores.currentRow(),0).text()
        if item != None:
            self.proveedor = self.proveedores.getProveedorCod(item)            
            if self.proveedor:
                self.proveedores_view.input_nombre_proveedor_modificar.setText(self.proveedor[1])
                self.proveedores_view.input_telefono_proveedor_modificar.setText(str(self.proveedor[2]))
                self.proveedores_view.input_email_proveedor_modificar.setText(self.proveedor[3])
                self.proveedores_view.input_direccion_proveedor_modificar.setText(self.proveedor[4])
                self.proveedores_view.input_descripcion_proveedor_modificar.setText(self.proveedor[5])
    

    def modificar_proveedor(self):
        if self.proveedor != "":
            nombre = self.proveedores_view.input_nombre_proveedor_modificar.text()
            telefono = int(self.proveedores_view.input_telefono_proveedor_modificar.text())
            email = self.proveedores_view.input_email_proveedor_modificar.text()
            direccion = self.proveedores_view.input_direccion_proveedor_modificar.text()
            descripcion = self.proveedores_view.input_descripcion_proveedor_modificar.text()

            self.proveedores.updateProveedores(self.cod,nombre,telefono,email,direccion,descripcion)
            self.mostrar_proveedores()

        
        
    def eliminar_proveedor(self):
        item = self.proveedores_view.table_proveedores.item(self.proveedores_view.table_proveedores.currentRow(),0).text()
        if item != None:
            proveedor = self.proveedores.getProveedorCod(item)
            if proveedor:
                self.proveedores.deleteProveedor(item)
                self.mostrar_proveedores()
