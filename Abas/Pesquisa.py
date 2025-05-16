import customtkinter as ctk
from tkinter import *
from tkinter import messagebox
import database  

def executarPesquisa(self):
    termo = self.entryPesquisa.get().strip()
    
    if not termo:
        messagebox.showwarning("Pesquisa", "Por favor, digite um termo para pesquisar")
        return
    
    try:
        resultados = database.buscar_produto_por_termo(termo)
        
        self.resultadosPesquisa.configure(state="normal")
        self.resultadosPesquisa.delete(1.0, END)
        
        if resultados:
            texto = ""
            for row in resultados:
                texto += (f"Produto: {row[0]}\n"
                          f"Código: {row[1]}\n"
                          f"Validade: {row[2]}\n"
                          f"Fornecedor: {row[3]}\n"
                          f"Categoria: {row[4]}\n"
                          f"Unidade: {row[5]}\n"
                          f"Observações: {row[6]}\n"
                          + "="*50 + "\n")
            self.resultadosPesquisa.insert(END, texto)
        else:
            self.resultadosPesquisa.insert(END, "Nenhum produto encontrado com esse termo.")
        
        self.resultadosPesquisa.configure(state="disabled")
            
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao pesquisar produtos:\n{str(e)}")

def setupPesquisa(self, tab):
    frame = ctk.CTkFrame(tab)
    frame.pack(padx=20, pady=20, fill="both", expand=True)

    lblTitulo = ctk.CTkLabel(frame, text="Pesquisar Produtos", font=("Century Gothic", 20, "bold"))
    lblTitulo.grid(row=0, column=0, columnspan=3, pady=(0, 20))

    self.entryPesquisa = ctk.CTkEntry(frame, width=400, placeholder_text="Digite nome, código ou fornecedor")
    self.entryPesquisa.grid(row=1, column=0, sticky="w", padx=(0, 10))

    botaoPesquisa = ctk.CTkButton(frame, text="BUSCAR", fg_color="#2ecc71", command=lambda: executarPesquisa(self))
    botaoPesquisa.grid(row=1, column=1, sticky="w")

    self.resultadosPesquisa = ctk.CTkTextbox(frame, width=650, height=300, state="disabled")
    self.resultadosPesquisa.grid(row=2, column=0, columnspan=3, pady=20)
