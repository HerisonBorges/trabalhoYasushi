'''
IDEIAS PARA MELHORIAS:

1. Criar uma área de remoção de produtos.
2. Criar uma área de edição de produtos.
    2.1. Edição de tipos de produtos.
    2.2. Edição das observações.
3. Criar uma área de pesquisa de produtos.
4. Criar área de login para conectar ao banco de dados.
5. Criar uma área de relatórios.
6. Recomendar nome de produtos e fornecedores baseados no que já existe.
'''
'''
12/05/2025

1 - Arquivo excel criado com comandos do excel
2- Arquivo database criado com comandos do psycopg2
3- Pasta Abas criada com os arquivos de cada aba

O QUE PRECISA SER FEITO, ANEXADO A IDEIAS DE MELHORAIS

1 - IMPLEMENTAR LOGICA PARA CARREGAR DADOS PARA EDIÇÃO, ( SE FOR POSSIVEL)
2- IMPLEMENTAR LOGICA PARA GERAR RELATORIOS

13/052025
1- IMPLEMENTAR LOGICA DE UNIDADE POR PRODUTO #MATHEUS

14/05/2025
2- IMPLEMENTADO A TELA DE LOGIN  #MATHEUS
'''

#Criar caixa container para preenchimento, título e geral

import customtkinter as ctk
from tkinter import *
from tkinter import messagebox
import openpyxl as xl
from datetime import datetime

'''
Se quiser importar um arquivo, basta fazer assim: import nome_arquivo ou import nome_da_pasta.nome_arquivo
Se quiser importar uma função específica, faça assim: from nome_arquivo import nome_funcao ou from nome_da_pasta.nome_arquivo import nome_funcao
'''

import database  
from Abas import Cadastro
from Abas import Pesquisa
from Abas import Edicao
from Abas import Relatorio

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self): 
        super().__init__()
        self.layout_config()
        self.appearence()
        self.criarContainers()
        self.CriandoAbas()

    def layout_config(self):
        self.title("Sistema de Gestão de Produtos")
        self.geometry("700x500")

    def appearence(self):
        self.lb_apm = ctk.CTkLabel(self, text="Tema", bg_color="transparent", text_color=['#000', "#fff"]).place(x=50, y=430)
        self.opt_apm = ctk.CTkOptionMenu(self, values=["Dark", "Light"], command=self.change_apm).place(x=50, y=460)
    
    def criarContainers(self):
        self.containerTitulo = ctk.CTkFrame(self, width=700, height=50, corner_radius=0, fg_color="teal")
        self.containerTitulo.place(x=0, y=0)

        title = ctk.CTkLabel(self.containerTitulo, text="Sistema de Gestão de Produtos", 
                             font=("century gothic bold", 24), text_color="#fff", bg_color="transparent")
        title.place(relx=0.5, rely=0.5, anchor="center")

        self.containerAbas = ctk.CTkFrame(self, width=700, height=450, corner_radius=0, fg_color="transparent")
        self.containerAbas.place(x=0, y=50)
    
    def CriandoAbas(self):
        self.tabview = ctk.CTkTabview(self.containerAbas, width=700, height=450)
        self.tabview.place(x=0, y=0)

        self.tabview.add("Cadastro")
        self.tabview.add("Pesquisa")
        self.tabview.add("Edição")
        self.tabview.add("Relatórios")

        Cadastro.Cadastro(self.tabview.tab("Cadastro"))
        self.executarPesquisa = lambda: Pesquisa.executarPesquisa(self)
        Pesquisa.setupPesquisa(self, self.tabview.tab("Pesquisa"))
        Edicao.setupEdicao(self, self.tabview.tab("Edição"))
        Relatorio.setupRelatorios(self, self.tabview.tab("Relatórios"))

    def change_apm(self, nova_aparencia):
        ctk.set_appearance_mode(nova_aparencia)

if __name__ == "__main__":
    from Login import login
    login()
