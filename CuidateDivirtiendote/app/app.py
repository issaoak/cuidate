from flask import Flask, request, jsonify, render_template, url_for, redirect, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
import mysql.connector
from mysql.connector import Error
import pyscrypt
import os
from models.ModelUser import ModelUser
from utils import check_password_hash_scrypt 


app = Flask(__name__)
app.config['MYSQL_HOST'] = 'db'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'cuidatedivirtiendote'
app.config['MYSQL_PORT'] = 3306  # Asegúrate de que este valor sea un entero, no una cadena


app.secret_key = 'my_secret'

login_manager_app = LoginManager(app)

# Generar un hash de contraseña usando pyscrypt
def generate_password_hash_scrypt(password):
    salt = os.urandom(16)
    hashed_password = pyscrypt.hash(password.encode('utf-8'), salt, N=1024, r=8, p=1, dkLen=32)
    return salt + hashed_password  # Combinamos salt y hash

# Verificar el hash de la contraseña
def check_password_hash_scrypt(stored_password, provided_password):
    salt = stored_password[:16]
    stored_hash = stored_password[16:]
    provided_hash = pyscrypt.hash(provided_password.encode('utf-8'), salt, N=1024, r=8, p=1, dkLen=32)
    return stored_hash == provided_hash

@login_manager_app.user_loader
def load_user(ID_usuario):
    conn = get_db_connection()  # Importación aquí para evitar el problema de circularidad
    return ModelUser.get_by_id(conn, ID_usuario)

def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host=app.config['MYSQL_HOST'],
            user=app.config['MYSQL_USER'],
            password=app.config['MYSQL_PASSWORD'],
            database=app.config['MYSQL_DB']
        )
        if conn.is_connected():
            print("Conexión exitosa a la base de datos")
            return conn
    except Error as e:
        print(f"Error al conectar a la base de datos: {e}")
        flash(f"Error al conectar a la base de datos: {e}", 'danger')
        return None

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        print("Email from form:", email)  # Debugging
        print("Password from form:", password)  # Debugging
        
        from models.entities.User import User  # Importación aquí para evitar el problema de circularidad
        user = User(0, email, password)
        conn = get_db_connection()
        if conn:
            with conn:
                from models.ModelUser import ModelUser  # Importación aquí para evitar el problema de circularidad
                logged_user = ModelUser.login(conn, user)
        
                if logged_user is not None:
                    if check_password_hash_scrypt(logged_user.Contraseña, password):
                        login_user(logged_user)
                        if logged_user.Rol == 'admin':
                            return redirect(url_for('menuAdmin'))
                        elif logged_user.Rol == 'userp':
                            return redirect(url_for('vista'))
                        else:
                            return redirect(url_for('principalgratis'))
                    else:
                        flash('Contraseña incorrecta', 'danger')
                        return redirect(url_for('login'))
                else:
                    flash('Correo electrónico no encontrado', 'danger')
                    return redirect(url_for('login'))
        else:
            flash('No se pudo conectar a la base de datos', 'danger')
            return redirect(url_for('login'))
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.errorhandler(404)
def paginano(e):
    return 'Revisar tu sintaxis: No encontré nada'

@app.errorhandler(401)
def noautorizado(e):
    return redirect(url_for('login'))

@app.route('/pruebaConexion')
def pruebaConexion():
    conn = get_db_connection()
    if conn:
        try:
            with conn:
                cursor = conn.cursor()
                cursor.execute("SELECT 1")
                datos = cursor.fetchone()
            return jsonify({'status': 'conexion exitosa', 'data': datos})
        except Exception as ex:
            return jsonify({'status': 'Error de conexion', 'mensaje': str(ex)})
    else:
        return jsonify({'status': 'Error de conexion', 'mensaje': 'No se pudo establecer conexión con la base de datos'})

@app.route('/menuUsuario')
@login_required
def menuUsuario():
    return render_template('menu_Usuarios.html')

@app.route('/')
def index():
    return render_template('menu_general.html')

@app.route('/registrox')
def registrox():
    return render_template('resgistrox.html')

@app.route('/menuAdmin')
@login_required
def menuAdmin():
    return render_template('index.html')

@app.route('/blog')
@login_required
def blog():
    return render_template('blog.html')

@app.route('/ayuda')
@login_required
def ayuda():
    return render_template('Ayuda.html')

