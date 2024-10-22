from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('nekomicon_bookstore.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    libros = conn.execute('SELECT * FROM libros LIMIT 20').fetchall()  # Cambia la consulta según tus necesidades
    conn.close()
    return render_template('/html/main.html', libros=libros)

@app.route('/comprar/<int:libro_id>')
def book_detail(libro_id):
    conn = get_db_connection()
    libro = conn.execute('SELECT * FROM libros WHERE id = ?', (libro_id,)).fetchone()
    conn.close()
    return render_template('book_detail.html', libro=libro)

if __name__ == '__main__':
    app.run(debug=True)

