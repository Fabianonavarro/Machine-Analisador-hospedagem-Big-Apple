import pandas as pd
import matplotlib.pyplot as plt
from datetime import date
from fpdf import FPDF
import os
import streamlit as st
import requests
from io import BytesIO
import streamlit.components.v1 as components

# Definindo a URL dos dados
URL = "https://drive.google.com/uc?export=download&id=1fFdsWMPPY3dneNPQMfXFtbtTTdVlAitV"

def download_file(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.content

def carregar_dados():
    # Mostra a mensagem de carregamento
    with st.spinner('Carregando dados...'):
        data = download_file(URL)
        df = pd.read_csv(BytesIO(data))
    return df

def formatar_respostas():
    resposta_style = """
    <style>
    .resposta {
        background-color: #cfe2f3; /* Fundo Azul muito claro */
        border-radius: 5px;
        padding: 15px;
        margin-bottom: 10px;
    }
    .resposta p {
        font-size: 22px; /* Tamanho da fonte das respostas */
        color: #2986cc; /* Texto Azul */
        font-weight: bold;
    }
   
    </style>
    """
    return resposta_style

def respostas(df):
    st.markdown(formatar_respostas(), unsafe_allow_html=True)
    
    st.markdown("""
    <div class="resposta">
        <p class="pergunta">1. Qual o valor médio do aluguel na cidade de Nova York?</p>
        <p>U$ {:.2f}</p>
    </div>
    """.format(df['price'].mean()), unsafe_allow_html=True)
    
    st.markdown("""
    <div class="resposta">
        <p class="pergunta">2. Quais os nomes das regiões que existem na cidade de Nova York?</p>
        <p>{}</p>
    </div>
    """.format(', '.join(df['neighbourhood_group'].unique())), unsafe_allow_html=True)

    st.markdown("""
    <div class="resposta">
        <p class="pergunta">3. Qual o valor do aluguel diário mais caro da cidade de Nova York?</p>
        <p>U$ {:.2f}</p>
    </div>
    """.format(df['price'].max()), unsafe_allow_html=True)
    
    st.markdown("""
    <div class="resposta">
        <p class="pergunta">4. Quais são as categorias de imóveis que estão cadastradas na cidade de Nova York?</p>
        <p>As categorias são: {}</p>
    </div>
    """.format(', '.join(df['room_type'].unique())), unsafe_allow_html=True)
    
    st.markdown("""
    <div class="resposta">
        <p class="pergunta">5. Quantos usuários (Hosts) únicos cadastrados existem dentro da base de dados da cidade de Nova York?</p>
        <p>{}</p>
    </div>
    """.format(df['host_id'].nunique()), unsafe_allow_html=True)
    
    st.markdown("""
    <div class="resposta">
        <p class="pergunta">6. Como é a variação dos preços dos imóveis em NY?</p>
        <p>Os preços estão dispersos em U$ {:.2f} em torno da média</p>
    </div>
    """.format(df['price'].std()), unsafe_allow_html=True)

def salvar_grafico(data, bins, cor, titulo, xlabel, ylabel, nome_arquivo):
    plt.figure(figsize=(10, 6))
    plt.hist(data, bins=bins, color=cor, edgecolor='black')
    plt.title(titulo)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.grid(True)
    plt.savefig(nome_arquivo)
    plt.close()

def graficos(df):
    st.write("### Gráficos:")
    salvar_grafico(df[df['price'] < 1250]['price'], 15, 'blue', "Distribuição dos Imóveis Baratos", "Preço", "Número de Imóveis", 'grafico_imoveis_baratos.png')
    salvar_grafico(df['number_of_reviews'], 12, 'green', "Distribuição do Número de Reviews", "Número de Reviews", "Número de Imóveis", 'grafico_numero_reviews.png')

    st.image('grafico_imoveis_baratos.png', caption='Distribuição dos Imóveis Baratos', use_column_width=True)
    st.image('grafico_numero_reviews.png', caption='Distribuição do Número de Reviews', use_column_width=True)

def pdf(df):
    formatted_date = date.today().strftime('%d/%m/%Y')
    medio = df['price'].mean()
    unica = ', '.join(df['neighbourhood_group'].unique())
    preco_aluguel = df['price'].max()
    room_unique = ', '.join(df['room_type'].unique())
    q_usuario = df['host_id'].nunique()
    desvio_padrao = df['price'].std()

    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.image("template.png", x=0, y=0, w=210, h=297)
    pdf.set_font("Arial", size=12)
    pdf.text(87, 33, f" {formatted_date}")
    pdf.text(65, 147, f" U$ {medio:.2f}")
    pdf.text(65, 155, f" {unica}")
    pdf.text(65, 164, f" U$ {preco_aluguel:.2f}")
    pdf.text(65, 174, f" {room_unique}")
    pdf.text(65, 184, f" {q_usuario}")
    pdf.text(65, 192, f" {desvio_padrao:.2f}")

    pdf.ln(20)
    if os.path.isfile('grafico_imoveis_baratos.png') and os.path.isfile('grafico_numero_reviews.png'):
        pdf.text(0, 217, "Imóveis Baratos")
        pdf.image('grafico_imoveis_baratos.png', x=0, y=223, w=100)
        pdf.text(100, 217, "Número de Reviews")
        pdf.image('grafico_numero_reviews.png', x=90, y=223, w=100)
    else:
        st.write("Um ou ambos os arquivos de gráficos não foram encontrados.")

    pdf_output_path = "respostas.pdf"
    if os.path.isfile(pdf_output_path):
        os.remove(pdf_output_path)
    pdf.output(pdf_output_path)
    st.write("PDF gerado com sucesso!")

    with open(pdf_output_path, "rb") as f:
        st.download_button(label="Baixar PDF", data=f, file_name=pdf_output_path)

def mapas():
    st.write("### Mapa dos Hotéis")
    with open('testemap.html', 'r') as f:
        map_html = f.read()
    components.html(map_html, height=600, scrolling=True)

def localizacao():
    st.write("### Localização das Hospedagens")
    with open('teste.html', 'r') as f:
        location_html = f.read()
    components.html(location_html, height=600, scrolling=True)

def pagina_inicial():
    st.title("Bem-vindo ao Analisador de Aluguéis de Nova York!")
    st.write("""
    New York City, conhecida como Big Apple, é uma cidade vibrante e cheia de vida. 
    Este aplicativo permite que você analise dados de aluguéis em Nova York.

    Utilize o menu lateral para:

    - Ver respostas às perguntas sobre os dados
    - Visualizar gráficos relacionados aos aluguéis
    - Explorar mapas dos hotéis e localizações de hospedagens
    - Gerar um PDF com as análises
    """)

    st.write("""
    <div style="background-color: #f5f5f5; padding: 10px; border-radius: 5px; position: fixed; bottom: 0; left: 0; width: 100%; text-align: center; box-shadow: 0 -2px 5px rgba(0, 0, 0, 0.1);">
        <p style="margin: 0; font-size: 16px; color: #0033cc;"><strong>Desenvolvido por Fabiano</strong></p>
        <p style="margin: 0;">
            📫 <a href="https://www.dio.me/users/nav_info_suporte" style="color: #0033cc; text-decoration: none;">Portfólio</a> |
            <a href="https://github.com/Fabianonavarro" style="color: #0033cc; text-decoration: none;">GitHub</a> |
            <a href="https://www.linkedin.com/in/fabiano-de-navarro" style="color: #0033cc; text-decoration: none;">LinkedIn</a>
        </p>
    </div>
    """, unsafe_allow_html=True)

def main():
    st.sidebar.title("Navegação")
    page = st.sidebar.radio("Escolha uma opção:", ["Página Inicial", "Respostas", "Gráficos", "PDF", "Mapas", "Localização"])
    
    if page == "Página Inicial":
        pagina_inicial()
    else:
        df = carregar_dados()
        if page == "Respostas":
            respostas(df)
        elif page == "Gráficos":
            graficos(df)
        elif page == "PDF":
            pdf(df)
        elif page == "Mapas":
            mapas()
        elif page == "Localização":
            localizacao()

if __name__ == "__main__":
    main()
