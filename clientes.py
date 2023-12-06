# Importamos las librerias

from flask import redirect, render_template
from datetime import datetime
import os

# Creamos la clase y definimos las funciones CRUD

class Clientes:
    def __init__(self, prog, conDB, cursor):
        self.prog = prog
        self.conDB = conDB
        self.cursor = cursor

# Funcion agregar

    def agregar(self, clie):
        sql = f"INSERT INTO clientes (idcliente, nombre, nacionalidad, celular, email, fnacimiento) VALUES ('{clie[0]}','{clie[1]}','{clie[2]}','{clie[3]}','{clie[4]}','{clie[5]}')"
        self.cursor.execute(sql)
        self.conDB.commit()


# Funcion buscar

    def buscar(self, num):
        sql = f"SELECT * FROM clientes WHERE idcliente={num}"
        self.cursor.execute(sql)
        resultado = self.cursor.fetchall()
        self.conDB.commit()
        return resultado

# Funcion consultar

    def consultar(self):
        sql = "SELECT * FROM clientes WHERE borrado=0"
        self.cursor.execute(sql)
        resultado = self.cursor.fetchall()
        return resultado

# Funcion actualizar

    def actualiza(self, clie):
        sql = f"UPDATE clientes SET nombre='{clie[1]}', nacionalidad='{clie[2]}',celular='{clie[3]}',\
        email='{clie[4]}', fnacimiento='{clie[5]}' WHERE idcliente='{clie[0]}'"
        self.cursor.execute(sql)
        self.conDB.commit()

    # Funcion borrar

    def borrar(self, id):
        sql = f"UPDATE clientes SET borrado=1 WHERE idcliente={id}"
        self.cursor.execute(sql)
        self.conDB.commit()
