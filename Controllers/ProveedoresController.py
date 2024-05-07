import sys
import os
myDir = os.getcwd()
sys.path.append(myDir)


from PyQt5.QtWidgets import QMessageBox
from PyQt5 import QtWidgets
from DataBase.Connection import connection
from Models.Proveedores import Proveedores



class ProveedoresController():
    

    #------Constructor---------------
    def __init__(self,PrincipalView):
        self.proveedores = Proveedores(connection())
        self.proveedores_view = PrincipalView

    
    #Listar la lista de Proveedores
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


    #Agregar nuevo proveedor
    def agregar_proveedor(self):
        self.proveedores_view.signal_proveedor_nuevo.setText("Espacios obligatorios*")

        nombre = self.proveedores_view.input_nombre_proveedor_nuevo.text()
        telefono = self.proveedores_view.input_telefono_proveedor_nuevo.text()
        email = self.proveedores_view.input_email_proveedor_nuevo.text()
        direccion = self.proveedores_view.input_direccion_proveedor_nuevo.text()
        descripcion = self.proveedores_view.input_descripcion_proveedor_nuevo.text()

        if nombre !="" and telefono !="" and email !="" and direccion !="":
            self.proveedores.insertProveedor(nombre,telefono,email,direccion,descripcion)
            self.limpiar_proveedor_nuevo()
            self.proveedores_view.signal_proveedor_nuevo.setText("Registrado con exito")
            self.mostrar_proveedores()
        else:
            self.proveedores_view.signal_proveedor_nuevo.setText("Hay espacios obligatorios vacios")




    #Cargar los datos del proveedor a los input para modificarlos
    def cargar_proveedor(self):
        self.proveedores_view.signal_proveedor_modificado.setText("Espacios obligatorios*")

        if self.proveedores_view.table_proveedores.currentRow() != -1:
            item = self.proveedores_view.table_proveedores.item(self.proveedores_view.table_proveedores.currentRow(),0).text()
            if item != None:
                self.proveedor = self.proveedores.getProveedorCod(item)            
                if self.proveedor:
                    self.proveedores_view.input_nombre_proveedor_modificar.setText(self.proveedor[1])
                    self.proveedores_view.input_telefono_proveedor_modificar.setText(self.proveedor[2])
                    self.proveedores_view.input_email_proveedor_modificar.setText(self.proveedor[3])
                    self.proveedores_view.input_direccion_proveedor_modificar.setText(self.proveedor[4])
                    self.proveedores_view.input_descripcion_proveedor_modificar.setText(self.proveedor[5])


    #Actualiza los datos de proveedor por los nuevos
    def modificar_proveedor(self):
            
        nombre = self.proveedores_view.input_nombre_proveedor_modificar.text()
        telefono = self.proveedores_view.input_telefono_proveedor_modificar.text()
        email = self.proveedores_view.input_email_proveedor_modificar.text()
        direccion = self.proveedores_view.input_direccion_proveedor_modificar.text()
        descripcion = self.proveedores_view.input_descripcion_proveedor_modificar.text()

        if nombre !="" and telefono !="" and email !="" and direccion !="":
            cod = self.proveedor[0]
            self.proveedores.updateProveedores(cod,nombre,telefono,email,direccion,descripcion)
            self.mostrar_proveedores()
            return True
        else:
            return False

        
    #Eliminar un proveedor seleccionado
    def eliminar_proveedor(self):
        current_row = self.proveedores_view.table_proveedores.currentRow()
        if current_row != -1:
            item = self.proveedores_view.table_proveedores.item(current_row, 0).text()
            if item:
                proveedor = self.proveedores.getProveedorCod(item)
                if proveedor:
                    self.proveedores.deleteProveedor(item)
                    self.mostrar_proveedores()
        else:
            mensaje = "Debes seleccionar un Proveedor"
            self.mensaje_advertencia(mensaje)




    #Limpiar los input para agregar un nuevo proveedor
    def limpiar_proveedor_nuevo(self):
            self.proveedores_view.input_nombre_proveedor_nuevo.clear()
            self.proveedores_view.input_telefono_proveedor_nuevo.clear()
            self.proveedores_view.input_email_proveedor_nuevo.clear()
            self.proveedores_view.input_direccion_proveedor_nuevo.clear()
            self.proveedores_view.input_descripcion_proveedor_nuevo.clear()





    #Buscar Proveedor
    def buscarProveedorPorNombre(self):
        nombre = self.proveedores_view.input_nombre_proveedor.text()
        datos = self.proveedores.getProveedorNom(nombre)

        if datos is not None:
            num_filas = len(datos)
        else:
            num_filas = 0

        num_columnas = self.proveedores_view.table_proveedores.columnCount()

        self.proveedores_view.table_proveedores.setRowCount(num_filas)
        self.proveedores_view.table_proveedores.setColumnCount(num_columnas)

        if datos:
            for fila, registro in enumerate(datos):
                for columna, valor in enumerate(registro):
                    item = QtWidgets.QTableWidgetItem(str(valor))
                    self.proveedores_view.table_proveedores.setItem(fila, columna, item)
            self.proveedores_view.input_nombre_proveedor.clear()
        else:
            self.mostrar_proveedores
            self.proveedores_view.input_nombre_proveedor.clear()



    def mensaje_advertencia(self,mensaje):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowTitle("Advertencia")
        msg.setText(mensaje)
        msg.exec_()
