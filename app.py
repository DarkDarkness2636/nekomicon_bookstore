from flask import Flask, render_template, request, redirect, url_for, session
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
import sqlite3

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta'  # Necesaria para manejar sesiones

# Inicializar Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)

# Rutas para las bases de datos
LIBROS_DATABASE_PATH = 'nekomicon_bookstore.db'
USUARIOS_DATABASE_PATH = 'usuarios.db'

# Función para la conexión a la base de datos de libros
def get_libros_db_connection():
    conn = sqlite3.connect(LIBROS_DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# Función para la conexión a la base de datos de usuarios
def get_usuarios_db_connection():
    conn = sqlite3.connect(USUARIOS_DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# Clase User para Flask-Login
class User(UserMixin):
    def __init__(self, id, username, password, is_admin):
        self.id = id
        self.username = username
        self.password = password
        self.is_admin = is_admin

# Cargar usuario
@login_manager.user_loader
def load_user(user_id):
    conn = get_usuarios_db_connection()
    user_data = conn.execute('SELECT * FROM usuarios WHERE id = ?', (user_id,)).fetchone()
    conn.close()
    return User(user_data['id'], user_data['username'], user_data['password'], user_data['is_admin']) if user_data else None

@app.route('/')
def index():
    conn = get_libros_db_connection()
    libros = conn.execute('SELECT * FROM libros').fetchall()
    conn.close()
    return render_template('main.html', libros=libros, current_user=current_user)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_usuarios_db_connection()
        user = conn.execute('SELECT * FROM usuarios WHERE username = ? AND password = ?', (username, password)).fetchone()
        conn.close()

        if user:
            user_obj = User(user['id'], user['username'], user['password'], user['is_admin'])
            login_user(user_obj)  # Iniciar sesión con Flask-Login
            return redirect(url_for('index'))  # Redirigir a la página principal
        else:
            return render_template('login.html', error='Credenciales incorrectas')

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()  # Cerrar sesión
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
