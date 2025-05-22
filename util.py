import customtkinter as ctk
from tkinter import *
from tkinter import messagebox
from datetime import datetime

#FUNÇÕES GERAIS
def tirarFoco(event):
    widget_atual = event.widget.focus_get()
    if widget_atual and isinstance(widget_atual, ctk.CTkEntry):
        widget_atual.focus_set()  # Mantém o foco no campo de entrada
    else:
        event.widget.focus_set()  # Mantém o foco no widget atual
        
def clear(var):
    for val in var:
        if isinstance(val, StringVar):
            val.set("")
        else:
            val.delete(0.0, END)
            
def centralizar(largura, altura, janela):
    largura_janela = largura
    altura_janela = altura

    pos_x = int(janela.winfo_screenwidth() / 2 - largura_janela / 2)
    pos_y = int(janela.winfo_screenheight() / 2 - altura_janela / 2)

    janela.geometry(f"{largura_janela}x{altura_janela}+{pos_x}+{pos_y}")

#FUNÇÕES DE VALIDAÇÃO DE CADASTRO
#Função que formata automaticamente a data de validade para o padrão dd/mm/aaaa
def formatar_validade(event, validade_value, validade_entry):
    validade = validade_value.get()
    if len(validade) == 8 and validade.isdigit():
        validade_value.set(f"{validade[:2]}/{validade[2:4]}/{validade[4:]}")
        validade_entry.icursor(len(validade_value.get()))  # Move o cursor para o fim

# Valida se a data é válida e se o produto está vencido
def validar_validade(valida, validade_value):
    try:
        dia = int(valida[0:2])
        mes = int(valida[3:5])
    except ValueError:
        messagebox.showerror("Sistema", "Erro!\nFormato de validade inválido.\nUse o formato dd/mm/aaaa")
        validade_value.set("")
        return "erro"

    data_atual = datetime.now()

    # Checa o comprimento
    if len(valida) != 10:
        messagebox.showerror("Sistema", "Erro!\nFormato de validade inválido.\nUse o formato dd/mm/aaaa")
        validade_value.set("")
        return "erro"

    # Verifica validade dos valores
    elif dia > 31 or (mes > 12 or mes <= 0):
        messagebox.showerror("Sistema", "Erro!\nData inválida.\nVerifique o dia, mês e ano")
        validade_value.set("")
        return "erro"

    # Verifica se a data está vencida
    elif datetime.strptime(valida, "%d/%m/%Y") < data_atual:
        messagebox.showerror("Sistema", "Produto vencido!\nVerifique a validade do produto")
        validade_value.set("")
        return "erro"