from os import name
import re
from flask import Flask, render_template, request, redirect, sessions, url_for, session
from flask.helpers import flash
from flask.wrappers import Request
from flask_mysqldb import MySQL,MySQLdb
import bcrypt, random

app = Flask(__name__)

app.secret_key="appFinal"

app.config['MYSQL_HOST'] = 'us-cdbr-east-04.cleardb.com'
app.config['MYSQL_USER'] = 'bd7f0fefac4285'
app.config['MYSQL_PASSWORD'] = '984020b1'
app.config['MYSQL_DB'] = 'heroku_1d59773a4d84e39'

mysql = MySQL(app)

semilla = bcrypt.gensalt()

@app.route('/')
def main():
    if 'admin' in session:
        return render_template('admin.html')
    else:
        if 'nombre' in session:
            return render_template('inicio.html')
        else:
            return render_template('ingresar.html')
            

@app.route('/regresar')
def regresar():
  return render_template('inicio.html') 

@app.route('/inicio', methods = ["GET", "POST"])
def inicio():
    if 'admin' in session:
        return render_template('admin.html')
    else:
        if 'nombre' in session:
            return render_template('inicio.html')
        else:
            return render_template('ingresar.html')



@app.route('/registro')
def enviarRegistro():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM identificacion')
    data = cur.fetchall()
    return render_template("registro.html", identificaciones = data)

@app.route('/registrar', methods = ["GET", "POST"])
def registrar():
    if (request.method == 'GET'):
        if 'admin' in session:
          return render_template('admin.html')
        elif 'nombre' in sessions:
          return render_template('inicio.html')
        else:
          cur = mysql.connection.cursor()
          cur.execute('SELECT * FROM identificacion')
          data = cur.fetchall()
          print(data)
          return render_template('ingresar.html', identificaciones = data)
    else:
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        userName = request.form['userName']
        id_rol = "1"

        id_identificacion = request.form['id_identificacion']
        cur = mysql.connection.cursor()
        sQuery = "SELECT id_identificacion, tipo FROM identificacion WHERE id_identificacion = %s"
        cur.execute(sQuery, [id_identificacion])
        usuarios = cur.fetchone()
        session['id_identificacion'] = usuarios[0]
        id_identification = session['id_identificacion']

        sQuery = "SELECT userName FROM usuarios"
        cur = mysql.connection.cursor()
        cur.execute(sQuery)
        userNames = cur.fetchall()
        print(userNames)
      
      
        identificacion = request.form['identificacion']
        fecha_nacimiento = request.form['fecha_nacimiento']
        correo = request.form['correo']
        contraseña = request.form['password']
        password_encode = contraseña.encode("utf-8")
        password_encriptado = bcrypt.hashpw(password_encode, semilla)
        estado = "Activo"
        print("Insertado")
        print("password_encode",password_encode)
        print("password_encriptado",password_encriptado)


        sQuery = "INSERT into usuarios (id_rol, nombre, apellido, id_identificacion, identificacion, fecha_nacimiento, contrasena ,userName,correo,estado) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

        cur = mysql.connection.cursor()
        cur.execute(sQuery,(id_rol,nombre,apellido,id_identification,identificacion,fecha_nacimiento,password_encriptado,userName,correo,estado))
        mysql.connection.commit()
        cur.close()



        if (id_rol == "1"):
            session['nombre'] = nombre
            session['correo'] = correo
            return render_template("inicio.html")
        else:
            session['admin'] = nombre
            return render_template("admin.html")



    
