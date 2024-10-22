import sqlite3

USUARIOS_DATABASE_PATH = 'usuarios.db'

def crear_base_datos_usuarios():
    conexion = sqlite3.connect(USUARIOS_DATABASE_PATH)
    cursor = conexion.cursor()

    # Crear tabla para usuarios
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            is_admin BOOLEAN NOT NULL DEFAULT 0
        )
    ''')

    # Insertar usuario admin
    cursor.execute('''
        INSERT OR IGNORE INTO usuarios (username, password, is_admin)
        VALUES ('admin', 'admin', 1)
    ''')

    conexion.commit()
    conexion.close()

if __name__ == '__main__':
    crear_base_datos_usuarios()
    print("Base de datos de usuarios creada y poblada con éxito.")