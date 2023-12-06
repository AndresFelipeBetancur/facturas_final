# Importamos las librerias

from flask import redirect, render_template
from datetime import datetime
import os

# Creamos la clase y definimos las funciones CRUD


class Reservas:
    def __init__(self, prog, conDB, cursor):
        self.prog = prog
        self.conDB = conDB
        self.cursor = cursor

# Funcion agregar

    def agregar(self, reser):
        sql = f"INSERT INTO reservas (idreserva,idcliente,idhabitacion,fecha_inicio,fecha_final,\
        cant_personas) VALUES ({reser[0]},'{reser[1]}','{reser[2]}','{reser[3]}','{reser[4]}',{reser[5]})"
        self.cursor.execute(sql)
        self.conDB.commit()


# Funcion buscar

    def buscar(self, num):
        sql = f"SELECT * FROM reservas WHERE idreserva={num}"
        self.cursor.execute(sql)
        resultado = self.cursor.fetchall()
        self.conDB.commit()
        return resultado

# Funcion consultar

    def consultar(self):
        sql = "SELECT * FROM reservas WHERE borrado=0"
        self.cursor.execute(sql)
        resultado = self.cursor.fetchall()
        return resultado

# Funcion actualizar

    def actualiza(self, reser):
        sql = f"UPDATE reservas SET idcliente='{reser[1]}', idhabitacion='{reser[2]}',\
        fecha_inicio='{reser[3]}',fecha_final='{reser[4]}', cant_personas={reser[5]} WHERE idreserva={reser[0]}"
        self.cursor.execute(sql)
        self.conDB.commit()

    # Funcion borrar

    def borrar(self, id):
        sql = f"UPDATE reservas SET borrado=1 WHERE idreserva={id}"
        self.cursor.execute(sql)
        self.conDB.commit()
