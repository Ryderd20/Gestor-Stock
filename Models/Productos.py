
import sys
import os
myDir = os.getcwd()
sys.path.append(myDir)

class Productos():
    #-----------Constructor----------------
    def __init__(self, connection):
        self.control = connection

        #-------------CREAR LA TABLA--------------
        cursor = self.control.cursor()
        sql = """CREATE TABLE IF NOT EXISTS "Tabla_Productos" (
            "CodProd" INTEGER NOT NULL,
            "Nombre" TEXT NOT NULL,
            "Proveedor" TEXT NOT NULL,
            "PrecioCompra" REAL NOT NULL,
            "PrecioVenta" REAL NOT NULL,
            "StockMin" INTEGER NOT NULL,
            "Descripcion" TEXT NOT NULL,
            PRIMARY KEY("CodProd" AUTOINCREMENT)
        );"""
        cursor.execute(sql)
        self.control.commit()

    # Obtener lista de Productos
    def getProductos(self):
        cursor = self.control.cursor()
        sql = """SELECT * FROM Tabla_Productos"""
        cursor.execute(sql)
        registro = cursor.fetchall()
        cursor.close()
        return registro

    # Obtener Producto por Codigo
    def getProductoCod(self, cod):
        cursor = self.control.cursor()
        sql = """SELECT * FROM Tabla_Productos WHERE CodProd = {}""".format(cod)
        cursor.execute(sql)
        registro = cursor.fetchone()
        cursor.close()
        if registro:
            return registro

    # Actualizar Producto
    def updateProducto(self, cod, nombre, precioCompra, precioVenta, stockMin, descripcion):
        cursor = self.control.cursor()
        sql = """UPDATE Tabla_Productos SET Nombre = "{}", PrecioCompra = "{}", PrecioVenta = "{}", StockMin = "{}", Descripcion = "{}" WHERE CodProd = "{}" """.format(nombre, precioCompra, precioVenta, stockMin, descripcion, cod)
        cursor.execute(sql)
        self.control.commit()
        cursor.close()

    # Agregar Nuevo Producto
    def insertProducto(self, nombre, proveedor, precioCompra, precioVenta, stockMin, descripcion):
        cursor = self.control.cursor()
        sql = """INSERT INTO Tabla_Productos (Nombre, Proveedor, PrecioCompra, PrecioVenta, StockMin, Descripcion) VALUES ("{}", "{}", "{}", "{}", "{}", "{}")""".format(nombre, proveedor, precioCompra, precioVenta, stockMin, descripcion)
        cursor.execute(sql)
        self.control.commit()

    # Eliminar un Producto
    def deleteProducto(self, cod):
        cursor = self.control.cursor()
        sql = """DELETE FROM Tabla_Productos WHERE CodProd = {}""".format(cod)
        cursor.execute(sql)
        self.control.commit()

    # Obtener Productos por Nombre
    def getProductoNom(self, nombre):
        cursor = self.control.cursor()
        sql = """SELECT * FROM Tabla_Productos WHERE LOWER(Nombre) LIKE LOWER('{}%')""".format(nombre)
        cursor.execute(sql)
        registro = cursor.fetchall()
        if registro:
            return registro

    # Obtener Precio de Producto
    def getPrecioProducto(self, cod):
        cursor = self.control.cursor()
        sql = """SELECT PrecioCompra FROM Tabla_Productos WHERE CodProd = {}""".format(cod)
        cursor.execute(sql)
        precio = cursor.fetchone()
        self.control.commit()
        return precio


