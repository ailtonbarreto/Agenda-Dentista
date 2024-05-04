import streamlit as st
import pandas as pd
import gspread as gs
import datetime as dt
from gspread import Worksheet

#---------------------------------------------------------------------------------------------------------------------
#page config

st.set_page_config(layout="wide",initial_sidebar_state='expanded',page_icon='🦷',page_title="Agenda Dentista")


with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>",unsafe_allow_html = True)
 
    
st.sidebar.image("logo.png")
st.sidebar.divider()
st.sidebar.text("Teste")

tab1, tab2, tab3, tab4 = st.tabs(["Agenda","Marcar Atendimento","Cancelar Atendimento","Cadastrar Paciente"])


#---------------------------------------------------------------------------------------------------------------------
#dataframe Agenda

gc = gs.service_account("agenda-dentista.json")
url = 'https://docs.google.com/spreadsheets/d/10KkJC1pi90WPlcbPKzb2ZBTBj-hTyORAl0oL7Uz69DI/edit?usp=sharing'
sh = gc.open_by_url(url)
ws = sh.get_worksheet(0)
planilha = ws.get_all_values()
df = pd.DataFrame(planilha[1:], columns=planilha[0])

df["Data"] = pd.to_datetime(df["Data"]).dt.strftime("%d/%m/%Y")
df["Hora"] = pd.to_datetime(df["Hora"]).dt.strftime("%H:%M")

#---------------------------------------------------------------------------------------------------------------------
#dataframe pacientes

sh1 = gc.open_by_url(url)
ws1 = sh.get_worksheet(1)
planilha1 = ws1.get_all_values()
df_paciente = pd.DataFrame(planilha1[1:], columns=planilha1[0])


#---------------------------------------------------------------------------------------------------------------------
#dataframe procedimentos

sh2 = gc.open_by_url(url)
ws2 = sh.get_worksheet(2)
planilha2 = ws2.get_all_values()
df_procedimento = pd.DataFrame(planilha2[1:], columns=planilha2[0])

#---------------------------------------------------------------------------------------------------------------------
#insert row logic

with tab2:    
    entrada_paciente= st.selectbox("Paciente",df_paciente['Paciente'].unique())

    entrada_data = st.date_input("Data da Consulta","today",format= "DD/MM/YYYY")

    entrada_hora = st.time_input("Hora",value=dt.time(8, 0))

    entrada_procedimento = st.selectbox("Procedimento", df_procedimento["Procedimento"].unique())
    

    if st.button("AGENDAR"):
        ws: Worksheet = sh.get_worksheet(0)
        entrada_data = entrada_data.strftime("%Y-%m-%d")
        entrada_hora = entrada_hora.strftime("%H:%M")
        
        nova_linha = [entrada_data, entrada_hora, entrada_paciente, entrada_procedimento, "Agendado"]
            
        
        ws.append_row(nova_linha)
            
        st.success("Agendamento Salvo")

#---------------------------------------------------------------------------------------------------------------------
#Delete Row
   
with tab3:

    filtro_paciente = st.selectbox('Filtro Paciente',df["Paciente"].unique())
    
    filtro_data = st.date_input("Data da Consultas","today",format="DD/MM/YYYY")
    filtro_data = filtro_data.strftime("%d/%m/%Y")

    opcoes = df.query('Paciente == @filtro_paciente & Data == @filtro_data')
    
    
    opcoesdelete = opcoes.first_valid_index()
    col1, = st.columns(1)
    
    linha1 = opcoesdelete
    

    with col1:
        opcoes = opcoes.set_index("Paciente",inplace=False)
        st.dataframe(opcoes,use_container_width=True)
        if st.button("EXCLUIR ATENDIMENTO"):
            
            ws1: Worksheet = sh.get_worksheet(0)
        
            ws1.delete_rows(int(linha1) + 2)
        
            st.success("Atendimento Excluído Com Sucesso!")

 

#---------------------------------------------------------------------------------------------------------------------

with tab1:
    entrada_data_inicio = st.date_input("Data Inicio","today",format= "DD/MM/YYYY")
    entrada_data_inicio = entrada_data_inicio.strftime("%d/%m/%Y")
    
       
    df_agenda = df.query('Data == @entrada_data_inicio').sort_values('Hora')
    
    st.dataframe(df_agenda,use_container_width=True,hide_index=True)


with tab4:
    st.title("🚧 Em Construção")

#---------------------------------------------------------------------------------------------------------------------
#Style
    
hideimagebutton = """
    <style>
    [data-testid="StyledFullScreenButton"]
    {
    visibility: hidden;
    }
    </style>
"""
st.markdown(hideimagebutton,unsafe_allow_html=True)


hidecontainerdataframe = """
    <style>
    [class="stElementToolbar st-emotion-cache-13qcx58 e2wxzia1"]
    {
    visibility: hidden;
    }
    </style>
"""
st.markdown(hidecontainerdataframe,unsafe_allow_html=True)



