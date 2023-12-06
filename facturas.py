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
        
        print("Consulta SQL:", sql)  
        self.cursor.execute(sql)
        self.conDB.commit()
        sql = f"UPDATE `comandas` SET `estado`='pagado' WHERE idcliente = {idCliente}"
        self.cursor.execute(sql)
        self.conDB.commit()
        
# Funcion buscar
        
    def buscar(self,num):
        sql=f"SELECT * FROM facturas WHERE idfactura={num} AND borrado=0"
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
        sql = f"SELECT * FROM comandas WHERE idregistro={num}"
        self.cursor.execute(sql)
        resultado = self.cursor.fetchall()
        self.conDB.commit()
        return resultado

    
    def buscar_id_comanda(self,num):
        sql = f"SELECT idcomanda FROM comandas WHERE idRegistro={num} LIMIT 1"
        self.cursor.execute(sql)
        resultado = self.cursor.fetchall()
        self.conDB.commit()
        return resultado[0]
        print(resultado)
        
# Funcion actualizar
    
    def actualiza(self,fact):
        sql = f"UPDATE facturas SET idRegistro='{fact[1]}', idCliente='{fact[2]}',idcomanda='{fact[3]}', fecha='{fact[4]}',total='{fact[5]}' WHERE idfactura={fact[0]}"
        self.cursor.execute(sql)
        self.conDB.commit()
    
    # Funcion borrar
            
    def borrar(self,id):
        sql = f"UPDATE facturas SET borrado=1 WHERE idfactura={id}"
        self.cursor.execute(sql)
        self.conDB.commit()


     # Funcion para buscar la informacion basica del cliente
            
    def info_cliente(self, id):
        sql = f"""SELECT clientes.idcliente, clientes.nombre, clientes.celular
                FROM clientes
                JOIN comandas ON clientes.idcliente = comandas.idregistro
                WHERE comandas.idregistro = {id}
                LIMIT 1;"""
        self.cursor.execute(sql)
        resultado = self.cursor.fetchall()
        self.conDB.commit()
        sql_factura = "SELECT idFactura FROM facturas ORDER BY idFactura DESC LIMIT 1"
        self.cursor.execute(sql_factura)
        num_factura = self.cursor.fetchone()[0] + 1
        huesped_lista = list(resultado[0])
        huesped_lista.append(num_factura)
        resultado = [tuple(huesped_lista)]

        return resultado
       
    def info_hospedaje(self,id):
        sql = f"SELECT registro.idhabitacion, registro.fecha_inicio, registro.fecha_final, habitaciones.precio, habitaciones.capacidad, habitaciones.tipo FROM habitaciones habitaciones JOIN registro ON habitaciones.idhabitacion = registro.idhabitacion WHERE registro.idregistro = '{id}'"
        self.cursor.execute(sql)
        resultado = self.cursor.fetchall()
        self.conDB.commit()
        return resultado
    

    def info_productos(self,id):
        sql = f"SELECT idcodigo,descripItem,cantidad,valor,fecha FROM comandas WHERE idregistro={id} AND borrado=0 AND tipoVenta='producto' AND estado='por pagar'"
        self.cursor.execute(sql)
        resultado = self.cursor.fetchall()
        self.conDB.commit()
        return resultado
    
    def info_servicios(self,id):
        sql = f"SELECT idcodigo,descripItem,duracion,valor,fecha FROM comandas WHERE idregistro={id} AND borrado=0 AND tipoVenta='servicio' AND estado='por pagar'"
        self.cursor.execute(sql)
        resultado = self.cursor.fetchall()
        self.conDB.commit()
        return resultado
    
    def info_alquiler(self,id):
        sql = f"SELECT idcodigo,descripItem,cantidad,valor,fecha FROM comandas WHERE idregistro={id} AND borrado=0"
        self.cursor.execute(sql)
        resultado = self.cursor.fetchall()
        self.conDB.commit()
        return resultado
    