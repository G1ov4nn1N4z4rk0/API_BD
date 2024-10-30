#pip install streamlit
#pip install streamlit_option_menu

import streamlit as st 
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu
from query import conexao

# *** primeira consulta / atualizacoes de dados
# consultar os dados
query = "SELECT * FROM tb_carro"

# carregar os dados
df = conexao(query)

# botao para atualizar
# se apertar o botao atualizara os dados da tabela do banco de dados 
if st.button("atualizar dados"):
    df = conexao(query)


# ************************* ESTRUTURA  LATERAL DE FILTROS ***********************************
#sidebar = barra lateral
#header("selecione o filtro") cabecario
st.sidebar.header("selecione o filtro")

marca = st.sidebar.multiselect("marca selecionada", # nome do seletor
                               options = df["marca"].unique(), # agrupar as informcaoes 
                               default=df["marca"].unique(), # as marcas 

                               )

modelo = st.sidebar.multiselect("modelo selecionado",
                                options= df["modelo"].unique(),
                                default=df["modelo"].unique()
                                )

ano = st.sidebar.multiselect("ano selecionado",
                             options = df["ano"].unique(),
                             default = df["ano"].unique()
                                )

valor = st.sidebar.multiselect(" valor selecionado",
                             options = df["valor"].unique(),
                             default = df["valor"].unique()
                                )


numero_vendas = st.sidebar.multiselect("numero de vendas selecionado",
                                       options = df["numero_vendas"].unique(),
                                       default = df["numero_vendas"].unique()
                                       )
cor = st.sidebar.multiselect("cor selecionado",
                             options = df["cor"].unique(),
                             default = df["cor"].unique()
                                )

# aplicar esses filtros selecionados
df_selecionado = df [
    (df['marca'].isin(marca)) &  # esta verificando se existe a marca com o nome usado pelo usuario
                                   # select * from tb_carro where marca = marca_p ****** cada linha esta fazendo isso
    (df["modelo"].isin(modelo)) &
    (df["ano"].isin(ano)) &
    (df["valor"].isin(valor)) &
    (df["cor"].isin(cor)) & 
    (df["numero_vendas"].isin(numero_vendas)) 
]

# ********* EXIBIR  VALORES MEDIOS - ESTATISTICAS 
# primeiro definir a funcao

def Home():
   with st.expander("tabela"): #cria uma caixa expansivel com um titulo
        mostrardados = st.multiselect('filter: ', df_selecionado, default=[])

    #verifica se o usuario selecionou as colunas para exibir
        if mostrardados:
        #exibe os dados filtrados pelas colunas selecionadas
           st.write(df_selecionado[mostrardados])
#verifica se o dataframe filtrado (df_selecionado) nao esta vazio
   if not df_selecionado.empty:
       venda_total = df_selecionado["numero_vendas"].sum()
       venda_media = df_selecionado["numero_vendas"].mean()
       venda_mediana = df_selecionado["numero_vendas"].median()

## cria tres colunas para exibir os totais calculos
       total1, total2, total3 = st.columns(3, gap="large")

       with total1:
           st.info("valor total de vendas dos carros", icon='📌')
           st.metric(label="total",value=f"{venda_total:,.0f}")

       with total2:
           st.info("valor medio das vendas", icon='📌')
           st.metric(label="media", value=f"{venda_media:,.0f}")

       with total3:
           st.info("valor mediano dos carros", icon='📌')
           st.metric(label="mediana", value=f"{venda_mediana:,.0f}")

    #exibe um aviso se nao houver dados selecionados
   else:
       st.warning("nenhum dado disponivel com os filtros selecionados")
    
#insere uma linha de divisioria para separar as secoes
   st.markdown("""-------------------------------------""")
       
#******************************** GRAFICOS **********************************
def graficos(df_selecionado):
    if df_selecionado.empty:
        st.warning("nenhum dado disponivel para gerar graficos")
        #interrompe a funcao , pq nao tem motivo pra continuar executando se nao tem dado
        return
    

    # criacao dos graficos
    #4 abas -> grafico de barras, grafico de linhas , grafico de pizza e dispersao
    graf1, graf2, graf3, graf4 = st.tabs(["grafico de barras","grafico de linhas","grafico de pizza","grafico de dispersao"])



Home()



