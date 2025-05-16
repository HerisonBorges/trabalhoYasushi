# Importações necessárias
import customtkinter as ctk
from tkinter import *
from tkinter import messagebox
import psycopg2  # Biblioteca para conexão com banco de dados PostgreSQL

# Função que configura a aba de relatórios
def setupRelatorios(self, tab):
    # Frame principal da aba
    frame = ctk.CTkFrame(tab)
    frame.pack(padx=20, pady=20, fill="both", expand=True)

    # Título da seção
    lblTitulo = ctk.CTkLabel(frame, text="RELATÓRIOS", font=("Century Gothic", 20, "bold"))
    lblTitulo.grid(row=0, column=0, columnspan=2, pady=20)

    # Combobox para selecionar o tipo de relatório
    self.comboRelatorios = ctk.CTkComboBox(
        frame,
        values=["Produtos próximos do vencimento", "Todos os produtos", "Por categoria"],
        width=300
    )
    self.comboRelatorios.grid(row=1, column=0, padx=10, pady=10, sticky="w")

    # Botão para gerar o relatório com base na opção selecionada
    botaoGerar = ctk.CTkButton(
        frame,
        text="GERAR RELATÓRIO",
        fg_color="#9b59b6",  # Cor roxa para destaque
        command=lambda: gerarRelatorio(self)
    )
    botaoGerar.grid(row=1, column=1, pady=10, padx=10, sticky="w")

    # Caixa de texto onde os resultados do relatório serão exibidos (inicialmente desabilitada)
    self.resultadoRelatorio = ctk.CTkTextbox(frame, width=700, height=300, state="disabled")
    self.resultadoRelatorio.grid(row=2, column=0, columnspan=2, pady=20)

# Função que executa a geração do relatório selecionado
def gerarRelatorio(self):
    tipo_relatorio = self.comboRelatorios.get()  # Pega a opção escolhida na combobox

    try:
        # Conexão com o banco de dados PostgreSQL
        conn = psycopg2.connect(
            host="localhost",
            database="Projetosexta",
            user="postgres",
            password="1234",
            port="5432"
        )
        cursor = conn.cursor()

        # Consulta SQL de acordo com o tipo de relatório escolhido
        if tipo_relatorio == "Todos os produtos":
            cursor.execute("SELECT nome_produto, cod_produto, validade, fornecedor, categoria, unidade, observacoes FROM produtos")
            dados = cursor.fetchall()
        
        elif tipo_relatorio == "Produtos próximos do vencimento":
            cursor.execute("""
                SELECT nome_produto, cod_produto, validade, fornecedor, categoria, unidade, observacoes
                FROM produtos
                WHERE validade <= CURRENT_DATE + INTERVAL '30 days'
            """)
            dados = cursor.fetchall()

        elif tipo_relatorio == "Por categoria":
            cursor.execute("""
                SELECT categoria, nome_produto, cod_produto, validade, fornecedor, unidade, observacoes
                FROM produtos
                ORDER BY categoria
            """)
            dados = cursor.fetchall()

        else:
            # Caso nenhuma opção válida tenha sido selecionada
            messagebox.showwarning("Relatório", "Selecione um tipo de relatório.")
            return

        # Fecha o cursor e a conexão com o banco
        cursor.close()
        conn.close()

        # Habilita a caixa de texto para mostrar os dados
        self.resultadoRelatorio.configure(state="normal")
        self.resultadoRelatorio.delete(1.0, END)  # Limpa o conteúdo anterior

        # Se houver dados, formata e insere no textbox
        if dados:
            texto = ""
            for row in dados:
                texto += (
                    f"Produto: {row[0]}\n"
                    f"Código: {row[1]}\n"
                    f"Validade: {row[2]}\n"
                    f"Fornecedor: {row[3]}\n"
                    f"Categoria: {row[4]}\n"
                    f"Unidade: {row[5]}\n"
                    f"Obs: {row[6]}\n"
                    + "=" * 50 + "\n"
                )
            self.resultadoRelatorio.insert(END, texto)
        else:
            # Mensagem se não houver dados
            self.resultadoRelatorio.insert(END, "Nenhum dado encontrado para esse relatório.")

        # Desabilita novamente para impedir edição do usuário
        self.resultadoRelatorio.configure(state="disabled")

    except Exception as e:
        # Mostra mensagem de erro se algo falhar na conexão ou na execução
        messagebox.showerror("Erro", f"Erro ao gerar relatório:\n{str(e)}")

