
import sys
import os
myDir = os.getcwd()
sys.path.append(myDir)


class Productos():


    #-----------Constructor----------------
    def __init__(self,connection):
        self.control = connection

        
        #-------------CREAR LA TABLA--------------
        cursor = self.control.cursor()
        sql = """CREATE TABLE IF NOT EXISTS "Tabla_Productos" (
            "CodProd"	INTEGER NOT NULL,
            "Nombre"	TEXT NOT NULL,
            "Proveedor"	TEXT NOT NULL,
            "Precio"	REAL NOT NULL,
            "Descripcion"	TEXT NOT NULL,
            PRIMARY KEY("CodProd" AUTOINCREMENT)
        );"""

        cursor.execute(sql)
        self.control.commit()
        

    #Obtener todos los Productos
    def getProductos(self):
        cursor = self.control.cursor()
        sql = """SELECT * FROM Tabla_Productos"""
        cursor.execute(sql)
        registro = cursor.fetchall()
        cursor.close()
        return registro
    
    #Obtener un Producto por Codigo
    def getProductoCod(self,cod):
        cursor = self.control.cursor()
        sql = """SELECT * FROM Tabla_Productos WHERE CodProd = {}""".format(cod)
        cursor.execute(sql)
        registro = cursor.fetchone()
        cursor.close()
        if registro:
            return registro
    
    #Actualizar Producto
    def updateProducto(self,cod,nombre,proveedor,precio,descripcion):
        cursor = self.control.cursor()
        sql = """UPDATE Tabla_Productos SET Nombre = "{}" , Proveedor = "{}" , Precio = "{}", Descripcion = "{}" WHERE CodProd = "{}" """.format(nombre,proveedor,precio,descripcion,cod)
        cursor.execute(sql)
        self.control.commit()
        cursor.close()

    #Agregar Nuevo Producto
    def insertProducto(self,nombre,proveedor,precio,descripcion):
        cursor = self.control.cursor()
        sql = """INSERT INTO Tabla_Productos (Nombre,Proveedor,Precio,Descripcion) VALUES ("{}","{}","{}","{}")""".format(nombre,proveedor,precio,descripcion)
        cursor.execute(sql)
        self.control.commit()

    #Eliminar un Producto
    def deleteProducto(self,cod):
        cursor = self.control.cursor()
        sql = """DELETE FROM Tabla_Productos WHERE CodProd = {}""".format(cod)
        cursor.execute(sql)
        self.control.commit()
    
    
    #Obetener Productos por Nombre
    def getProductoNom(self,nom):
        cursor = self.control.cursor()
        sql = """SELECT * FROM Tabla_Productos WHERE Nombre = ?"""
        cursor.execute(sql, (nom,))
        registro = cursor.fetchall()
        if registro:
            return registro
        
    #Obtener Precio de Producto
    def getPrecioProducto(self,cod):
        cursor = self.control.cursor()
        sql = """SELECT Precio FROM Tabla_Productos WHERE CodProd = {}""".format(cod)
        cursor.execute(sql)
        precio = cursor.fetchone()
        self.control.commit()
        return precio
    
    #Obtener Nombre de Producto
    def getNombreProducto(self,cod):
        cursor = self.control.cursor()
        sql = """SELECT Nombre FROM Tabla_Productos WHERE CodProd = {}""".format(cod)
        cursor.execute(sql)
        nombre = cursor.fetchone()
        self.control.commit()
        return nombre
        
