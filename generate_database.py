import sqlite3

DATABASE_PATH = 'nekomicon_bookstore.db'

def crear_base_datos():
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

    # Insertar algunos libros de ejemplo en la tabla libros
    libros_data = [
        ('El Juego de Ender', 'Orson Scott Card', 'Un niño prodigio es entrenado en una escuela militar espacial.', 379.00, 'imagenes/portada_ender.jpeg', 'Ciencia Ficción'),
        ('1984', 'George Orwell', 'Una novela distópica sobre un futuro totalitario.', 188.10, 'imagenes/1984_portada.jpg', 'Ficción'),
        ('Harry Potter y la Piedra Filosofal', 'J.K. Rowling', 'Un joven descubre su identidad como mago.', 319.00, 'imagenes/hppf_portada.jpg', 'Fantasía'),
        ('Cien años de soledad', 'Gabriel García Márquez', 'La historia de la familia Buendía en el pueblo ficticio de Macondo.', 278.00, 'imagenes/portada_cien_anos_de_soledad.jpg', 'Ficción'),
        ('El Señor de los Anillos', 'J.R.R. Tolkien', 'La lucha épica entre el bien y el mal en la Tierra Media.', 648.00, 'imagenes/lotr_portada.jpg', 'Fantasía'),
        ('Orgullo y prejuicio', 'Jane Austen', 'Una novela sobre el amor y las relaciones sociales en la Inglaterra del siglo XIX.', 225.00, 'imagenes/oyp.jpg', 'Romance'),
        ('El alquimista', 'Paulo Coelho', 'Un joven pastor andaluz busca un tesoro en Egipto.', 299.00, 'imagenes/elalqui.jpg', 'Ficción'),
        ('Crónica de una muerte anunciada', 'Gabriel García Márquez', 'La historia de un asesinato anunciado en un pequeño pueblo.', 175.00, 'imagenes/cduma.jpg', 'Ficción'),
        ('El gran Gatsby', 'F. Scott Fitzgerald', 'Una novela sobre la decadencia del sueño americano en los años 20.', 210.00, 'imagenes/gatsby.jpg', 'Ficción'),
        ('Moby Dick', 'Herman Melville', 'La caza de una ballena blanca obsesiva por un capitán loco.', 350.00, 'imagenes/moby.jpg', 'Aventura'),
        ('La sombra del viento', 'Carlos Ruiz Zafón', 'Un joven encuentra un libro que cambiará su vida para siempre.', 330.00, 'imagenes/viento.jpg', 'Misterio'),
        ('Don Quijote de la Mancha', 'Miguel de Cervantes', 'Las aventuras de un hidalgo que se convierte en caballero andante.', 420.00, 'imagenes/quijote.jpg', 'Clásico'),
        ('Cumbres borrascosas', 'Emily Brontë', 'Una historia de amor y venganza en los páramos ingleses.', 275.00, 'imagenes/cumbres.jpg', 'Romance'),
        ('El código Da Vinci', 'Dan Brown', 'Un thriller que involucra misterio religioso y conspiraciones.', 295.00, 'imagenes/codigo.jpg', 'Thriller'),
        ('Sapiens: De animales a dioses', 'Yuval Noah Harari', 'Una breve historia de la humanidad desde la prehistoria hasta el presente.', 450.00, 'imagenes/sapiens.jpg', 'No Ficción')
    ]

    # Insertar libros en la tabla
    cursor.executemany('''
        INSERT INTO libros (titulo, autor, descripcion, precio, imagen, categoria)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', libros_data)

    # Asumimos que los IDs de los libros anteriores son 1, 2, 3, 4 y 5.
    cursor.execute('INSERT INTO libros_mas_vendidos (id) VALUES (1), (2)')
    cursor.execute('INSERT INTO libros_nuevos (id) VALUES (3), (4)')

    conexion.commit()
    conexion.close()

if __name__ == '__main__':
    crear_base_datos()
    print("Base de datos creada y poblada con éxito.")
