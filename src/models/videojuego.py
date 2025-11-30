from abc import ABC, abstractmethod

class Videojuego(ABC):
    def __init__(self, titulo, desarrollador, precio, plataforma="PC", target="Teen"):
        self.titulo = titulo
        self.desarrollador = desarrollador
        self.precio = precio
        self.plataforma = plataforma
        self.target = target
        self.jugadores_activos = 0
        self.calificaciones = [] # Lista de enteros 1-5

    @abstractmethod
    def iniciar(self):
        pass

    @abstractmethod
    def guardar_progreso(self, usuario_id, datos):
        pass

    @abstractmethod
    def cargar_progreso(self, usuario_id):
        pass

    def obtener_info(self):
        return {
            "titulo": self.titulo,
            "desarrollador": self.desarrollador,
            "precio": self.precio,
            "plataforma": self.plataforma,
            "target": self.target
        }
