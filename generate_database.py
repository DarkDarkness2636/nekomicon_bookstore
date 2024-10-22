import sqlite3

# Crear la base de datos
conn = sqlite3.connect('libreria.db')
c = conn.cursor()

# Crear tabla libros
c.execute('''
    CREATE TABLE IF NOT EXISTS libros (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo TEXT,
        autor TEXT,
        imagen TEXT
    )
''')

# Insertar datos de ejemplo
libros = [
    ('El Principito', 'Antoine de Saint-Exupéry', 'https://via.placeholder.com/150'),
    ('1984', 'George Orwell', 'https://via.placeholder.com/150'),
    ('El Hobbit', 'J.R.R. Tolkien', 'https://via.placeholder.com/150'),
    ('Cien Años de Soledad', 'Gabriel García Márquez', 'https://via.placeholder.com/150'),
    ('Don Quijote de la Mancha', 'Miguel de Cervantes', 'https://via.placeholder.com/150'),
    ('Moby Dick', 'Herman Melville', 'https://via.placeholder.com/150'),
    ('Crónica de una muerte anunciada', 'Gabriel García Márquez', 'https://via.placeholder.com/150'),
    ('Orgullo y prejuicio', 'Jane Austen', 'https://via.placeholder.com/150'),
    ('Guerra y paz', 'León Tolstói', 'https://via.placeholder.com/150'),
    ('El guardián entre el centeno', 'J.D. Salinger', 'https://via.placeholder.com/150'),
]

c.executemany("INSERT INTO libros (titulo, autor, imagen) VALUES (?, ?, ?)", libros)

conn.commit()
conn.close()
