
import sys
import os
myDir = os.getcwd()
sys.path.append(myDir)


class Articulos():


    #-----------Constructor----------------
    def __init__(self,connection):
        self.control = connection

        
        #-------------CREAR LA TABLA--------------
        cursor = self.control.cursor()
        sql = """CREATE TABLE IF NOT EXISTS "Tabla_Articulos" (
            "Codigo"	INTEGER NOT NULL,
            "Nombre"	TEXT NOT NULL,
            "Proveedor"	TEXT NOT NULL,
            "Costo"	REAL NOT NULL,
            "Precio"	REAL NOT NULL,
            "Descripcion"	TEXT NOT NULL,
            PRIMARY KEY("Codigo" AUTOINCREMENT)
        );"""

        cursor.execute(sql)
        self.control.commit()
        

    #Obtener todos los Articulos
    def getArticulos(self):
        cursor = self.control.cursor()
        sql = """SELECT * FROM Tabla_Articulos"""
        cursor.execute(sql)
        registro = cursor.fetchall()
        cursor.close()
        return registro
    
    #Obtener un Articulo por Codigo
    def getArticuloCod(self,cod):
        cursor = self.control.cursor()
        sql = """SELECT * FROM Tabla_Articulos WHERE Codigo = {}""".format(cod)
        cursor.execute(sql)
        registro = cursor.fetchone()
        cursor.close()
        if registro:
            return registro
    
    #Actualizar Articulo
    def updateArticulo(self,cod,nombre,proveedor,costo,precio,descripcion):
        cursor = self.control.cursor()
        sql = """UPDATE Tabla_Articulos SET Nombre = "{}" , Proveedor = "{}" , Costo = "{}", Precio = "{}", Descripcion = "{}" WHERE Codigo = "{}" """.format(nombre,proveedor,costo,precio,descripcion,cod)
        cursor.execute(sql)
        self.control.commit()
        cursor.close()

    #Agregar Nuevo Articulo
    def insertArticulo(self,nombre,proveedor,costo,precio,descripcion):
        cursor = self.control.cursor()
        sql = """INSERT INTO Tabla_Articulos (Nombre,Proveedor,Costo,Precio,Descripcion) VALUES ("{}","{}","{}","{}","{}")""".format(nombre,proveedor,costo,precio,descripcion)
        cursor.execute(sql)
        self.control.commit()

    #Eliminar un Articulo
    def deleteArticulo(self,cod):
        cursor = self.control.cursor()
        sql = """DELETE FROM Tabla_Articulos WHERE Codigo = {}""".format(cod)
        cursor.execute(sql)
        self.control.commit()
    
    #Obetener Articulos por Nombre
    def getArticuloNom(self,nom):
        cursor = self.control.cursor()
        sql = """SELECT * FROM Tabla_Articulos WHERE Nombre = ?"""
        cursor.execute(sql, (nom,))
        registro = cursor.fetchall()
        if registro:
            return registro
        
