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
        num_columnas = 6 #self.proveedores_view.table_proveedores.rowCount    
        

        self.proveedores_view.table_proveedores.setRowCount(num_filas)
        self.proveedores_view.table_proveedores.setColumnCount(num_columnas)

        for fila, registro in enumerate(datos):
            for columna, valor in enumerate(registro):
                item = QtWidgets.QTableWidgetItem(str(valor))
                self.proveedores_view.table_proveedores.setItem(fila, columna, item)

    def cargar_proveedor(self):
        table = self.proveedores_view.table_proveedores
        if table.currentItem() != None:
            self.cod = table.currentItem().text()
            self.proveedor = self.proveedores.getProveedorCod(self.cod)

            
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

            #cod =  str("'"+ self.cod + "'")
            #print(cod)
            self.proveedores.updateProveedores(self.cod,nombre,telefono,email,direccion,descripcion)
            self.mostrar_proveedores()

        
        


    
    def eliminar_proveedor(self):
        table = self.proveedores_view.table_proveedores
        if table.currentItem() != None:
            cod = table.currentItem().text()
            proveedor = self.proveedores.getProveedorCod(cod)
            if proveedor:
                self.proveedores.deleteProveedor(cod)
                self.mostrar_proveedores()