@app.route('/ingresar', methods = ["GET", "POST"])
def ingresar():
    if (request.method == 'GET'):
        if 'admin' in session:
          return render_template('admin.html')
        elif 'nombre' in sessions:
          return render_template('inicio.html')
        else:
          return render_template('ingresar.html')
    else:
        correo = request.form['correo']
        password = request.form['password']
        password_encode = password.encode("utf-8")

        cur = mysql.connection.cursor()
        sQuery = "SELECT correo, contrasena, id_rol FROM usuarios WHERE correo = %s"
        cur.execute(sQuery, [correo])
        usuarios = cur.fetchone()
        print(usuarios)
        cur.close()

        if(usuarios != None):
            password_encriptado_encode = usuarios[1].encode()
            print(password_encriptado_encode)

            if(bcrypt.checkpw(password_encode, password_encriptado_encode)):

                session['id_rol'] = usuarios[2]
                session['correo'] = usuarios[0]

                variable = session['id_rol']
                print(variable)

                if variable == 2:
                  print("Admin")
                  return render_template("admin.html")
                else:
                  print("User")
                  return render_template("inicio.html")

            else:
                print("incorrecto")
                flash("el password no es correcto", "alert-warning")
                return render_template("ingresar.html")
        else:
            print("incorrecto2")
            flash("El coreero no existe", "alert-warning")
            return render_template("ingresar.html")

@app.route('/salir')
def salir():
    session.clear()
    return render_template("ingresar.html")



"""

Registro mascota

"""

@app.route('/mascota')
def enviarMascota():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM usuarios')
    data3 = cur.fetchall()
    

    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM raza')
    data2 = cur.fetchall()
    

    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM color')
    data1 = cur.fetchall()
   


    return render_template('registroMascota.html', usuarios = data3, razas = data2, colores = data1)

@app.route('/registrarMascota', methods = ["GET", "POST"])
def registrarMascota():

    if (request.method == 'GET'):
        if 'admin' in session:
          return render_template('admin.html')
        elif 'nombre' in sessions:
          return render_template('inicio.html')
        else:
          return render_template('ingresar.html')
    else:

        
        nombre = request.form['nombre']
        print(nombre)

        id_usuario2 = request.form['nombre_usuario']
        cur = mysql.connection.cursor()
        sQuery = "SELECT id_usuario, nombre FROM usuarios WHERE id_usuario = %s"
        cur.execute(sQuery, [id_usuario2])
        usuarios2 = cur.fetchone()
        session['id_usuario'] = usuarios2[0]
        id_usuario = session['id_usuario']

        id_raza = request.form['id_raza']
        cur = mysql.connection.cursor()
        sQuery = "SELECT id_raza, raza FROM raza WHERE id_raza = %s"
        cur.execute(sQuery, [id_raza])
        usuarios1 = cur.fetchone()
        session['id_raza'] = usuarios1[0]
        id_usuario = session['id_raza']
        
        
  
        id_color = request.form['id_color']
        cur = mysql.connection.cursor()
        sQuery = "SELECT id_color, nombre FROM color WHERE id_color = %s"
        cur.execute(sQuery, [id_color])
        usuarios1 = cur.fetchone()
        session['id_color'] = usuarios1[0]
        id_usuario = session['id_color']
       
  

        descripcion = request.form['descripcion']
        fehca_nacimiento = request.form['fehca_nacimiento']
        estado = "Activo"

        sQuery = "INSERT into mascotas (id_usuario, id_raza, id_color, fehca_nacimiento, nombre, descripcion, estado) VALUES (%s,%s,%s,%s,%s,%s,%s)"

        cur = mysql.connection.cursor()
        cur.execute(sQuery,(id_usuario2 , id_raza, id_color, fehca_nacimiento, nombre, descripcion, estado))
        mysql.connection.commit()
        


        return render_template("inicio.html")




@app.route('/enviarMascota', methods = ["GET", "POST"])
def enviarTablas():
    return render_template('mostrarTablas.html')


"""

Registrar servicio

"""        

@app.route('/servicio')
def enviarServicio():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM mascotas')
    data3 = cur.fetchall()
 

    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM doctor')
    data2 = cur.fetchall()
    

    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM tiposervicio')
    data1 = cur.fetchall()
    

    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM formapago')
    data4 = cur.fetchall()
    


    return render_template('servicio.html', mascotas = data3, doctores = data2, tiposervicios = data1, pagos = data4)

