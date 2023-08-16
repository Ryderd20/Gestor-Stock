import sys

from PyQt5.QtWidgets import QApplication,QMainWindow
from PyQt5.QtCore import QPropertyAnimation,QEasingCurve
from PyQt5 import QtCore,QtWidgets
from PyQt5.uic import loadUi


from Controllers.ArticulosController import ArticulosController





class VentanaPrincipal(QMainWindow):
    #---------------------CONSTRUCTOR-------------------
    def __init__(self):
        super(VentanaPrincipal,self).__init__()
        loadUi("Views/Principal.ui",self)
        

        #----------------Controladores----------------
        self.articulos_controller = ArticulosController(self)

        
        
        #------------------------------------BOTONES------------------------

        #---------------Menu---------------

        self.btn_articulos.clicked.connect(lambda:self.stackedWidget.setCurrentWidget(self.page_articulos))
        self.btn_articulos.clicked.connect(self.articulos_controller.mostrar_articulos)
    

        #---------------Articulos--------------
        self.btn_agregar_art.clicked.connect(lambda:self.stackedWidget.setCurrentWidget(self.page_agregar_art))
        self.btn_confirmar_art.clicked.connect(lambda:self.articulos_controller.crear_articulo(self.input_cod_art.text(),self.input_nom_art.text(),self.input_prec_art.text(),self.input_desc_art.text(),self.input_prov_art.text()))
        self.btn_confirmar_art.clicked.connect(lambda:self.stackedWidget.setCurrentWidget(self.page_articulos))
        self.btn_cancel_art.clicked.connect(lambda:self.stackedWidget.setCurrentWidget(self.page_articulos))

        self.btn_eliminar_art.clicked.connect(lambda:self.articulos_controller.eliminar_articulo())
        self.btn_buscar_art.clicked.connect(lambda:self.articulos_controller.buscar_Articulo(self.input_nombre_art.text()))
    



    
            

        






if __name__ == "__main__":
    app = QApplication(sys.argv)
    mi_app = VentanaPrincipal()
    mi_app.show()
    sys.exit(app.exec_())



