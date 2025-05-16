# IDEIAS PARA MELHORIAS:
'''
1. Criar uma área de remoção de produtos.
2. Criar uma área de edição de produtos.
    2.1. Edição de tipos de produtos.
    2.2. Edição das observações.
3. Criar uma área de pesquisa de produtos.
4. Criar área de login para conectar ao banco de dados.
5. Criar uma área de relatórios.

'''

# REGISTRO DE PROGRESSO
'''
12/05/2025
1 - Arquivo excel criado com comandos do excel
2 - Arquivo database criado com comandos do psycopg2
3 - Pasta Abas criada com os arquivos de cada aba

A FAZER:
1 - Implementar lógica para carregar dados para edição (se possível).
2 - Implementar lógica para gerar relatórios.

'''

# Importações necessárias
import customtkinter as ctk
from tkinter import *
from tkinter import messagebox
import openpyxl as xl
from datetime import datetime

import database  # Módulo para interagir com o banco de dados
from Abas import Cadastro, Pesquisa, Edicao, Relatorio  # Importa as funções das abas

# Configurações de aparência globais do customtkinter
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

# Classe principal do aplicativo
class App(ctk.CTk):
    def __init__(self): 
        super().__init__()
        self.layout_config()      # Configuração da janela
        self.appearence()         # Menu para alterar tema
        self.criarContainers()    # Cria os containers da interface
        self.CriandoAbas()        # Cria e organiza as abas

    # Configuração da janela principal
    def layout_config(self):
        self.title("Sistema de Gestão de Produtos")
        self.geometry("820x650")  # Define o tamanho da janela

    # Menu de seleção de tema (Dark ou Light)
    def appearence(self):
        self.lb_apm = ctk.CTkLabel(self, text="Tema", bg_color="transparent", text_color=['#000', "#fff"])
        self.lb_apm.place(x=50, y=580)

        self.opt_apm = ctk.CTkOptionMenu(self, values=["Dark", "Light"], command=self.change_apm)
        self.opt_apm.place(x=50, y=610)
    
    # Criação dos containers principais da interface
    def criarContainers(self):
        # Container do título (barra superior)
        self.containerTitulo = ctk.CTkFrame(self, width=820, height=50, corner_radius=0, fg_color="teal")
        self.containerTitulo.place(x=0, y=0)

        # Título centralizado
        title = ctk.CTkLabel(self.containerTitulo, text="Sistema de Gestão de Produtos", 
                             font=("Century Gothic Bold", 24), text_color="#fff", bg_color="transparent")
        title.place(relx=0.5, rely=0.5, anchor="center")

        # Container para as abas abaixo do título
        self.containerAbas = ctk.CTkFrame(self, width=800, height=510, corner_radius=0, fg_color="transparent")
        self.containerAbas.place(x=10, y=60)  # Pequeno espaçamento para não encostar nas bordas
    
    # Criação e organização das abas
    def CriandoAbas(self):
        # Criação do widget de abas
        self.tabview = ctk.CTkTabview(self.containerAbas, width=800, height=510)
        self.tabview.place(x=0, y=0)

        # Adiciona as abas
        self.tabview.add("Cadastro")
        self.tabview.add("Pesquisa")
        self.tabview.add("Edição")
        self.tabview.add("Relatórios")

        # Inicializa os conteúdos de cada aba
        Cadastro.Cadastro(self.tabview.tab("Cadastro"))  # Aba Cadastro
        self.executarPesquisa = lambda: Pesquisa.executarPesquisa(self)  # Prepara função de pesquisa
        Pesquisa.setupPesquisa(self, self.tabview.tab("Pesquisa"))  # Aba Pesquisa
        Edicao.setupEdicao(self, self.tabview.tab("Edição"))  # Aba Edição
        Relatorio.setupRelatorios(self, self.tabview.tab("Relatórios"))  # Aba Relatórios

    # Muda o tema da aplicação
    def change_apm(self, nova_aparencia):
        ctk.set_appearance_mode(nova_aparencia)

#from Login import login
#login()

from Login import login  # importa sua função de login
from app import App        # importa a classe App (sua janela principal)

def main():
    # Abre o login e espera o resultado
    logado = login()
    if logado:
        # Se login OK, abre o app principal
        app = App()
        app.mainloop()
    else:
        print("Login não realizado. Saindo...")

if __name__ == "__main__":
    main()
