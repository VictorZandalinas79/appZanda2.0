from datetime import datetime, timedelta
import streamlit as st

def init_timer_state():
    if 'timer_running' not in st.session_state:
        st.session_state.timer_running = False
    if 'start_time' not in st.session_state:
        st.session_state.start_time = None
    if 'elapsed_time' not in st.session_state:
        st.session_state.elapsed_time = timedelta()

def toggle_timer():
    if not st.session_state.timer_running:
        st.session_state.start_time = datetime.now()
        st.session_state.timer_running = True
    else:
        st.session_state.timer_running = False
        if st.session_state.start_time:
            st.session_state.elapsed_time += datetime.now() - st.session_state.start_time

def get_current_time():
    if st.session_state.timer_running:
        return st.session_state.elapsed_time + (datetime.now() - st.session_state.start_time)
    return st.session_state.elapsed_time

def format_time(td):
    total_seconds = int(td.total_seconds())
    minutes = total_seconds // 60
    seconds = total_seconds % 60
    return f"{minutes:02d}:{seconds:02d}"