@app.route('/plantilla')
@login_required
def plantilla():
    return render_template('plantilla.html')

@app.route('/registro')
@login_required
def registro():
    return render_template('registro_usuario.html')

@app.route('/dietasR')
@login_required
def dietasR():
    return render_template('dietasR.html')

@app.route('/ejercicioR')
@login_required
def ejercicioR():
    return render_template('ejerciciosR.html')

@app.route('/verDietas')
@login_required
def verDietas():
    conn = get_db_connection()
    if conn:
        try:
            with conn:
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM dieta')
                consultaD = cursor.fetchall()
                print(consultaD)
            return render_template('consulta_dietas.html', dietas=consultaD)
        except Exception as e:
            print(e)
            return 'Error al consultar dietas'
    else:
        return 'Error al conectar a la base de datos'

@app.route('/verEjercicios')
@login_required
def verEjercicios():
    conn = get_db_connection()
    if conn:
        try:
            with conn:
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM ejercicios')
                consultaE = cursor.fetchall()
                print(consultaE)
            return render_template('consulta_ejercicios.html', ejercicios=consultaE)
        except Exception as e:
            print(e)
            return 'Error al consultar ejercicios'
    else:
        return 'Error al conectar a la base de datos'

@app.route('/GuardarDieta', methods=['POST'])
def GuardarDieta():
    if request.method == 'POST':
        try:
            Fnombre = request.form['dietName']
            Fdescripcion = request.form['dietDescription']
            conn = get_db_connection()
            if conn:
                with conn:
                    cursor = conn.cursor()
                    cursor.execute('INSERT INTO dieta(Nombre, Descripcion) VALUES (%s, %s)', (Fnombre, Fdescripcion))
                    conn.commit()
                flash('Dieta agregada correctamente', 'success')
                return redirect(url_for('dietasR'))
            else:
                flash('No se pudo conectar a la base de datos', 'danger')
                return redirect(url_for('dietasR'))
        except Exception as e:
            flash('Error al agregar dieta' + str(e))
            return redirect(url_for('dietasR'))

@app.route('/GuardarEjercicio', methods=['POST'])
def GuardarEjercicio():
    if request.method == 'POST':
        try:
            Fnombre = request.form['ejerName']
            fmusculo = request.form['ejermusculo']
            ftipo = request.form['ejertipo']
            conn = get_db_connection()
            if conn:
                with conn:
                    cursor = conn.cursor()
                    cursor.execute('INSERT INTO ejercicios(Nombre, Grupo_muscular, Tipo_ejercicio) VALUES (%s, %s, %s)', (Fnombre, fmusculo, ftipo))
                    conn.commit()
                flash('Ejercicio agregado correctamente', 'success')
                return redirect(url_for('ejercicioR'))
            else:
                flash('No se pudo conectar a la base de datos', 'danger')
                return redirect(url_for('ejercicioR'))
        except Exception as e:
            flash('Error al agregar ejercicio' + str(e))
            return redirect(url_for('ejercicioR'))

@app.route('/eliminarD/<id>')
def eliminarD(id):
    conn = get_db_connection()
    if conn:
        try:
            with conn:
                cursor = conn.cursor()
                cursor.execute('DELETE FROM dieta WHERE ID_dieta = %s', (id,))
                conn.commit()
            flash('Dieta eliminada correctamente', 'success')
            return redirect(url_for('verDietas'))
        except Exception as e:
            flash('Error al eliminar la dieta: ' + str(e), 'danger')
            return redirect(url_for('verDietas'))
    else:
        flash('No se pudo conectar a la base de datos', 'danger')
        return redirect(url_for('verDietas'))

@app.route('/eliminarE/<id>')
def eliminarE(id):
    conn = get_db_connection()
    if conn:
        try:
            with conn:
                cursor = conn.cursor()
                cursor.execute('DELETE FROM ejercicios WHERE ID_ejercicio = %s', (id,))
                conn.commit()
            flash('Ejercicio eliminado correctamente', 'success')
            return redirect(url_for('verEjercicios'))
        except Exception as e:
            flash('Error al eliminar el ejercicio: ' + str(e))
            return redirect(url_for('verEjercicios'))
    else:
        flash('No se pudo conectar a la base de datos', 'danger')
        return redirect(url_for('verEjercicios'))

