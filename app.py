import streamlit as st

st.set_page_config(page_title="Laberinto Sorpresa", page_icon="🎮", layout="centered")

# Coordenadas iniciales del jugador y la meta en una matriz de 4x4
if "pos_y" not in st.session_state:
    st.session_state.pos_y = 3  # Fila inicial (abajo)
if "pos_x" not in st.session_state:
    st.session_state.pos_x = 0  # Columna inicial (izquierda)

# Meta fija en la esquina superior derecha
META_Y, META_X = 0, 3

# Obstáculos fijos (paredes o enemigos en el laberinto)
OBSTACULOS = [(1, 1), (2, 1), (1, 2)]

st.markdown("<h2 style='text-align: center;'>🕹️ Laberinto de Cumpleaños</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: gray;'>Usa los botones táctiles para moverte por el mapa y llegar a la flor 🌸</p>", unsafe_allow_html=True)

# Lógica de movimiento
def mover(dy, dx):
    nuevo_y = st.session_state.pos_y + dy
    nuevo_x = st.session_state.pos_x + dx
    # Limites del mapa (4x4)
    if 0 <= nuevo_y <= 3 and 0 <= nuevo_x <= 3:
        if (nuevo_y, nuevo_x) not in OBSTACULOS:
            st.session_state.pos_y = nuevo_y
            st.session_state.pos_x = nuevo_x
        else:
            st.toast("⚠️ ¡Ay! Te chocaste con un obstáculo del laberinto.", icon="❌")

# Dibujar el mapa visualmente en una cuadrícula
matriz = [["⬜", "⬜", "⬜", "⬜"] for _ in range(4)]
matriz[META_Y][META_X] = "🌸"  # Meta
for oy, ox in OBSTACULOS:
    matriz[oy][ox] = "🧱"      # Paredes/Bloques

# Poner al jugador en su posición actual
matriz[st.session_state.pos_y][st.session_state.pos_x] = "🐱"  # O pon tu emoji favorito

# Renderizar la cuadrícula en pantalla
for fila in matriz:
    cols = st.columns(4)
    for i, celda in enumerate(fila):
        with cols[i]:
            st.markdown(f"<h3 style='text-align: center; margin: 0;'>{celda}</h3>", unsafe_allow_html=True)

st.write("")

# Comprobar si ganó
if st.session_state.pos_y == META_Y and st.session_state.pos_x == META_X:
    st.balloons()
    st.success("🎉 ¡FELICIDADES! Llegaste a la meta y descubriste la sorpresa.")
    st.markdown("""
    ### 🎂 ¡Feliz Cumpleaños!
    Gracias por ser una gran amiga, por las risas y los buenos momentos. ¡Que la pases increíble hoy y siempre! 🎁
    """)
    if st.button("🔄 Volver a empezar"):
        st.session_state.pos_y = 3
        st.session_state.pos_x = 0
        st.rerun()
else:
    # Controles táctiles en cruz (como un D-Pad de celular)
    col1, col2, col3 = st.columns(3)
    with col2:
        if st.button("⬆️ Arriba"):
            mover(-1, 0)
            st.rerun()
            
    col4, col5, col6 = st.columns(3)
    with col4:
        if st.button("⬅️ Izq"):
            mover(0, -1)
            st.rerun()
    with col5:
        if st.button("⬇️ Abajo"):
            mover(1, 0)
            st.rerun()
    with col6:
        if st.button("➡️ Der"):
            mover(0, 1)
            st.rerun()
