# Importamos las librerias

from flask import redirect, render_template
from datetime import datetime
import os


class Vehiculos:
    def __init__(self, prog, conDB, cursor):
        self.prog = prog
        self.conDB = conDB
        self.cursor = cursor

    def agregar(self, auto):
        ahora = datetime.now()
        fname, fext = os.path.splitext(auto[10].filename)
        nombreFoto = "E"+ahora.strftime("%Y%m%d%H%M%S")+fext
        auto[10].save("uploads/"+nombreFoto)
        sql = f"INSERT INTO gest_vehic (id_placa,tipo,marca,num_ocupa,estado,consumo,soat,tecno_mec,permiso,kilometraje,img,precio) VALUES ('{auto[0]}','{auto[1]}','{auto[2]}','{auto[3]}','{auto[4]}','{auto[5]}','{auto[6]}','{auto[7]}','{auto[8]}',{auto[9]},'{nombreFoto}',{auto[11]})"
        self.cursor.execute(sql)
        self.conDB.commit()

    def buscar(self, placa):
        sql = f"SELECT * FROM gest_vehic WHERE id_placa ='{placa}'"
        self.cursor.execute(sql)
        resultado = self.cursor.fetchall()
        self.conDB.commit()
        return resultado

    def princi(self, marca):
        sql = f"SELECT * FROM gest_vehic WHERE marca LIKE '{marca}%' AND estado = 0"
        self.cursor.execute(sql)
        resultado = self.cursor.fetchall()
        self.conDB.commit()
        return resultado

    def consultar(self):
        sql = "SELECT * FROM gest_vehic"
        self.cursor.execute(sql)
        resultado = self.cursor.fetchall()
        return resultado

    def contardisponiblecarros(self):
        sql = f"SELECT COUNT(*) FROM `gest_vehic` WHERE estado = 'disponible' AND tipo = 'carro';"
        self.cursor.execute(sql)
        Vehi = self.cursor.fetchall()
        return Vehi

    def contardisponiblemotos(self):
        sql = f"SELECT COUNT(*) FROM `gest_vehic` WHERE estado = 'disponible' AND tipo = 'moto';"
        self.cursor.execute(sql)
        moto = self.cursor.fetchall()
        return moto

    def modifica(self, placa):
        sql = f"UPDATE gest_vehic SET tipo='{placa[1]}',marca='{placa[2]}',num_ocupa={placa[3]},estado='{placa[4]}',consumo='{placa[5]}',soat='{placa[6]}',tecno_mec='{placa[7]}',permiso='{placa[8]}',kilometraje={placa[9]},precio={placa[11]} WHERE id_placa='{placa[0]}'"
        self.cursor.execute(sql)
        self.conDB.commit()
        if placa[10].filename != "":
            sql = f"SELECT img FROM gest_vehic WHERE id_placa='{placa[0]}'"
            self.cursor.execute(sql)
            resultado = self.cursor.fetchall()
            self.conDB.commit()
            os.remove(os.path.join(
                self.prog.config['CARPETAUP'], resultado[0][0]))
            ahora = datetime.now()
            fname, fext = os.path.splitext(placa[10].filename)
            nombreFoto = "E"+ahora.strftime("%Y%m%d%H%M%S")+fext
            placa[10].save("uploads/"+nombreFoto)
            sql = f"UPDATE gest_vehic SET img='{nombreFoto}' WHERE id_placa='{placa[0]}'"
            self.cursor.execute(sql)
            self.conDB.commit()

    def borrar(self, placa):
        sql = f"DELETE FROM gest_vehic WHERE id_placa ='{placa}'"
        self.cursor.execute(sql)
        self.conDB.commit()
