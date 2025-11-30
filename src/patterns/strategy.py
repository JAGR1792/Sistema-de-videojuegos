from abc import ABC, abstractmethod
import random

# Estrategia de Matchmaking
class MatchmakingStrategy(ABC):
    @abstractmethod
    def encontrar_partida(self, jugador, juego):
        pass

class MatchmakingAleatorio(MatchmakingStrategy):
    def encontrar_partida(self, jugador, juego):
        return f"Buscando cualquier partida disponible para {jugador} en {juego.titulo}..."

class MatchmakingPorRango(MatchmakingStrategy):
    def encontrar_partida(self, jugador, juego):
        # jugador es ahora un objeto User de la DB
        rango_min = jugador.elo - 100
        rango_max = jugador.elo + 100
        return f"Buscando oponente con ELO entre {rango_min} y {rango_max} para {jugador.username} (ELO: {jugador.elo})..."

# Estrategia de Monetizacion
class MonetizacionStrategy(ABC):
    @abstractmethod
    def calcular_precio(self, precio_base):
        pass

class MonetizacionF2P(MonetizacionStrategy):
    def calcular_precio(self, precio_base):
        return 0.0

class MonetizacionPremium(MonetizacionStrategy):
    def calcular_precio(self, precio_base):
        return precio_base

class MonetizacionSuscripcion(MonetizacionStrategy):
    def calcular_precio(self, precio_base):
        return 15.0  # Precio fijo mensual

class MonetizacionDescuento(MonetizacionStrategy):
    def calcular_precio(self, precio_base):
        return precio_base * 0.8 # 20% de descuento

# Estrategia de Puntuacion
class PuntuacionStrategy(ABC):
    @abstractmethod
    def calcular_puntuacion_final(self, calificaciones):
        pass

class PuntuacionPromedioSimple(PuntuacionStrategy):
    def calcular_puntuacion_final(self, calificaciones):
        if not calificaciones:
            return 0.0
        return sum(calificaciones) / len(calificaciones)

class PuntuacionPonderadaReciente(PuntuacionStrategy):
    def calcular_puntuacion_final(self, calificaciones):
        # Da mas peso a las ultimas calificaciones (simulado)
        if not calificaciones:
            return 0.0
        # Simplemente tomamos el promedio de la ultima mitad de calificaciones
        recientes = calificaciones[len(calificaciones)//2:]
        return sum(recientes) / len(recientes)