@app.route('/editarD/<id>')
def editarD(id):
    conn = get_db_connection()
    if conn:
        with conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM dieta WHERE ID_dieta = %s', (id,))
            dietaE = cursor.fetchone()
        return render_template('editar_dietas.html', dieta=dietaE)
    else:
        flash('No se pudo conectar a la base de datos', 'danger')
        return redirect(url_for('verDietas'))

@app.route('/editarE/<id>')
def editarE(id):
    conn = get_db_connection()
    if conn:
        with conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM ejercicios WHERE ID_ejercicio = %s', (id,))
            ejercicioE = cursor.fetchone()
        return render_template('editar_ejercicios.html', ejercicio=ejercicioE)
    else:
        flash('No se pudo conectar a la base de datos', 'danger')
        return redirect(url_for('verEjercicios'))

@app.route('/ActualizarDieta/<id>', methods=['POST'])
@login_required
def ActualizarDieta(id):
    if request.method == 'POST':
        try:
            Enombre = request.form['dietName']
            Edescripcion = request.form['dietDescription']
            conn = get_db_connection()
            if conn:
                with conn:
                    cursor = conn.cursor()
                    cursor.execute('UPDATE dieta SET Nombre=%s, Descripcion=%s WHERE ID_dieta=%s', (Enombre, Edescripcion, id))
                    conn.commit()
                flash('Dieta editada correctamente', 'success')
                return redirect(url_for('verDietas'))
            else:
                flash('No se pudo conectar a la base de datos', 'danger')
                return redirect(url_for('verDietas'))
        except Exception as e:
            flash('Error al guardar la dieta:' + str(e))
            return redirect(url_for('verDietas'))

@app.route('/verUsuarios')
@login_required
def verUsuarios():
    conn = get_db_connection()
    if conn:
        try:
            with conn:
                cursor = conn.cursor()
                cursor.execute('SELECT ID_usuario, Nombre, Apellido_paterno, Apellido_materno, Numero_Telefono, Email FROM usuarios')
                consultaU = cursor.fetchall()
                print(consultaU)
            return render_template('consulta_usuarios.html', usuarios=consultaU)
        except Exception as e:
            print(e)
            return 'Error al consultar usuarios'
    else:
        return 'Error al conectar a la base de datos'

@app.route('/GuardarUsuario', methods=['POST'])
def guardarUsuario():
    if request.method == 'POST':
        try:
            Fnombre = request.form['txtnombre']
            Fapellido_p = request.form['txtapellido_paterno']
            Fapellido_m = request.form['txtapellido_materno']
            Fnumerot = request.form['txtnumero_telefono']
            Fcorreo = request.form['txtemail']
            Fcontrasena = request.form['txtcontrasena']
            Frole = request.form['txtrole']

            hashed_password = generate_password_hash_scrypt(Fcontrasena)
            conn = get_db_connection()
            if conn:
                with conn:
                    cursor = conn.cursor()
                    cursor.execute(
                        'INSERT INTO usuarios(Nombre, Apellido_paterno, Apellido_materno, Numero_Telefono, Email, Contrasena, Rol) VALUES (%s, %s, %s, %s, %s, %s, %s)', 
                        (Fnombre, Fapellido_p, Fapellido_m, Fnumerot, Fcorreo, hashed_password, Frole)
                    )
                    conn.commit()
                flash('Usuario agregado correctamente', 'success')
                return redirect(url_for('login'))
            else:
                flash('No se pudo conectar a la base de datos', 'danger')
                return redirect(url_for('registro'))
        except Exception as e:
            flash('Error al agregar usuario: ' + str(e))
            return redirect(url_for('registro'))

@app.route('/eliminar/<id>')
def eliminar(id):
    conn = get_db_connection()
    if conn:
        try:
            with conn:
                cursor = conn.cursor()
                cursor.execute('DELETE FROM usuarios WHERE ID_usuario = %s', (id,))
                conn.commit()
            flash('Usuario eliminado correctamente', 'success')
            return redirect(url_for('verUsuarios'))
        except Exception as e:
            flash('Error al eliminar el usuario: ' + str(e), 'danger')
            return redirect(url_for('verUsuarios'))
    else:
        flash('No se pudo conectar a la base de datos', 'danger')
        return redirect(url_for('verUsuarios'))

