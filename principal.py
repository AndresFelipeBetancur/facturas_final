from datetime import date, datetime, timedelta
import hashlib
from random import randint
from click import Path
from flask import Flask, Response, current_app, make_response, redirect, render_template, request, send_from_directory, session, send_file
import jinja2
import mysql.connector
import os
import pdfkit # hace uso del programa wkhtmltopdf // instalar esta libreria ----MODULO FELIPE----
import webbrowser as vb #instalar esta libreria ----MODULO FELIPE----



from usuarios import Usuarios
from clientes import Clientes
from habitaciones import Habitaciones
from reservas import Reservas
from registro import Registros
from Vehiculos import Vehiculos
from alquiler import Alquiler
from productos import Productos
from comandas import Comandas
from facturas import Facturas
from comunicaciones import Comunicaciones
from ventas import Ventas


prog = Flask(__name__)
prog.secret_key=str(randint(100000,999999))
prog.config["PERMANENT_SESSION_LIFETIME"] = timedelta(minutes=60)
conexion = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="bdhotel",
)
miCursor = conexion.cursor()
misUsuarios = Usuarios(prog,conexion,miCursor)
misClientes = Clientes(prog,conexion,miCursor)
misHabitaciones = Habitaciones (prog,conexion,miCursor)
misReservas = Reservas(prog,conexion,miCursor)
misRegistros = Registros(prog,conexion,miCursor)
misVehiculos = Vehiculos(prog, conexion, miCursor)
misAlquileres= Alquiler(prog,conexion,miCursor)
misProductos = Productos(prog,conexion,miCursor)
misVentas = Ventas(prog,conexion,miCursor)
misFacturas = Facturas(prog,conexion,miCursor)
misComandas = Comandas(prog,conexion,miCursor)
misComunicaciones = Comunicaciones(prog,conexion,miCursor)

CARPETAUP = os.path.join('uploads')
prog.config['CARPETAUP'] = CARPETAUP

@prog.route('/uploads/<nombre>')
def uploads(nombre):
    return send_from_directory(prog.config['CARPETAUP'],nombre)

# Ruta para  Usuarios ( Grupo Aidalia )

@prog.route('/')
def index():
    return render_template("usuarios/login.html",msg="")

@prog.route('/login',methods=['POST'])
def login():
    id = request.form['uname']
    contra = request.form['psw']
    resultado = misUsuarios.loguear(id,contra)
    if len(resultado)>0:
        session['loginOk'] = True
        session['nomUsuario'] = resultado[0][0]
        sql = "SELECT COUNT(*) AS totalHabDisp FROM habitaciones WHERE estado = 'DISPONIBLE';"
        cursor = conexion.cursor()
        cursor.execute(sql)
        disponible = cursor.fetchall()
        conexion.commit()
        sql = "SELECT COUNT(*) AS totalHabOcup FROM habitaciones WHERE estado = 'OCUPADA';"
        cursor.execute(sql)
        ocupada = cursor.fetchall()
        conexion.commit() 
        sql ="SELECT COUNT(*) AS totalHabLimp FROM habitaciones WHERE estado = 'LIMPIEZA';"
        cursor = conexion.cursor()
        cursor.execute(sql)
        limpieza = cursor.fetchall()
        conexion.commit()
        sql = "SELECT COUNT(*) AS totalHabMant FROM habitaciones WHERE estado = 'MANTENIMIENTO';"
        cursor = conexion.cursor()
        cursor.execute(sql)
        mantenimiento = cursor.fetchall()
        conexion.commit()
        sql = "SELECT COUNT(*) AS totalvehiculos FROM gest_vehic WHERE estado = 1;"
        cursor = conexion.cursor()
        cursor.execute(sql)
        totalveh = cursor.fetchall()
        conexion.commit()
        sql = "SELECT COUNT(*) AS totalproductos FROM productos WHERE estado = 'DISPONIBLE';"
        cursor = conexion.cursor()
        cursor.execute(sql)
        totalprod = cursor.fetchall()
        conexion.commit()
        sql = "SELECT COUNT(*) AS totalpqrs FROM comunicaciones WHERE borrado = 0;"
        cursor = conexion.cursor()
        cursor.execute(sql)
        totalpqrs = cursor.fetchall()
        conexion.commit() 
        sql = "SELECT COUNT(*) AS totalservicios FROM servicios WHERE borrado = 0;"
        cursor = conexion.cursor()
        cursor.execute(sql)
        totalserv = cursor.fetchall()
        conexion.commit()
        return render_template("principal.html", nom=resultado[0][0], disp=disponible[0][0], ocup=ocupada[0][0], limp=limpieza[0][0], mant=mantenimiento[0][0], totveh=totalveh[0][0], totprod=totalprod[0][0],totpqrs=totalpqrs[0][0], totserv=totalserv[0][0])
    else:
        return render_template("login.html",msg="Credenciales incorrectas")
    
# Establecemos la ruta a templates/principal


@prog.route('/principal')
def principal():
    if session.get('loginOk'):
        return render_template("principal.html")
    else:
        return redirect('/')

# Ruta para Clientes ( Grupo Jhon Alejandro )


@prog.route('/clientes')
def clientes():
    if session.get('loginOk'):
        resultado = misClientes.consultar()
        return render_template("clientes/clientes.html", res=resultado)
    else:
        return redirect('/')

# Buscador Clientes

