# Importamos las librerias

from flask import redirect, render_template
from datetime import datetime
import os

# Creamos la clase y definimos las funciones CRUD


class Registros:
    def __init__(self, prog, conDB, cursor):
        self.prog = prog
        self.conDB = conDB
        self.cursor = cursor

# Funcion agregar

    def agregar(self, reg):
        sql = f"INSERT INTO registro (idregistro,idhabitacion,idcliente,fecha_inicio,fecha_final,precio) VALUES ({reg[0]},{reg[1]},{reg[2]},'{reg[3]}','{reg[4]}',{reg[5]})"
        self.cursor.execute(sql)
        self.conDB.commit()


# Funcion buscar

    def buscar(self, num):
        sql = f"SELECT * FROM registro WHERE idregistro={num}"
        self.cursor.execute(sql)
        resultado = self.cursor.fetchall()
        self.conDB.commit()
        return resultado

# Funcion consultar

    def consultar(self):
        sql = "SELECT * FROM registro WHERE borrado=0"
        self.cursor.execute(sql)
        resultado = self.cursor.fetchall()
        return resultado

# Funcion actualizar

    def actualiza(self, reg):
        sql = f"UPDATE registro SET idhabitacion={reg[1]}, idcliente={reg[2]},fecha_inicio='{reg[3]}',\
        fecha_final='{reg[4]}', precio={reg[5]} WHERE idregistro={reg[0]}"
        self.cursor.execute(sql)
        self.conDB.commit()

    # Funcion borrar

    def borrar(self, id):
        sql = f"UPDATE registro SET borrado=1 WHERE idregistro={id}"
        self.cursor.execute(sql)
        self.conDB.commit()