@app.route('/registrarServicio', methods = ["GET", "POST"])
def registrarServicio():

    if (request.method == 'GET'):
        if 'admin' in session:
          return render_template('admin.html')
        elif 'nombre' in sessions:
          return render_template('inicio.html')
        else:
          return render_template('ingresar.html')
    else:

        id_mascota = request.form['id_mascota']
        cur = mysql.connection.cursor()
        sQuery = "SELECT id_mascota, nombre FROM mascotas WHERE id_mascota = %s"
        cur.execute(sQuery, [id_mascota])
        usuarios = cur.fetchone()
        session['id_mascota'] = usuarios[0]
        id_mascota = session['id_mascota']
       

        id_doctor = request.form['id_doctor']
        cur = mysql.connection.cursor()
        sQuery = "SELECT id_doctor, nombre FROM doctor WHERE id_doctor = %s"
        cur.execute(sQuery, [id_doctor])
        usuarios = cur.fetchone()
        session['id_doctor'] = usuarios[0]
        id_doctor = session['id_doctor']
      

        id_tipoServicio = request.form['id_tipo_servicio']
        cur = mysql.connection.cursor()
        sQuery = "SELECT id_tipoServicio, servicio FROM tiposervicio WHERE id_tipoServicio = %s"
        cur.execute(sQuery, [id_tipoServicio])
        usuarios = cur.fetchone()
        session['id_tipoServicio'] = usuarios[0]
        id_tipoServicio = session['id_tipoServicio']
      

        Descripcion = request.form['comentario']
        fecha = request.form['fecha']
        costo = request.form['costo']

        
       
        Estado = "Activo"

        sQuery = "INSERT into servicios (id_tipoServicio, Descripcion, costo, Estado, id_mascotas,fecha, id_doctor) VALUES (%s,%s,%s,%s,%s,%s,%s)"

        cur = mysql.connection.cursor()
        cur.execute(sQuery,(id_tipoServicio, Descripcion, costo, Estado, id_mascota, fecha, id_doctor))
        mysql.connection.commit()
        cur.close()

        return render_template("inicio.html")


"""

Registrar factura

"""

@app.route('/enviarFactura')
def enviarFactura():

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM formapago")
    data = cur.fetchall()

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM mascotas")
    data2 = cur.fetchall()

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM doctor")
    data3 = cur.fetchall()
  
  


    return render_template('registroFactura.html', pagos = data, mascotas = data2, doctores = data3 )

@app.route('/registrarFactura', methods = ["GET", "POST"])
def registrarFactura():

    if (request.method == 'GET'):
        if 'admin' in session:
          return render_template('admin.html')
        elif 'nombre' in sessions:
          return render_template('inicio.html')
        else:
          return render_template('ingresar.html')
    else:
        id_mascota = request.form['id_mascota']
        cur = mysql.connection.cursor()
        sQuery = "SELECT id_mascota, nombre FROM mascotas WHERE id_mascota = %s"
        cur.execute(sQuery, [id_mascota])
        usuarios = cur.fetchone()
        session['id_mascota'] = usuarios[0]
        id_mascota = session['id_mascota']
      
        id_doctor = request.form['id_doctor']
        cur = mysql.connection.cursor()
        sQuery = "SELECT id_doctor, nombre FROM doctor WHERE id_doctor = %s"
        cur.execute(sQuery, [id_doctor])
        usuarios = cur.fetchone()
        session['id_doctor'] = usuarios[0]
        id_doctor = session['id_doctor']
      
        id_pago = request.form['id_pago']
        cur = mysql.connection.cursor()
        sQuery = "SELECT id_pago, Nombre FROM formapago WHERE id_pago = %s"
        cur.execute(sQuery, [id_pago])
        usuarios = cur.fetchone()
        session['id_pago'] = usuarios[0]
        id_pago = session['id_pago']
       

        Estado = "Activo"
        Numero_Factura = random.randrange(10000)
        fecha_generada = request.form['fecha']


        sQuery = "INSERT into factura (Numero_Factura, Fecha_generacion, Forma_pago, Estado, id_doctor, id_mascota) VALUES (%s,%s,%s,%s,%s,%s)"

        cur = mysql.connection.cursor()
        cur.execute(sQuery,(Numero_Factura, fecha_generada ,id_pago, Estado, id_doctor, id_mascota))
        mysql.connection.commit()
        cur.close()

        return render_template("inicio.html")
          






"""

Admin

"""  