@prog.route('/buscarClientes', methods=['GET','POST'])
def buscarClientes():
    if request.method == "POST":
       search = request.form['nombre']
       sql = ("SELECT * FROM clientes WHERE nombre='%s' ORDER BY nombre ASC" % (search,))

            #"SELECT nombre, movil FROM clientes LIKE '% %';"

       cursor = conexion.cursor()
       cursor.execute(sql)
       resultadoBusqueda = cursor.fetchone()
       conexion.commit()
       return render_template("clientes/buscarcliente.html", miData=resultadoBusqueda)
   
   
@prog.route('/agregacliente')
def agregacliente():
    if session.get('loginOk'):
       sql = "SELECT nombre FROM clientes WHERE borrado=0"
       cursor = conexion.cursor()
       cursor.execute(sql)
       cliente = cursor.fetchall()
       conexion.commit()
       return render_template("clientes/agregacliente.html",  clie = cliente)


@prog.route("/guardacliente", methods=['POST'])
def guardacliente():
    num = request.form['numero']
    nomc = request.form['nombre']
    nac = request.form['nacionalidad']
    cel = request.form['celular']
    em = request.form['email']
    fnac = request.form['fnacimiento']
    cliente = [num, nomc, nac, cel, em, fnac]
    if len(misClientes.buscar(num)) > 0:
        return render_template("clientes/agregacliente.html", mensaje="Número de cliente ya existe!!!")
    else:
        misClientes.agregar(cliente)
        return redirect('/clientes')


@prog.route("/modificacliente/<num>")
def modificacliente(num):
    if session.get('loginOk'):
        resultado = misClientes.buscar(num)
        return render_template("clientes/modificacliente.html", clie=resultado[0])
    else:
        return redirect('/')


@prog.route("/actualizacliente", methods=['POST'])
def actualizacliente():
    num = request.form['numero']
    nomc = request.form['nombre']
    nac = request.form['nacionalidad']
    cel = request.form['celular']
    em = request.form['email']
    fnac = request.form['fnacimiento']
    cliente = [num, nomc, nac, cel, em, fnac]
    misClientes.actualiza(cliente)
    return redirect("/clientes")


@prog.route("/borracliente/<id>")
def borracliente(id):
    if session.get('loginOk'):
        misClientes.borrar(id)
        return redirect("/clientes")
    else:
        return redirect('/')
    
    
# Ruta para Habitaciones ( Grupo Jhon Alejandro )    

@prog.route('/habitaciones')
def habitaciones():
    if session.get('loginOk'):
        resultado = misHabitaciones.consultar()
        return render_template("habitaciones/habitaciones.html",res = resultado)
    else:
        return redirect('/')

@prog.route('/agregahabitacion')
def agregahabitacion():
    if session.get('loginOk'):
       sql = "SELECT idhabitacion FROM habitaciones WHERE borrado=0"
       cursor = conexion.cursor()
       cursor.execute(sql)
       habitacion = cursor.fetchall()
       conexion.commit()
       return render_template("habitaciones/agregahabitacion.html",  hab = habitacion) 
    

@prog.route("/guardahabitacion", methods=['POST'])
def guardahabitacion():
    num = request.form['numero']
    tip = request.form['tipo']
    desc = request.form['descripcion']
    cap = request.form['capacidad']
    prec = request.form['precio']
    est = request.form['estado']
    fot = request.files['foto']
    habitacion=[num,tip,desc,cap,prec,est,fot]
    if len(misHabitaciones.buscar(num))>0:
        return render_template("habitaciones/agregahabitacion.html",mensaje="Número de habitacion ya existe!!!")
    else:
        misHabitaciones.agregar(habitacion)
        return redirect('/habitaciones')

@prog.route("/modificahabitacion/<num>")
def modificarhabitacion(num):
    if session.get('loginOk'):
        resultado = misHabitaciones.buscar(num)
        return render_template("habitaciones/modificahabitacion.html", hab=resultado[0])
    else:
        return redirect('/')

@prog.route("/actualizahabitacion", methods=['POST'])
def actualizahabitacion():
    num = request.form['numero']
    tip = request.form['tipo']
    desc = request.form['descripcion']
    cap = request.form['capacidad']
    prec = request.form['precio']
    est = request.form['estado']
    fot = request.files['foto']
    habitacion=[num,tip,desc,cap,prec,est,fot]
    misHabitaciones.actualiza(habitacion)
    return redirect("/habitaciones")

@prog.route("/borrahabitacion/<id>")
def borrahabitacion(id):
    if session.get('loginOk'):
        misHabitaciones.borrar(id)
        return redirect("/habitaciones")
    else:
        return redirect('/')
       
    
# Ruta para Registro ( Grupo Jhon Alejandro )

@prog.route('/registro')
def registro():
    if session.get('loginOk'):
        resultado = misRegistros.consultar()
        return render_template("registro/registro.html",res = resultado)
    else:
        return redirect('/')

@prog.route('/agregaregistro')
def agregaregistro():
    if session.get('loginOk'):
       sql = "SELECT idregistro FROM registro WHERE borrado=0"
       cursor = conexion.cursor()
       cursor.execute(sql)
       registro = cursor.fetchall()
       conexion.commit()
       return render_template("registro/agregaregistro.html",  reg = registro) 
    

@prog.route("/guardaregistro", methods=['POST'])
def guardaregistro():
    num = request.form['numero']
    idclie = request.form['idcliente']
    idhab = request.form['idhabitacion']
    fini = request.form['fecha_inicio']
    ffin = request.form['fecha_final']
    prec = request.form['precio']
    registro=[num,idclie,idhab,fini,ffin,prec]
    if len(misRegistros.buscar(num))>0:
        return render_template("registro/agregaregistro.html",mensaje="Número de registro ya existe!!!")
    else:
        misRegistros.agregar(registro)
        return redirect('/registro')

