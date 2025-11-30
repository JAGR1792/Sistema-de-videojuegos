from abc import ABC, abstractmethod
import random

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
    def __init__(self):
        self.logros_genericos = [
            ("Jugador Dedicado", "Has jugado con gran pasion.", 0.25),
            ("Maestro del Teclado", "Tus dedos vuelan sobre las teclas.", 0.15),
            ("No te rindas", "La perseverancia es clave.", 0.30),
            ("Explorador", "Has visto cada rincon del mapa.", 0.10),
            ("Coleccionista", "Te gusta tenerlo todo.", 0.05),
            ("Velocista", "Mas rapido que la luz.", 0.08),
            ("Estratega", "Cada movimiento cuenta.", 0.12),
            ("Lobo Solitario", "Mejor solo que mal acompañado.", 0.18),
            ("Jugador de Equipo", "El trabajo en equipo es esencial.", 0.18),
            ("Invencible", "Nadie puede contigo.", 0.01),
            ("Veterano", "Has visto muchas cosas.", 0.10),
            ("Novato con Suerte", "A veces es mejor tener suerte que habilidad.", 0.20),
            ("Cazador de Glitches", "Encontraste algo que no debias.", 0.05),
            ("Amante del Lore", "Lees todos los dialogos.", 0.15),
            ("Speedrunner", "El tiempo es oro.", 0.05),
            ("Completista", "El 100% no es suficiente.", 0.02),
            ("Social", "Haces amigos facilmente.", 0.20),
            ("Nocturno", "La noche es tu aliada.", 0.20),
            ("Madrugador", "A quien madruga...", 0.20),
            ("Maratonista", "No puedes parar de jugar.", 0.10),
            ("Francotirador", "Donde pones el ojo, pones la bala.", 0.08),
            ("Tanque", "Aguantas lo que te echen.", 0.12),
            ("Curandero", "Salvas vidas.", 0.12),
            ("Diplomatico", "Las palabras son tu arma.", 0.10),
            ("Comerciante", "El dinero mueve el mundo.", 0.15),
            ("Artesano", "Creas maravillas con tus manos.", 0.10),
            ("Alquimista", "Pociones y mezclas peligrosas.", 0.08),
            ("Mago", "El poder arcano fluye en ti.", 0.08),
            ("Guerrero", "La fuerza bruta es la solucion.", 0.15),
            ("Ladron", "Lo que es tuyo es mio.", 0.08)
        ]

    def actualizar(self, evento, datos):
        # Logica simple de logros basada en eventos
        if evento == "compra_realizada":
            self._otorgar_logro(datos['usuario'], datos['juego'], "Comprador Compulsivo", "Realizaste tu primera compra.")
            # Probabilidad de logro extra por comprar
            if random.random() < 0.1:
                self._otorgar_logro(datos['usuario'], datos['juego'], "Inversionista", "Apoyas a los desarrolladores.")

        elif evento == "partida_terminada":
            self._otorgar_logro(datos['usuario'], datos['juego'], "Primeros Pasos", "Jugaste tu primera partida.")
            
            # Intentar otorgar logros aleatorios de la lista grande
            self._intentar_logros_aleatorios(datos['usuario'], datos['juego'])

        elif evento == "actualizacion_realizada":
            # Este evento no suele dar logros al usuario, pero podria
            pass

    def _intentar_logros_aleatorios(self, username, juego_titulo):
        # Intentamos ver si toca alguno de la lista grande
        for nombre, descripcion, probabilidad in self.logros_genericos:
            if random.random() < probabilidad:
                self._otorgar_logro(username, juego_titulo, nombre, descripcion)

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
            
            # Simulacion aleatoria de parches dia 1
            if random.choice([True, False]):
                print(f"[ACTUALIZACIONES] !ATENCION! Se ha detectado un parche de Dia 1 critico para {datos['juego']}. Descargando...")


class SistemaAnalisis(Observer):
    def actualizar(self, evento, datos):
        print(f"[ANALISIS] Evento registrado: {evento} | Datos: {datos}")
        # Aqui se podria guardar en una base de datos para analisis posterior
