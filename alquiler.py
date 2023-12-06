class Alquiler:
    def __init__(self,prog,conDB,cursor):
        self.prog = prog
        self.conDB = conDB 
        self.cursor=cursor
    
    def buscar(self,alquiler):
        sql=f"SELECT * FROM gest_alqui WHERE id_alqui ='{alquiler}'"
        self.cursor.execute(sql)
        resultado = self.cursor.fetchall()
        self.conDB.commit()
        return resultado

    def agregar(self,alquiler):
        sql=f"INSERT INTO gest_alqui (id_alqui,placa,id_registro,num_licencia,fech_alqui,fech_devo,id_comanda,comentario) VALUES ( {alquiler[0]},'{alquiler[1]}',{alquiler[2]},'{alquiler[3]}','{alquiler[4]}',\
        '{alquiler[5]}','{alquiler[6]}','{alquiler[7]}')"
        self.cursor.execute(sql)
        self.conDB.commit()


    def borrar(self,alquiler):
        sql =f"DELETE FROM gest_alqui WHERE id_alqui ='{alquiler}'"
        self.cursor.execute(sql)
        self.conDB.commit()

    def modifica(self,alquiler):
        sql=f"UPDATE gest_alqui SET placa='{alquiler[1]}',id_registro={alquiler[2]},\
        num_licencia='{alquiler[3]}',fech_alqui='{alquiler[4]}',fech_devo='{alquiler[5]}',\
        id_comanda={alquiler[6]},comentario='{alquiler[7]}' WHERE id_alqui='{alquiler[0]}'"
        self.cursor.execute(sql)
        self.conDB.commit()

    def consultar(self):
        sql = "SELECT * FROM gest_alqui"
        self.cursor.execute(sql)
        resultado = self.cursor.fetchall()
        return resultado