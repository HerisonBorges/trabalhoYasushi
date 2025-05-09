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


'''
08/05/2025

O QUE FOI FEITO, COM MUITO CUSTO :(

1 - abas para pesquisa, edição e relatorios

O QUE PRECISA SER FEITO, ANEXADO A IDEIAS DE MELHORAIS

1 - IMPLEMENTAR LOGICA PARA CARREGAR DADOS PARA EDIÇÃO, ( SE FOR POSSIVEL)
2- IMPLEMENTAR LOGICA PARA GERAR RELATORIOS
3 - FICOU FORA DE QUADRO A INTERFACE, MAS ISSO E FACIL DE ARRUMAR
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
        self.CriandoAbas() # cria as abas do sistema

    def layout_config(self):
        self.title("Sistema de Gestão de Produtos") # Define o título da janela
        self.geometry("700x500") # Define o tamanho da janela (largura x altura)

    def appearence(self):
        self.lb_apm = ctk.CTkLabel(self, text="Tema", bg_color="transparent", text_color=['#000', "#fff"]).place(x=50, y=430)
        self.opt_apm = ctk.CTkOptionMenu(self, values=["Dark", "Light"], command=self.change_apm).place(x=50, y=460)

    def CriandoAbas(self):
        # criando 4 abas na interface
        self.tabview = ctk.CTkTabview(self, width=750, height=550)
        self.tabview.place(x=25, y=25)

        # adicionando as abas
        self.tabview.add("Cadastro") # Aqui sera a aba para cadastrar os produtos
        self.tabview.add("Pesquisa")
        self.tabview.add("Edição")
        self.tabview.add("Relatórios")

        # configurando cada aba
        self.setupCadastro(self.tabview.tab("Cadastro"))
        self.setupPesquisa(self.tabview.tab("Pesquisa"))
        self.setupEdicao(self.tabview.tab("Edição"))
        self.setupRelatorios(self.tabview.tab("Relatórios"))

    def setupCadastro(self, tab):
        # Criando o cabeçalho da aplicação
        frame = ctk.CTkFrame(tab, width=700, height=50, corner_radius=0, fg_color="teal")
        frame.place(x=0, y=10)

        # Título centralizado
        title = ctk.CTkLabel(frame, text="Sistema de Gestão de Produtos", font=("century gothic bold", 24), text_color="#fff", bg_color="transparent")
        title.place(relx=0.5, rely=0.5, anchor="center")  # Centralizado no frame

        # Instrução para o usuário
        span = ctk.CTkLabel(tab, text="Por favor, preencha todos os campos do formulário!", font=("century gothic bold", 16), text_color=["#000", "#fff"]).place(x=50, y=70)

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
            
            # Definindo a largura das colunas e deixando em negrito o cabeçalho
            for col in range(1, folha.max_column + 1):
                coluna = xl.utils.get_column_letter(col)
                folha.column_dimensions[coluna].width = 20
                folha.cell(row=1, column=col).font = xl.styles.Font(bold=True)
            
            # Criando a tabela
            tab = Table(displayName="TabelaProdutos", ref=f"A1:F{folha.max_row}")
            
            # Estilo da tabela
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

                # atualiza a tabela
                tab = folha.tables['TabelaProdutos']
                tab.ref = f"A1:F{folha.max_row}"
                
                ficheiro.save(r"Produtos.xlsx")
                messagebox.showinfo("Sistema", "Dados salvos com sucesso")
                
                clear() # Limpa os campos após salvar
                
                ########## ESSA PARTE CONECTA AO PGADMIN  #############
                try: 
                    conexao = psycopg2.connect(
                        host="localhost",
                        database="produtos_db", # COLOQUE O NOME DO SEU BANCO DE DADOS
                        user="postgres",
                        password="0L0k1nh0_123!", # COLOQUE A SENHA DO SEU BANCO DE DADOS
                        port="5432"
                    )
                    cursor = conexao.cursor()

                    # inserindo as informações na tabela
                    cursor.execute("""INSERT INTO produtos (nome_produto, cod_barras, validade, fornecedor, categoria, observacoes) 
                                    VALUES (%s, %s, %s, %s, %s, %s)""", 
                                    (nome_produto, cod_barras, validade, fornecedor, categoria, obs))

                    conexao.commit()
                    cursor.close()
                    conexao.close()

                except Exception as erro:
                    messagebox.showerror("Erro no banco de dados", f"Erro ao inserir no PostgreSQL:\n{erro}")

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
        nome_entry = ctk.CTkEntry(tab, width=350, textvariable=nome_value, font=("Century Gothic bold", 16), fg_color="transparent")
        cod_barras_entry = ctk.CTkEntry(tab, width=200, textvariable=cod_barras_value, font=("Century Gothic bold", 16), fg_color="transparent")
        validade_entry = ctk.CTkEntry(tab, width=150, textvariable=validade_value, font=("Century Gothic bold", 16), fg_color="transparent")
        fornecedor_entry = ctk.CTkEntry(tab, width=200, textvariable=fornecedor_value, font=("Century Gothic bold", 16), fg_color="transparent")

        # Formata a validade para o padrão dd/mm/aaaa
        def formatar_validade(event): # "event" recebe o evento "<KeyRelease>" toda vez que o usuário digita
            validade = validade_value.get()
            
            if len(validade) == 8 and validade.isdigit(): 
                validade_value.set(f"{validade[:2]}/{validade[2:4]}/{validade[4:]}")
                validade_entry.icursor(len(validade_value.get()))  # Move o cursor para o final do texto
                
        # verifica se a validade está correta e se o produto não está vencido
        def validar_validade(valida):
            # Verifica se foi preenchido totalmente o campo validade
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
                
            # Verifica se o produto está vencido
            elif datetime.strptime(valida, "%d/%m/%Y") < data_atual:
                messagebox.showerror("Sistema", "Produto vencido!\nVerifique a validade do produto")
                validade_value.set("")
                
        # Se sair do compo validade, formata a validade
        validade_entry.bind("<KeyRelease>", formatar_validade)
        
        # Combobox
        categoria_combobox = ctk.CTkComboBox(tab, values=["Alimento", "Higiene", "Limpeza", "Outros"], font=("Century Gothic bold", 14), width=150)
        categoria_combobox.set("Alimento")

        # Entrada de observações
        obs_entry = ctk.CTkTextbox(tab, width=450, height=150, font=("Arial", 18), border_color="#aaa", border_width=2, fg_color="transparent")

        # Rótulos para cada campo
        lb_nome = ctk.CTkLabel(tab, text="Nome do Produto:", font=("century gothic bold", 16), text_color=["#000", "#fff"])
        lb_cod = ctk.CTkLabel(tab, text="Código de Barras:", font=("century gothic bold", 16), text_color=["#000", "#fff"])
        lb_validade = ctk.CTkLabel(tab, text="Validade:", font=("century gothic bold", 16), text_color=["#000", "#fff"])
        lb_categoria = ctk.CTkLabel(tab, text="Categoria", font=("century gothic bold", 16), text_color=["#000", "#fff"])
        lb_fornecedor = ctk.CTkLabel(tab, text="Fornecedor", font=("century gothic bold", 16), text_color=["#000", "#fff"])
        lb_obs = ctk.CTkLabel(tab, text="Observações", font=("century gothic bold", 16), text_color=["#000", "#fff"])

        # Botões para salvar e limpar os dados
        btn_submit = ctk.CTkButton(tab, text="SALVAR DADOS", command=submit, fg_color="#151", hover_color="#131").place(x=300, y=420)
        btn_clear = ctk.CTkButton(tab, text="LIMPAR CAMPOS", command=clear, fg_color="#555", hover_color="#333").place(x=500, y=420)

        # Posicionamento dos elementos na tela
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
                    termo.lower() in str(row[1]).lower() or  # Código de barras
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

    def setupEdicao(self, tab):
        # Aba de edição
        lblTitulo = ctk.CTkLabel(tab, text="EDITAR PRODUTO", font=("Century Gothic", 20, "bold"))
        lblTitulo.pack(pady=20)

        # Campo para código do produto
        self.entryEdicao = ctk.CTkEntry(
            tab,
            width=300,
            placeholder_text="Digite o código do produto"
        )
        self.entryEdicao.pack(pady=10)

        # Botão para carregar dados
        botaoCarregar = ctk.CTkButton(
            tab,
            text="CARREGAR DADOS",
            fg_color="#3498db",
            command=self.carregarDadosEdicao
        )
        botaoCarregar.pack(pady=10)

    def carregarDadosEdicao(self):
        # Implementar lógica para carregar dados para edição
        messagebox.showinfo("Edição", "Funcionalidade de edição será implementada em breve")

    def setupRelatorios(self, tab):
        # Aba de relatórios
        lblTitulo = ctk.CTkLabel(tab, text="RELATÓRIOS", font=("Century Gothic", 20, "bold"))
        lblTitulo.pack(pady=20)

        # Opções de relatório
        self.comboRelatorios = ctk.CTkComboBox(
            tab,
            values=["Produtos próximos do vencimento", "Todos os produtos", "Por categoria"]
        )
        self.comboRelatorios.pack(pady=10)

        # Botão para gerar relatorio
        botaoGerar = ctk.CTkButton(
            tab,
            text="GERAR RELATÓRIO",
            fg_color="#9b59b6",
            command=self.gerarRelatorio
        )
        botaoGerar.pack(pady=20)

    def gerarRelatorio(self):
        # Implementar lógica para gerar relatórios
        messagebox.showinfo("Relatórios", "Funcionalidade de relatórios será implementada em breve")

    def change_apm(self, nova_aparencia):
        ctk.set_appearance_mode(nova_aparencia)

if __name__ == "__main__":
    app = App()
    app.mainloop()