import sys
import os
myDir = os.getcwd()
sys.path.append(myDir)

from PyQt5 import QtWidgets
from DataBase.Connection import connection
from Models.Articulos import Articulos
from Models.Proveedores import Proveedores

#------comentario prueba---------------

class ArticulosController():
    

    #------Constructor---------------
    def __init__(self,view):
        self.articulos = Articulos(connection())
        self.proveedores = Proveedores(connection())
        self.art_view = view

    #Muestra la lista de Articulos
    def mostrar_articulos(self):
        datos = self.articulos.getArticulos()
        num_filas = len(datos)
        num_columnas = 6     #podria obtenerlo solo con self.art_view.table_articulos.rowCount  //probar
        

        self.art_view.table_articulos.setRowCount(num_filas)
        self.art_view.table_articulos.setColumnCount(num_columnas)

        for fila, registro in enumerate(datos):
            for columna, valor in enumerate(registro):
                item = QtWidgets.QTableWidgetItem(str(valor))
                self.art_view.table_articulos.setItem(fila, columna, item)
        
        self.art_view.comboBox_nuevo_articulo_listaProv.clear()
        self.art_view.comboBox_modificar_articulo_listaProv.clear()


    #Agregar nuevo Articulo
    def agregar_articulo(self):
        self.art_view.signal_nuevo_articulo.setText("Espacios obligatorios*")

        nombre = self.art_view.input_nombre_articulo_nuevo.text()
        proveedor = self.art_view.comboBox_nuevo_articulo_listaProv.currentText()
        costo = self.art_view.input_costo_articulo_nuevo.text()
        precio = self.art_view.input_precio_articulo_nuevo.text()
        descripcion = self.art_view.input_descripcion_articulo_nuevo.text()

        if nombre !="" and costo !="" and precio !="":
            try:
                costo_float = float(costo)
                precio_float = float(precio)

                self.articulos.insertArticulo(nombre,proveedor,costo_float,precio_float,descripcion)
                self.limpiar_articulo_nuevo()
                self.art_view.signal_nuevo_articulo.setText("Registrado con exito")
            except ValueError:
                self.art_view.signal_nuevo_articulo.setText("Los espacios Costo y Precio deben ser numerales")
        else:
            self.art_view.signal_nuevo_articulo.setText("Hay espacios obligatorios vacios")


    #Elimina el Articulo seleccionado
    def eliminar_articulo(self):
        item = self.art_view.table_articulos.item(self.art_view.table_articulos.currentRow(),0).text()
        if item != None:
            articulo = self.articulos.getArticuloCod(item)
            if articulo:
                self.articulos.deleteArticulo(item)
                self.mostrar_articulos()

    #Guardar Articulo
    def modificar_articulo(self):
            
        nombre = self.art_view.input_nombre_articulo_modificar.text()
        proveedor = self.art_view.comboBox_modificar_articulo_listaProv.currentText()
        costo = self.art_view.input_costo_articulo_modificar.text()
        precio = self.art_view.input_precio_articulo_modificar.text()
        descripcion = self.art_view.input_descripcion_articulo_modificar.text()

        
        if nombre !="" and costo !="" and precio != "":
            try:
                costo_float = float(costo)
                precio_float = float(precio)
                cod = self.articulo[0]
                self.articulos.updateArticulo(cod,nombre,proveedor,costo_float,precio_float,descripcion)
                self.mostrar_articulos()
            except ValueError:
                self.art_view.signal_modificar_articulo.setText("Los espacios Costo y Precio deben ser numerales")
            
            return True
        else:
            return False
    
    
    #Cargar Articulo para Modificar
    def cargar_articulo(self):
        self.art_view.signal_articulo_modificado.setText("Espacios obligatorios*")
        self.cargarListaProveedores()


        if self.art_view.table_articulos.currentRow() != -1:
            item = self.art_view.table_articulos.item(self.art_view.table_articulos.currentRow(), 0).text()
            if item is not None:
                # Obtén el artículo como una instancia de la clase Articulos
                self.articulo = self.articulos.getArticuloCod(item)
                if self.articulo:
                    # Actualiza el atributo 'articulos' con la instancia del artículo
                    self.art_view.input_nombre_articulo_modificar.setText(self.articulo[1])
                    self.art_view.input_costo_articulo_modificar.setText(str(self.articulo[3]))
                    self.art_view.input_precio_articulo_modificar.setText(str(self.articulo[4]))
                    self.art_view.input_descripcion_articulo_modificar.setText(self.articulo[5])



    #Limpiar los input para agregar un nuevo articulo
    def limpiar_articulo_nuevo(self):
            self.art_view.input_nombre_articulo_nuevo.clear()
            self.art_view.input_costo_articulo_nuevo.clear()
            self.art_view.input_precio_articulo_nuevo.clear()
            self.art_view.input_descripcion_articulo_nuevo.clear()

    #Cargar Lista de Proveedores en ComboBox
    def cargarListaProveedores(self):
        self.art_view.comboBox_nuevo_articulo_listaProv.clear()
        lista = self.proveedores.getListProveevores()
        self.art_view.comboBox_nuevo_articulo_listaProv.addItem("Ninguno")
        self.art_view.comboBox_modificar_articulo_listaProv.addItem("Ninguno")
        for prov in lista:
            texto_proveedor = str(prov).replace("(", "").replace(")", "").replace("'", "").replace('"', '').replace(',', '')
            self.art_view.comboBox_nuevo_articulo_listaProv.addItem(texto_proveedor)
            self.art_view.comboBox_modificar_articulo_listaProv.addItem(texto_proveedor)


     #hsfd   

    #Buscar Articulo
    def buscarArticuloPorNombre(self):
        nombre = self.art_view.input_nombre_articulo_buscar.text()
        datos = self.articulos.getArticuloNom(nombre)

        if datos is not None:
            num_filas = len(datos)
        else:
            num_filas = 0

        num_columnas = self.art_view.table_articulos.columnCount()

        self.art_view.table_articulos.setRowCount(num_filas)
        self.art_view.table_articulos.setColumnCount(num_columnas)

        if datos:
            for fila, registro in enumerate(datos):
                for columna, valor in enumerate(registro):
                    item = QtWidgets.QTableWidgetItem(str(valor))
                    self.art_view.table_articulos.setItem(fila, columna, item)
            self.art_view.input_nombre_articulo_buscar.clear()
        else:
            self.mostrar_articulos
            self.art_view.input_nombre_articulo_buscar.clear()
    








        

        
        




    




        




    