@prog.route("/modificaregistro/<num>")
def modificarregistro(num):
    if session.get('loginOk'):
        resultado = misRegistros.buscar(num)
        return render_template("registro/modificaregistro.html",reg=resultado[0])
    else:
        return redirect('/')

@prog.route("/actualizaregistro", methods=['POST'])
def actualizaregistro():
    num = request.form['numero']
    idclie = request.form['idcliente']
    idhab = request.form['idhabitacion']
    fini = request.form['fecha_inicio']
    ffin = request.form['fecha_final']
    prec = request.form['precio']
    registro=[num,idclie,idhab,fini,ffin,prec]
    misRegistros.actualiza(registro)
    return redirect("/registro")

@prog.route("/borraregistro/<id>")
def borraregistro(id):
    if session.get('loginOk'):
        misRegistros.borrar(id)
        return redirect("/registro")
    else:
        return redirect('/')

# Ruta para Reservas ( Grupo Jhon Alejandro )

@prog.route('/reservas')
def reservas():
    if session.get('loginOk'):
        resultado = misReservas.consultar()
        return render_template("reservas/reservas.html",res = resultado)
    else:
        return redirect('/')

@prog.route('/buscarReservas', methods=['GET','POST'])
def buscarReservas():
    if request.method == "POST":
       search = request.form['buscar']
       sql = ("SELECT * FROM reservas WHERE idreserva='%s' ORDER BY idreserva DESC" % (search,))
       cursor = conexion.cursor()
       cursor.execute(sql)
       resultadoBusqueda = cursor.fetchone()
       conexion.commit()
       return render_template("reservas/buscareserva.html", miData=resultadoBusqueda)
   

@prog.route('/agregareserva')
def agregareserva():
    if session.get('loginOk'):
       sql = "SELECT idreserva FROM reservas WHERE borrado=0"
       cursor = conexion.cursor()
       cursor.execute(sql)
       reserva = cursor.fetchall()
       conexion.commit()
       sql = "SELECT idcliente, nombre FROM clientes WHERE borrado=0"
       cursor.execute(sql)
       clientes = cursor.fetchall()
       conexion.commit() 
       sql = "SELECT idhabitacion FROM habitaciones WHERE borrado=0"
       cursor = conexion.cursor()
       cursor.execute(sql)
       habitacion = cursor.fetchall()
       conexion.commit()
       return render_template("reservas/agregareserva.html",  reser=reserva, clie=clientes, 
       hab = habitacion) 
    

@prog.route("/guardareserva", methods=['POST'])
def guardareserva():
    num = request.form['numero']
    idclie = request.form['idcliente']
    idhab = request.form['idhabitacion']
    fini = request.form['fecha_inicio']
    ffin = request.form['fecha_final']
    cantper = request.form['cant_personas']
    reserva=[num,idclie,idhab,fini,ffin,cantper]
    if len(misReservas.buscar(num))>0:
        return render_template("reservas/agregareserva.html",mensaje="Número de reserva ya existe!!!")
    else:
        misReservas.agregar(reserva)
        return redirect('/reservas')

@prog.route("/modificareserva/<num>")
def modificarreserva(num):
    if session.get('loginOk'):
        resultado = misReservas.buscar(num)
        return render_template("reservas/modificareserva.html",reser=resultado[0])
    else:
        return redirect('/')

@prog.route("/actualizareserva", methods=['POST'])
def actualizareserva():
    num = request.form['numero']
    idclie = request.form['idcliente']
    idhab = request.form['idhabitacion']
    fini = request.form['fecha_inicio']
    ffin = request.form['fecha_final']
    cantper = request.form['cant_personas']
    reserva=[num,idclie,idhab,fini,ffin,cantper]
    misReservas.actualiza(reserva)
    return redirect("/reservas")

@prog.route("/borrareserva/<id>")
def borrareserva(id):
    if session.get('loginOk'):
        misReservas.borrar(id)
        return redirect("/reservas")
    else:
        return redirect('/')


# ---------- Ruta para Vehiculos ( Grupo Harold David )------------------

# Ruta si el usuario intenta ingresar y no esta logeado (Harold David)

@prog.route('/404Error')
def error404():
    return render_template("404Error/404error.html")
   
# Ruta para Vehiculos ( Grupo Harold David )

@prog.route('/catalogo')
def catalogo():
    if session.get('loginOk'):
        resultado = misVehiculos.consultar()
        return render_template("Vehiculos/catalogo.html", res=resultado)
    else:
        return redirect('/404Error')
    
@prog.route('/buscarauto',methods=['POST'])
def buscarauto():
    marca=request.form['marca']
    if session.get('loginOk'):
        resultado=misVehiculos.princi(marca)
        return render_template("Vehiculos/catalogo.html", res=resultado)
    else:
        return redirect('/principal',mensaje='Marca no disponible')
    
       

@prog.route("/borrarauto/<placa>")
def Borrar(placa):
    misVehiculos.borrar(placa)
    return redirect ('/catalogo')

@prog.route('/agregarauto')
def agregar():
    if session.get('loginOk'):
        return render_template("Vehiculos/agregar.html")
    else:
        redirect('/404Error')

