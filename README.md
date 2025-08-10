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
