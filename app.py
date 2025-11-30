from flask import Flask, jsonify, request, render_template, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from src.services.plataforma import PlataformaVideojuegos
from src.patterns.observer import SistemaLogros, SistemaActualizaciones, SistemaAnalisis
from src.models.db import db
from src.models.entities import User, Game
import os

app = Flask(__name__)
app.secret_key = 'supersecretkey' # Necesario para sesiones
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plataforma.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

plataforma = PlataformaVideojuegos()

# Registrar observadores
plataforma.agregar_observer(SistemaLogros())
plataforma.agregar_observer(SistemaActualizaciones())
plataforma.agregar_observer(SistemaAnalisis())

# Crear tablas al inicio
with app.app_context():
    db.create_all()
    
    # Gestionar usuario admin
    admin_user = User.query.filter_by(username='admin').first()
    hashed_password = generate_password_hash('123')
    
    if not admin_user:
        # Crear si no existe
        admin = User(username='admin', password=hashed_password, role='admin', elo=9999)
        db.session.add(admin)
        db.session.commit()
    else:
        # Actualizar password si ya existe (para arreglar problemas de migracion de texto plano a hash)
        admin_user.password = hashed_password
        db.session.commit()

    # Crear Juegos por defecto si no existen
    if not Game.query.first():
        juegos_default = [
            Game(titulo="Genshin Impact", desarrollador="HoYoverse", precio=0.0, tipo="Rol", plataforma="PC", target="Teen"),
            Game(titulo="EA FC 24", desarrollador="EA Sports", precio=69.99, tipo="Deportes", plataforma="PS5", target="Everyone"),
            Game(titulo="Call of Duty: MW3", desarrollador="Activision", precio=69.99, tipo="Accion", plataforma="Xbox", target="Mature"),
            Game(titulo="Civilization VI", desarrollador="Firaxis", precio=29.99, tipo="Estrategia", plataforma="PC", target="Everyone")
        ]
        db.session.add_all(juegos_default)
        db.session.commit()
        print("Juegos por defecto creados.")

# Decorador para requerir login
def login_required(f):
    def wrapper(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    wrapper.__name__ = f.__name__
    return wrapper

# Decorador para requerir admin
def admin_required(f):
    def wrapper(*args, **kwargs):
        if 'user_id' not in session or session.get('role') != 'admin':
            return "Acceso denegado. Se requiere rol de administrador.", 403
        return f(*args, **kwargs)
    wrapper.__name__ = f.__name__
    return wrapper

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Busqueda segura usando ORM (previene SQL Injection basico)
        user = User.query.filter_by(username=username).first()
        
        # Verificacion de hash de contrasena (Seguridad Realista)
        if user and check_password_hash(user.password, password):
            if user.is_banned:
                return "Tu cuenta ha sido suspendida."
            session['user_id'] = user.id
            session['username'] = user.username
            session['role'] = user.role
            session['elo'] = user.elo
            return redirect(url_for('index'))
        else:
            return "Credenciales invalidas"
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # En un entorno realista, el registro publico es SOLO para usuarios
        role = 'user'
        
        if User.query.filter_by(username=username).first():
            return "El usuario ya existe"
            
        # Hashing de contrasena antes de guardar
        hashed_password = generate_password_hash(password)
        new_user = User(username=username, password=hashed_password, role=role)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/games', methods=['GET'])
@login_required
def games():
    lista_juegos = plataforma.listar_juegos()
    return render_template('games.html', juegos=lista_juegos)

@app.route('/admin', methods=['GET'])
@admin_required
def admin_panel():
    users = plataforma.obtener_usuarios()
    return render_template('admin.html', users=users)

@app.route('/admin/create_game', methods=['POST'])
@admin_required
def create_game():
    try:
        tipo = request.form.get('tipo')
        titulo = request.form.get('titulo')
        desarrollador = request.form.get('desarrollador')
        precio = float(request.form.get('precio'))
        plataforma_juego = request.form.get('plataforma', 'PC')
        target = request.form.get('target', 'Teen')
        
        plataforma.registrar_juego(tipo, titulo, desarrollador, precio, plataforma_juego, target)
        return redirect(url_for('admin_panel'))
    except ValueError:
        return "Error en los datos", 400

@app.route('/admin/create_admin', methods=['POST'])
@admin_required
def create_admin():
    username = request.form['username']
    password = request.form['password']
    
    if User.query.filter_by(username=username).first():
        return "El usuario ya existe", 400
        
    hashed_password = generate_password_hash(password)
    new_admin = User(username=username, password=hashed_password, role='admin', elo=9999)
    db.session.add(new_admin)
    db.session.commit()
    return redirect(url_for('admin_panel'))

@app.route('/admin/ban_user', methods=['POST'])
@admin_required
def ban_user():
    user_id = request.form.get('user_id')
    plataforma.banear_usuario(user_id)
    return redirect(url_for('admin_panel'))

@app.route('/store', methods=['GET'])
@login_required
def store():
    juego_seleccionado = request.args.get('juego')
    items = []
    if juego_seleccionado:
        items = plataforma.obtener_items_venta(juego_seleccionado)
    
    return render_template('store.html', juegos=plataforma.listar_juegos(), items=items, juego_seleccionado=juego_seleccionado)

@app.route('/store/buy', methods=['POST'])
@login_required
def buy_item():
    user_id = session['user_id']
    juego = request.form.get('juego')
    item = request.form.get('item')
    
    mensaje = plataforma.comprar_item(user_id, juego, item)
    
    items = plataforma.obtener_items_venta(juego)
    return render_template('store.html', juegos=plataforma.listar_juegos(), items=items, juego_seleccionado=juego, mensaje=mensaje)

@app.route('/library', methods=['GET'])
@login_required
def library():
    return render_template('library.html', juegos=plataforma.listar_juegos())

@app.route('/library/update', methods=['POST'])
@login_required
def update_game():
    juego = request.form.get('juego')
    mensaje = plataforma.verificar_actualizaciones(juego)
    return render_template('library.html', juegos=plataforma.listar_juegos(), mensaje=mensaje)

@app.route('/library/rate', methods=['POST'])
@login_required
def rate_game():
    user_id = session['user_id']
    juego = request.form.get('juego')
    puntuacion = int(request.form.get('puntuacion'))
    comentario = request.form.get('comentario')
    
    mensaje = plataforma.calificar_juego(user_id, juego, puntuacion, comentario)
    return render_template('library.html', juegos=plataforma.listar_juegos(), mensaje=mensaje)

@app.route('/library/play', methods=['POST'])
@login_required
def play_game():
    user_id = session['user_id']
    juego_titulo = request.form.get('juego')
    
    # Demostracion de Polimorfismo (Iniciar, Guardar, Cargar)
    logs = plataforma.simular_sesion_juego(user_id, juego_titulo)
    
    return render_template('library.html', juegos=plataforma.listar_juegos(), logs_juego=logs, juego_jugado=juego_titulo)

@app.route('/matchmaking', methods=['GET', 'POST'])
@login_required
def matchmaking():
    resultado = None
    lista_juegos = plataforma.listar_juegos()
    
    if request.method == 'POST':
        user_id = session['user_id']
        titulo = request.form.get('titulo')
        competitivo = request.form.get('competitivo') == 'true'
        
        resultado = plataforma.buscar_partida(titulo, user_id, competitivo)
        
    return render_template('matchmaking.html', juegos=lista_juegos, resultado=resultado, elo=session.get('elo'))

if __name__ == '__main__':
    app.run(debug=True)