@app.route('/formaPago', methods = ["GET", "POST"])
def formaPago():
  if (request.method == 'GET'):
        if 'admin' in session:
          return render_template('admin.html')
        elif 'nombre' in sessions:
          return render_template('inicio.html')
        else:
          return render_template('ingresar.html')
  else:
      nombre = request.form["nombre"]
      Estado = "Activo"

      sQuery = "INSERT into formapago (Nombre, estado) VALUES (%s,%s)"

      cur = mysql.connection.cursor()
      cur.execute(sQuery,(nombre, Estado))
      mysql.connection.commit()
      cur.close()

      return render_template("admin.html")
   



@app.route('/enviarAdmin', methods = ["GET", "POST"])
def enviarUsuarioAdmin():
  cur = mysql.connection.cursor()
  cur.execute("SELECT * FROM identificacion")
  data = cur.fetchall()
 

  cur = mysql.connection.cursor()
  cur.execute("SELECT * FROM rol")
  data2 = cur.fetchall()


  return render_template("registroAdmin.html", identificaciones = data, rols = data2)
    



@app.route('/registroAdmin', methods = ["GET", "POST"])
def registroUsuarioAdmin():
    if (request.method == 'GET'):
      if 'admin' in session:
        return render_template('admin.html')
      elif 'nombre' in sessions:
        return render_template('inicio.html')
      else:
        return render_template('ingresar.html')
    else:
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        userName = request.form['userName']

        id_rol = request.form['rol']
        cur = mysql.connection.cursor()
        sQuery = "SELECT id_rol , rol FROM rol WHERE id_rol = %s"
        cur.execute(sQuery, [id_rol])
        usuarios = cur.fetchone()
        session['id_rol'] = usuarios[0]
        id_rol = session['id_rol']
       
        id_identificacion = request.form['id_identificacion']
        cur = mysql.connection.cursor()
        sQuery = "SELECT id_identificacion, tipo FROM identificacion WHERE id_identificacion = %s"
        cur.execute(sQuery, [id_identificacion])
        usuarios = cur.fetchone()
        session['id_identificacion'] = usuarios[0]
        id_identification = session['id_identificacion']
        

        sQuery = "SELECT userName FROM usuarios"
        cur = mysql.connection.cursor()
        cur.execute(sQuery)
        userNames = cur.fetchall()
     
      
        identificacion = request.form['identificacion']
        fecha_nacimiento = request.form['fecha_nacimiento']
        correo = request.form['correo']
        contraseña = request.form['password']
        password_encode = contraseña.encode("utf-8")
        password_encriptado = bcrypt.hashpw(password_encode, semilla)
        estado = "Activo"
        print("Insertado")
        print("password_encode",password_encode)
        print("password_encriptado",password_encriptado)


        sQuery = "INSERT into usuarios (id_rol, nombre, apellido, id_identificacion, identificacion, fecha_nacimiento, contrasena ,userName,correo,estado) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

        cur = mysql.connection.cursor()
        cur.execute(sQuery,(id_rol,nombre,apellido,id_identification,identificacion,fecha_nacimiento,password_encriptado,userName,correo,estado))
        mysql.connection.commit()
        cur.close()

        if (id_rol == "1"):
            session['nombre'] = nombre
            session['correo'] = correo
            return render_template("inicio.html")
        else:
            session['admin'] = nombre
            return render_template("admin.html")




@app.route('/tipoDoctor', methods = ["GET", "POST"])
def registrarDoctor():
    if (request.method == 'GET'):
        if 'admin' in session:
          return render_template('admin.html')
        elif 'nombre' in sessions:
          return render_template('inicio.html')
        else:
          return render_template('ingresar.html')
    else:
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        area_especialidad = request.form['area_especialidad']
        descripcion = request.form['descripcion']
        estado = "Activo"

        sQuery = "INSERT into doctor (nombre,apellido, area_especialidad,descripcion, estado) VALUES (%s,%s,%s,%s,%s)"

        cur = mysql.connection.cursor()
        cur.execute(sQuery,(nombre,apellido, area_especialidad,descripcion,estado))
        mysql.connection.commit()
        cur.close()

        return render_template("admin.html")


"""

Inactivo

"""



