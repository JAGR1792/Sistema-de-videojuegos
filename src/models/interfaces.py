from abc import ABC, abstractmethod

class Multijugador(ABC):
    @abstractmethod
    def buscar_partida(self):
        pass

    @abstractmethod
    def conectar_jugadores(self, jugadores):
        pass

class ConMicrotransacciones(ABC):
    @abstractmethod
    def listar_items_venta(self):
        pass

    @abstractmethod
    def procesar_compra(self, item_id, usuario_id):
        pass

class Actualizable(ABC):
    @abstractmethod
    def verificar_actualizacion(self):
        pass

    @abstractmethod
    def descargar_parche(self):
        pass

class Calificable(ABC):
    @abstractmethod
    def calificar(self, puntuacion, comentario):
        pass

    @abstractmethod
    def obtener_promedio_calificacion(self):
        pass
