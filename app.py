import streamlit as st
import pandas as pd
import gspread as gs
import datetime as dt
from gspread import Worksheet

#---------------------------------------------------------------------------------------------------------------------
#page config

st.set_page_config(layout="wide",initial_sidebar_state='expanded',page_icon='🦷',page_title="Agenda Dentista")
st.sidebar.image("tooth.png")

tab1, tab2, tab3 = st.tabs(["Agenda","Marcar Atendimento","Editar Atendimento"])


#---------------------------------------------------------------------------------------------------------------------
#data sheet

gc = gs.service_account("agenda-dentista.json")
url = 'https://docs.google.com/spreadsheets/d/10KkJC1pi90WPlcbPKzb2ZBTBj-hTyORAl0oL7Uz69DI/edit?usp=sharing'
sh = gc.open_by_url(url)
ws = sh.get_worksheet(0)
planilha = ws.get_all_values()
df = pd.DataFrame(planilha[1:], columns=planilha[0])

df["Data"] = pd.to_datetime(df["Data"]).dt.strftime("%d/%m/%Y")
df["Hora"] = pd.to_datetime(df["Hora"]).dt.strftime("%H:%M")

#---------------------------------------------------------------------------------------------------------------------
#insert row logic

with tab2:    
    entrada_paciente= st.selectbox("Paciente",df['Paciente'].unique())

    entrada_data = st.date_input("Data da Consulta","today",format= "DD/MM/YYYY")

    entrada_hora = st.time_input("Hora")

    entrada_procedimento = st.selectbox("Procedimento", df["Procedimento"].unique())
    

    if st.button("ADICIONAR"):
        ws: Worksheet = sh.get_worksheet(0)
        entrada_data = entrada_data.strftime("%Y-%m-%d")
        entrada_hora = entrada_hora.strftime("%H:%M")
        # Criar uma nova linha com os dados inseridos
        nova_linha = [entrada_data,entrada_paciente,entrada_hora, entrada_procedimento, "Agendado"]
            
        # Adicionar a nova linha à planilha
        ws.append_row(nova_linha)
            
        st.success("Agendamento Salvo")
        

#---------------------------------------------------------------------------------------------------------------------

with tab1:
    entrada_data_agenda = st.date_input("Selecione a Data","today",format= "DD/MM/YYYY")
    entrada_data_agenda = entrada_data_agenda.strftime("%d/%m/%Y")
    df_agenda = df.query('Data == @entrada_data_agenda')
    
    st.table(df_agenda)
    
