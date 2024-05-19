import sys

from PyQt5.QtWidgets import QApplication,QMainWindow,QMessageBox
from PyQt5.uic import loadUi
from PyQt5.QtCore import QDate

from Controllers.ProveedoresController import ProveedoresController
from Controllers.ProductosController import ProductosController
from Controllers.StockController import StockController
from Controllers.ComprasController import ComprasController
from Controllers.VentasController import VentasController



class VentanaPrincipal(QMainWindow):
    #---------------------CONSTRUCTOR-------------------
    def __init__(self):
        super(VentanaPrincipal,self).__init__()
        loadUi("Views/Principal.ui",self)
        self.dateEdit_final.setDate(QDate.currentDate())
        self.dateEdit_inicial.setDate(QDate.currentDate())
        

    
        #----------------Controladores----------------
        self.proveedores_controller = ProveedoresController(self)
        self.productos_controller = ProductosController(self)
        self.stock_controller = StockController(self)
        self.ventas_controller = VentasController(self)
        self.compras_controller = ComprasController(self)
        
        

        #--------------------Botones Menu Principal------------------------
        
        #Ir a Gestion de Ventas
        self.btn_gestionventas.clicked.connect(lambda:self.stackedWidget.setCurrentWidget(self.page_ventas))
        self.btn_gestionventas.clicked.connect(self.ventas_controller.mostrar_ventas)
        self.btn_gestionventas.clicked.connect(self.stock_controller.mostrar_alerta_stock_bajo)


        #Ir a Gestion de Stock
        self.btn_gestionstock.clicked.connect(lambda:self.stackedWidget.setCurrentWidget(self.page_stock))
        self.btn_gestionstock.clicked.connect(self.stock_controller.mostrar_stock)

        #Ir a Gestion de Compras
        self.btn_compras.clicked.connect(lambda:self.stackedWidget.setCurrentWidget(self.page_compras))
        self.btn_compras.clicked.connect(lambda:self.compras_controller.cargarListaProveedores())
        self.btn_compras.clicked.connect(lambda:self.compras_controller.mostrar_compras())
        
        #Ir a Gestion de Productos
        self.btn_productos.clicked.connect(lambda:self.stackedWidget.setCurrentWidget(self.page_productos))
        self.btn_productos.clicked.connect(self.productos_controller.mostrar_productos)

        #Ir a Gestion de Proveedores
        self.btn_proveedores.clicked.connect(lambda:self.stackedWidget.setCurrentWidget(self.page_proveedores))
        self.btn_proveedores.clicked.connect(self.proveedores_controller.mostrar_proveedores)

        #Salir
        self.btn_salir.clicked.connect(lambda:self.close())



        #-------------------------------Gestion de Ventas---------------------------

        #Ingresar nueva Venta
        self.btn_nuevaVenta.clicked.connect(lambda:self.stackedWidget.setCurrentWidget(self.page_nueva_venta))
        self.btn_nuevaVenta.clicked.connect(lambda:self.ventas_controller.nueva_venta(self.getFecha()))

        #Mostrar Detalle de Venta
        self.table_ventas.itemSelectionChanged.connect(lambda:self.ventas_controller.mostrar_detalleVentaSeleccionada())

        #Eliminar Venta seleccionada
        self.btn_eliminarVenta.clicked.connect(lambda:self.ventas_controller.eliminar_venta_seleccionada())

        #Buscar Ventas entre Fechas
        self.btn_buscar_fecha.clicked.connect(lambda:self.ventas_controller.buscar_ventas_por_rango_de_fechas())
        self.btn_buscar_fecha_cancelar.clicked.connect(lambda:self.ventas_controller.mostrar_ventas())

        #-------------------------------Detalle de Venta--------------------------
        #Agregar Producto a Detalle
        self.btn_agregar_detalleVenta.clicked.connect(self.ventas_controller.cargar_producto)
        self.btn_agregar_detalleVenta.clicked.connect(self.ventas_controller.mostrar_stock)

        #Restar Producto a Detalle
        self.btn_restar_detalleVenta.clicked.connect(self.ventas_controller.restar_producto)
        self.btn_restar_detalleVenta.clicked.connect(self.ventas_controller.mostrar_stock)

        #Confirmar Venta
        self.btn_detalleVenta_confirmar.clicked.connect(lambda:self.stackedWidget.setCurrentWidget(self.page_ventas))
        self.btn_detalleVenta_confirmar.clicked.connect(self.ventas_controller.mostrar_ventas)
        self.btn_detalleVenta_confirmar.clicked.connect(self.stock_controller.mostrar_alerta_stock_bajo)

        #Cancelar Venta
        self.btn_detalleVenta_cancelar.clicked.connect(lambda:self.stackedWidget.setCurrentWidget(self.page_ventas))
        self.btn_detalleVenta_cancelar.clicked.connect(self.ventas_controller.cancelar_venta)
        self.btn_detalleVenta_cancelar.clicked.connect(self.ventas_controller.mostrar_ventas)

        #Buscar los Productos en stock
        self.btn_buscar_stockEnDetalle.clicked.connect(lambda:self.ventas_controller.buscar_producto_por_nombre())


        #-------------------------------Gestion de Stock---------------------------

        #Buscar Producto en Stock
        self.btn_buscar_prodStock_porNom.clicked.connect(self.stock_controller.buscar_producto_por_nombre)

        #Restar de Stock
        self.btn_eliminar_stock.clicked.connect(self.stock_controller.restar_cantidad_producto)


        #--------------------------------Gestion de Compras-----------------------------------------
        
        #Nueva Compra
        self.btn_nuevaCompra.clicked.connect(lambda:self.stackedWidget.setCurrentWidget(self.page_nueva_compra))
        self.btn_nuevaCompra.clicked.connect(lambda:self.compras_controller.nueva_compra(self.getFecha()))


        #Mostrar Detalle de Compra
        self.table_compras.itemSelectionChanged.connect(lambda:self.compras_controller.mostrar_detalleCompraSeleccionada())

        #Eliminar Compra
        self.btn_eliminarCompra.clicked.connect(lambda:self.compras_controller.eliminar_compra_seleccionada())



        #---------------------------------Gestion Detalle de Compra-------------------------------------------
        #Confirmar Compra
        self.btn_detalleCompra_confirmar.clicked.connect(lambda:self.stackedWidget.setCurrentWidget(self.page_compras))
        self.btn_detalleCompra_confirmar.clicked.connect(lambda:self.compras_controller.mostrar_compras())
        self.btn_detalleCompra_confirmar.clicked.connect(lambda:self.compras_controller.añadir_compra_a_stock())

        #Cancelar Compra
        self.btn_detalleCompra_cancelar.clicked.connect(lambda:self.stackedWidget.setCurrentWidget(self.page_compras))
        self.btn_detalleCompra_cancelar.clicked.connect(lambda:self.compras_controller.cancelar_compra())
        self.btn_detalleCompra_cancelar.clicked.connect(lambda:self.compras_controller.mostrar_compras())

        #Buscar Producto
        self.btn_buscar_producto_detalleCompra.clicked.connect(lambda:self.compras_controller.buscar_producto_de_proveedor())



        #Agregar Producto al Detalle de la Compra
        self.btn_agregar_detalleCompra.clicked.connect(lambda:self.compras_controller.cargar_producto())

        #Restar Producto al Detalle de la Compra
        self.btn_restar_detalleCompra.clicked.connect(lambda:self.compras_controller.restar_producto())
        
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
            msg.setText("Debes seleccionar un Proveedor")
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
            msg.setText("Debes seleccionar un Producto")
            msg.exec_()


    def validarProductoModificado(self):  
              
        if self.productos_controller.modificar_producto():
            self.stackedWidget.setCurrentWidget(self.page_productos)
    

    def getFecha(self):
        fecha = QDate.currentDate()
        fecha_str = fecha.toString("yyyy-MM-dd")
        return (fecha_str)







    



if __name__ == "__main__":
    app = QApplication(sys.argv)
    mi_app = VentanaPrincipal()
    mi_app.showMaximized()
    sys.exit(app.exec_())
    
    




