# 🎮 Plataforma Gaming Backend – Flask

Bienvenido al repositorio backend de nuestra **plataforma gaming**.  
Este sistema está diseñado para ofrecer una experiencia completa a jugadores, integrando:

- Biblioteca de juegos
- Logros
- Matchmaking multijugador
- Compras in-game
- Actualizaciones automáticas
- Análisis de comportamiento

---

## 🚀 Características principales

### 📚 Biblioteca de juegos
- Gestión de títulos, géneros, desarrolladores y plataformas.
- Integración con la **API de RAWG** para obtener metadatos enriquecidos.

### 🏆 Sistema de logros
- Registro y visualización de logros por juego y usuario.
- Soporte para porcentajes de desbloqueo y progresión.

### 🤝 Matchmaking multijugador
- Algoritmo de emparejamiento basado en **nivel tipo Elo**, disponibilidad y preferencias.
- Implementado con el patrón **Strategy** para intercambiar lógicas de emparejamiento dinámicamente.


### 🛒 Compras in-game
- Gestión de transacciones virtuales e inventario de usuario.
- Pasarela de pagos simulada.

### 🔄 Actualizaciones automáticas
- Sistema de notificaciones y sincronización de versiones de juegos y DLC.

### 📊 Análisis de jugadores
- Seguimiento de actividad, tiempo de juego, logros desbloqueados y comportamiento en partidas.

---

## 📈 Sistema de ranking

El matchmaking utiliza un **sistema de puntuación tipo Elo** para evaluar la habilidad de cada jugador y generar emparejamientos equilibrados.

- **Elo**: Método clásico de puntuación usado en ajedrez y muchos juegos competitivos. Ajusta el puntaje de cada jugador después de cada partida en función del resultado y la diferencia de nivel.

- **TrueSkill**: Implementación avanzada desarrollada por Microsoft, que considera la incertidumbre en la habilidad del jugador y permite un emparejamiento más preciso en entornos multijugador.

**Funcionamiento básico:**
1. Todos los jugadores inician con un puntaje base.
2. Después de cada partida, el puntaje se ajusta según el resultado (victoria, derrota o empate) y la dificultad del oponente.
3. El sistema de matchmaking prioriza emparejar jugadores con puntajes similares para mantener la competitividad.

El sistema está desacoplado mediante el patrón **Strategy**, lo que permite cambiar entre **Elo** y **TrueSkill** sin modificar el núcleo de la aplicación.


---

## 🧱 Tecnologías utilizadas

- **Backend:** Flask + SQLite 
- **Base de datos:** PostgreSQL  
- **API externa:** RAWG Video Games Database  
- **Autenticación:** JWT  
- **Diseño modular:** POO avanzada con patrones **Strategy**, **Factory** y **Observer**

---

## 📦 Instalación

```bash
git clone https://github.com/JAGR1792/Sistema-de-videojuegos.git
cd plataforma-gaming-flask
python -m venv venv
source venv/bin/activate  # o venv\Scripts\activate en Windows
pip install -r requirements.txt
