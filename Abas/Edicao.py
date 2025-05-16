import customtkinter as ctk
from tkinter import *
from tkinter import messagebox
import database

def setupEdicao(app, tab):
    # Container principal dentro da aba
    frame = ctk.CTkFrame(tab)
    frame.pack(padx=20, pady=20, fill="both", expand=True)

    # Título
    titulo = ctk.CTkLabel(frame, text="EDITAR PRODUTO", font=("Century Gothic", 20, "bold"))
    titulo.grid(row=0, column=0, columnspan=3, pady=(0,20))

    # Critério de busca
    ctk.CTkLabel(frame, text="Buscar por:", anchor="w").grid(row=1, column=0, sticky="w")
    criterio_var = StringVar(value="cod_produto")
    criterio_combobox = ctk.CTkComboBox(frame, values=["cod_produto", "nome_produto", "fornecedor"], variable=criterio_var, width=150)
    criterio_combobox.grid(row=1, column=1, sticky="w", padx=(5,20))

    # Campo de busca
    app.entryBusca = ctk.CTkEntry(frame, width=300, placeholder_text="Digite o valor para buscar")
    app.entryBusca.grid(row=1, column=2, sticky="w")

    # Botão carregar
    btn_carregar = ctk.CTkButton(frame, text="CARREGAR", fg_color="#3498db",
                                 command=lambda: carregarDadosEdicao(app, criterio_var.get()))
    btn_carregar.grid(row=1, column=3, padx=(20,0))

    # Campos editáveis com labels e entries
    campos = ["nome_produto", "cod_produto", "validade", "fornecedor", "categoria", "unidade"]
    app.entries = {}

    for i, campo in enumerate(campos, start=2):
        lbl = ctk.CTkLabel(frame, text=campo.replace("_", " ").title() + ": ", anchor="w", width=120)
        lbl.grid(row=i, column=0, sticky="w", pady=5)

        entry = ctk.CTkEntry(frame, width=300)
        entry.grid(row=i, column=1, columnspan=3, sticky="w", pady=5)
        app.entries[campo] = entry

    # Observações como Textbox com label
    lbl_obs = ctk.CTkLabel(frame, text="Observações:", anchor="nw", width=120)
    lbl_obs.grid(row=i+1, column=0, sticky="nw", pady=5)
    txt_obs = ctk.CTkTextbox(frame, width=300, height=80)
    txt_obs.grid(row=i+1, column=1, columnspan=3, sticky="w", pady=5)
    app.entries["observacoes"] = txt_obs

    # Botão salvar
    btn_salvar = ctk.CTkButton(frame, text="SALVAR ALTERAÇÕES", fg_color="#15a",
                               command=lambda: salvarAlteracoes(app))
    btn_salvar.grid(row=i+2, column=0, columnspan=4, pady=10)

def carregarDadosEdicao(app, criterio):
    valor = app.entryBusca.get()
    if not valor:
        messagebox.showwarning("Aviso", "Digite o valor para busca.")
        return

    dados = database.buscar_produto_por_campo(criterio, valor)
    if dados:
        app.dados_antigos = dict(zip(
            ["nome_produto", "cod_produto", "validade", "fornecedor", "categoria", "unidade", "observacoes"],
            dados))
        for campo, widget in app.entries.items():
            if campo == "observacoes":
                widget.delete("1.0", END)
                widget.insert("1.0", app.dados_antigos[campo])
            else:
                widget.delete(0, END)
                widget.insert(0, app.dados_antigos[campo])
    else:
        messagebox.showerror("Erro", "Produto não encontrado.")

def salvarAlteracoes(app):
    novos_dados = {}
    for campo, widget in app.entries.items():
        if campo == "observacoes":
            novos_dados[campo] = widget.get("1.0", END).strip()
        else:
            novos_dados[campo] = widget.get().strip()

    cod_produto_original = app.dados_antigos.get("cod_produto")

    sucesso = database.atualizar_produto(cod_produto_original, novos_dados)
    if sucesso:
        messagebox.showinfo("Sucesso", "Produto atualizado com sucesso!")
        app.dados_antigos = novos_dados.copy()
    else:
        messagebox.showerror("Erro", "Erro ao atualizar o produto.")
