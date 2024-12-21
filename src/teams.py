import streamlit as st
import pandas as pd

def init_teams_state():
    if 'players' not in st.session_state:
        st.session_state.players = []

def load_team_players(uploaded_file):
    if uploaded_file is not None:
        try:
            st.session_state.players = pd.read_csv(uploaded_file)["Jugador"].tolist()
            return True
        except Exception as e:
            st.error(f"Error al cargar el archivo: {str(e)}")
            return False
    return False

def render_team_setup():
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Equipo Local")
        uploaded_file = st.file_uploader("Importar jugadores (CSV)", type="csv")
        if uploaded_file is not None:
            if load_team_players(uploaded_file):
                st.write("Jugadores importados:", st.session_state.players)
    
    with col2:
        st.subheader("Equipo Visitante")
        return st.text_input("Nombre del rival")