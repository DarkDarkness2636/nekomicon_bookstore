from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

# Función para obtener libros desde la base de datos
def obtener_libros():
    conn = sqlite3.connect('libreria.db')
    c = conn.cursor()
    c.execute('SELECT * FROM libros')
    libros = c.fetchall()
    conn.close()
    return libros

@app.route('/')
def index():
    libros = obtener_libros()
    return render_template('main.html', libros=libros)

if __name__ == '__main__':
    app.run(debug=True)
