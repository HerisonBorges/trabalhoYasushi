# Importações necessárias
import customtkinter as ctk
from tkinter import *
from tkinter import messagebox
import database  # módulo para interações com o banco de dados
import util  # módulo com funções auxiliares
from Abas import Pesquisa

# Função principal da aba Cadastro
def Cadastro(self, tab):
    # Mensagem inicial para o usuário
    span = ctk.CTkLabel(tab, text="Por favor, preencha todos os campos do formulário!", 
                        font=("century gothic bold", 16), text_color=["#000", "#fff"]).place(x=50, y=20)
    
    # Função chamada ao clicar em "SALVAR DADOS"
    def submit():
        # Captura os valores inseridos nos campos
        nome_produto = nome_value.get()
        cod_produto = cod_produto_value.get()
        util.formatar_validade("", validade_value, validade_entry)  # Garante que a validade seja formatada corretamente
        sucesso = util.validar_validade(validade_value.get(), validade_value)  # Valida a validade
        validade = validade_value.get()
        fornecedor = fornecedor_value.get()
        unidade = unidade_value.get()  # Matheus
        categoria = categoria_combobox.get()
        obs = obs_entry.get(0.0, END)  # Captura as observações

        # Verifica se todos os campos obrigatórios foram preenchidos
        if sucesso == "erro":
            pass
        elif not all([nome_produto, cod_produto, validade, fornecedor, unidade]):
            messagebox.showerror("Sistema", "Erro!\nPor favor preencha todos os dados")
        else:
            messagebox.showinfo("Sistema", "Dados salvos com sucesso")
            util.clear([nome_value, cod_produto_value, validade_value, fornecedor_value, unidade_value, obs_entry])  # Limpa os campos
            database.insert(  # Salva no banco
                nome_produto, cod_produto, validade, fornecedor, categoria, unidade, obs
            )
        
        Pesquisa.mostrarProduto(database.selectAll(), self.produtos_frame, self.header)

    # Variáveis que armazenam os dados digitados
    nome_value = StringVar()
    cod_produto_value = StringVar()
    validade_value = StringVar()
    fornecedor_value = StringVar()
    unidade_value = StringVar()

    # Campos de entrada (Entry)
    nome_entry = ctk.CTkEntry(tab, width=350, textvariable=nome_value, font=("Century Gothic bold", 16), fg_color="transparent")
    cod_produto_entry = ctk.CTkEntry(tab, width=200, textvariable=cod_produto_value, font=("Century Gothic bold", 16), fg_color="transparent")
    validade_entry = ctk.CTkEntry(tab, width=150, textvariable=validade_value, font=("Century Gothic bold", 16), fg_color="transparent")
    fornecedor_entry = ctk.CTkEntry(tab, width=200, textvariable=fornecedor_value, font=("Century Gothic bold", 16), fg_color="transparent")
    unidade_entry = ctk.CTkEntry(tab, width=150, textvariable=unidade_value, font=("Century Gothic bold", 16), fg_color="transparent")  # Matheus

    # Aplica a formatação automática da validade enquanto o usuário digita
    validade_entry.bind("<KeyRelease>", lambda event: util.formatar_validade(event, validade_value, validade_entry))

    # Combobox de categoria do produto
    categoria_combobox = ctk.CTkComboBox(tab, values=["Alimento", "Higiene", "Limpeza", "Outros"], 
                                         font=("Century Gothic bold", 14), width=150)
    categoria_combobox.set("Alimento")  # Valor padrão

    # Caixa de texto para observações
    obs_entry = ctk.CTkTextbox(tab, width=380, height=130, font=("Arial", 18), 
                               border_color="#aaa", border_width=2, fg_color="transparent")

    # Rótulos dos campos
    lb_nome = ctk.CTkLabel(tab, text="Nome do Produto:", font=("century gothic bold", 16), text_color=["#000", "#fff"])
    lb_cod = ctk.CTkLabel(tab, text="Código do Produto:", font=("century gothic bold", 16), text_color=["#000", "#fff"])
    lb_validade = ctk.CTkLabel(tab, text="Validade:", font=("century gothic bold", 16), text_color=["#000", "#fff"])
    lb_categoria = ctk.CTkLabel(tab, text="Categoria", font=("century gothic bold", 16), text_color=["#000", "#fff"])
    lb_fornecedor = ctk.CTkLabel(tab, text="Fornecedor", font=("century gothic bold", 16), text_color=["#000", "#fff"])
    lb_unidade = ctk.CTkLabel(tab, text="Unidade", font=("century gothic bold", 16), text_color=["#000", "#fff"])  # Matheus
    lb_obs = ctk.CTkLabel(tab, text="Observações", font=("century gothic bold", 16), text_color=["#000", "#fff"])

    # Botões para salvar e limpar dados
    btn_submit = ctk.CTkButton(
        tab, 
        text="SALVAR DADOS", 
        command=submit, 
        fg_color="#151", 
        hover_color="#131")
    btn_submit.place(x=300, y=370)

    btn_clear = ctk.CTkButton(
        tab, 
        text="LIMPAR CAMPOS", 
        command=lambda: util.clear([nome_value, cod_produto_value, validade_value, fornecedor_value, unidade_value, obs_entry]),
        fg_color="#555", 
        hover_color="#333")
    btn_clear.place(x=500, y=370)

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
    unidade_entry.place(x=50, y=230)  # Matheus

    lb_obs.place(x=270, y=200)
    obs_entry.place(x=270, y=230)

    tab.bind("<Button-1>", util.tirarFoco)  # Remove o foco do campo de busca ao clicar fora dele