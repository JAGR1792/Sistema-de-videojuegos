from src.patterns.observer import Subject
from src.patterns.factory import JuegoFactory
from src.patterns.strategy import MatchmakingAleatorio, MatchmakingPorRango, PuntuacionPromedioSimple, MonetizacionDescuento, MonetizacionPremium
from src.models.interfaces import ConMicrotransacciones, Actualizable, Calificable
from src.models.db import db
from src.models.entities import Game, User, Purchase, Rating
from src.models.implementaciones import JuegoAccion, JuegoEstrategia, JuegoRol, JuegoDeportivo
from functools import lru_cache

class PlataformaVideojuegos(Subject):
    def __init__(self):
        super().__init__()
        # Ya no necesitamos listas en memoria, usamos DB
        self.matchmaking_strategy = MatchmakingAleatorio()
        self.monetizacion_strategy = MonetizacionPremium()

    def registrar_juego(self, tipo, titulo, desarrollador, precio, plataforma="PC", target="Teen"):
        # Usamos Factory para validar logica de negocio si es necesario, 
        # pero persistimos usando SQLAlchemy
        
        # Validacion simple usando el factory (lanza error si tipo es invalido)
        JuegoFactory.crear_juego(tipo, titulo, desarrollador, precio, plataforma, target)
        
        nuevo_juego = Game(
            titulo=titulo, 
            desarrollador=desarrollador, 
            precio=precio, 
            tipo=tipo,
            plataforma=plataforma,
            target=target
        )
        db.session.add(nuevo_juego)
        db.session.commit()
        
        # Invalidamos cache al agregar nuevo contenido
        self.listar_juegos.cache_clear()
        
        self.notificar_observers("juego_lanzado", {"juego": titulo, "plataforma": plataforma})
        return nuevo_juego

    @lru_cache(maxsize=32)
    def listar_juegos(self):
        print("[CACHE MISS] Consultando DB para listar juegos...")
        juegos = Game.query.all()
        return [j.obtener_info() for j in juegos]

    def buscar_partida(self, titulo_juego, user_id, es_competitivo=False):
        juego = Game.query.filter_by(titulo=titulo_juego).first()
        usuario = User.query.get(user_id)
        
        if not juego:
            return "Juego no encontrado."
        if not usuario:
            return "Usuario no encontrado."
        if usuario.is_banned:
            return "ERROR: Usuario baneado. No puedes buscar partida."
        
        self.notificar_observers("busqueda_partida", {"usuario": usuario.username, "juego": titulo_juego})

        # Instanciamos la clase logica para acceder a metodos especificos si fuera necesario
        # pero para matchmaking usamos la estrategia directamente con los datos de la DB
        if es_competitivo:
            estrategia = MatchmakingPorRango()
        else:
            estrategia = MatchmakingAleatorio()
            
        return estrategia.encontrar_partida(usuario, juego)

    def comprar_item(self, user_id, titulo_juego, item_name):
        juego_db = Game.query.filter_by(titulo=titulo_juego).first()
        usuario = User.query.get(user_id)
        
        if not juego_db or not usuario:
            return "Error: Juego o Usuario no encontrado."
        
        # Recreamos el objeto logico para verificar capacidades (Interfaces)
        juego_logico = JuegoFactory.crear_juego(juego_db.tipo, juego_db.titulo, juego_db.desarrollador, juego_db.precio)
        
        if isinstance(juego_logico, ConMicrotransacciones):
            # Buscar precio base del item
            items = self.obtener_items_venta(titulo_juego) # Usamos el metodo con cache
            item_data = next((i for i in items if i['name'] == item_name), None)
            
            if item_data:
                # Aplicar Estrategia de Monetizacion (Ej: Descuento si el usuario es VIP o evento)
                # Para demo, usamos MonetizacionDescuento aleatoriamente o fija
                estrategia_cobro = MonetizacionDescuento()
                precio_final = estrategia_cobro.calcular_precio(item_data['price'])
                
                nueva_compra = Purchase(user_id=user_id, game_title=titulo_juego, item_name=item_name)
                db.session.add(nueva_compra)
                db.session.commit()
                
                self.notificar_observers("compra_realizada", {"usuario": usuario.username, "juego": titulo_juego, "item": item_name, "precio": precio_final})
                return f"Compra exitosa: {item_name} por ${precio_final:.2f} (Precio base: ${item_data['price']})"
            else:
                return "Item no encontrado."
        else:
            return "Este juego no soporta microtransacciones."

    @lru_cache(maxsize=64)
    def obtener_items_venta(self, titulo_juego):
        print(f"[CACHE MISS] Generando items para {titulo_juego}...")
        juego_db = Game.query.filter_by(titulo=titulo_juego).first()
        if not juego_db: 
            return []
            
        juego_logico = JuegoFactory.crear_juego(juego_db.tipo, juego_db.titulo, juego_db.desarrollador, juego_db.precio)
        
        if isinstance(juego_logico, ConMicrotransacciones):
            return juego_logico.listar_items_venta()
        return []

    def calificar_juego(self, user_id, titulo_juego, puntuacion, comentario):
        juego_db = Game.query.filter_by(titulo=titulo_juego).first()
        usuario = User.query.get(user_id)
        
        if not juego_db: return "Juego no encontrado."
        
        # Verificar si ya califico
        existing_rating = Rating.query.filter_by(user_id=user_id, game_id=juego_db.id).first()
        if existing_rating:
            return "Ya has calificado este juego."

        juego_logico = JuegoFactory.crear_juego(juego_db.tipo, juego_db.titulo, juego_db.desarrollador, juego_db.precio)

        if isinstance(juego_logico, Calificable):
            nuevo_rating = Rating(user_id=user_id, game_id=juego_db.id, score=puntuacion, comment=comentario)
            db.session.add(nuevo_rating)
            db.session.commit()
            
            # Calcular promedio
            ratings = [r.score for r in juego_db.ratings]
            estrategia = PuntuacionPromedioSimple()
            promedio = estrategia.calcular_puntuacion_final(ratings)
            
            self.notificar_observers("calificacion_recibida", {"usuario": usuario.username, "juego": titulo_juego, "puntuacion": puntuacion})
            return f"Calificacion registrada. Nuevo promedio global: {promedio:.2f}"
        else:
            return "Este juego no se puede calificar."

    def verificar_actualizaciones(self, titulo_juego):
        juego_db = Game.query.filter_by(titulo=titulo_juego).first()
        if not juego_db: return "Juego no encontrado."
        
        juego_logico = JuegoFactory.crear_juego(juego_db.tipo, juego_db.titulo, juego_db.desarrollador, juego_db.precio)

        if isinstance(juego_logico, Actualizable):
            check = juego_logico.verificar_actualizacion()
            descarga = juego_logico.descargar_parche()
            self.notificar_observers("actualizacion_realizada", {"juego": titulo_juego})
            return f"{check} -> {descarga}"
        else:
            return "Este juego no tiene sistema de actualizaciones automaticas."

    def simular_sesion_juego(self, user_id, titulo_juego):
        """
        Demuestra el polimorfismo de las mecanicas de guardado/carga y el inicio del juego.
        """
        juego_db = Game.query.filter_by(titulo=titulo_juego).first()
        usuario = User.query.get(user_id)
        
        if not juego_db or not usuario:
            return ["Error: Juego o Usuario no encontrado."]
            
        # Instanciamos el juego concreto (Polimorfismo)
        juego_logico = JuegoFactory.crear_juego(juego_db.tipo, juego_db.titulo, juego_db.desarrollador, juego_db.precio)
        
        logs = []
        
        # 1. Iniciar (Polimorfico)
        logs.append(f"INICIO: {juego_logico.iniciar()}")
        
        # 2. Guardar Progreso (Polimorfico)
        # Simulamos datos de juego
        datos_simulados = {"nivel": 5, "score": 1500, "posicion": "x:10,y:20"}
        logs.append(f"GUARDADO: {juego_logico.guardar_progreso(usuario.id, datos_simulados)}")
        
        # 3. Cargar Progreso (Polimorfico)
        logs.append(f"CARGA: {juego_logico.cargar_progreso(usuario.id)}")
        
        # Notificar evento para logros
        self.notificar_observers("partida_terminada", {"usuario": usuario.username, "juego": titulo_juego})
        
        return logs

    def obtener_logros_usuario(self, user_id):
        from src.models.entities import Achievement
        return Achievement.query.filter_by(user_id=user_id).all()

    def obtener_promedio_juego(self, game_id):
        # Usamos la estrategia de puntuacion
        ratings = Rating.query.filter_by(game_id=game_id).all()
        scores = [r.score for r in ratings]
        
        estrategia = PuntuacionPromedioSimple()
        return estrategia.calcular_puntuacion_final(scores)
            
    # Metodos Admin
    def obtener_usuarios(self):
        return User.query.all()
        
    def banear_usuario(self, user_id):
        user = User.query.get(user_id)
        if user:
            user.is_banned = not user.is_banned # Toggle ban
            db.session.commit()
            return True
        return False
