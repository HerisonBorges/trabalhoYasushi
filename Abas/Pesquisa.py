import customtkinter as ctk
from tkinter import *
from tkinter import messagebox
import openpyxl as xl

def executarPesquisa(self):
        termo = self.entryPesquisa.get().strip()  # Obtém o termo de pesquisa
        
        if not termo:
            messagebox.showwarning("Pesquisa", "Por favor, digite um termo para pesquisar")
            return
        
        try:
            # Carrega o arquivo Excel
            workbook = xl.load_workbook('Produtos.xlsx')
            sheet = workbook.active
            
            resultados = []
            
            # Procura em todas as linhas (exceto cabeçalho)
            for row in sheet.iter_rows(min_row=2, values_only=True):
                # Verifica se o termo está em qualquer campo (nome, código, fornecedor)
                if (termo.lower() in str(row[0]).lower() or  # Nome do produto
                    termo.lower() in str(row[1]).lower() or  # Código do Produto
                    termo.lower() in str(row[3]).lower()):   # Fornecedor
                    
                    resultados.append(f"Produto: {row[0]}\nCódigo: {row[1]}\nValidade: {row[2]}\nFornecedor: {row[3]}\nCategoria: {row[4]}\nObs: {row[5]}\n{'='*50}\n")
            
            if resultados:
                self.resultadosPesquisa.delete(1.0, END)  # Limpa resultados anteriores
                self.resultadosPesquisa.insert(END, "".join(resultados))
            else:
                messagebox.showinfo("Pesquisa", "Nenhum produto encontrado com esse termo")
                
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao pesquisar produtos:\n{str(e)}")

def setupPesquisa(self, tab):
    # aba de pesquisa
    lblTitulo = ctk.CTkLabel(tab, text="Pesquisar Produtos", 
                    font=("Century Gothic", 20, "bold"))
    lblTitulo.pack(pady=20)

    # campo de busca
    self.entryPesquisa = ctk.CTkEntry(
        tab,
        width=400,
        placeholder_text="Digite nome, codigo, ou fornecedor"
    )
    self.entryPesquisa.pack(pady=10)

    # botao de pesquisa
    botaoPesquisa = ctk.CTkButton(
        tab,
        text="BUSCAR",
        fg_color="#2ecc71",
        command=self.executarPesquisa
    )
    botaoPesquisa.pack(pady=10)

    # Area de resultados
    self.resultadosPesquisa = ctk.CTkTextbox(tab, width=650, height=300)
    self.resultadosPesquisa.pack(pady=20)
