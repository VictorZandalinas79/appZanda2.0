import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import csv

def init_session_state():
    if 'timer_running' not in st.session_state:
        st.session_state.timer_running = False
    if 'start_time' not in st.session_state:
        st.session_state.start_time = None
    if 'elapsed_time' not in st.session_state:
        st.session_state.elapsed_time = timedelta()
    if 'half' not in st.session_state:
        st.session_state.half = "Primera Parte"
    if 'events' not in st.session_state:
        st.session_state.events = []
    if 'players' not in st.session_state:
        st.session_state.players = []

def toggle_timer():
    if not st.session_state.timer_running:
        st.session_state.start_time = datetime.now()
        st.session_state.timer_running = True
    else:
        st.session_state.timer_running = False
        if st.session_state.start_time:
            st.session_state.elapsed_time += datetime.now() - st.session_state.start_time

def format_time(td):
    total_seconds = int(td.total_seconds())
    minutes = total_seconds // 60
    seconds = total_seconds % 60
    return f"{minutes:02d}:{seconds:02d}"

def main():
    st.title("⚽ Registro de Partido")
    init_session_state()

    # Timer section
    col1, col2, col3 = st.columns([2,1,1])
    with col1:
        if st.session_state.timer_running:
            current_time = st.session_state.elapsed_time + (datetime.now() - st.session_state.start_time)
        else:
            current_time = st.session_state.elapsed_time
        st.header(f"⏱️ {format_time(current_time)}")
    
    with col2:
        st.button("Start/Stop", on_click=toggle_timer)
    
    with col3:
        st.session_state.half = st.selectbox("Periodo", ["Primera Parte", "Segunda Parte"])

    # Team setup
    st.header("Configuración de Equipos")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Equipo Local")
        uploaded_file = st.file_uploader("Importar jugadores (CSV)", type="csv")
        if uploaded_file is not None:
            st.session_state.players = pd.read_csv(uploaded_file)["Jugador"].tolist()
            st.write("Jugadores importados:", st.session_state.players)
    
    with col2:
        st.subheader("Equipo Visitante")
        rival_name = st.text_input("Nombre del rival")

    # Event registration
    st.header("Registro de Eventos")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        team = st.radio("Equipo", ["Local", "Visitante"])
    
    with col2:
        event_type = st.selectbox("Tipo de Evento", 
            ["Gol", "Asistencia", "Gol en Contra", "Tarjeta Amarilla", "Tarjeta Roja"])
    
    with col3:
        if team == "Local":
            player = st.selectbox("Jugador", st.session_state.players if st.session_state.players else [""])
        else:
            player = st.text_input("Jugador Rival")

    if st.button("Registrar Evento"):
        if player and event_type:
            event = {
                "Tiempo": format_time(current_time),
                "Periodo": st.session_state.half,
                "Equipo": team,
                "Jugador": player,
                "Evento": event_type
            }
            st.session_state.events.append(event)

    # Events table
    st.header("Eventos del Partido")
    if st.session_state.events:
        df = pd.DataFrame(st.session_state.events)
        st.dataframe(df)

if __name__ == "__main__":
    main()