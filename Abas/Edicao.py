import customtkinter as ctk
from tkinter import *
from tkinter import messagebox
import database
import util
from Abas import Pesquisa

# Função para configurar a aba de edição de produto
def setupEdicao(app, tab):
    # Container principal dentro da aba
    frame = ctk.CTkFrame(tab)
    frame.pack(padx=20, pady=20, fill="both", expand=True)

    # Título da aba
    titulo = ctk.CTkLabel(frame, text="EDITAR PRODUTO", font=("Century Gothic", 20, "bold"))
    titulo.grid(row=0, column=0, columnspan=3, pady=(0,20))

    # Critério de busca (rótulo + combobox)
    ctk.CTkLabel(frame, text="Buscar por:", anchor="w").grid(row=1, column=0, sticky="w")
    criterio_var = StringVar(value="cod_produto")  # Valor padrão
    criterio_combobox = ctk.CTkComboBox(frame, values=["cod_produto", "nome_produto", "fornecedor"], variable=criterio_var, width=150, state="readonly")
    criterio_combobox.grid(row=1, column=1, sticky="w", padx=(5,20))

    # Campo onde o usuário digita o valor a ser buscado
    app.entryBusca = ctk.CTkEntry(frame, width=300, placeholder_text="Digite o valor para buscar")
    app.entryBusca.grid(row=1, column=2, sticky="w")

    # Botão para carregar dados do produto
    btn_carregar = ctk.CTkButton(frame, text="CARREGAR", fg_color="#3498db",
                                 command=lambda: carregarDadosEdicao(app, criterio_var.get()))
    btn_carregar.grid(row=1, column=3, padx=(20,0))

    # Lista dos campos que poderão ser editados
    campos = ["nome_produto", "cod_produto", "validade", "fornecedor", "categoria", "unidade"]
    app.entries = {}  # Dicionário para guardar os widgets de entrada

    # Criação dos campos editáveis (labels + entries)
    for i, campo in enumerate(campos, start=2):
        lbl = ctk.CTkLabel(frame, text=campo.replace("_", " ").title() + ": ", anchor="w", width=120)
        lbl.grid(row=i, column=0, sticky="w", pady=5)

        entry = ctk.CTkEntry(frame, width=300)
        entry.grid(row=i, column=1, columnspan=3, sticky="w", pady=5)
        app.entries[campo] = entry  # Guarda o widget com o nome do campo como chave

    # Campo de observações (Textbox multilinha)
    lbl_obs = ctk.CTkLabel(frame, text="Observações:", anchor="nw", width=120)
    lbl_obs.grid(row=i+1, column=0, sticky="nw", pady=5)
    txt_obs = ctk.CTkTextbox(frame, width=300, height=80)
    txt_obs.grid(row=i+1, column=1, columnspan=3, sticky="w", pady=5)
    app.entries["observacoes"] = txt_obs  # Adiciona a textbox ao dicionário

    # Botão para salvar alterações
    btn_salvar = ctk.CTkButton(frame, text="SALVAR ALTERAÇÕES", fg_color="#15a",
                               command=lambda: salvarAlteracoes(app))
    btn_salvar.grid(row=i+2, column=0, columnspan=4, pady=10)
    
    frame.bind("<Button-1>", util.tirarFoco)  # Remove o foco do campo de busca ao clicar fora dele

# Função para buscar dados do produto e preencher os campos
def carregarDadosEdicao(app, criterio):
    valor = app.entryBusca.get()  # Obtém o valor digitado pelo usuário
    if not valor:
        messagebox.showwarning("Aviso", "Digite o valor para busca.")
        return

    # Busca no banco de dados com base no critério e valor fornecidos
    dados = database.selectCampo(criterio, valor)
    if dados:
        # Cria um dicionário com os dados antigos usando os nomes dos campos
        app.dados_antigos = dict(zip(
            ["nome_produto", "cod_produto", "validade", "fornecedor", "categoria", "unidade", "observacoes"],
            dados))
        
        # Preenche os campos da interface com os dados recuperados
        for campo, widget in app.entries.items():
            if campo == "observacoes":
                widget.delete("1.0", END)
                widget.insert("1.0", app.dados_antigos[campo])
            else:
                widget.delete(0, END)
                widget.insert(0, app.dados_antigos[campo])
    else:
        # Produto não encontrado
        messagebox.showerror("Erro", "Produto não encontrado.")

# Função para salvar os dados editados
def salvarAlteracoes(app):
    novos_dados = {}  # Dicionário com os novos dados preenchidos

    # Coleta os dados dos campos do formulário
    for campo, widget in app.entries.items():
        if campo == "observacoes":
            novos_dados[campo] = widget.get("1.0", END).strip()
        else:
            novos_dados[campo] = widget.get().strip()

    # Obtém o código original do produto (chave para atualização)
    cod_produto_original = app.dados_antigos.get("cod_produto")

    # Chama a função de atualização no banco
    sucesso = database.update(cod_produto_original, novos_dados)
    if sucesso:
        messagebox.showinfo("Sucesso", "Produto atualizado com sucesso!")
        app.dados_antigos = novos_dados.copy()  # Atualiza os dados armazenados como referência
        
        Pesquisa.mostrarProduto(database.selectAll(), app.produtos_frame, app.header)
        
    else:
        messagebox.showerror("Erro", "Erro ao atualizar o produto.")
