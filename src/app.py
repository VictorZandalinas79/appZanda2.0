import streamlit as st
from timer import init_timer_state, toggle_timer, get_current_time, format_time
from teams import init_teams_state, render_team_setup
from events import init_events_state, add_event, render_events_table, EVENT_TYPES
from exporters.google_sheets import export_to_sheets
from exporters.pdf_export import create_match_report
import pandas as pd
import os

def init_session_state():
    init_timer_state()
    init_teams_state()
    init_events_state()

def render_timer():
    col1, col2, col3 = st.columns([2,1,1])
    with col1:
        current_time = get_current_time()
        st.header(f"⏱️ {format_time(current_time)}")
    
    with col2:
        st.button("Start/Stop", on_click=toggle_timer)
    
    with col3:
        st.session_state.half = st.selectbox("Periodo", ["Primera Parte", "Segunda Parte"])
    
    return current_time

def render_export_section():
    st.header("Exportar Datos")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Exportar a Google Sheets"):
            if st.session_state.events:
                events_df = pd.DataFrame(st.session_state.events)
                sheets_url = export_to_sheets(
                    events_df, 
                    st.session_state.players,
                    st.session_state.get('rival_name', 'Rival')
                )
                st.success(f"Datos exportados! [Abrir Spreadsheet]({sheets_url})")
            else:
                st.warning("No hay eventos para exportar")
    
    with col2:
        if st.button("Exportar a PDF"):
            if st.session_state.events:
                events_df = pd.DataFrame(st.session_state.events)
                pdf_file = create_match_report(
                    events_df,
                    st.session_state.players,
                    st.session_state.get('rival_name', 'Rival')
                )
                
                with open(pdf_file, "rb") as file:
                    st.download_button(
                        label="Descargar PDF",
                        data=file,
                        file_name=pdf_file,
                        mime="application/pdf"
                    )
                # Clean up the file after download
                os.remove(pdf_file)
            else:
                st.warning("No hay eventos para exportar")

def main():
    st.title("⚽ Registro de Partido")
    init_session_state()

    current_time = render_timer()
    
    st.header("Configuración de Equipos")
    rival_name = render_team_setup()
    if rival_name:
        st.session_state.rival_name = rival_name

    st.header("Registro de Eventos")
    render_event_form(current_time)

    st.header("Eventos del Partido")
    render_events_table()
    
    render_export_section()

if __name__ == "__main__":
    main()