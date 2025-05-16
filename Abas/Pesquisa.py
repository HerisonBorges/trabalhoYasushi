# Importações necessárias
import customtkinter as ctk
from tkinter import *
from tkinter import messagebox
import database  # Módulo responsável pelas operações com o banco de dados

# Função que realiza a busca com base no termo digitado
def executarPesquisa(self):
    # Captura o termo de pesquisa e remove espaços em branco
    termo = self.entryPesquisa.get().strip()
    
    # Verifica se o usuário digitou algo
    if not termo:
        messagebox.showwarning("Pesquisa", "Por favor, digite um termo para pesquisar")
        return
    
    try:
        # Busca produtos no banco de dados usando o termo
        resultados = database.buscar_produto_por_termo(termo)
        
        # Habilita o campo de resultados para edição temporária
        self.resultadosPesquisa.configure(state="normal")
        self.resultadosPesquisa.delete(1.0, END)  # Limpa o conteúdo atual
        
        if resultados:
            texto = ""
            for row in resultados:
                # Monta o texto com os dados dos produtos encontrados
                texto += (f"Produto: {row[0]}\n"
                          f"Código: {row[1]}\n"
                          f"Validade: {row[2]}\n"
                          f"Fornecedor: {row[3]}\n"
                          f"Categoria: {row[4]}\n"
                          f"Unidade: {row[5]}\n"
                          f"Observações: {row[6]}\n"
                          + "="*50 + "\n")
            # Insere o texto no campo de resultados
            self.resultadosPesquisa.insert(END, texto)
        else:
            # Exibe mensagem se nenhum produto for encontrado
            self.resultadosPesquisa.insert(END, "Nenhum produto encontrado com esse termo.")
        
        # Desabilita o campo novamente para edição
        self.resultadosPesquisa.configure(state="disabled")
            
    except Exception as e:
        # Em caso de erro, exibe uma mensagem de erro
        messagebox.showerror("Erro", f"Erro ao pesquisar produtos:\n{str(e)}")

# Função para configurar a aba de pesquisa
def setupPesquisa(self, tab):
    # Frame principal dentro da aba
    frame = ctk.CTkFrame(tab)
    frame.pack(padx=20, pady=20, fill="both", expand=True)

    # Título da aba
    lblTitulo = ctk.CTkLabel(frame, text="Pesquisar Produtos", font=("Century Gothic", 20, "bold"))
    lblTitulo.grid(row=0, column=0, columnspan=3, pady=(0, 20))

    # Campo de entrada para o termo de pesquisa
    self.entryPesquisa = ctk.CTkEntry(frame, width=400, placeholder_text="Digite nome, código ou fornecedor")
    self.entryPesquisa.grid(row=1, column=0, sticky="w", padx=(0, 10))

    # Botão de busca que chama a função executarPesquisa
    botaoPesquisa = ctk.CTkButton(frame, text="BUSCAR", fg_color="#2ecc71", command=lambda: executarPesquisa(self))
    botaoPesquisa.grid(row=1, column=1, sticky="w")
    
    # Campo de texto que exibe os resultados da busca (inicialmente desabilitado)
    self.resultadosPesquisa = ctk.CTkTextbox(frame, width=650, height=300, state="disabled")
    self.resultadosPesquisa.grid(row=2, column=0, columnspan=3, pady=20)
