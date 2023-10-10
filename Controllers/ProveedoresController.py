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
