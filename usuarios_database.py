import sqlite3
import bcrypt
from werkzeug.security import generate_password_hash

USUARIOS_DATABASE_PATH = 'usuarios.db'

def crear_base_datos_usuarios():
    conexion = sqlite3.connect(USUARIOS_DATABASE_PATH)
    cursor = conexion.cursor()

    # Crear tabla para usuarios con contraseña encriptada
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            is_admin BOOLEAN NOT NULL DEFAULT 0
        )
    ''')

    # Crea una contraseña encriptada para el administrador
    username = "admin"
    password = "admin"  # Cambia esta a tu contraseña deseada
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

# Inserta el usuario administrador en la base de datos
    cursor.execute('''
    INSERT INTO usuarios (username, password, is_admin)
    VALUES (?, ?, ?)
''',(username, hashed_password, 1))  # 1 para indicar que es administrador

    conexion.commit()
    conexion.close()

if __name__ == '__main__':
    crear_base_datos_usuarios()
    print("Base de datos de usuarios creada y poblada con éxito.")
