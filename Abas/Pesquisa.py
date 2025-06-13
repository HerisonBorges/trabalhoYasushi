import customtkinter as ctk
from tkinter import messagebox
from PIL import Image
import database as db
import util

campos = ["codigo", "nome", "validade", "fornecedor", "categoria", "unidade"] #As chaves do dicionário

def mostrarProduto(array_produtos, container, header):
    
    #Limpa o container antes de adicionar novos produtos
    for widget in container.winfo_children():
        if not widget == header:
            widget.destroy()
    
    if not array_produtos:
        ctk.CTkLabel(container, text="Nenhum produto encontrado.", font=("Arial", 14)).pack(pady=20)
        return
    
    produtos = [dict(zip(campos, produto)) for produto in array_produtos] #Cria uma lista de dicionários com os produtos
        
    #Adiciona os produtos dentro do frame que mostra os produtos
    for produto in produtos:
        linha = ctk.CTkFrame(container)
        linha.pack(fill="x")
        
        #Borda esquerda
        ctk.CTkFrame(linha, width=2, fg_color="#333333", height=40).pack(side="left", fill="y")
        
         #Borda direita
        ctk.CTkFrame(linha, width=2, fg_color="#333333", height=40).pack(side="right", fill="y")
        
        # Criação dos labels para cada campo do produto
        labelNome = ctk.CTkLabel(linha, text=produto["nome"], width=80) #labelNome e cod estão trocados e estou com preguiça de consertar, mas tá funcionando
        labelNome.pack(side="left")
        
        labelCod = ctk.CTkLabel(linha, text=produto["codigo"], width=80)
        labelCod.pack(side="left")
        
        labelForn = ctk.CTkLabel(linha, text=produto["validade"], width=80) #Não questiona, só aceita
        labelForn.pack(side="left")
        
        labelVal = ctk.CTkLabel(linha, text=produto["fornecedor"], width=80)
        labelVal.pack(side="left")
        
        labelCat = ctk.CTkLabel(linha, text=produto["categoria"], width=80)
        labelCat.pack(side="left")
        
        labelUnidade = ctk.CTkLabel(linha, text=produto["unidade"], width=80)
        labelUnidade.pack(side="left")
        
        #Local para escrever a quantidade
        entryQuant = ctk.CTkEntry(linha, width=40)
        entryQuant.pack(side="left", padx=5)
        
        #Soma a quantidade com a unidade que já existe
        bntSoma = ctk.CTkButton(
            linha, 
            text="+", 
            width=30, 
            fg_color="transparent",
            hover_color="#4E4E4E",
            font=("Arial", 16, "bold"),
            command=lambda e=entryQuant, u=labelUnidade, c=labelNome.cget("text"): adicionarUnidade(e, {"unidade": u.cget("text")}, u, c)
        ) #temos que p=produto e e=entryQuant para não pegar somente o último produto
        bntSoma.pack(side="left", padx=2)
        
        #Subtrai a quantidade com a unidade que já existe somente se for menor ou igual
        bntSub = ctk.CTkButton(
            linha, 
            text="-", 
            width=30, 
            fg_color="transparent",
            hover_color="#4E4E4E",
            font=("Arial", 16, "bold"),
            command=lambda e=entryQuant, u=labelUnidade, c=labelNome.cget("text"): removerUnidade(e, {"unidade": u.cget("text")}, u, c)
        )
        bntSub.pack(side="left", padx=4)
        
        '''img_trash= ctk.CTkImage(Image.open("img\delete.png"), size=(18,18))'''
        #Excluir o produto
        bntExcluir = ctk.CTkButton(
            linha,
            text="Excluir",
            text_color="#af0000",
            width=26,
            height=26,
            
            fg_color="transparent",
            hover_color="#4E4E4E",
            command=lambda l=labelNome: excluirProduto(l)
        )
        bntExcluir.pack(side="left", padx=5)
        
        #Altera a fonte e o cursor ao passar o mouse em cima dos botões
        util.mudarCursor(bntSoma)
        util.mudarCursor(bntSub)
        util.mudarCursor(bntExcluir)

