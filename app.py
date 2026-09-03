import streamlit as st

st.set_page_config(page_title="Misión Cumpleaños", page_icon="🎂", layout="centered")

# Inicializar el estado del juego en la web
if "paso" not in st.session_state:
    st.session_state.paso = 1

st.markdown("<h1 style='text-align: center; color: #333;'>🎂 Misión Cumpleaños: El Laberinto 🎂</h1>", unsafe_allow_html=True)
st.write("")

if st.session_state.paso == 1:
    st.info("🌧️ Estás atrapada en un laberinto nocturno bajo la lluvia. ¡Debes guiarte por los pasillos para llegar a la flor y desbloquear la sorpresa!")
    st.write("### Nivel 1: El inicio del pasillo")
    
    col1, col2, col3 = st.columns(3)
    with col2:
        if st.button("⬆️ Avanzar"):
            st.session_state.paso = 2
            st.rerun()

elif st.session_state.paso == 2:
    st.warning("⚠️ ¡Cuidado! Hay un obstáculo móvil patrullando la zona. Elige tu ruta con inteligencia.")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅️ Ir por la izquierda"):
            st.error("¡Oh no! Te topaste con el enemigo. Volviendo al inicio del laberinto...")
            st.session_state.paso = 1
            st.rerun()
    with col2:
        if st.button("➡️ Ir por la derecha (Seguro)"):
            st.session_state.paso = 3
            st.rerun()

elif st.session_state.paso == 3:
    st.success("✨ ¡Muy bien! Ya esquivaste el peligro y estás a un solo paso de la meta.")
    
    col1, col2, col3 = st.columns(3)
    with col2:
        if st.button("🌸 ¡Llegar a la Flor y Ganar!"):
            st.session_state.paso = 4
            st.rerun()

elif st.session_state.paso == 4:
    # Pantalla de Victoria: Tarjeta estilo la imagen de cumpleaños
    st.balloons()
    
    st.markdown("<h2 style='text-align: center; color: #ff69b4;'>¡FELIZ CUMPLEAÑOS!</h2>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center; color: #666;'>¡Te deseo lo mejor en tu día!</h4>", unsafe_allow_html=True)
    
    # Dibujo visual del pastel con emojis
    st.markdown("""
    <div style="text-align: center; font-size: 70px; margin: 20px 0;">
    🎂🕯️
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("<p style='text-align: center; font-size: 17px; color: #444;'><b>Gracias por todos los momentos, las risas y las historias que compartimos.</b></p>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 15px; color: #666;'>De parte de todo el grupo: ¡Feliz cumpleaños y que la pases increíble!</p>", unsafe_allow_html=True)
    
    st.write("")
    col1, col2, col3 = st.columns(3)
    with col2:
        if st.button("🔄 Jugar otra vez"):
            st.session_state.paso = 1
            st.rerun()
