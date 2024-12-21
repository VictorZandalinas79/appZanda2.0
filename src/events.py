import streamlit as st
import pandas as pd

def init_events_state():
    if 'events' not in st.session_state:
        st.session_state.events = []
    if 'half' not in st.session_state:
        st.session_state.half = "Primera Parte"

def add_event(time, player, team, event_type):
    event = {
        "Tiempo": time,
        "Periodo": st.session_state.half,
        "Equipo": team,
        "Jugador": player,
        "Evento": event_type
    }
    st.session_state.events.append(event)

def render_events_table():
    if st.session_state.events:
        df = pd.DataFrame(st.session_state.events)
        st.dataframe(df)

EVENT_TYPES = [
    "Gol",
    "Asistencia",
    "Gol en Contra",
    "Tarjeta Amarilla",
    "Tarjeta Roja"
]