@app.route('/editar/<id>')
def editar(id):
    conn = get_db_connection()
    if conn:
        with conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM usuarios WHERE ID_usuario=%s', (id,))
            usuarioE = cursor.fetchone()
        return render_template('editar_usuarios.html', usuario=usuarioE)
    else:
        flash('No se pudo conectar a la base de datos', 'danger')
        return redirect(url_for('verUsuarios'))

@app.route('/ActualizarUsuario/<id>', methods=['POST'])
@login_required
def ActualizarUsuario(id):
    if request.method == 'POST':
        try:
            Enombre = request.form['txtnombre']
            Eapellido_p = request.form['txtapellido_paterno']
            Eapellido_m = request.form['txtapellido_materno']
            Enumerot = request.form['txtnumero_telefono']
            Ecorreo = request.form['txtemail']
            Econtrasena = request.form['txtcontrasena']
            Erole = request.form['txtrole']

            conn = get_db_connection()
            if conn:
                with conn:
                    if Econtrasena:  # Si se proporciona una nueva contraseña
                        hashed_password = generate_password_hash_scrypt(Econtrasena)
                        cursor = conn.cursor()
                        cursor.execute(
                            'UPDATE usuarios SET Nombre=%s, Apellido_paterno=%s, Apellido_materno=%s, Numero_Telefono=%s, Email=%s, Contraseña=%s, Rol=%s WHERE ID_usuario=%s',
                            (Enombre, Eapellido_p, Eapellido_m, Enumerot, Ecorreo, hashed_password, Erole, id)
                        )
                    else:  # Si no se proporciona una nueva contraseña
                        cursor = conn.cursor()
                        cursor.execute(
                            'UPDATE usuarios SET Nombre=%s, Apellido_paterno=%s, Apellido_materno=%s, Numero_Telefono=%s, Email=%s, Rol=%s WHERE ID_usuario=%s',
                            (Enombre, Eapellido_p, Eapellido_m, Enumerot, Ecorreo, Erole, id)
                        )
                    conn.commit()
                flash('Usuario editado correctamente', 'success')
                return redirect(url_for('verUsuarios'))
            else:
                flash('No se pudo conectar a la base de datos', 'danger')
                return redirect(url_for('verUsuarios'))
        except Exception as e:
            flash('Error al guardar el usuario: ' + str(e), 'danger')
            return redirect(url_for('verUsuarios'))

@app.route('/ActualizarEjercicio/<id>', methods=['POST'])
@login_required
def ActualizarEjercicio(id):
    if request.method == 'POST':
        try:
            Enombre = request.form['ejerName']
            Emusculo = request.form['ejermusculo']
            Etipo = request.form['ejertipo']

            conn = get_db_connection()
            if conn:
                with conn:
                    cursor = conn.cursor()
                    cursor.execute(
                        'UPDATE ejercicios SET Nombre=%s, Grupo_muscular=%s, Tipo_ejercicio=%s WHERE ID_ejercicio=%s', 
                        (Enombre, Emusculo, Etipo, id)
                    )
                    conn.commit()
                flash('Ejercicio editado correctamente', 'success')
                return redirect(url_for('verEjercicios'))
            else:
                flash('No se pudo conectar a la base de datos', 'danger')
                return redirect(url_for('verEjercicios'))
        except Exception as e:
            flash('Error al guardar el ejercicio:' + str(e))
            return redirect(url_for('verEjercicios'))

# Rutas para los usuarios premium 

@app.route('/vista')
@login_required
def vista():
    return render_template('vista.html')

@app.route('/alimentacionPersonalizada')
@login_required
def alimentacionPersonalizada():
    return render_template('PlanA.html')

@app.route('/objetivo')
@login_required
def objetivo():
    return render_template('objetivo.html')

@app.route('/nutriologo')
@login_required
def nutriologo():
    return render_template('Nut.html')

@app.route('/entrenador')
@login_required
def entrenador():
    return render_template('EP.html')

@app.route('/DietasUsuarioP')
@login_required
def DietasUsuarioP():
    return render_template('dieta.html')

@app.route('/EjerciciosUsuarioP')
@login_required
def EjerciciosUsuarioP():
    return render_template('Ejp.html')

# Rutas para los usuarios gratuitos
@app.route('/planes')
def planes():
    return render_template('Planes.html')

@app.route('/formulario')
def formulario():
    return render_template('Formulario.html')

@app.route('/principalgratis')
def principalgratis():
    return render_template('principal.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6000, debug=True)