@prog.route('/agregar',methods=['POST'])
def agregarGuardar():
    plac=request.form['Placa']
    tipo=request.form['tipo']
    marc=request.form['Marca']
    numOcup=request.form['numOcupantes']
    estd=request.form['estado']
    consum=request.form['consumo']
    soat=request.form['soat']
    tecnoMec=request.form['tecno_mec']
    perm=request.form['permiso']
    kilom=request.form['kilometraje']
    img=request.form['img']
    prec=request.form['precio']
    auto=[plac,tipo,marc,numOcup,estd,consum,soat,tecnoMec,perm,kilom,img,prec]
    if len(misVehiculos.buscar(plac))>0:
        return render_template("Vehiculos/agregar.html",mensaje="Vehiculo existente")
    else:
        misVehiculos.agregar(auto)
        return redirect ("/catalogo")
    
@prog.route('/modificavehiculo/<placa>')
def modifica(placa):
    resultado=misVehiculos.buscar(placa)
    return render_template("Vehiculos/modificarauto.html", placa=resultado[0])

@prog.route('/modificarGuardar',methods=['POST'])
def modificaGuardar():
    plac=request.form['Placa']
    tipo=request.form['tipo']
    marc=request.form['Marca']
    numOcup=request.form['numOcupantes']
    estd=request.form['estado']
    consum=request.form['consumo']
    soat=request.form['soat']
    tecnoMec=request.form['tecno_mec']
    perm=request.form['permiso']
    kilom=request.form['kilometraje']
    img=request.form['img']
    prec=request.form['precio']
    auto=[plac,tipo,marc,numOcup,estd,consum,soat,tecnoMec,perm,kilom,img,prec]
    misVehiculos.modifica(auto)
    return redirect('/catalogo')

#Ruta para Alquiler ( Grupo Harold David)
@prog.route('/alquiler')
def alquiler():
    if session.get('loginOk'):
        resultado= misAlquileres.consultar()
        return render_template("Vehiculos/alquiler(1).html", res=resultado)
    else:
        redirect('/404Error')

@prog.route('/agregaralquiler')
def agregaral():
    if session.get('loginOk'):
        return render_template("Vehiculos/Agregaralquiler.html")
    else:
        redirect('/404Error')


@prog.route('/borraralquiler/<idalquiler>')
def borraralquiler(idalquiler):
    misAlquileres.borrar(idalquiler)
    return redirect('/catalogo')

@prog.route('/agregaralq',methods=['POST'])
def agregaralquiler():
    idalq=request.form['id_alquiler']
    placa=request.form['placa']
    idreg=request.form['id_registro']
    numlic=request.form['num_licencia']
    fechalq=request.form['fecha_alquiler']
    fechadev=request.form['fecha_devolucion']
    comand=request.form['ID_Comanda']
    coment=request.form['comentario']
    alqui=[idalq,placa,idreg,numlic,fechalq,fechadev,comand,coment]
    if len(misAlquileres.buscar(idalq))>0:
        return render_template("Vehiculos/AgregarAlquiler.html",mensaje="Alquiler Existente")
    else:
        misAlquileres.agregar(alqui)
        return redirect("/alquiler")

@prog.route('/modificaalquiler/<idalquiler>')
def modificaalq(idalquiler):
    resultado=misAlquileres.buscar(idalquiler)
    return render_template("Vehiculos/modificaralqui.html", idalquiler=resultado[0])

@prog.route('/modificaralquilerGuardar',methods=['POST'])
def modificaalGuardar():
    idalq=request.form['ID_Alquiler']
    placa=request.form['placa']
    idreg=request.form['ID_registro']
    numlic=request.form['num_licencia']
    fechalq=request.form['fecha_alquiler']
    fechadev=request.form['fecha_devolucion']
    comand=request.form['ID_comanda']
    coment=request.form['comentario']
    alqui=[idalq,placa,idreg,numlic,fechalq,fechadev,comand,coment]
    misAlquileres.modifica(alqui)
    return redirect('alquiler')


# Ruta para Productos ( Grupo Adriana Herrera )

@prog.route('/productos')
def productos():
    if session.get('loginOk'):
        resultado = misProductos.consultar()
        return render_template("productos/productos.html",res=resultado)
    else:
        return redirect('/')
    
@prog.route('/buscarProducto', methods=['GET','POST'])
def buscarProducto():
    if request.method == "POST":
       search = request.form['buscar']
       sql = ("SELECT * FROM productos WHERE idProd='%s' ORDER BY idProd DESC" % (search,))
       cursor = conexion.cursor()
       cursor.execute(sql)
       resultadoBusqueda = cursor.fetchone()
       conexion.commit()
       return render_template("productos/buscaproducto.html", miData=resultadoBusqueda)

@prog.route('/agregaproducto')
def agregaproducto():
    if session.get('loginOk'):
       sql = "SELECT nombre FROM productos WHERE borrado=0"
       cursor = conexion.cursor()
       cursor.execute(sql)
       producto = cursor.fetchall()
       conexion.commit()
       return render_template("productos/agregaproducto.html",  prod = producto) 
    

@prog.route("/guardaproducto", methods=['POST'])
def guardaproducto():
    num = request.form['numero']
    nomp = request.form['nomProd']
    desc = request.form['descripcion']
    cant = request.form['cantidad']
    prec = request.form['precio']
    iv = request.form['iva']
    est = request.form['estado']
    fot = request.files['foto']
    producto=[num,nomp,desc,cant,prec,iv,est,fot]
    if len(misProductos.buscar(num))>0:
        return render_template("productos/agregaproducto.html",mensaje="Número de producto ya existe!!!")
    else:
        misProductos.agregar(producto)
        return redirect('/productos')

@prog.route("/modificarproducto/<num>")
def modificarproducto(num):
    if session.get('loginOk'):
        resultado = misProductos.buscar(num)
        return render_template("productos/modificarproducto.html",prod=resultado[0])
    else:
        return redirect('/')

