import sys

from PyQt5.QtWidgets import QApplication,QMainWindow,QMessageBox
from PyQt5.uic import loadUi

from Controllers.ProveedoresController import ProveedoresController


from Controllers.ArticulosController import ArticulosController





class VentanaPrincipal(QMainWindow):
    #---------------------CONSTRUCTOR-------------------
    def __init__(self):
        super(VentanaPrincipal,self).__init__()
        loadUi("Views/Principal.ui",self)
        

    
        #----------------Controladores----------------
        self.proveedores_controller = ProveedoresController(self)
        self.articulos_controller = ArticulosController(self)

        
        

        #--------------------Botones Menu Superior------------------------
        self.btn_gestionstock.clicked.connect(lambda:self.stackedWidget_menuSecundario.setCurrentWidget(self.stackedWidget_menuStock))
        self.btn_gestionstock.clicked.connect(lambda:self.stackedWidget.setCurrentWidget(self.page_stock))

        self.btn_gestioncompras.clicked.connect(lambda:self.stackedWidget_menuSecundario.setCurrentWidget(self.stackedWidget_menuCompras))
        self.btn_gestioncompras.clicked.connect(lambda:self.stackedWidget.setCurrentWidget(self.page_compras))

        self.btn_gestionventas.clicked.connect(lambda:self.stackedWidget_menuSecundario.setCurrentWidget(self.stackedWidget_menuVentas))
        self.btn_gestionventas.clicked.connect(lambda:self.stackedWidget.setCurrentWidget(self.page_ventas))


     
        #--------------------Botones Menu Secundario--------------
        
        self.btn_stock.clicked.connect(lambda:self.stackedWidget.setCurrentWidget(self.page_stock))

        self.btn_articulos.clicked.connect(lambda:self.stackedWidget.setCurrentWidget(self.page_articulos))
        self.btn_articulos.clicked.connect(self.articulos_controller.mostrar_articulos)

        
        self.btn_compras.clicked.connect(lambda:self.stackedWidget.setCurrentWidget(self.page_compras))
        
        self.btn_proveedores.clicked.connect(lambda:self.stackedWidget.setCurrentWidget(self.page_proveedores))
        self.btn_proveedores.clicked.connect(self.proveedores_controller.mostrar_proveedores)


        self.btn_ventas.clicked.connect(lambda:self.stackedWidget.setCurrentWidget(self.page_ventas))
        self.btn_clientes.clicked.connect(lambda:self.stackedWidget.setCurrentWidget(self.page_clientes))



        

        

        #-------------------------------Gestion de Proveedores---------------------------
        #Agregar Proveedor
        self.btn_agregar_proveedor.clicked.connect(lambda:self.stackedWidget.setCurrentWidget(self.page_nuevo_proveedor))

        self.btn_guardar_proveedor_nuevo.clicked.connect(self.proveedores_controller.agregar_proveedor)
        self.btn_atras_proveedor_nuevo.clicked.connect(lambda:self.stackedWidget.setCurrentWidget(self.page_proveedores))

        #Modificar Proveedor
        self.btn_modificar_proveedor.clicked.connect(self.validarSeleccionDeProveedor)
        self.btn_modificar_proveedor.clicked.connect(self.proveedores_controller.cargar_proveedor)
        
        self.btn_guardar_proveedor_modificar.clicked.connect(self.validarProveedorModificado)
        self.btn_cancelar_proveedor_modificar.clicked.connect(lambda:self.stackedWidget.setCurrentWidget(self.page_proveedores))

        #Eliminar Proveedor
        self.btn_eliminar_proveedor.clicked.connect(self.proveedores_controller.eliminar_proveedor)




        #-------------------------------Gestion de Articulos--------------
        #Agregar Articulo
        self.btn_agregar_articulo.clicked.connect(lambda:self.stackedWidget.setCurrentWidget(self.page_nuevo_articulo))
        self.btn_agregar_articulo.clicked.connect(self.articulos_controller.cargarListaProveedores)

        self.btn_atras_articulo_nuevo.clicked.connect(lambda:self.stackedWidget.setCurrentWidget(self.page_articulos))
        self.btn_atras_articulo_nuevo.clicked.connect(self.articulos_controller.mostrar_articulos)

        self.btn_guardar_articulo.clicked.connect(self.articulos_controller.agregar_articulo)

        #Modificar Articulo
        self.btn_modificar_articulo.clicked.connect(lambda:self.stackedWidget.setCurrentWidget(self.page_modificar_articulo))
        self.btn_modificar_articulo.clicked.connect(self.articulos_controller.cargarListaProveedores)
        self.btn_cancelar_articulo_modificar.clicked.connect(lambda:self.stackedWidget.setCurrentWidget(self.page_articulos))

        #Eliminar Articulo
        self.btn_eliminar_articulo.clicked.connect(lambda:self.articulos_controller.eliminar_articulo())
        self.btn_buscar_art.clicked.connect(self.articulos_controller.buscarArticuloPorNombre)



    #---------------------------------FUNCIONES--------------------------------
    def validarSeleccionDeProveedor(self):
        if self.table_proveedores.currentRow() != -1:
            self.stackedWidget.setCurrentWidget(self.page_modificar_proveedor)
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle("Advertencia")
            msg.setText("Debes seleccionar un proveedor")
            msg.exec_()

    def validarProveedorModificado(self):
        
        if self.proveedores_controller.modificar_proveedor():
            self.stackedWidget.setCurrentWidget(self.page_proveedores)
        else:
            self.signal_proveedor_modificado.setText("Hay espacios obligatorios vacios")
    


            






    



    
            

        






if __name__ == "__main__":
    app = QApplication(sys.argv)
    mi_app = VentanaPrincipal()
    mi_app.show()
    sys.exit(app.exec_())

    




