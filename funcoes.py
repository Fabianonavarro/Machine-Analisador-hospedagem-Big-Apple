import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from datetime import date
import time
from fpdf import FPDF
import textwrap
import plotly.express as px
import folium
import webbrowser

current_date = date.today()
formatted_date = current_date.strftime('%d/%m/%Y')
print(formatted_date)
print("\n")

# Definindo todas as funções e rotinas para o sistema  

def menu():
      
  menu = """\n
  ================ MENU ================
  [1]\tRespotas
  [2]\tGraficos
  [3]\tMapas dos hoteis
  [4]\tLocalizacao hospedagens
  [5]\tGerar Pdf
  []\t
  [7]\tSair
  => """
  return input(textwrap.dedent(menu))

# Dados     
# df = pd.read_csv( 'AB_NYC_2019.csv' )
URL = "https://drive.google.com/file/d/1fFdsWMPPY3dneNPQMfXFtbtTTdVlAitV/view?usp=drive_link"
df = pd.read_csv('https://drive.google.com/uc?export=download&id='+URL.split('/')[-2])
            
def respostas():
  print("1. Qual o valor médio do aluguel na cidade de Nova York?")    
  # calcular o valor medio do preco
  preco = df.loc[:, 'price']
  medio = np.mean (preco)
  print (f" O valor medio do aluguel e: U$ {medio:.2f}")
  print("----------------------------------------------------")    

  print("2. Quais os nomes das regiões que existem na cidade de Nova York?")
  regiao = df.loc[:, 'neighbourhood_group']
  unica =  pd.unique ( regiao)
  print (f"As regiões unicas são: {unica:} " )   
  print("----------------------------------------------------")
      
  print("3. Qual o valor do aluguel diário mais caro da cidade de Nova York?")
# calcular o valor maximo aluguel
  preco_aluguel = df.loc[:, 'price']
  preco_aluguel = np.amax( preco_aluguel)
  print (f" O valor Maxino do aluguel e: U$ {preco_aluguel:.2f}")
  print("----------------------------------------------------")
     
  print("4.Quais são as categorias de imóveis que estão cadastradas na cidade de Nova York?")
	# selecionar o tipo de sala
  room_type = df.loc[:, 'room_type']
	# mostrar os valores únicos
  room_unique = pd.unique( room_type )
	# mostrar os valores
  print(f"As categorias são:, {room_unique} ")
  print("----------------------------------------------------")
 
  print("5.Quantos usuários (Hosts) únicos cadastrados existem dentro da base de dados da cidade de Nova York?")

  q_usuario= df.loc[:, 'host_id']
  q_usuario = np.unique( q_usuario )
  q_usuario = len( q_usuario)

  print (f"A quantidade hosts únicos: {q_usuario}")
  print("----------------------------------------------------")
  
  print("6. Como é a variação do preços dos imóveis em NY?")

	# selecionar a coluna price
  price = df.loc[:, 'price']
	# calcular o desvio padrão
  desvio_padrao = np.std( price )

  print(f'Os preços estão disperson em U$ {desvio_padrao:.2f} em torno da média')
  print("----------------------------------------------------")
  return
  
def graficos():
  print("7. Existem mais imóveis baratos ou caros?")

# selecionar a coluna price e filtrar linhas
  linhas = df.loc[:, 'price'] < 1250
  price = df.loc[linhas, 'price']
  print("Existem mais de 20.000 imóveis com valor de aluguel de até U$ 100,00")
# desenhar o histograma

  plt.hist( price, bins=15);
  plt.show()
  
  print("Aguardem proximo grafico")
  time.sleep(2)
  
  print("----------------------------------------------------------------------")
  
  print('''8. Qual a distribuição do número de Reviews?
	Existem imóveis com muitos e outro com poucos reviews?''')
	# selecionar a coluna price e filtrar linhas
  linhas = df.loc[:, 'number_of_reviews'] < 300
  number_reviews = df.loc[linhas, 'number_of_reviews']
  print("Existem quase 30.000 imóveis com até 10 avaliações.")
	# desenhar o histograma
  plt.hist(number_reviews , bins=12);
  plt.show()
  return
  
def mapas(): # para facilitar ja foi gerador o testemapa
    webbrowser.open_new_tab('testemap.html')
    return

def localizacao(): # para facilitar ja foi gerador o teste
  webbrowser.open_new_tab('teste.html')
  return  

def pdf():
  current_date = date.today()
  formatted_date = current_date.strftime('%d/%m/%Y')

#dados para os calculos 
  preco = df.loc[:, 'price']
  medio = np.mean (preco)

  regiao = df.loc[:, 'neighbourhood_group']
  unica =  pd.unique ( regiao)

  preco_aluguel = df.loc[:, 'price']
  preco_aluguel = np.amax( preco_aluguel)

  room_type = df.loc[:, 'room_type']
	# mostrar os valores únicos
  room_unique = pd.unique( room_type )

  q_usuario= df.loc[:, 'host_id']
  q_usuario = np.unique( q_usuario )
  q_usuario = len( q_usuario)

  price = df.loc[:, 'price']
	# calcular o desvio padrão
  desvio_padrao = np.std( price )
  
# Gerar PDF
  pdf = FPDF()
  pdf.add_page()
  pdf.set_font("Arial")
  pdf.image("template.png", x=0, y=0 )

  pdf.text(115, 33, formatted_date)

  pdf.text(100, 147, f" U$ {medio:.2f}")     
  pdf.text(100, 155, f" {unica:} " )   
  pdf.text(100, 164, f" U$ {preco_aluguel:.2f}")
  pdf.text(100, 172, f" {room_unique}" )
  pdf.text(100, 184, f" {q_usuario}")
  pdf.text(100, 192, f" {desvio_padrao:.2f} ")

  pdf.output("respostas.pdf")
  print("Respostas em PDF gerado com sucesso!")
  return ()

def sair():
  print("saindo")
 # break
  return
