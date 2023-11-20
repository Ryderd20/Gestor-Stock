import sqlite3

from sqlite3 import Cursor
    

    
def connection():
    conn = sqlite3.connect("DataBase\DB_Textil.db")
    print("Base de datos conectada!")
    return conn