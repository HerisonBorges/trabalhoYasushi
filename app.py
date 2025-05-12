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
import excel
import database
from Abas import Cadastro
from Abas import Pesquisa
from Abas import Edicao
from Abas import Relatorio

# Aparência do sistema
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self): 
        super().__init__() # Inicializa a janela principal da classe App
        self.layout_config() # Define tamanho e título da janela
        self.appearence() # Adiciona seletor de tema (claro, escuro, sistema)
        self.criarContainers() # Cria os containers para o título e abas
        self.CriandoAbas() # cria as abas do sistema

    def layout_config(self):
        self.title("Sistema de Gestão de Produtos") # Define o título da janela
        self.geometry("700x500") # Define o tamanho da janela (largura x altura)

    def appearence(self):
        self.lb_apm = ctk.CTkLabel(self, text="Tema", bg_color="transparent", text_color=['#000', "#fff"]).place(x=50, y=430)
        self.opt_apm = ctk.CTkOptionMenu(self, values=["Dark", "Light"], command=self.change_apm).place(x=50, y=460)
    
    def criarContainers(self):
        #Container para o título
        self.containerTitulo = ctk.CTkFrame(self, width=700, height=50, corner_radius=0, fg_color="teal")
        self.containerTitulo.place(x=0, y=0)

        #Adicionando o título no container
        title = ctk.CTkLabel(self.containerTitulo, text="Sistema de Gestão de Produtos", 
                             font=("century gothic bold", 24), text_color="#fff", bg_color="transparent")
        title.place(relx=0.5, rely=0.5, anchor="center")

        #Container para as abas
        self.containerAbas = ctk.CTkFrame(self, width=700, height=450, corner_radius=0, fg_color="transparent")
        self.containerAbas.place(x=0, y=50)
    
    def CriandoAbas(self):
        # criando 4 abas na interface
        self.tabview = ctk.CTkTabview(self.containerAbas, width=700, height=450)
        self.tabview.place(x=0, y=0)

        # adicionando as abas
        self.tabview.add("Cadastro") # Aqui sera a aba para cadastrar os produtos
        self.tabview.add("Pesquisa")
        self.tabview.add("Edição")
        self.tabview.add("Relatórios")

        # configurando cada aba
        Cadastro.Cadastro(self.tabview.tab("Cadastro"))
        self.executarPesquisa = lambda: Pesquisa.executarPesquisa(self) #criando a função de pesquisa (lambda é como se fosse um def mas sem nome)
        Pesquisa.setupPesquisa(self,self.tabview.tab("Pesquisa"))
        Edicao.setupEdicao(self, self.tabview.tab("Edição"))
        Relatorio.setupRelatorios(self, self.tabview.tab("Relatórios"))

    def change_apm(self, nova_aparencia):
        ctk.set_appearance_mode(nova_aparencia)

if __name__ == "__main__":
    app = App()
    app.mainloop()