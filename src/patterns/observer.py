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

class SistemaLogros(Observer):
    def actualizar(self, evento, datos):
        if evento == "partida_terminada":
            print(f"[LOGROS] Verificando logros para usuario {datos['usuario']} tras finalizar partida.")

class SistemaActualizaciones(Observer):
    def actualizar(self, evento, datos):
        if evento == "juego_lanzado":
            print(f"[ACTUALIZACIONES] Programando verificacion de parches para {datos['juego']}.")

class SistemaAnalisis(Observer):
    def actualizar(self, evento, datos):
        print(f"[ANALISIS] Evento registrado: {evento} | Datos: {datos}")
        # Aqui se podria guardar en una base de datos para analisis posterior
