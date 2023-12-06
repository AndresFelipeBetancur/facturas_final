# Importamos las librerias

from flask import redirect, render_template
from datetime import datetime
import os

# Creamos la clase y definimos las funciones CRUD


class Ventas:
    def __init__(self, prog, conDB, cursor):
        self.prog = prog
        self.conDB = conDB
        self.cursor = cursor


# Funcion agregar

    def agregar(self,vent):
       
        sql = f"INSERT INTO ventas (idventa,idcomanda,idcodigo,descripItem,idregistro,idcliente,idhabitacion,fecha,cantidad,valor,subtotal,estado) VALUES ('{vent[0]}',{vent[1]},'{vent[2]}',{vent[3]},'{vent[4]}','{vent[5]}','{vent[6]}','{vent[7]}',{vent[8]},{vent[9]},{vent[10]},'{vent[11]}')"
        self.cursor.execute(sql)
        self.conDB.commit()
      

# Funcion buscar

    def buscar(self,num):
        sql = f"SELECT * FROM ventas WHERE idventa={num} ORDER BY idcliente"
        self.cursor.execute(sql)
        resultado = self.cursor.fetchall()
        self.conDB.commit()
        return resultado
    

# Funcion consultar

    def consultar(self):
        sql = "SELECT * FROM ventas WHERE borrado=0"
        self.cursor.execute(sql)
        resultado = self.cursor.fetchall()
        return resultado

# Funcion actualizar

    def actualiza(self,vent):
        sql = f"UPDATE ventas SET idventa={vent[1]} idcodigo={vent[2]}, descripItem='{vent[3]}', idregistro={vent[4]},idcliente='{vent[5]}',idhabitacion='{vent[6]}', fecha='{vent[7]}', cantidad={vent[8]},valor={vent[9]},subtotal={vent[10]},estado='{vent[11]}' WHERE idventa='{vent[0]}'"
        self.cursor.execute(sql)
        self.conDB.commit()
      

    # Funcion borrar

    def borrar(self, id):
        sql = f"UPDATE ventas SET borrado=1 WHERE idventa={id}"
        self.cursor.execute(sql)
        self.conDB.commit()
