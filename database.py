import psycopg2
from tkinter import messagebox

def salvarBancoDeDados(nome_produto, cod_produto, validade, fornecedor, categoria, obs):
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
        cursor.execute("""INSERT INTO produtos (nome_produto, cod_produto, validade, fornecedor, categoria, observacoes) 
                        VALUES (%s, %s, %s, %s, %s, %s)""", 
                        (nome_produto, cod_produto, validade, fornecedor, categoria, obs))

        conexao.commit()
        cursor.close()
        conexao.close()

    except Exception as erro:
        messagebox.showerror("Erro no banco de dados", f"Erro ao inserir no PostgreSQL:\n{erro}")