# Importamos las librerias

from flask import redirect, render_template
from datetime import datetime
import os

# Creamos la clase y definimos las funciones CRUD

class Comunicaciones:
    def __init__(self,prog,conDB,cursor):
        self.prog = prog
        self.conDB = conDB
        self.cursor = cursor

# Funcion agregar

    def agregar(self,comun):    
        sql = f"INSERT INTO comunicaciones (idcomunicacion,idcliente,fecha,tipo,descripcion,estado) VALUES ({comun[0]},{comun[1]},'{comun[2]}',\
        '{comun[3]}','{comun[4]}','{comun[5]}')"
        self.cursor.execute(sql)
        self.conDB.commit()
       
    
# Funcion buscar
        
    def buscar(self,num):
        sql=f"SELECT * FROM comunicaciones WHERE idcomunicacion={num}"
        self.cursor.execute(sql)
        resultado = self.cursor.fetchall()
        self.conDB.commit()
        return resultado
    
# Funcion consultar

    def consultar(self):
        sql = "SELECT * FROM comunicaciones WHERE borrado=0"
        self.cursor.execute(sql)
        resultado = self.cursor.fetchall()
        return resultado

# Funcion actualizar
    
    def actualiza(self,comun):
        sql=f"UPDATE comunicaciones SET idcliente={comun[1]}, fecha='{comun[2]}', tipo='{comun[3]}',descripcion='{comun[4]}', estado='{comun[5]}' WHERE idcomunicacion={comun[0]}"
        self.cursor.execute(sql)
        self.conDB.commit()
        
    
    # Funcion borrar
            
    def borrar(self,id):
        sql = f"UPDATE comunicaciones SET borrado=1 WHERE idcomunicacion={id}"
        self.cursor.execute(sql)
        self.conDB.commit()