#Soma a quantidade do produto com o valor digitado no entryQuant
def adicionarUnidade(entryQuant, dict, labelUnidade ,cod):
    try:
        print(entryQuant.get(), dict["unidade"])
        valor = int(entryQuant.get()) + dict["unidade"]
        dict["unidade"] = valor 
        
        labelUnidade.configure(text=valor) #Atualiza o label com a nova quantidade
        db.update(cod, dict)
    
    except ValueError as e:
        if entryQuant.get() == "":
            valor = int(dict["unidade"]) + 1
            dict["unidade"] = valor
            
            labelUnidade.configure(text=valor)
            db.update(cod, dict) #atualiza o banco de dados
        
        else:
            messagebox.showerror("Erro", "Digite um número válido.")
            
#Subtrai a quantidade do produto com o valor digitado no entryQuant
def removerUnidade(entryQuant, dict, labelUnidade, cod):
    try:
        valor = dict["unidade"] - int(entryQuant.get())
        if valor > dict["unidade"]:
            messagebox.showerror("Erro", "Valor maior que o disponível.")
            return
        
        else:
            dict["unidade"] = valor
            
            labelUnidade.configure(text=valor) #Atualiza o label com a nova quantidade           
            db.update(cod, dict) #atualiza o banco de dados
    
    except ValueError as e:
        if int(dict["unidade"]) < 1:
            messagebox.showerror("Erro", "Quantidade zerada desse produto")
        
        else:
            valor = int(dict["unidade"])- 1
            dict["unidade"] = valor
            
            labelUnidade.configure(text=valor) #Atualiza o label com a nova quantidade
            db.update(cod, dict) #atualiza o banco de dados

#Função para excluir um produto
def excluirProduto(labelCod):
    cod = labelCod.cget("text")
    
    if messagebox.askyesno("Confirmação", f"Você tem certeza que deseja excluir o produto com código {cod}?"):
        print(cod)
        db.delete(cod)
        messagebox.showinfo("Sucesso", "Produto excluído com sucesso.")
        labelCod.master.destroy()  # Remove a linha do produto excluído
    else:
        messagebox.showinfo("Cancelado", "Exclusão cancelada.")

def setupPesquisa(self, tab):
    # Configuração do layout da aba
    frame = ctk.CTkFrame(tab)
    frame.pack(padx=20, pady=20, fill="both", expand=True)
    
    barra_frame = ctk.CTkFrame(frame)
    barra_frame.pack(anchor="e", pady=(0,10))
    
    #Campo de entrada para o termo de pesquisa
    self.entryPesquisa = ctk.CTkEntry(barra_frame, width=200, placeholder_text="nome, código, fornecedor ou categoria")
    self.entryPesquisa.pack(side="left", padx=(0, 5))

    # Campo de texto que exibe os resultados da busca (inicialmente desabilitado)
    self.produtos_frame = ctk.CTkFrame(frame)
    self.produtos_frame.pack(fill="x", pady=20)
    
    # Linha de cabeçalho
    self.header = ctk.CTkFrame(self.produtos_frame, fg_color="#333333")
    self.header.pack(fill="x", pady=(0, 5))
    
    #Preenche o cabeçalho com os campos
    for campo, largura in zip(campos, [80, 80, 80, 80, 80, 80]):
        ctk.CTkLabel(self.header, text=campo.upper(), width=largura, font=("Arial", 12, "bold")).pack(side="left")
        
    # Linha vertical de separação no cabeçalho
    ctk.CTkLabel(self.header, text="Ações", width=120, font=("Arial", 12, "bold")).pack(side="left")
    
    # Botão de busca que chama a função executarPesquisa
    botaoPesquisa = ctk.CTkButton(barra_frame, width=70 ,text="BUSCAR", fg_color="#2ecc71", hover_color="#27ae60",text_color="#000", command=lambda: mostrarProduto(db.selectSpecific(self.entryPesquisa.get().strip()), self.produtos_frame, self.header))
    botaoPesquisa.pack(side="left")
    
    botaoPesquisa.bind("<Enter>", lambda e: botaoPesquisa.configure(fg_color="#27ae60", cursor="hand2")) #Muda a cor do botão ao passar o mouse
    botaoPesquisa.bind("<Leave>", lambda e: botaoPesquisa.configure(fg_color="#2acc71", cursor="hand2")) #Volta a cor original
    
    mostrarProduto(db.selectAll(), self.produtos_frame, self.header)
    
    self.bind("<Button-1>", util.tirarFoco)  # Remove o foco do campo de busca ao clicar fora dele