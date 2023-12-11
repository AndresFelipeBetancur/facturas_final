# Importamos las librerias

from flask import redirect, render_template
from datetime import datetime
import os

# Creamos la clase y definimos las funciones CRUD

class Facturas:
    def __init__(self,prog,conDB,cursor):
        self.prog = prog
        self.conDB = conDB
        self.cursor = cursor

# Funcion agregar

    def guardar(self, fact,fecha,idCliente,idFactura):    
        sql = f"INSERT INTO facturas (idFactura,idRegistro, idCliente, fecha, total, idComanda) VALUES ({idFactura},{fact[0]},{idCliente},'{fecha}',{fact[1]},{fact[2]})"  
        self.cursor.execute(sql)
        self.conDB.commit()
        #ADEMAS DE INSERTAR LOS DATOS DE LA FACTURA EN LA TABLE FACTURA
        #SE DEBE DE CAMBIAR EL ESTADO DE LOS PRODUCTOS Y SERVICIOS CONSUMIDOS
        #EN LA TABLA COMANDAS
        sql = f"UPDATE `comandas` SET `estado`='pagado' WHERE idcliente = {idCliente}"
        self.cursor.execute(sql)
        self.conDB.commit()
        
# Funcion buscar
        #LAS FACTURAS SE BUSCAN POR SU FECHA DE REALIZACION
    def buscar(self,fecha):
        sql=f"SELECT * FROM facturas WHERE fecha='{fecha}' AND borrado=0;"
        self.cursor.execute(sql)
        resultado = self.cursor.fetchall()
        self.conDB.commit()
        return resultado
    
# Funcion consultar

    def consultar(self):
        sql = "SELECT * FROM facturas WHERE borrado=0"
        self.cursor.execute(sql)
        resultado = self.cursor.fetchall()
        return resultado

#se buscan los registros de consumo del huesped para llenar la factura
    def realizar(self,num):
        sql = f"SELECT * FROM comandas WHERE idcliente={num}"
        self.cursor.execute(sql)
        resultado = self.cursor.fetchall()
        self.conDB.commit()
        return resultado

    
    def buscar_id_comanda(self,num):
        sql = f"SELECT idcomanda FROM comandas WHERE idcliente={num} LIMIT 1"
        self.cursor.execute(sql)
        resultado = self.cursor.fetchall()
        self.conDB.commit()
        return resultado[0][0]


    # Funcion borrar
    def borrar(self,id):
        sql = f"UPDATE facturas SET borrado=1 WHERE idfactura={id}"
        self.cursor.execute(sql)
        self.conDB.commit()


    # Funcion para buscar la informacion basica del cliente
    def info_cliente(self, id):
        sql = f"""SELECT clientes.idcliente, clientes.nombre, clientes.celular
                FROM clientes
                JOIN comandas ON clientes.idcliente = comandas.idcliente
                WHERE comandas.idcliente = {id}
                LIMIT 1;"""
        self.cursor.execute(sql)
        resultado = self.cursor.fetchall()
        self.conDB.commit()
        #SE CONSULTA EL ULTIMO NUMERO DE LA ULTIMA FACTURA Y SE LE SUMA UNO 
        sqlId = "SELECT idFactura FROM facturas ORDER BY idFactura DESC LIMIT 1"
        self.cursor.execute(sqlId)
        #EL METODO 'FETCHONE LO USO YA QUE SOLO NECESITO RECIBIR UNA SOLA LINEA'
        numFactura = self.cursor.fetchone()[0] + 1
        #CONVIERTO RESULTADO EN UNA LISTA YA QUE UNA TUPLA NO SE PUEDE MODIFICAR
        huespedLista = list(resultado[0])
        huespedLista.append(numFactura)
        resultado = [tuple(huespedLista)]
        return resultado
       
    def info_hospedaje(self,id):
        sql = f"SELECT registro.idhabitacion, registro.fecha_inicio, registro.fecha_final, habitaciones.precio, habitaciones.capacidad, habitaciones.tipo FROM habitaciones habitaciones JOIN registro ON habitaciones.idhabitacion = registro.idhabitacion WHERE registro.idcliente = {id}"
        self.cursor.execute(sql)
        resultado = self.cursor.fetchall()
        self.conDB.commit()
        return resultado
    

    def info_productos(self,id):
        sql = f"SELECT idcodigo,descripItem,cantidad,valor,fecha FROM comandas WHERE idcliente={id} AND borrado=0 AND idcodigo='PRODUCTO' AND estado='por pagar'"
        self.cursor.execute(sql)
        resultado = self.cursor.fetchall()
        self.conDB.commit()
        return resultado
    
    def info_servicios(self,id):
        sql = f"SELECT idcodigo,descripItem,cantidad,valor,fecha FROM comandas WHERE idcliente={id} AND borrado=0 AND idcodigo='SERVICIO' AND estado='por pagar'"
        self.cursor.execute(sql)
        resultado = self.cursor.fetchall()
        self.conDB.commit()
        return resultado
    
    #EN CASO DE QUE SE REQUIERA SEPARAR LOS SERVICIOS DE ALQUILER DE VEHICULOS 
    #DE LOS PRODUCTOS Y SERVICIOS CONSUMIDOS.
    #EN ESE CASO SE DEBE DE AGREGAR LA OPCION ALQUILER EN LA COLUMNA:'idcodigo' DE LA TABLA COMANDAS
    """
    def info_alquiler(self,id):
        sql = f"SELECT idcodigo,descripItem,cantidad,valor,fecha FROM comandas WHERE idcliente={id} AND borrado=0 AND idcodigo='ALQUILER' AND estado='por pagar'"
        self.cursor.execute(sql)
        resultado = self.cursor.fetchall()
        self.conDB.commit()
        return resultado
    """