@app.route('/eliminarRol/<id>', methods = ['POST'])
def eliminarRol(id):
  if (request.method == 'GET'):
        if 'admin' in session:
          return render_template('admin.html')
        elif 'nombre' in sessions:
          return render_template('inicio.html')
        else:
          return render_template('ingresar.html')
  else:
    ESTADO = "Inactivo"
    cur = mysql.connection.cursor()
    cur.execute("""
      UPDATE rol
      SET estado = %s
      WHERE id_rol = %s
    """ , (ESTADO, id))
    mysql.connection.commit()
    cur.close()

@app.route('/eliminarUsuario/<id>', methods = ['POST'])
def eliminarUsuario(id):
  if (request.method == 'GET'):
        if 'admin' in session:
          return render_template('admin.html')
        elif 'nombre' in sessions:
          return render_template('inicio.html')
        else:
          return render_template('ingresar.html')
  else:
    ESTADO = "Inactivo"
    cur = mysql.connection.cursor()
    cur.execute("""
      UPDATE usuarios
      SET estado = %s
      WHERE id_usuarios = %s
    """ , (ESTADO, id))
    mysql.connection.commit()
    cur.close()



@app.route('/eliminarServicio/<id>', methods = ['POST'])
def eliminarServicio(id):
  if (request.method == 'GET'):
        if 'admin' in session:
          return render_template('admin.html')
        elif 'nombre' in sessions:
          return render_template('inicio.html')
        else:
          return render_template('ingresar.html')
  else:
    ESTADO = "Inactivo"
    cur = mysql.connection.cursor()
    cur.execute("""
      UPDATE tiposervicio
      SET estado = %s
      WHERE id_tipoServicio = %s
    """ , (ESTADO, id))
    mysql.connection.commit()
    cur.close()

@app.route('/eliminarDoctor/<id>', methods = ['POST'])
def eliminarDoctor(id):
  if (request.method == 'GET'):
        if 'admin' in session:
          return render_template('admin.html')
        elif 'nombre' in sessions:
          return render_template('inicio.html')
        else:
          return render_template('ingresar.html')
  else:
    ESTADO = "Inactivo"
    cur = mysql.connection.cursor()
    cur.execute("""
      UPDATE doctor
      SET estado = %s
      WHERE id_doctor = %s
    """ , (ESTADO, id))
    mysql.connection.commit()
    cur.close()
    
    
    return render_template("admin.html")

@app.route('/eliminarRaza/<id>', methods = ['POST'])
def eliminarRaza(id):
  if (request.method == 'GET'):
        if 'admin' in session:
          return render_template('admin.html')
        elif 'nombre' in sessions:
          return render_template('inicio.html')
        else:
          return render_template('ingresar.html')
  else:
    ESTADO = "Inactivo"
    cur = mysql.connection.cursor()
    cur.execute("""
      UPDATE raza
      SET estado = %s
      WHERE id_raza = %s
    """ , (ESTADO, id))
    mysql.connection.commit()
    cur.close()
    
    
    return render_template("admin.html")

@app.route('/eliminarMascota/<id>', methods = ['POST'])
def eliminarMascota(id):
  if (request.method == 'GET'):
        if 'admin' in session:
          return render_template('admin.html')
        elif 'nombre' in sessions:
          return render_template('inicio.html')
        else:
          return render_template('ingresar.html')
  else:
    ESTADO = "Inactivo"
    cur = mysql.connection.cursor()
    cur.execute("""
      UPDATE mascotas
      SET estado = %s
      WHERE id_mascota = %s
    """ , (ESTADO, id))
    mysql.connection.commit()
    cur.close()
    
    
    return render_template("admin.html")   

@app.route('/eliminarColor/<id>', methods = ['POST'])
def eliminarColor(id):
  if (request.method == 'GET'):
        if 'admin' in session:
          return render_template('admin.html')
        elif 'nombre' in sessions:
          return render_template('inicio.html')
        else:
          return render_template('ingresar.html')
  else:
    ESTADO = "Inactivo"
    cur = mysql.connection.cursor()
    cur.execute("""
      UPDATE color
      SET estado = %s
      WHERE id_color = %s
    """ , (ESTADO, id))
    mysql.connection.commit()
    cur.close()
    
    
    return render_template("admin.html")  

