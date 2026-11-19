import streamlit as st
import pandas as pd
import plotly.express as px
import openpyxl

path = 'censo_1872.xlsx'

df = pd.read_excel(path, engine='openpyxl')
df = df.drop_duplicates()

#somas e dfs
homens_livres_soma = df['homens_livres'].sum()
homens_livres = df['homens_livres']

homens_escravizados_soma = df['homens_escravizados'].sum()
homens_escravizados = df['homens_escravizados']

mulheres_livres_soma = df['mulheres_livres'].sum()
mulheres_livres = df['mulheres_livres']

mulheres_escravizadas_soma = df['mulheres_escravizadas'].sum()
mulheres_escravizadas = df['mulheres_escravizadas']

#percentual
percentual_homens_livres = homens_livres_soma / (homens_livres_soma + homens_escravizados_soma)
percentual_homens_escravizados = homens_escravizados_soma / (homens_livres_soma + homens_escravizados_soma)

percentual_mulheres_livres = mulheres_livres_soma / (mulheres_livres_soma + mulheres_escravizadas_soma)
percentual_mulheres_escravizadas = mulheres_escravizadas_soma / (mulheres_livres_soma + mulheres_escravizadas_soma)

#soma_total
soma_total = homens_livres_soma + homens_escravizados_soma + mulheres_escravizadas_soma + mulheres_livres_soma

df_final = pd.DataFrame(
    [
        {
        'homens_livres' : homens_livres_soma, 
        'homens_escravizados' : homens_escravizados_soma,
        'mulheres_livres' : mulheres_livres_soma, 
        'mulheres_escravizadas' : mulheres_escravizadas_soma,
        'soma_total' : soma_total, 
        'percentual_homens_livres' : percentual_homens_livres,
        'percentual_homens_escravizados' : percentual_homens_escravizados,
        'percentual_mulheres_livres' : percentual_mulheres_livres,
        'percentual_mulheres_escravizadas' : percentual_mulheres_escravizadas
        },       
    ]
)

#Streamlit
st.set_page_config(page_title="Censo 1872", layout="wide")

st.title("Censo 1872")
st.header("Informações em Tabela e Gráficos sobre o Censo de 1872")

st.markdown("Fonte de Dados : https://basedosdados.org/")

visualizacao = st.sidebar.selectbox(
    "Escolha uma opção de visualização 📊",
    ["Tabela", "Gráficos"]
)

if(visualizacao == "Tabela"):
    st.dataframe(df_final)

if(visualizacao == "Gráficos"):
    col1, col2 = st.columns(2)

    dados_pizza_homens = pd.DataFrame(
        [
        {"Homens": "homens livres", 'Percentual' : percentual_homens_livres},
        {"Homens": "homens escravizados", 'Percentual' : percentual_homens_escravizados},
        ]
    )

    dados_pizza_mulheres = pd.DataFrame(
        [
        {"Mulheres": "mulheres livres", 'Percentual' : percentual_mulheres_livres},
        {"Mulheres": "mulheres escravizadas", 'Percentual' : percentual_mulheres_escravizadas},
        ]
    )

    with col1:
        fig_pizza = px.pie(
            dados_pizza_homens,
            names="Homens",
            values="Percentual",
            title="Percentual de Homens Livres e Escravizados",
            color="Homens",
            color_discrete_map={"homens livres": "#FF6B6B", "homens escravizados": "#00F5D4"},
            template="plotly_dark"
        )
        fig_pizza.update_traces(textinfo="percent+label+value")
        fig_pizza.update_layout(paper_bgcolor="#111827", plot_bgcolor="#111827")
        st.plotly_chart(fig_pizza, use_container_width=True)

    with col2:
        fig_pizza = px.pie(
            dados_pizza_mulheres,
            names="Mulheres",
            values="Percentual",
            title="Percentual de Mulheres Livres e Escravizadas",
            color="Mulheres",
            color_discrete_map={"mulheres livres": "#FF6B6B", "mulheres escravizadas": "#00F5D4"},
            template="plotly_dark"
        )
        fig_pizza.update_traces(textinfo="percent+label+value")
        fig_pizza.update_layout(paper_bgcolor="#111827", plot_bgcolor="#111827")
        st.plotly_chart(fig_pizza, use_container_width=True)