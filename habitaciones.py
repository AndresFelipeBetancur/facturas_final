# Importamos las librerias

from flask import redirect, render_template
from datetime import datetime
import os

# Creamos la clase y definimos las funciones CRUD


class Habitaciones:
    def __init__(self, prog, conDB, cursor):
        self.prog = prog
        self.conDB = conDB
        self.cursor = cursor

# Funcion agregar

    def agregar(self,hab):
        ahora = datetime.now()
        fname, fext = os.path.splitext(hab[6].filename)
        nombreFoto = "E"+ahora.strftime("%Y%m%d%H%M%S")+fext
        hab[6].save("uploads/"+nombreFoto)
        sql = f"INSERT INTO habitaciones (idhabitacion,tipo,descripcion,capacidad,precio,estado,foto) VALUES ({hab[0]},'{hab[1]}','{hab[2]}','{hab[3]}',{hab[4]},'{hab[5]}','{nombreFoto}')"
        self.cursor.execute(sql)
        self.conDB.commit()

# Funcion buscar

    def buscar(self,num):
        sql = f"SELECT * FROM habitaciones WHERE idhabitacion={num}"
        self.cursor.execute(sql)
        resultado = self.cursor.fetchall()
        self.conDB.commit()
        return resultado

# Funcion consultar

    def consultar(self):
        sql = "SELECT * FROM habitaciones WHERE borrado=0"
        self.cursor.execute(sql)
        resultado = self.cursor.fetchall()
        return resultado

# Funcion actualizar

    def actualiza(self,hab):
        sql = f"UPDATE habitaciones SET tipo='{hab[1]}',descripcion='{hab[2]}',capacidad={hab[3]},\
        precio={hab[4]}, estado='{hab[5]}' WHERE idhabitacion={hab[0]}"
        self.cursor.execute(sql)
        self.conDB.commit()
        if hab[6].filename != "":
            sql = f"SELECT foto FROM habitaciones WHERE idhabitacion={hab[0]}"
            self.cursor.execute(sql)
            resultado = self.cursor.fetchall()
            self.conDB.commit()
            os.remove(os.path.join(self.prog.config['CARPETAUP'], resultado[0][0]))
            ahora = datetime.now()
            fname, fext = os.path.splitext(hab[6].filename)
            nombreFoto = "E"+ahora.strftime("%Y%m%d%H%M%S")+fext
            hab[6].save("uploads/"+nombreFoto)
            sql = f"UPDATE habitaciones SET foto='{nombreFoto}' WHERE idhabitacion={hab[0]}"
            self.cursor.execute(sql)
            self.conDB.commit()

    # Funcion borrar

    def borrar(self, id):
        sql = f"UPDATE habitaciones SET borrado=1 WHERE idhabitacion={id}"
        self.cursor.execute(sql)
        self.conDB.commit()
