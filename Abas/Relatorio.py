import customtkinter as ctk
from tkinter import *
from tkinter import messagebox

def setupRelatorios(self, tab):
        # Aba de relatórios
        lblTitulo = ctk.CTkLabel(tab, text="RELATÓRIOS", font=("Century Gothic", 20, "bold"))
        lblTitulo.pack(pady=20)

        # Opções de relatório
        self.comboRelatorios = ctk.CTkComboBox(
            tab,
            values=["Produtos próximos do vencimento", "Todos os produtos", "Por categoria"]
        )
        self.comboRelatorios.pack(pady=10)

        # Botão para gerar relatorio
        botaoGerar = ctk.CTkButton(
            tab,
            text="GERAR RELATÓRIO",
            fg_color="#9b59b6",
            command=gerarRelatorio
        )
        botaoGerar.pack(pady=20)

def gerarRelatorio():
    # Implementar lógica para gerar relatórios
    messagebox.showinfo("Relatórios", "Funcionalidade de relatórios será implementada em breve")