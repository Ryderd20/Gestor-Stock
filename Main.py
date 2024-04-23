import sys

from PyQt5.QtWidgets import QApplication,QMainWindow,QMessageBox
from PyQt5.uic import loadUi

from Controllers.ProveedoresController import ProveedoresController
from Controllers.ProductosController import ProductosController




class VentanaPrincipal(QMainWindow):
    #---------------------CONSTRUCTOR-------------------
    def __init__(self):
        super(VentanaPrincipal,self).__init__()
        loadUi("Views/Principal.ui",self)
        

    
        #----------------Controladores----------------
        self.proveedores_controller = ProveedoresController(self)
        self.productos_controller = ProductosController(self)

        
        

        #--------------------Botones Menu Principal------------------------
        
        #Ir a Gestion de Vesntas
        self.btn_gestionventas.clicked.connect(lambda:self.stackedWidget.setCurrentWidget(self.page_ventas))

        #Ir a Gestion de Stock
        self.btn_gestionstock.clicked.connect(lambda:self.stackedWidget.setCurrentWidget(self.page_stock))
        
        #Ir a Gestion de Productos
        self.btn_productos.clicked.connect(lambda:self.stackedWidget.setCurrentWidget(self.page_productos))
        self.btn_productos.clicked.connect(self.productos_controller.mostrar_productos)

        #Ir a Gestion de Proveedores
        self.btn_proveedores.clicked.connect(lambda:self.stackedWidget.setCurrentWidget(self.page_proveedores))
        self.btn_proveedores.clicked.connect(self.proveedores_controller.mostrar_proveedores)

        #Salir
        self.btn_salir.clicked.connect(lambda:self.close())


        
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

        #Buscar Proveedor
        self.btn_buscar_proveedor.clicked.connect(self.proveedores_controller.buscarProveedorPorNombre)


        #-------------------------------Gestion de Productos--------------
        #Agregar Producto
        self.btn_agregar_producto.clicked.connect(lambda:self.stackedWidget.setCurrentWidget(self.page_nuevo_producto))
        self.btn_agregar_producto.clicked.connect(self.productos_controller.cargarListaProveedores)

        self.btn_atras_producto_nuevo.clicked.connect(lambda:self.stackedWidget.setCurrentWidget(self.page_productos))
        self.btn_atras_producto_nuevo.clicked.connect(self.productos_controller.mostrar_productos)

        self.btn_guardar_producto.clicked.connect(self.productos_controller.agregar_producto)

        #Modificar Producto
        self.btn_modificar_producto.clicked.connect(self.validarSeleccionDeProducto)
        self.btn_modificar_producto.clicked.connect(self.productos_controller.cargar_producto)
        
        self.btn_guardar_producto_modificar.clicked.connect(self.validarProductoModificado)
        self.btn_cancelar_producto_modificar.clicked.connect(lambda:self.stackedWidget.setCurrentWidget(self.page_productos))
        

        #Eliminar Producto
        self.btn_eliminar_producto.clicked.connect(lambda:self.productos_controller.eliminar_producto())

        #Buscar Producto
        self.btn_buscar_prod.clicked.connect(self.productos_controller.buscarProductoPorNombre)

    
    
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
    


    def validarSeleccionDeProducto(self):
        if self.table_productos.currentRow() != -1:
            self.stackedWidget.setCurrentWidget(self.page_modificar_producto)
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle("Advertencia")
            msg.setText("Debes seleccionar un producto")
            msg.exec_()

    def validarProductoModificado(self):
        
        if self.productos_controller.modificar_producto():
            self.stackedWidget.setCurrentWidget(self.page_productos)
        else:
            self.signal_producto_modificado.setText("Hay espacios obligatorios vacios")        






    



    
            

        






if __name__ == "__main__":
    app = QApplication(sys.argv)
    mi_app = VentanaPrincipal()
    mi_app.showMaximized()
    sys.exit(app.exec_())
    
    




