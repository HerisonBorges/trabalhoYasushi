import customtkinter as ctk
from tkinter import *
from tkinter import messagebox
import openpyxl, xlrd
import pathlib
from openpyxl import Workbook
from openpyxl import load_workbook
import psycopg2
from tkinter import messagebox


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
        self.opt_apm = ctk.CTkOptionMenu(self, values=["Light", "Dark", "System"], command=self.change_apm).place(x=50, y=460)

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
            workbook = Workbook()
            folha = workbook.active
            folha['A1'] = "Nome do Produto"
            folha['B1'] = "Código de Barras"
            folha['C1'] = "Validade"
            folha['D1'] = "Fornecedor"
            folha['E1'] = "Categoria"
            folha['F1'] = "Observações"

            workbook.save("Produtos.xlsx")
        # Função para salvar os dados preenchidos no Excel
        def submit():
            # Obtém os valores dos campos
            nome_produto = nome_value.get()
            cod_barras = cod_barras_value.get()
            validade = validade_value.get()
            fornecedor = fornecedor_value.get()
            categoria = categoria_combobox.get()
            obs = obs_entry.get(0.0, END)

            # Verifica se todos os campos obrigatórios estão preenchidos
            if (nome_produto == "" or cod_barras == "" or validade == "" or fornecedor == ""):
                messagebox.showerror("Sistema", "Erro!\nPor favor preencha todos os dados")
            else:
                ficheiro = openpyxl.load_workbook('Produtos.xlsx')
                folha = ficheiro.active
                folha.cell(column=1, row=folha.max_row+1, value=nome_produto)
                folha.cell(column=2, row=folha.max_row, value=cod_barras)
                folha.cell(column=3, row=folha.max_row, value=validade)
                folha.cell(column=4, row=folha.max_row, value=fornecedor)
                folha.cell(column=5, row=folha.max_row, value=categoria)
                folha.cell(column=6, row=folha.max_row, value=obs)

                ficheiro.save(r"Produtos.xlsx")
                messagebox.showinfo("Sistema", "Dados salvos com sucesso")


            ########## ESSA PARTE CONECTA AO PGADMIN  #############
            try: 
                conexao = psycopg2.connect(
                    host="localhost",
                    database="produtos_db",
                    user="postgres",
                    password="159357.Ab",
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