@app.route('/eliminarPago/<id>', methods = ['POST'])
def eliminarPago(id):
  if (request.method == 'GET'):
        if 'admin' in session:
          return render_template('admin.html')
        elif 'nombre' in sessions:
          return render_template('inicio.html')
        else:
          return render_template('ingresar.html')
  else:
    ESTADO = "Inactivo"
    cur = mysql.connection.cursor()
    cur.execute("""
      UPDATE formapago
      SET estado = %s
      WHERE id_pago = %s
    """ , (ESTADO, id))
    mysql.connection.commit()
    cur.close()
    
    
    return render_template("admin.html")   


"""

Activar 

"""


@app.route('/activarUusario/<id>', methods = ['POST'])
def activarUusario(id):
  if (request.method == 'GET'):
        if 'admin' in session:
          return render_template('admin.html')
        elif 'nombre' in sessions:
          return render_template('inicio.html')
        else:
          return render_template('ingresar.html')
  else:
    ESTADO = "Activo"
    cur = mysql.connection.cursor()
    cur.execute("""
      UPDATE usuarios
      SET estado = %s
      WHERE id_usuarios = %s
    """ , (ESTADO, id))
    mysql.connection.commit()
    cur.close()

    return render_template("admin.html")

@app.route('/activarRol/<id>', methods = ['POST'])
def activarRol(id):
  if (request.method == 'GET'):
        if 'admin' in session:
          return render_template('admin.html')
        elif 'nombre' in sessions:
          return render_template('inicio.html')
        else:
          return render_template('ingresar.html')
  else:
    ESTADO = "Activo"
    cur = mysql.connection.cursor()
    cur.execute("""
      UPDATE rol
      SET estado = %s
      WHERE id_rol = %s
    """ , (ESTADO, id))
    mysql.connection.commit()
    cur.close()

    return render_template("admin.html")

@app.route('/activarServicio/<id>', methods = ['POST'])
def activarServicio(id):
  if (request.method == 'GET'):
        if 'admin' in session:
          return render_template('admin.html')
        elif 'nombre' in sessions:
          return render_template('inicio.html')
        else:
          return render_template('ingresar.html')
  else:
    ESTADO = "Activo"
    cur = mysql.connection.cursor()
    cur.execute("""
      UPDATE tiposervicio
      SET estado = %s
      WHERE id_tipoServicio = %s
    """ , (ESTADO, id))
    mysql.connection.commit()
    cur.close()

    return render_template("admin.html")


@app.route('/activarPago/<id>', methods = ['POST'])
def activarPago(id):
  if (request.method == 'GET'):
        if 'admin' in session:
          return render_template('admin.html')
        elif 'nombre' in sessions:
          return render_template('inicio.html')
        else:
          return render_template('ingresar.html')
  else:
    ESTADO = "Activo"
    cur = mysql.connection.cursor()
    cur.execute("""
      UPDATE formapago
      SET estado = %s
      WHERE id_pago = %s
    """ , (ESTADO, id))
    mysql.connection.commit()
    cur.close()

    return render_template("admin.html")


@app.route('/activarColor/<id>', methods = ['POST'])
def activarColor(id):
  if (request.method == 'GET'):
        if 'admin' in session:
          return render_template('admin.html')
        elif 'nombre' in sessions:
          return render_template('inicio.html')
        else:
          return render_template('ingresar.html')
  else:
    ESTADO = "Activo"
    cur = mysql.connection.cursor()
    cur.execute("""
      UPDATE color
      SET estado = %s
      WHERE id_color = %s
    """ , (ESTADO, id))
    mysql.connection.commit()
    cur.close()
    
    
    return render_template("admin.html")  


@app.route('/activarDoctor/<id>', methods = ['POST'])
def activarDoctor(id):
  if (request.method == 'GET'):
        if 'admin' in session:
          return render_template('admin.html')
        elif 'nombre' in sessions:
          return render_template('inicio.html')
        else:
          return render_template('ingresar.html')
  else:
    ESTADO = "Activo"
    cur = mysql.connection.cursor()
    cur.execute("""
      UPDATE doctor
      SET estado = %s
      WHERE id_doctor = %s
    """ , (ESTADO, id))
    mysql.connection.commit()
    cur.close()
    
    
    return render_template("admin.html")

