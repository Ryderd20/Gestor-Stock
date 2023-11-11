import sys

from PyQt5.QtWidgets import QApplication,QMainWindow
from PyQt5.QtCore import QPropertyAnimation,QEasingCurve
from PyQt5 import QtCore,QtWidgets
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

        
        
        #------------------------------------BOTONES------------------------

        #---------------Menu Principal---------------
        self.btn_gestionstock.clicked.connect(lambda:self.stackedWidget_menuSecundario.setCurrentWidget(self.stackedWidget_menuStock))
        self.btn_gestionstock.clicked.connect(lambda:self.stackedWidget.setCurrentWidget(self.page_stock))

        self.btn_gestioncompras.clicked.connect(lambda:self.stackedWidget_menuSecundario.setCurrentWidget(self.stackedWidget_menuCompras))
        self.btn_gestioncompras.clicked.connect(lambda:self.stackedWidget.setCurrentWidget(self.page_compras))

        self.btn_gestionventas.clicked.connect(lambda:self.stackedWidget_menuSecundario.setCurrentWidget(self.stackedWidget_menuVentas))
        self.btn_gestionventas.clicked.connect(lambda:self.stackedWidget.setCurrentWidget(self.page_ventas))


     
    

        #---------------Menu Secundario--------------
        
        self.btn_stock.clicked.connect(lambda:self.stackedWidget.setCurrentWidget(self.page_stock))

        self.btn_articulos.clicked.connect(lambda:self.stackedWidget.setCurrentWidget(self.page_articulos))
        self.btn_articulos.clicked.connect(self.articulos_controller.mostrar_articulos)

        
        self.btn_compras.clicked.connect(lambda:self.stackedWidget.setCurrentWidget(self.page_compras))
        
        self.btn_proveedores.clicked.connect(lambda:self.stackedWidget.setCurrentWidget(self.page_proveedores))
        self.btn_proveedores.clicked.connect(self.proveedores_controller.mostrar_proveedores)


        self.btn_ventas.clicked.connect(lambda:self.stackedWidget.setCurrentWidget(self.page_ventas))
        self.btn_clientes.clicked.connect(lambda:self.stackedWidget.setCurrentWidget(self.page_clientes))



        

        




        #---------------Proveedores------------------
        self.btn_agregar_proveedor.clicked.connect(lambda:self.stackedWidget.setCurrentWidget(self.page_nuevo_proveedor))
        self.btn_cancelar_proveedor_nuevo.clicked.connect(lambda:self.stackedWidget.setCurrentWidget(self.page_proveedores))



        self.btn_modificar_proveedor.clicked.connect(lambda:self.stackedWidget.setCurrentWidget(self.page_modificar_proveedor))
        self.btn_modificar_proveedor.clicked.connect(self.proveedores_controller.cargar_proveedor)

        self.btn_guardar_proveedor_modificar.clicked.connect(self.proveedores_controller.modificar_proveedor)
        self.btn_guardar_proveedor_modificar.clicked.connect(lambda:self.stackedWidget.setCurrentWidget(self.page_proveedores))
        self.btn_cancelar_proveedor_modificar.clicked.connect(lambda:self.stackedWidget.setCurrentWidget(self.page_proveedores))

        self.btn_eliminar_proveedor.clicked.connect(self.proveedores_controller.eliminar_proveedor)

        #---------------Articulos--------------
        #self.btn_agregar_articulo.clicked.connect(lambda:self.stackedWidget.setCurrentWidget(self.page_nuevo_proveedor))
        #self.btn_cancelar_articulo_nuevo.clicked.connect(lambda:self.stackedWidget.setCurrentWidget(self.page_proveedores))

        self.btn_agregar_articulo.clicked.connect(lambda:self.stackedWidget.setCurrentWidget(self.page_agregar_art))
        #self.btn_guardar_articulo.clicked.connect(lambda:self.articulos_controller.crear_articulo(self.input_cod_art.text(),self.input_nom_art.text(),self.input_prec_art.text(),self.input_desc_art.text(),self.input_prov_art.text()))
        self.btn_cancelar_articulo_nuevo.clicked.connect(lambda:self.stackedWidget.setCurrentWidget(self.page_articulos))

        #self.btn_eliminar_art.clicked.connect(lambda:self.articulos_controller.eliminar_articulo())
        #self.btn_buscar_art.clicked.connect(lambda:self.articulos_controller.buscar_Articulo(self.input_nombre_art.text()))
    



    
            

        






if __name__ == "__main__":
    app = QApplication(sys.argv)
    mi_app = VentanaPrincipal()
    mi_app.show()
    sys.exit(app.exec_())

    




