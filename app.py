from flask import Flask, render_template, request, redirect, url_for, session
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
import sqlite3
import stripe

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta'  # Necesaria para manejar sesiones

# Inicializar Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)

# Rutas para las bases de datos
LIBROS_DATABASE_PATH = 'nekomicon_bookstore.db'
USUARIOS_DATABASE_PATH = 'usuarios.db'

stripe.api_key = 'sk_test_51QCk4iBVPHQKEtjfeQZXblbOogBEtpHMuyqnWcIqSo5WJtkpFk0nBLXzMe5ImSUXtQ2W4kXkE1WjjZQ43eaqIciO00gXAImpJK'  # Clave secreta

@app.route('/create-checkout-session/<int:libro_id>', methods=['POST'])
def create_checkout_session(libro_id):
    conn = get_libros_db_connection()
    libro = conn.execute('SELECT * FROM libros WHERE id = ?', (libro_id,)).fetchone()
    conn.close()

    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'mxn',
                    'product_data': {
                        'name': libro['titulo'],  # Nombre del libro
                    },
                    'unit_amount': int(libro['precio'] * 100),  # Precio en centavos (Stripe usa centavos)
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url='http://127.0.0.1:5000/success',
            cancel_url='http://127.0.0.1:5000/cancel',
        )
        return redirect(checkout_session.url, code=303)
    except Exception as e:
        return str(e)


# Ruta para el pago
@app.route('/create-checkout-session/cart', methods=['POST'])
@login_required
def create_checkout_session_cart():
    conn = get_libros_db_connection()
    cart_items = []
    total_price = 0

    if 'cart' in session:
        cart_items = conn.execute('SELECT * FROM libros WHERE id IN ({})'.format(','.join('?' * len(session['cart']))), session['cart']).fetchall()

        # Calcular el total
        total_price = sum(libro['precio'] for libro in cart_items)

    conn.close()

    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'mxn',
                    'product_data': {
                        'name': 'Carrito de libros',  # Nombre general para el carrito
                    },
                    'unit_amount': int(total_price * 100),  # Total en centavos
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url='http://127.0.0.1:5000/success',
            cancel_url='http://127.0.0.1:5000/cancel',
        )
        return redirect(checkout_session.url, code=303)
    except Exception as e:
        return str(e)


@app.route('/success')
def success():
    return "Pago completado con éxito."

@app.route('/cancel')
def cancel():
    return "Pago cancelado."


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

def get_db_connection():
    conn = sqlite3.connect('nekomicon_bookstore.db')
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
    return render_template('html/main.html', libros=libros, current_user=current_user)

@app.route('/cart')
@login_required
def cart():
    if not current_user.is_authenticated:
        return redirect(url_for('login', message="Por favor, inicia sesión para acceder al carrito"))

    conn = get_libros_db_connection()
    cart_items = []
    total_price = 0

    if 'cart' in session:
        cart_items = conn.execute('SELECT * FROM libros WHERE id IN ({})'.format(','.join('?' * len(session['cart']))), session['cart']).fetchall()
        total_price = sum(item['precio'] for item in cart_items)

    conn.close()
    return render_template('html/cart.html', cart_items=cart_items, total_price=total_price)

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
            return render_template('html/login.html', error='Credenciales incorrectas')

    return render_template('html/login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()  # Cerrar sesión
    return redirect(url_for('index'))

@app.route('/add_to_cart/<int:libro_id>')
def add_to_cart(libro_id):
    if 'cart' not in session:
        session['cart'] = []

    session['cart'].append(libro_id)  # Agrega el ID del libro al carrito
    session.modified = True  # Marca la sesión como modificada
    return redirect(url_for('cart'))  # Redirige al carrito después de agregar


@app.route('/remove_from_cart/<int:libro_id>')
def remove_from_cart(libro_id):
    if 'cart' in session:
        session['cart'].remove(libro_id)  # Elimina el libro del carrito
        session.modified = True
    return redirect(url_for('cart'))  # Redirige al carrito después de eliminar

@app.route('/checkout')
@login_required  # Solo para usuarios autenticados
def checkout():
    if 'cart' not in session or len(session['cart']) == 0:
        return redirect(url_for('cart'))  # Si el carrito está vacío, redirigir

    # Aquí puedes procesar el pago, por ahora solo simulamos
    session.pop('cart', None)  # Vacía el carrito después del "pago"
    return render_template('html/checkout_success.html')

@app.route('/comprar/<int:libro_id>')
def book_detail(libro_id):
    conn = get_db_connection()
    libro = conn.execute('SELECT * FROM libros WHERE id = ?', (libro_id,)).fetchone()
    conn.close()
    return render_template('html/book_detail.html', libro=libro)

if __name__ == '__main__':
    app.run(debug=True)
