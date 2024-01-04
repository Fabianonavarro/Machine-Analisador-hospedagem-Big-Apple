'''
Projeto banco dados
Desenvolvido por Fabiano de Lima Navarro
'''
# Importando as bibliotecas
from funcoes import *
import textwrap

# Definindo Main com as opcoes  

while True:
    
    opcao = menu()
    
    if opcao == "1":
        respostas()
    
    elif opcao =="2":
        graficos()

    elif opcao =="3":
        mapas()
        
    elif opcao =="4":
        localizacao()

    elif opcao =="5":
        pdf()
        
    elif opcao == "7":
        sair()
        break
else:
    print("Operação inválida, por favor selecione novamente a operação desejada.")