@prog.route("/actualizaproducto", methods=['POST'])
def actualizaproducto():
    num = request.form['numero']
    nomp = request.form['nomProd']
    desc = request.form['descripcion']
    cant = request.form['cantidad']
    prec = request.form['precio']
    iv = request.form['iva']
    est = request.form['estado']
    fot = request.files['foto']
    producto=[num,nomp,desc,cant,prec,iv,est,fot]
    misProductos.actualiza(producto)
    return redirect("/productos")

@prog.route("/borraproducto/<id>")
def borraproducto(id):
    if session.get('loginOk'):
        misProductos.borrar(id)
        return redirect("/productos")
    else:
        return redirect('/')
 

    
    
# Ruta para Comandas ( Grupo Adriana Herrera )


@prog.route('/comandas')
def comandas():
    if session.get('loginOk'):
       resultado = misComandas.consultar()
       return render_template("comandas/comandas.html", res=resultado)
    else:
        return redirect('/')



@prog.route('/buscarcomanda', methods=['GET','POST'])
def buscarcomanda():
    if request.method == "POST":
       search = request.form['buscar']
       sql = ("SELECT * FROM comandas WHERE idcliente='%s' " % (search,))
       cursor = conexion.cursor()
       cursor.execute(sql)
       resultado= cursor.fetchall()
       conexion.commit()
       return render_template("comandas/buscarcomanda.html", res=resultado)


@prog.route('/agregacomanda')
def agregacomanda():
    if session.get('loginOk'):
       sql = "SELECT idregistro FROM registro WHERE borrado=0"
       cursor = conexion.cursor()
       cursor.execute(sql)
       registro = cursor.fetchall()
       conexion.commit()
       sql = "SELECT idcliente, nombre FROM clientes WHERE borrado=0"
       cursor.execute(sql)
       clientes = cursor.fetchall()
       conexion.commit() 
       sql = "SELECT nombre FROM productos WHERE borrado=0"
       cursor = conexion.cursor()
       cursor.execute(sql)
       productos = cursor.fetchall()
       conexion.commit()
       sql = "SELECT idhabitacion FROM habitaciones WHERE borrado=0"
       cursor = conexion.cursor()
       cursor.execute(sql)
       habitacion = cursor.fetchall()
       conexion.commit()
       return render_template("comandas/agregacomanda.html", reg = registro, cli = clientes, prod = productos, hab = habitacion)


@prog.route("/guardacomanda", methods=['POST'])
def guardacomanda():

    num = request.form['numero']
    idcod = request.form['idcodigo']
    desc = request.form['descripItem']
    reg = request.form['idregistro']
    clie = request.form['idcliente']
    hab = request.form['idhabitacion']
    fech = request.form['fecha']
    cant = request.form['cantidad']
    val = request.form['valor']
    sub = request.form['subtotal']
    est = request.form['estado']
    fot = request.files['foto']
    comanda = [num,idcod,desc,reg,clie,hab,fech,cant,val,sub,est,fot]
    if len(misComandas.buscar(num))>0:
        return render_template("comandas/agregacomanda.html", mensaje="Número de comanda ya existe!!!")
    else:
        misComandas.agregar(comanda)
        return redirect('/comandas')
    

@prog.route("/modificacomanda/<num>")
def modificacomanda(num):
    if session.get('loginOk'):
        resultado = misComandas.buscar(num)
        return render_template("comandas/modificacomanda.html", com=resultado[0])
    else:
        return redirect('/')



@prog.route("/actualizacomanda", methods=['POST'])
def actualizacomanda():
    num = request.form['numero']
    idcod = request.form['idcodigo']
    desc = request.form['descripItem']
    reg = request.form['idregistro']
    clie = request.form['idcliente']
    hab = request.form['idhabitacion']
    fech = request.form['fecha']
    cant = request.form['cantidad']
    val = request.form['valor']
    sub = request.form['subtotal']
    est = request.form['estado']
    fot = request.files['foto']
    comanda = [num,idcod,desc,reg,clie,hab,fech,cant,val,sub,est,fot]
    misComandas.actualiza(comanda)
    return redirect("/comandas")


@prog.route("/borracomanda/<id>")
def borracomanda(id):
    if session.get('loginOk'):
        misComandas.borrar(id)
        return redirect("/comandas")
    else:
        return redirect('/')
 
# Ruta para Ventas( Grupo Adriana)

@prog.route('/ventas')
def ventas():
    if session.get('loginOk'):
        resultado = misVentas.consultar()
        return render_template("ventas/agregaventa.html",res=resultado)
    else:
        return redirect('/')


@prog.route("/guardaventa", methods=['POST'])
def guardaventa():

    num = request.form['numero']
    idcom = request.form['idcomanda']
    idcod = request.form['idcodigo']
    desc = request.form['descripItem']
    reg = request.form['idregistro']
    clie = request.form['idcliente']
    hab = request.form['idhabitacion']
    fech = request.form['fecha']
    cant = request.form['cantidad']
    val = request.form['valor']
    sub = request.form['subtotal']
    est = request.form['estado']
    fot = request.files['foto']
    venta = [num,idcom,idcod,desc,reg,clie,hab,fech,cant,val,sub,est,fot]
    if len(misVentas.buscar(num))>0:
        return render_template("ventas/buscarventa.html", mensaje="Número de comanda ya existe!!!")
    else:
        misVentas.agregar(venta)
        return redirect('/ventas')
    
