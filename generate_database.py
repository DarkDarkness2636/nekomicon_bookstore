import sqlite3

# Ruta de la base de datos
DATABASE_PATH = 'nekomicon_bookstore.db'

def crear_base_datos():
    # Conectar a la base de datos (se creará si no existe)
    conexion = sqlite3.connect(DATABASE_PATH)
    cursor = conexion.cursor()

    # Crear tabla para todos los libros
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS libros (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            autor TEXT NOT NULL,
            descripcion TEXT,
            precio REAL NOT NULL,
            imagen TEXT,
            categoria TEXT
        )
    ''')

    # Crear tabla para libros más vendidos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS libros_mas_vendidos (
            id INTEGER PRIMARY KEY,
            FOREIGN KEY (id) REFERENCES libros (id)
        )
    ''')

    # Crear tabla para libros nuevos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS libros_nuevos (
            id INTEGER PRIMARY KEY,
            FOREIGN KEY (id) REFERENCES libros (id)
        )
    ''')

    # Insertar algunos libros de ejemplo en la tabla libros
    libros_data = [
        ('El Juego de Ender', 'Orson Scott Card', 'Un niño prodigio es entrenado en una escuela militar espacial.', 379.00, 'imagenes/portada_ender.jpeg', 'Ciencia Ficción'),
        ('1984', 'George Orwell', 'Una novela distópica sobre un futuro totalitario.', 14.99, 'ruta/a/imagen2.jpg', 'Ficción'),
        ('Harry Potter y la Piedra Filosofal', 'J.K. Rowling', 'Un joven descubre su identidad como mago.', 19.99, 'ruta/a/imagen3.jpg', 'Fantasía'),
        ('Cien años de soledad', 'Gabriel García Márquez', 'La historia de la familia Buendía en el pueblo ficticio de Macondo.', 12.50, 'ruta/a/imagen4.jpg', 'Ficción'),
        ('El Señor de los Anillos', 'J.R.R. Tolkien', 'La lucha épica entre el bien y el mal en la Tierra Media.', 20.00, 'ruta/a/imagen5.jpg', 'Fantasía')
    ]

    # Insertar libros en la tabla
    cursor.executemany('''
        INSERT INTO libros (titulo, autor, descripcion, precio, imagen, categoria)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', libros_data)

    # Asumimos que los IDs de los libros anteriores son 1, 2, 3, 4 y 5.
    # Insertar libros en la tabla libros_mas_vendidos
    cursor.execute('INSERT INTO libros_mas_vendidos (id) VALUES (1), (2)')  # Libros 1 y 2 son más vendidos

    # Insertar libros en la tabla libros_nuevos
    cursor.execute('INSERT INTO libros_nuevos (id) VALUES (3), (4)')  # Libros 3 y 4 son nuevos

    # Guardar los cambios y cerrar la conexión
    conexion.commit()
    conexion.close()

if __name__ == '__main__':
    crear_base_datos()
    print("Base de datos creada y poblada con éxito.")
