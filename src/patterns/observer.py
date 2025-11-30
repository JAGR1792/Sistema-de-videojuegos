from abc import ABC, abstractmethod

class Observer(ABC):
    @abstractmethod
    def actualizar(self, evento, datos):
        pass

class Subject:
    def __init__(self):
        self._observers = []

    def agregar_observer(self, observer):
        self._observers.append(observer)

    def eliminar_observer(self, observer):
        self._observers.remove(observer)

    def notificar_observers(self, evento, datos):
        for observer in self._observers:
            observer.actualizar(evento, datos)

from src.models.db import db
from src.models.entities import Achievement, User

class SistemaLogros(Observer):
    def actualizar(self, evento, datos):
        # Logica simple de logros basada en eventos
        if evento == "compra_realizada":
            self._otorgar_logro(datos['usuario'], datos['juego'], "Comprador Compulsivo", "Realizaste tu primera compra.")
        elif evento == "partida_terminada":
            self._otorgar_logro(datos['usuario'], datos['juego'], "Primeros Pasos", "Jugaste tu primera partida.")
        elif evento == "actualizacion_realizada":
            # Este evento no suele dar logros al usuario, pero podria
            pass

    def _otorgar_logro(self, username, juego_titulo, nombre_logro, descripcion):
        # Necesitamos el contexto de la app para escribir en DB si se ejecuta asincrono, 
        # pero aqui corre en el mismo hilo request
        user = User.query.filter_by(username=username).first()
        if user:
            # Verificar si ya tiene el logro
            existe = Achievement.query.filter_by(user_id=user.id, game_title=juego_titulo, name=nombre_logro).first()
            if not existe:
                nuevo_logro = Achievement(user_id=user.id, game_title=juego_titulo, name=nombre_logro, description=descripcion)
                db.session.add(nuevo_logro)
                db.session.commit()
                print(f"[LOGROS] Logro desbloqueado para {username}: {nombre_logro}")

class SistemaActualizaciones(Observer):
    def actualizar(self, evento, datos):
        if evento == "juego_lanzado":
            print(f"[ACTUALIZACIONES] Programando verificacion de parches para {datos['juego']}.")

class SistemaAnalisis(Observer):
    def actualizar(self, evento, datos):
        print(f"[ANALISIS] Evento registrado: {evento} | Datos: {datos}")
        # Aqui se podria guardar en una base de datos para analisis posterior
