import sqlite3

from sqlite3 import Cursor
    

"""
    def __init__(self):
        self.conexion = sqlite3.connect("DB_Textil.db")

"""


    
def connection():
    conn = sqlite3.connect("DataBase\DB_Textil.db")
    print("Base de datos conectada!")
    return conn