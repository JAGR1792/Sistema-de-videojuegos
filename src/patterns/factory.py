from src.models.implementaciones import JuegoAccion, JuegoEstrategia, JuegoRol, JuegoDeportivo

class JuegoFactory:
    @staticmethod
    def crear_juego(tipo, titulo, desarrollador, precio, plataforma="PC", target="Teen"):
        # Nota: Las clases concretas deben actualizarse para aceptar estos nuevos parametros
        # Por simplicidad, los inyectaremos despues de la creacion o asumiremos que el constructor base los maneja
        # si actualizamos las implementaciones para llamar a super().__init__ correctamente.
        
        juego = None
        if tipo == "accion":
            juego = JuegoAccion(titulo, desarrollador, precio)
        elif tipo == "estrategia":
            juego = JuegoEstrategia(titulo, desarrollador, precio)
        elif tipo == "rol":
            juego = JuegoRol(titulo, desarrollador, precio)
        elif tipo == "deportes":
            juego = JuegoDeportivo(titulo, desarrollador, precio)
        else:
            raise ValueError(f"Tipo de juego desconocido: {tipo}")
            
        # Asignamos los atributos extra manualmente ya que las implementaciones heredan de Videojuego
        # y Videojuego ya tiene estos campos en su __init__ actualizado, pero las implementaciones
        # podrian no estar pasando todos los argumentos al super().
        juego.plataforma = plataforma
        juego.target = target
        return juego