@prog.route("/actualizaventa", methods=['POST'])
def actualizaventa():
    num = request.form['numero']
    idcom = request.form['idcomanda']
    idcod = request.form['idcodigo']
    desc = request.form['descripItem']
    reg = request.form['idregistro']
    clie = request.form['idcliente']
    hab = request.form['idhabitacion']
    fech = request.form['fecha']
    cant = request.form['cantidad']
    val = request.form['valor']
    sub = request.form['subtotal']
    est = request.form['estado']
    fot = request.files['foto']
    venta = [num,idcom,idcod,desc,reg,clie,hab,fech,cant,val,sub,est,fot]
    misVentas.actualiza(venta)
    return redirect("/ventas")


@prog.route("/modificaventa/<num>")
def modificaventa(num):
    if session.get('loginOk'):
        resultado = misVentas.buscar(num)
        return render_template("ventas/modificaventa.html", vent=resultado[0])
    else:
        return redirect('/')
    
@prog.route("/borraventa<id>")
def borraventa(id):
    if session.get('loginOk'):
        misVentas.borrar(id)
        return redirect("/ventas")
    else:
        return redirect('/')
    
# Ruta para Comunicaciones ( Grupo Aidalia)

@prog.route('/comunicaciones')
def comunicaciones():
    if session.get('loginOk'):
        resultado = misComunicaciones.consultar()
        return render_template("comunicaciones/pqrs.html",res=resultado)
    else:
        return redirect('/')

@prog.route('/agregarpqrs')
def agregarpqrs():
    if session.get('loginOk'):
       sql = "SELECT idcomunicacion FROM comunicaciones WHERE borrado=0"
       cursor = conexion.cursor()
       cursor.execute(sql)
       comunicacion = cursor.fetchall()
       conexion.commit()
       return render_template("comunicaciones/agregarpqrs.html",  comun = comunicacion) 
    

@prog.route("/guardapqrs", methods=['POST'])
def guardapqrs():
    num = request.form['numero']
    clie = request.form['idcliente']
    fec = request.form['fecha']
    tip = request.form['tipo']
    desc = request.form['descripcion']
    est = request.form['estado']
    comunicacion=[num,clie,fec,tip,desc,est]
    if len(misComunicaciones.buscar(num))>0:
        return render_template("comunicaciones/agregarpqrs.html",mensaje="Número de comunicacion ya existe!!!")
    else:
        misComunicaciones.agregar(comunicacion)
        return redirect('/comunicaciones')

@prog.route("/modificarpqrs/<num>")
def modificarpqrs(num):
    if session.get('loginOk'):
        resultado = misComunicaciones.buscar(num)
        return render_template("comunicaciones/modificarpqrs.html",comun=resultado[0])
    else:
        return redirect('/')

@prog.route("/actualizapqrs", methods=['POST'])
def actualizapqrs():
   num = request.form['numero']
   clie = request.form['idcliente']
   fec = request.form['fecha']
   tip = request.form['tipo']
   desc = request.form['descripcion']
   est = request.form['estado']
   comunicacion=[num,clie,fec,tip,desc,est]
   misComunicaciones.actualiza(comunicacion)
   return redirect("/comunicaciones")

@prog.route("/borrapqrs<id>")
def borrapqrs(id):
    if session.get('loginOk'):
        misComunicaciones.borrar(id)
        return redirect("/comunicaciones")
    else:
        return redirect('/')

# //////////////////FACTURAS ANDRES FELIPE\\\\\\\\\\\\\\\\\\\\\
    
@prog.route('/facturas')
def facturas():
    if session.get('loginOk'):
        resultado = misFacturas.consultar()
        return render_template("facturas/facturas1.html",res=resultado)
    else:
        return redirect('/')

@prog.route("/buscafactura",methods=['POST'])
def buscafactura():
    if session.get('loginOk'):
        idfactura = request.form['idfactura']
        resultado = misFacturas.buscar(idfactura)
        if resultado:
            mensaje="¡Se han encontrado resultados para su busqueda!"
            return render_template("facturas/buscafactura.html",res=resultado,msg=mensaje)
        else:
            mensaje = "No se han encontrado resultados para su busqueda"
            return render_template("facturas/buscafactura.html",res=resultado,msg1=mensaje)
        
    else:
        return redirect('/')


