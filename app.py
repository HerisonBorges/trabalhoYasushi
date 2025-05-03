'''
O QUE FOI FEITO NESTE CÓDIGO:
(Escreva aqui o que você fez no código para facilitar para o próximo entender)

1. Criação de uma tabela no Excel
2. Verificações de validade
'''

'''
IDEIAS PARA MELHORIAS:

1. Criar uma área de remoção de produtos.
2. Criar uma área de edição de produtos.
    2.1. Edição de tipos de produtos.
    2.2. Edição das observações.
3. Criar uma área de pesquisa de produtos.
4. Criar área de login para conectar ao banco de dados.
5. Criar uma área de relatórios.
6. Recomendar nome de produtos e fornecedores baseados no que já existe.
'''

import customtkinter as ctk
from tkinter import *
from tkinter import messagebox
import openpyxl as xl
import pathlib
from openpyxl.worksheet.table import Table, TableStyleInfo
import psycopg2
from datetime import datetime

# Aparência do sistema
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self): 
        super().__init__() # Inicializa a janela principal da classe App
        self.layout_config() # Define tamanho e título da janela
        self.appearence() # Adiciona seletor de tema (claro, escuro, sistema)
        self.todo_sistema()# Monta a interface gráfica e a lógica principal

    def layout_config(self):
        self.title("Sistema de Gestão de Produtos") # Define o título da janela
        self.geometry("700x500")                    # Define o tamanho da janela (largura x altura)

    def appearence(self):
        self.lb_apm = ctk.CTkLabel(self, text="Tema", bg_color="transparent", text_color=['#000', "#fff"]).place(x=50, y=430)
        self.opt_apm = ctk.CTkOptionMenu(self, values=["Dark", "Light"], command=self.change_apm).place(x=50, y=460)

    def todo_sistema(self):

        # Criando o cabeçalho da aplicação
        frame = ctk.CTkFrame(self, width=700, height=50, corner_radius=0, fg_color="teal")
        frame.place(x=0, y=10)

        # Título centralizado
        title = ctk.CTkLabel(frame, text="Sistema de Gestão de Produtos", font=("century gothic bold", 24), text_color="#fff", bg_color="transparent")
        title.place(relx=0.5, rely=0.5, anchor="center")  # Centralizado no frame

        # Instrução para o usuário
        span = ctk.CTkLabel(self, text="Por favor, preencha todos os campos do formulário!", font=("century gothic bold", 16), text_color=["#000", "#fff"]).place(x=50, y=70)


        # Verifica se o arquivo Excel existe. Se não, cria com os cabeçalhos
        ficheiro = pathlib.Path("Produtos.xlsx")

        if ficheiro.exists():
            pass
        else:
            workbook = xl.Workbook()
            folha = workbook.active
            folha['A1'] = "Nome do Produto"
            folha['B1'] = "Código de Barras"
            folha['C1'] = "Validade"
            folha['D1'] = "Fornecedor"
            folha['E1'] = "Categoria"
            folha['F1'] = "Observações"
            
            #Definindo a largura das colunas e deixando em negrito o cabeçalho
            for col in range(1, folha.max_column + 1):
                coluna = xl.utils.get_column_letter(col)
                folha.column_dimensions[coluna].width = 20
                folha.cell(row=1, column=col).font = xl.styles.Font(bold=True)
            
            #Criando a tabela
            tab = Table(displayName="TabelaProdutos", ref=f"A1:F{folha.max_row}")
            
            #Estilo da tabela
            estilo = TableStyleInfo(
                name="TableStyleMedium9",
                showFirstColumn=False,
                showLastColumn=False,
                showRowStripes=True,
                showColumnStripes=False
            )
            
            tab.tableStyleInfo = estilo
            folha.add_table(tab)

            workbook.save("Produtos.xlsx")
        # Função para salvar os dados preenchidos no Excel
        def submit():
            # Obtém os valores dos campos
            nome_produto = nome_value.get()
            cod_barras = cod_barras_value.get()
            formatar_validade("")
            validar_validade(validade_value.get())
            validade = validade_value.get()
            fornecedor = fornecedor_value.get()
            categoria = categoria_combobox.get()
            obs = obs_entry.get(0.0, END)

            # Verifica se todos os campos obrigatórios estão preenchidos
            if not all([nome_produto, cod_barras, validade, fornecedor]):
                messagebox.showerror("Sistema", "Erro!\nPor favor preencha todos os dados")
                
            else:
                ficheiro = xl.load_workbook('Produtos.xlsx')
                folha = ficheiro.active
                
                # Adiciona os dados na próxima linha disponível
                folha.append([nome_produto, cod_barras, validade, fornecedor, categoria, obs])

                #atualiza a tabela
                tab = folha.tables['TabelaProdutos']
                tab.ref = f"A1:F{folha.max_row}"
                
                ficheiro.save(r"Produtos.xlsx")
                messagebox.showinfo("Sistema", "Dados salvos com sucesso")
                
                clear() #Limpa os campos após salvar
                
                ########## ESSA PARTE CONECTA AO PGADMIN  #############
                try: 
                    conexao = psycopg2.connect(
                        host="localhost",
                        database="produtos_db", #COLOQUE O NOME DO SEU BANCO DE DADOS
                        user="postgres",
                        password="0L0k1nh0_123!", #COLOQUE A SENHA DO SEU BANCO DE DADOS
                        port="5432"
                    )
                    cursor = conexao.cursor()

                    #inserindo as informações na tabela
                    cursor.execute("""INSERT INTO produtos (nome_produto, cod_barras, validade, fornecedor, categoria, observacoes)VALUES (%s, %s, %s, %s, %s, %s)""", (nome_produto, cod_barras, validade, fornecedor, categoria, obs))

                    conexao.commit()
                    cursor.close()
                    conexao.close()

                except Exception as erro:
                    messagebox.showerror("Erro no banco de dados", f"Erro ao inserir no PostgreSQL:\n{erro}")

                ##############################################################################################
        
        # Função para limpar todos os campos do formulário
        def clear():
            nome_value.set("")
            cod_barras_value.set("")
            validade_value.set("")
            fornecedor_value.set("")
            obs_entry.delete(0.0, END)

        # Variáveis de texto
        nome_value = StringVar()
        cod_barras_value = StringVar()
        validade_value = StringVar()
        fornecedor_value = StringVar()

        # Entradas
        nome_entry = ctk.CTkEntry(self, width=350, textvariable=nome_value, font=("Century Gothic bold", 16), fg_color="transparent")
        cod_barras_entry = ctk.CTkEntry(self, width=200, textvariable=cod_barras_value, font=("Century Gothic bold", 16), fg_color="transparent")
        validade_entry = ctk.CTkEntry(self, width=150, textvariable=validade_value, font=("Century Gothic bold", 16), fg_color="transparent")
        fornecedor_entry = ctk.CTkEntry(self, width=200, textvariable=fornecedor_value, font=("Century Gothic bold", 16), fg_color="transparent")

        #Formata a validade para o padrão dd/mm/aaaa
        def formatar_validade (event): #"event" recebe o evento "<KeyRelease>" toda vez que o usuário digita
            validade = validade_value.get()
            
            if len(validade) == 8 and validade.isdigit(): 
                validade_value.set(f"{validade[:2]}/{validade[2:4]}/{validade[4:]}")
                validade_entry.icursor(len(validade_value.get()))  # Move o cursor para o final do texto
                
        #verifica se a validade está correta e se o produto não está vencido
        def validar_validade(valida):
            #Verifica se foi preenchido totalmente o campo validade
            try:
                dia = int(valida[0:2])
                mes = int(valida[3:5])
                ano = valida[6:10]
            except ValueError:
                messagebox.showerror("Sistema", "Erro!\nFormato de validade inválido.\nUse o formato dd/mm/aaaa")
                validade_value.set("")
                return
            
            data_atual = datetime.now()
            
            # Verifica se o campo validade está no formato correto
            if len(valida) != 10:
                messagebox.showerror("Sistema", "Erro!\nFormato de validade inválido.\nUse o formato dd/mm/aaaa")
                validade_value.set("")
            
            # Verifica se o dia, mês e ano são válidos
            elif dia > 31 or (mes > 12 or mes <= 0):
                messagebox.showerror("Sistema", "Erro!\nData inválida.\nVerifique o dia, mês e ano")
                validade_value.set("")
                
            #Verifica se o produto está vencido
            elif datetime.strptime(valida, "%d/%m/%Y") < data_atual:
                messagebox.showerror("Sistema", "Produto vencido!\nVerifique a validade do produto")
                validade_value.set("")
                
        
        #Se sair do compo validade, formata a validade
        validade_entry.bind("<KeyRelease>", formatar_validade)
        
        #Se clicar fora do campo, ele perder o foco
        def focus_out (event):
            if event.widget == self:
                self.focus()
        
        # Se clicar fora do campo, ele perder o foco
        self.bind("<Button-1>", focus_out)
        
        # Combobox
        categoria_combobox = ctk.CTkComboBox(self, values=["Alimento", "Higiene", "Limpeza", "Outros"], font=("Century Gothic bold", 14), width=150)
        categoria_combobox.set("Alimento")

        # Entrada de observações
        obs_entry = ctk.CTkTextbox(self, width=450, height=150, font=("Arial", 18), border_color="#aaa", border_width=2, fg_color="transparent")

        # Rótulos para cada campo
        lb_nome = ctk.CTkLabel(self, text="Nome do Produto:", font=("century gothic bold", 16), text_color=["#000", "#fff"])
        lb_cod = ctk.CTkLabel(self, text="Código de Barras:", font=("century gothic bold", 16), text_color=["#000", "#fff"])
        lb_validade = ctk.CTkLabel(self, text="Validade:", font=("century gothic bold", 16), text_color=["#000", "#fff"])
        lb_categoria = ctk.CTkLabel(self, text="Categoria", font=("century gothic bold", 16), text_color=["#000", "#fff"])
        lb_fornecedor = ctk.CTkLabel(self, text="Fornecedor", font=("century gothic bold", 16), text_color=["#000", "#fff"])
        lb_obs = ctk.CTkLabel(self, text="Observações", font=("century gothic bold", 16), text_color=["#000", "#fff"])

        # Botões para salvar e limpar os dados
        btn_submit = ctk.CTkButton(self, text="SALVAR DADOS", command=submit, fg_color="#151", hover_color="#131").place(x=300, y=420)
        btn_clear = ctk.CTkButton(self, text="LIMPAR CAMPOS", command=clear, fg_color="#555", hover_color="#333").place(x=500, y=420)

        #Posicionamento dos elementos na tela
        lb_nome.place(x=50, y=120)
        nome_entry.place(x=50, y=150)

        lb_cod.place(x=450, y=120)
        cod_barras_entry.place(x=450, y=150)

        lb_validade.place(x=300, y=190)
        validade_entry.place(x=300, y=220)

        lb_categoria.place(x=500, y=190)
        categoria_combobox.place(x=500, y=220)

        lb_fornecedor.place(x=50, y=190)
        fornecedor_entry.place(x=50, y=220)

        lb_obs.place(x=50, y=260)
        obs_entry.place(x=200, y=260)

    def change_apm(self, nova_aparencia):
        ctk.set_appearance_mode(nova_aparencia)

if __name__ == "__main__":
    app = App()
    app.mainloop()