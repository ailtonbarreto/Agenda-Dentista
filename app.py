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


sh1 = gc.open_by_url(url)
ws1 = sh.get_worksheet(1)
planilha1 = ws.get_all_values()
df_paciente = pd.DataFrame(planilha[1:], columns=planilha[0])

#---------------------------------------------------------------------------------------------------------------------
#insert row logic

with tab2:    
    entrada_paciente= st.selectbox("Paciente",df_paciente['Paciente'].unique())

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
        
# with tab3:

    # filtro_cliente = st.selectbox('Cliente',df["Cliente"].unique())

    # opcoes = df.query('Ano == @filtro_ano & Mês == @filtro_mes & Cliente == @filtro_cliente')
    
    # opcoes = opcoes.drop(columns=["Data","Ano","Mês"])
    
    # opcoesdelete = opcoes.index.tolist()
    # col1, col2 = st.columns([1, 10])
    
    # with col1:
    #     linha1 = st.selectbox("Selecionar linha", opcoesdelete)
    
    
    
    # with col2:
    #     if st.button("EXCLUIR ENTRADA"):
            
    #         ws1: Worksheet = sh.get_worksheet(0)
        
    #         ws1.delete_rows(int(linha1) + 2)
        
    #         st.success("Entrada Excluída Com Sucesso!")

    #     opcoes["Valor"] = opcoes["Valor"].apply(lambda x: f'R$ {x:,.2f}')
    #     opcoes["Data Vencimento"] =pd.to_datetime(opcoes["Data Vencimento"]).dt.strftime('%d/%m/%Y')

#---------------------------------------------------------------------------------------------------------------------

with tab1:
    entrada_data_agenda = st.date_input("Selecione a Data","today",format= "DD/MM/YYYY")
    entrada_data_agenda = entrada_data_agenda.strftime("%d/%m/%Y")
    df_agenda = df.query('Data == @entrada_data_agenda')
    
    st.table(df_agenda)
    