@prog.route('/agregafactura',methods=['POST'])
def agregafactura():
    if session.get('loginOk'): 
        resultado = misFacturas.consultar() 
        idhuesped = request.form['idregistro']
        if not misFacturas.realizar(idhuesped):
            return render_template("/facturas/facturas1.html",msg="no se encontro un registro de consumo asociado a este huesped",res=resultado)
        else:
            # Obtén la fecha actual
            fecha_actual = date.today()
            # Formatea la fecha en el formato 'AAAA-MM-DD'
            fechaActual = fecha_actual.strftime('%Y-%m-%d')
            #Recopilar la informacion de la factura asociada al cliente
            huespedInfo = misFacturas.info_cliente(idhuesped)
            idFactura = huespedInfo[0][-1] 
            idCliente = huespedInfo[0][0]
            #Recopilar la informacion asociada a los productos que consumio el cliente
            productosComsumidos = misFacturas.info_productos(idhuesped)
            subtotalP = []
            productosModificados = []
            #Si hay productos consumidos se les cobra un iva del 19%
            #En caso de que no se encuentren productos no se realiza el proceso
            if productosComsumidos:
                ivaP = 0.19
                for producto in productosComsumidos:
                    productoLista = list(producto)
                    cantidad = producto[2]
                    valor = producto[3]
                    subtotal = cantidad * valor * ivaP + valor
                    productoLista.append(subtotal)
                    subtotalP.append(subtotal)
                    productoLista.append(ivaP)
                    productosModificados.append(productoLista)
            
            #Recopilar la informacion asociada a los servicios que consumio el cliente
            serviciosConsumidos = misFacturas.info_servicios(idhuesped)
            subtotalS = 0
            serviciosModificados = []
            subtotalS = []
            #Si hay servicios consumidos se les cobra un iva del 19%
            #En caso de que no se encuentren servicios no se realiza el proceso
            if serviciosConsumidos:
                ivaS = 0.19
                for servicio in serviciosConsumidos:
                    servicioLista=list(servicio)
                    servicioLista.append(ivaS)
                    valor = servicioLista[3]
                    subtotal = valor*ivaS+valor
                    servicioLista.append(subtotal)
                    subtotalS.append(subtotal)
                    serviciosModificados.append(tuple(servicioLista))
            
            #Recopilar informacion del hospedaje del huesped
            detallesHospedaje = misFacturas.info_hospedaje(idhuesped)
            
            #consulto la nacionalidad del huesped, si es extranjero no le cobro iva
            cursor = conexion.cursor()
            sql = f"SELECT nacionalidad FROM clientes WHERE idcliente = {idhuesped}"
            cursor.execute(sql)
            nacionalidad = cursor.fetchall()[0][0]
            conexion.commit()
            
            if nacionalidad=="Colombia":
                ivaH = 0.19
                subtotalH = []
                hospedajeModificados = []
                hospedaje_combinados = []
                for hospedaje in detallesHospedaje:
                    hospedajeLista=list(hospedaje)
                    valor = hospedajeLista[3]
                    subtotal = valor*ivaH+valor
                    subtotalH.append(subtotal)
                    hospedajeLista.append(subtotal)
                    hospedajeLista.append(ivaH)
                    hospedajeModificados.append(tuple(hospedajeLista))
                    hospedaje_combinados = list(zip(hospedajeModificados,subtotalH))
            else:
                ivaH = 0
                subtotalH = []
                hospedajeModificados = []
                hospedaje_combinados = []
                for hospedaje in detallesHospedaje:
                    hospedaje_lista=list(hospedaje)
                    valor = hospedaje_lista[3]
                    subtotal =  (valor) 
                    subtotalH.append(subtotal)
                    hospedajeModificados.append(tuple(hospedaje_lista))
                    hospedaje_combinados = list(zip(hospedajeModificados,subtotalH))
            
            #/////////CALCULO DEL TOTAL\\\\\\\\\\\
            total = 0
            #SI HAY SERVICIOS PERO NO PRODUCTOS
            if serviciosModificados and not productosModificados:
                #calcular el total de la factura
                for hospedaje in hospedaje_combinados:
                    indice2 = hospedaje[1]
                    total += indice2
                    total += sum(subtotalS)
                return render_template("facturas/nuevafactura.html",servicios=serviciosModificados,idCliente=idCliente,idFactura=idFactura,hospedaje=detallesHospedaje,fecha=fechaActual,cliente=huespedInfo,id=idhuesped,total=total)
            #SI HAY PRODUCTOS PERO NO SERVICIOS
            elif productosModificados and not serviciosModificados:
                #calcular el total de la factura
                for hospedaje in hospedaje_combinados:
                    indice2 = hospedaje[1]
                    total += indice2
                    total += sum(subtotalP)
                return render_template("facturas/nuevafactura.html",productos_combinados=productosModificados,idCliente=idCliente,idFactura=idFactura,hospedaje=hospedaje_combinados,fecha=fechaActual,cliente=huespedInfo,id=idhuesped,total=total)
            #SI HAY SERVICIOS Y PRODUCTOS
            elif serviciosModificados and productosModificados:
                for hospedaje in hospedaje_combinados:
                    indice2 = hospedaje[1]
                    total += indice2
                    total += sum(subtotalS)  
                    total += sum(subtotalP)
                return render_template("facturas/nuevafactura.html",servicios=serviciosModificados,productos_combinados=productosModificados,idCliente=idCliente,idFactura=idFactura,hospedaje=hospedaje_combinados,fecha=fechaActual,cliente=huespedInfo,id=idhuesped,total=total)
            #EN CASO DE QUE NO EXISTA UN REGISTRO DE CONSUMO DE SERVICIOS Y PRODUCTOS
            #SE HACE UN CALCULO DEL TOTAL SOLO CON EL REGISTRO DE HOSPEDAJE
            else:
                #calcular el total de la factura
                for hospedaje in hospedaje_combinados:
                    indice2 = hospedaje[1]
                    total += indice2
                    total += sum(subtotalP)
                return render_template("facturas/nuevafactura.html",idCliente=idCliente,idFactura=idFactura,hospedaje=hospedaje_combinados,fecha=fechaActual,cliente=huespedInfo,id=idhuesped,total=total)
    else:
        render_template("/facturas.html")
   
   
