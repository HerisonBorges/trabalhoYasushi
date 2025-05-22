import customtkinter as ctk
from tkinter import messagebox
import tkinter as tk
import database as db
import util

'''
O QUE FAZER:
1- Função para filtrar os produtos
2- Função para mostrar os produtos filtrados
3- Salvar os produtos para que não precisem ser carregados toda vez que a aba for aberta
4- Mudar a unidade no banco de dados
5- Criar uma função para adicionar e remover produtos
6- Atualizar os produtos se adicionar, remover ou editar algum produto
7- Fazer o filtro e um campo para selecionar oq vai ser filtrado para que não fique pesado o código

OBS: .pack_forget() esconde o ctk selecionado
'''
campos = ["codigo", "nome", "fornecedor", "validade", "categoria", "unidade"] #As chaves do dicionário
produtosAll = {campo: [] for campo in campos}

def mostrarProduto(array_produtos, container):
    for widget in container.winfo_children(): #Limpa o container antes de adicionar novos produtos
        widget.destroy()
    
    # Linha de cabeçalho
    header = ctk.CTkFrame(container, fg_color="#333333")
    header.pack(fill="x", pady=(0, 5))
    
    #Preenche o cabeçalho com os campos
    for campo, largura in zip(campos, [80, 80, 80, 80, 80, 80]):
        ctk.CTkLabel(header, text=campo.upper(), width=largura, font=("Arial", 12, "bold")).pack(side="left")
        
    # Linha vertical de separação no cabeçalho
    ctk.CTkLabel(header, text="|", width=10, font=("Arial", 12, "bold")).pack(side="left")
    ctk.CTkLabel(header, text="Ações", width=120, font=("Arial", 12, "bold")).pack(side="left")
    
    produtos = [dict(zip(campos, produto)) for produto in array_produtos] #Cria uma lista de dicionários com os produtos
        
    #Adiciona os produtos dentro do frame que mostra os produtos
    for produto in produtos:
        linha = ctk.CTkFrame(container) #cria um frame para cada produto
        linha.pack(fill="x")
        
        # Criação dos labels para cada campo do produto
        labelNome = ctk.CTkLabel(linha, text=produto["nome"], width=80)
        labelNome.pack(side="left")
        produtosAll["codigo"].append(labelNome.cget("text")) #u fiz alguma coisa que tem que colocar ao contrário, apenas aceitem
        
        labelCod = ctk.CTkLabel(linha, text=produto["codigo"], width=80)
        labelCod.pack(side="left")
        produtosAll["nome"].append(labelCod.cget("text"))
        
        labelForn = ctk.CTkLabel(linha, text=produto["fornecedor"], width=80)
        labelForn.pack(side="left")
        produtosAll["validade"].append(labelForn.cget("text"))
        
        labelVal = ctk.CTkLabel(linha, text=produto["validade"], width=80)
        labelVal.pack(side="left")
        produtosAll["fornecedor"].append(labelVal.cget("text"))
        
        labelCat = ctk.CTkLabel(linha, text=produto["categoria"], width=80)
        labelCat.pack(side="left")
        produtosAll["categoria"].append(labelCat.cget("text"))
        
        labelUnidade = ctk.CTkLabel(linha, text=produto["unidade"], width=80)
        labelUnidade.pack(side="left")
        produtosAll["unidade"].append(labelUnidade.cget("text"))
        
        # Linha vertical de separação
        ctk.CTkLabel(linha, text="|", width=10, font=("Arial", 12, "bold")).pack(side="left")
        
        #Local para escrever a quantidade
        entryQuant = ctk.CTkEntry(linha, width=40)
        entryQuant.pack(side="left", padx=5)
        
        #Soma a quantidade com a unidade que já existe
        bntSoma = ctk.CTkButton(linha, text="+", width=30, command=lambda e=entryQuant, u=labelUnidade: adicionarProduto(e, u)) #temos que p=produto e e=entryQuant para não pegar somente o último produto
        bntSoma.pack(side="left", padx=2)
        
        #Subtrai a quantidade com a unidade que já existe somente se for menor ou igual
        bntSub = ctk.CTkButton(linha, text="-", width=30, command=lambda e=entryQuant, u=labelUnidade: removerProduto(e, u))
        bntSub.pack(side="left", padx=4)

#Soma a quantidade do produto com o valor digitado no entryQuant
def adicionarProduto(entryQuant, labelUnidade):
    try:
        valor = int(entryQuant.get())
        labelUnidade.configure(text=labelUnidade.cget("text") + valor) #Atualiza o label com a nova quantidade
    
    except ValueError as e:
        messagebox.showerror("Erro", "Digite um número válido.")

def removerProduto(entryQuant, labelUnidade):
    try:
        valor = int(entryQuant.get())
        if valor > labelUnidade.cget("text"):
            messagebox.showerror("Erro", "Valor maior que o disponível.")
            return
        
        else:
            labelUnidade.configure(text=labelUnidade.cget("text") - valor) #Atualiza o label com a nova quantidade
    
    except ValueError as e:
        messagebox.showerror("Erro", "Digite um número válido.")

def filtrar(produtos, termo):
    produtos

def setupPesquisa(self, tab):
    # Configuração do layout da aba
    frame = ctk.CTkFrame(tab)
    frame.pack(padx=20, pady=20, fill="both", expand=True)
    
    barra_frame = ctk.CTkFrame(frame)
    barra_frame.pack(anchor="e", pady=(0,10))
    
    # Campo de entrada para o termo de pesquisa
    self.entryPesquisa = ctk.CTkEntry(barra_frame, width=200, placeholder_text="nome, código, fornecedor ou categoria")
    self.entryPesquisa.pack(side="left", padx=(0, 5))

    # Botão de busca que chama a função executarPesquisa
    botaoPesquisa = ctk.CTkButton(barra_frame, width=70 ,text="BUSCAR", fg_color="#2ecc71", text_color="#000")
    botaoPesquisa.pack(side="left")
    
    botaoPesquisa.bind("<Enter>", lambda e: botaoPesquisa.configure(fg_color="#27ae60", cursor="hand2")) #Muda a cor do botão ao passar o mouse
    botaoPesquisa.bind("<Leave>", lambda e: botaoPesquisa.configure(fg_color="#2acc71", cursor="hand2")) #Volta a cor original
    botaoPesquisa.bind("<ButtonPress-1>", lambda e: botaoPesquisa.configure(fg_color="#27ae50"))
    botaoPesquisa.bind("<ButtonRelease-1>", lambda e: botaoPesquisa.configure(fg_color="#2ecc71"))
    
    # Campo de texto que exibe os resultados da busca (inicialmente desabilitado)
    produtos_frame = ctk.CTkFrame(frame)
    produtos_frame.pack(fill="x", pady=20)
    
    mostrarProduto(db.selectAll(), produtos_frame)
    
    self.bind("<Button-1>", util.tirarFoco)  # Remove o foco do campo de busca ao clicar fora dele
    print(produtosAll)
    