@app.route('/activarRaza/<id>', methods = ['POST'])
def activarRaza(id):
  if (request.method == 'GET'):
        if 'admin' in session:
          return render_template('admin.html')
        elif 'nombre' in sessions:
          return render_template('inicio.html')
        else:
          return render_template('ingresar.html')
  else:
    ESTADO = "Activo"
    cur = mysql.connection.cursor()
    cur.execute("""
      UPDATE raza
      SET estado = %s
      WHERE id_raza = %s
    """ , (ESTADO, id))
    mysql.connection.commit()
    cur.close()
    
    return render_template("admin.html")

@app.route('/activarMascota/<id>', methods = ['POST'])
def activarMascota(id):
  if (request.method == 'GET'):
        if 'admin' in session:
          return render_template('admin.html')
        elif 'nombre' in sessions:
          return render_template('inicio.html')
        else:
          return render_template('ingresar.html')
  else:
    ESTADO = "Activo"
    cur = mysql.connection.cursor()
    cur.execute("""
      UPDATE mascotas
      SET estado = %s
      WHERE id_mascota = %s
    """ , (ESTADO, id))
    mysql.connection.commit()
    cur.close()
    
    return render_template("admin.html")  







      

@app.route('/enviarTablaMascota')
def enviarTablaMascota():
    return render_template('mostrarTablas.html')
    


@app.route('/tipoServicio', methods = ["GET", "POST"])
def tipoServicio():
    if (request.method == 'GET'):
        if 'admin' in session:
          return render_template('admin.html')
        elif 'nombre' in sessions:
          return render_template('inicio.html')
        else:
          return render_template('ingresar.html')
    else:
        servicio = request.form['servicio']
        descripcion = request.form['descripcion']
     

        sQuery = "INSERT into tiposervicio (servicio,descripcion) VALUES (%s,%s)"

        cur = mysql.connection.cursor()
        cur.execute(sQuery,(servicio,descripcion))
        mysql.connection.commit()
        cur.close()

        return render_template("admin.html")

@app.route('/tipoColor', methods = ["GET", "POST"])
def tipoColor():
    if (request.method == 'GET'):
        if 'admin' in session:
          return render_template('admin.html')
        elif 'nombre' in sessions:
          return render_template('inicio.html')
        else:
          return render_template('ingresar.html')
    else:
        nombre = request.form['nombre']
        estado = "Activo"
        cur = mysql.connection.cursor()
        cur.execute("INSERT into color (nombre, estado) VALUES (%s,%s)", (nombre,estado))
        mysql.connection.commit()
        cur.close()

        return render_template("admin.html")

@app.route('/tipoRaza', methods = ["GET", "POST"])
def registrarRaza():
    if (request.method == 'GET'):
        if 'admin' in session:
          return render_template('admin.html')
        elif 'nombre' in sessions:
          return render_template('inicio.html')
        else:
          return render_template('ingresar.html')
    else:
        raza = request.form['raza']
        tamano = request.form['tamano']
        especie = request.form['especie']


        sQuery = "INSERT into raza (raza,tamano, especie) VALUES (%s,%s,%s)"

        cur = mysql.connection.cursor()
        cur.execute(sQuery,(raza,tamano, especie))
        mysql.connection.commit()
        cur.close()

        return render_template("admin.html")

@app.route('/tablaInfo')
def tabla():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM raza')
    data = cur.fetchall()


    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM doctor')
    data2 = cur.fetchall()
    

    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM identificacion')
    data3 = cur.fetchall()
 

    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM mascotas')
    data4 = cur.fetchall()
 

    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM color')
    data5 = cur.fetchall()


    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM formapago')
    data6 = cur.fetchall()
  

    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM tiposervicio')
    data7 = cur.fetchall()

    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM usuarios')
    data8 = cur.fetchall()

    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM rol')
    data9 = cur.fetchall()
   
    return render_template('tableInfo.html', razas = data, doctors = data2, identificacions = data3, mascotas = data4 , colores = data5, pagos = data6, servicios = data7, usuarios = data8, rols = data9)

    

if __name__ == '__main__':
    app.run(debug=True)