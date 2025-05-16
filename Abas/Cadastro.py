import customtkinter as ctk
from tkinter import *
from tkinter import messagebox
import openpyxl as xl
from datetime import datetime

import excel
import database

def Cadastro(tab):
        # Instrução para o usuário
        span = ctk.CTkLabel(tab, text="Por favor, preencha todos os campos do formulário!", font=("century gothic bold", 16), text_color=["#000", "#fff"]).place(x=50, y=20)

        excel.salvarExcel() # Chama a função para salvar os dados no Excel

        # Função para salvar os dados preenchidos no Excel
        def submit():
            # Obtém os valores dos campos
            nome_produto = nome_value.get()
            cod_produto = cod_produto_value.get()
            formatar_validade("")
            validar_validade(validade_value.get())
            validade = validade_value.get()
            fornecedor = fornecedor_value.get()
            unidade = unidade_value.get()#matheus
            categoria = categoria_combobox.get()
            obs = obs_entry.get(0.0, END)

            # Verifica se todos os campos obrigatórios estão preenchidos
            if not all([nome_produto, cod_produto, validade, fornecedor, unidade]):
                messagebox.showerror("Sistema", "Erro!\nPor favor preencha todos os dados")
                
            else:
                
                messagebox.showinfo("Sistema", "Dados salvos com sucesso")
                
                clear() # Limpa os campos após salvar
                database.salvarBancoDeDados(nome_produto, cod_produto, validade, fornecedor, categoria, unidade, obs) # Salva os dados no banco de dados
        
        # Função para limpar todos os campos do formulário
        def clear():
            nome_value.set("")
            cod_produto_value.set("")
            validade_value.set("")
            fornecedor_value.set("")
            unidade_value.set("")
            obs_entry.delete(0.0, END)

        # Variáveis de texto
        nome_value = StringVar()
        cod_produto_value = StringVar()
        validade_value = StringVar()
        fornecedor_value = StringVar()
        unidade_value = StringVar()

        # Entradas
        nome_entry = ctk.CTkEntry(tab, width=350, textvariable=nome_value, font=("Century Gothic bold", 16), fg_color="transparent")
        cod_produto_entry = ctk.CTkEntry(tab, width=200, textvariable=cod_produto_value, font=("Century Gothic bold", 16), fg_color="transparent")
        validade_entry = ctk.CTkEntry(tab, width=150, textvariable=validade_value, font=("Century Gothic bold", 16), fg_color="transparent")
        fornecedor_entry = ctk.CTkEntry(tab, width=200, textvariable=fornecedor_value, font=("Century Gothic bold", 16), fg_color="transparent")
        unidade_entry = ctk.CTkEntry(tab, width=150, textvariable=unidade_value, font=("Century Gothic bold", 16), fg_color="transparent")#matheus
        # Campo de unidade
        
        
        


        # Formata a validade para o padrão dd/mm/aaaa
        def formatar_validade(event): # "event" recebe o evento "<KeyRelease>" toda vez que o usuário digita
            validade = validade_value.get()
            
            if len(validade) == 8 and validade.isdigit(): 
                validade_value.set(f"{validade[:2]}/{validade[2:4]}/{validade[4:]}")
                validade_entry.icursor(len(validade_value.get()))  # Move o cursor para o final do texto
                
        # verifica se a validade está correta e se o produto não está vencido
        def validar_validade(valida):
            # Verifica se foi preenchido totalmente o campo validade
            try:
                dia = int(valida[0:2])
                mes = int(valida[3:5])
                ano = valida[6:10]
            except ValueError:
                messagebox.showerror("Sistema", "Erro!\nFormato de validade inválido.\nUse o formato dd/mm/aaaa")
                validade_value.set("")
                return
            
            data_atual = datetime.now()
            
            # Verifica se o campo validade está no formato correto
            if len(valida) != 10:
                messagebox.showerror("Sistema", "Erro!\nFormato de validade inválido.\nUse o formato dd/mm/aaaa")
                validade_value.set("")
            
            # Verifica se o dia, mês e ano são válidos
            elif dia > 31 or (mes > 12 or mes <= 0):
                messagebox.showerror("Sistema", "Erro!\nData inválida.\nVerifique o dia, mês e ano")
                validade_value.set("")
                
            # Verifica se o produto está vencido
            elif datetime.strptime(valida, "%d/%m/%Y") < data_atual:
                messagebox.showerror("Sistema", "Produto vencido!\nVerifique a validade do produto")
                validade_value.set("")
                
        # Se sair do compo validade, formata a validade
        validade_entry.bind("<KeyRelease>", formatar_validade)
        
        # Combobox
        categoria_combobox = ctk.CTkComboBox(tab, values=["Alimento", "Higiene", "Limpeza", "Outros"], font=("Century Gothic bold", 14), width=150)
        categoria_combobox.set("Alimento")

        # Entrada de observações
        obs_entry = ctk.CTkTextbox(tab, width=380, height=130, font=("Arial", 18), border_color="#aaa", border_width=2, fg_color="transparent")

        # Rótulos para cada campo
        lb_nome = ctk.CTkLabel(tab, text="Nome do Produto:", font=("century gothic bold", 16), text_color=["#000", "#fff"])
        lb_cod = ctk.CTkLabel(tab, text="Código do Produto:", font=("century gothic bold", 16), text_color=["#000", "#fff"])
        lb_validade = ctk.CTkLabel(tab, text="Validade:", font=("century gothic bold", 16), text_color=["#000", "#fff"])
        lb_categoria = ctk.CTkLabel(tab, text="Categoria", font=("century gothic bold", 16), text_color=["#000", "#fff"])
        lb_fornecedor = ctk.CTkLabel(tab, text="Fornecedor", font=("century gothic bold", 16), text_color=["#000", "#fff"])
        lb_unidade = ctk.CTkLabel(tab, text="Unidade", font=("century gothic bold", 16), text_color=["#000", "#fff"]) #matheus
        lb_obs = ctk.CTkLabel(tab, text="Observações", font=("century gothic bold", 16), text_color=["#000", "#fff"])

        # Botões para salvar e limpar os dados
        btn_submit = ctk.CTkButton(tab, text="SALVAR DADOS", command=submit, fg_color="#151", hover_color="#131").place(x=300, y=370)
        btn_clear = ctk.CTkButton(tab, text="LIMPAR CAMPOS", command=clear, fg_color="#555", hover_color="#333").place(x=500, y=370)

        # Posicionamento dos elementos na tela
        lb_nome.place(x=50, y=70)
        nome_entry.place(x=50, y=100)

        lb_cod.place(x=450, y=70)
        cod_produto_entry.place(x=450, y=100)

        lb_validade.place(x=300, y=140)
        validade_entry.place(x=300, y=170)

        lb_categoria.place(x=500, y=140)
        categoria_combobox.place(x=500, y=170)

        lb_fornecedor.place(x=50, y=140)
        fornecedor_entry.place(x=50, y=170)

        lb_unidade.place(x=50, y=200)
        unidade_entry.place(x=50, y=230)#matheus


        lb_obs.place(x=270, y=200)
        obs_entry.place(x=270, y=230)
