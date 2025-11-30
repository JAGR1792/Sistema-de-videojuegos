from .db import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False) # En prod usar hash
    role = db.Column(db.String(20), default='user') # 'admin' o 'user'
    elo = db.Column(db.Integer, default=1000)
    is_banned = db.Column(db.Boolean, default=False)
    
    # Relaciones
    purchases = db.relationship('Purchase', backref='user', lazy=True)
    ratings = db.relationship('Rating', backref='user', lazy=True)

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    desarrollador = db.Column(db.String(100), nullable=False)
    precio = db.Column(db.Float, nullable=False)
    tipo = db.Column(db.String(50), nullable=False)
    plataforma = db.Column(db.String(50), default="PC")
    target = db.Column(db.String(50), default="Teen")
    
    # Para simplificar, guardamos calificaciones aqui tambien o las calculamos
    ratings = db.relationship('Rating', backref='game', lazy=True)

    def obtener_info(self):
        return {
            "id": self.id,
            "titulo": self.titulo,
            "desarrollador": self.desarrollador,
            "precio": self.precio,
            "tipo": self.tipo,
            "plataforma": self.plataforma,
            "target": self.target
        }

class Purchase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    game_title = db.Column(db.String(100), nullable=False) # Guardamos titulo por simplicidad
    item_name = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

class Rating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.String(200))