@prog.route("/guardafactura/<id>/<total>")
def guardafactura(id,total):
    if session.get('loginOk'):
        idhuesped = id
        # Obtén la fecha actual
        fecha_actual = date.today()
        # Formatea la fecha en el formato 'AAAA-MM-DD'
        fechaActual = fecha_actual.strftime('%Y-%m-%d')
        #Recopilar la informacion de la factura asociada al cliente
        huespedInfo = misFacturas.info_cliente(idhuesped)
        idFactura = huespedInfo[0][-1]
        idCliente = huespedInfo[0][0]
        
        #Recopilar la informacion asociada a los productos que consumio el cliente
        productosComsumidos = misFacturas.info_productos(idhuesped)
        subtotalP = []
        productosModificados = []
        #Si hay productos consumidos se les cobra un iva del 19%
        #En caso de que no se encuentren productos no se realiza el proceso
        if productosComsumidos:
            ivaP = 0.19
            for producto in productosComsumidos:
                producto_lista = list(producto)
                cantidad = producto[2]
                valor = producto[3]
                subtotal = cantidad * valor * ivaP + valor
                producto_lista.append(subtotal)
                subtotalP.append(subtotal)
                producto_lista.append(ivaP)
                productosModificados.append(producto_lista)
            
        #Recopilar la informacion asociada a los servicios que consumio el cliente
        serviciosConsumidos = misFacturas.info_servicios(idhuesped)
        subtotalS = 0
        serviciosModificados = []
        subtotalS = []
        #Si hay servicios consumidos se les cobra un iva del 19%
        #En caso de que no se encuentren servicios no se realiza el proceso
        if serviciosConsumidos:
            ivaS = 0.19
            for servicio in serviciosConsumidos:
                servicio_lista=list(servicio)
                servicio_lista.append(ivaS)
                valor = servicio_lista[3]
                subtotal = valor*ivaS+valor
                servicio_lista.append(subtotal)
                subtotalS.append(subtotal)
                serviciosModificados.append(tuple(servicio_lista))
            
        #Recopilar informacion del hospedaje del huesped
        detallesHospedaje = misFacturas.info_hospedaje(idhuesped)
        #consulto la nacionalidad del huesped, si es extranjero no le cobro iva
        cursor = conexion.cursor()
        sql = f"SELECT nacionalidad FROM clientes WHERE idcliente = {idhuesped}"
        cursor.execute(sql)
        nacionalidad = cursor.fetchall()[0][0]
        conexion.commit()
        if nacionalidad=="Colombia":
            ivaH = 0.19
            subtotalH = []
            hospedajeModificados = []
            hospedaje_combinados = []
            for hospedaje in detallesHospedaje:
                hospedaje_lista=list(hospedaje)
                valor = hospedaje_lista[3]
                subtotal = valor*ivaH+valor
                subtotalH.append(subtotal)
                hospedaje_lista.append(subtotal)
                hospedaje_lista.append(ivaH)
                hospedajeModificados.append(tuple(hospedaje_lista))
                hospedaje_combinados = list(zip(hospedajeModificados,subtotalH))
        else:
            ivaH = 0
            subtotalH = []
            hospedajeModificados = []
            hospedaje_combinados = []
            for hospedaje in detallesHospedaje:
                hospedaje_lista=list(hospedaje)
                valor = hospedaje_lista[3]
                subtotal =  (valor) 
                subtotalH.append(subtotal)
                hospedajeModificados.append(tuple(hospedaje_lista))
                hospedaje_combinados = list(zip(hospedajeModificados,subtotalH))
            
                
        #EL TOTAL ME LLEGA COMO ARGUMENTO DE LA FUNCION
        #POR LO TANTO NO DEBO DE CALCULARLO NUEVAMENTE
        
        #Generar pdf
        with open('__pycache__/temp.html', 'w', encoding='utf-8') as temp_file:
                temp_file.write(render_template("facturas/nuevafactura.html",servicios=serviciosModificados,productos_combinados=productosModificados,idCliente=idCliente,idFactura=idFactura,hospedaje=hospedaje_combinados,fecha=fechaActual,cliente=huespedInfo,id=idhuesped,total=total))
        #PIP INSTALL PDFKIT, Y SE DEBE DE IMPORTAR
        #ADICIONALMENTE SE DEBE DE INSTALLAR UN SOFTWARE EXTERNO: WKHTMLTOPDF
        pdfkit.from_file('__pycache__/temp.html',f'pdffactura/{idFactura}.pdf',options={"enable-local-file-access": None})
        
        #SE GUARDAN LOS DATOS DE LA FACTURA
        #se necesita consultar el idComanda
        idcomanda = misFacturas.buscar_id_comanda(idhuesped)
        factura = [idhuesped,total,idcomanda]
        misFacturas.guardar(factura,fechaActual,idCliente,idFactura)
            
        session['msg1'] = '¡La factura se guardó exitosamente! y adicionalmente se genero un pdf en la carpeta pdf-factura.'
        return redirect("/facturas?msg1=¡La factura se guardó exitosamente! y adicionalmente se genero un pdf en la carpeta pdf-factura.")
    else:
        return redirect('/')


@prog.route("/borrafactura/<id>")
def borrafactura(id):
    if session.get('loginOk'):
        misFacturas.borrar(id)
        return redirect("/facturas")
    else:
        return redirect('/') 
    
@prog.route("/verfactura/<id>")
def verfactura(id):
    if session.get('loginOk'):
        session['msg1'] = 'La factura se abrio en una nueva ventana'
        #SE DEBE CREAR UNA CARPETA LLAMADA PDFFACTURA AL MISMO NIVEL DE PRINCIPAL
        ruta_pdf = f'D:/User/Escritorio/FACTURAS_FINAL/pdffactura/{id}.pdf'
        #import webbrowser as vb ASI SE IMPORTA LA LIBRERIA
        # ESTA SE USA EN LA LINEA DE ABAJO PARA ABRIR EL PDF DE LA FACTURA
        vb.open_new(ruta_pdf); return redirect("/facturas?msg1=La factura se abrió en una nueva ventana")     
    else:
        return redirect('/')
    

# ////////////////// FIN FACTURAS ANDRES FELIPE\\\\\\\\\\\\\\\\\\\\\


    
# Este codigo hace parte de la libreria de Flask para crear el servidor local    
    
if __name__ == '__main__':
    prog.run(host='0.0.0.0',debug=True,port='8085')
