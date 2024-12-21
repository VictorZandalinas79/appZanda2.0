from fpdf import FPDF
import pandas as pd
from datetime import datetime

class MatchReport(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'Reporte del Partido', 0, 1, 'C')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Página {self.page_no()}', 0, 0, 'C')

def create_match_report(events_df, players_list, rival_name):
    pdf = MatchReport()
    pdf.add_page()
    
    # Title and Date
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(0, 10, f'Partido vs {rival_name}', 0, 1, 'C')
    pdf.set_font('Arial', '', 12)
    pdf.cell(0, 10, f'Fecha: {datetime.now().strftime("%d/%m/%Y")}', 0, 1, 'C')
    pdf.ln(10)
    
    # Players List
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, 'Lista de Jugadores', 0, 1)
    pdf.set_font('Arial', '', 12)
    for player in players_list:
        pdf.cell(0, 8, f'• {player}', 0, 1)
    pdf.ln(10)
    
    # Events Table
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, 'Eventos del Partido', 0, 1)
    pdf.set_font('Arial', '', 10)
    
    # Table headers
    cols_width = [25, 25, 30, 40, 30]
    headers = ['Tiempo', 'Periodo', 'Equipo', 'Jugador', 'Evento']
    for i, header in enumerate(headers):
        pdf.cell(cols_width[i], 10, header, 1)
    pdf.ln()
    
    # Table content
    for _, row in events_df.iterrows():
        for i, col in enumerate(row):
            pdf.cell(cols_width[i], 10, str(col), 1)
        pdf.ln()
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"reporte_partido_{timestamp}.pdf"
    pdf.output(filename)
    return filename