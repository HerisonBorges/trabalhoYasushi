import psycopg2
from tkinter import messagebox

def salvarBancoDeDados(nome_produto, cod_produto, validade, fornecedor, categoria, unidade, obs):
    try:
        conexao = psycopg2.connect(
            host="localhost",
            database="Projetosexta",
            user="postgres",
            password="1234",
            port="5432"
        )
        cursor = conexao.cursor()
        cursor.execute("""
            INSERT INTO produtos (nome_produto, cod_produto, validade, fornecedor, categoria, unidade, observacoes)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (nome_produto, cod_produto, validade, fornecedor, categoria, unidade, obs))
        conexao.commit()
        cursor.close()
        conexao.close()
    except Exception as erro:
        messagebox.showerror("Erro no banco de dados", f"Erro ao inserir no PostgreSQL:\n{erro}")

def buscar_produto_por_campo(campo, valor):
    try:
        conexao = psycopg2.connect(
            host="localhost",
            database="Projetosexta",
            user="postgres",
            password="1234",
            port="5432"
        )
        cursor = conexao.cursor()

        query = f"""
            SELECT nome_produto, cod_produto, validade, fornecedor, categoria, unidade, observacoes
            FROM produtos
            WHERE {campo} = %s
        """
        cursor.execute(query, (valor,))
        resultado = cursor.fetchone()
        cursor.close()
        conexao.close()
        return resultado
    except Exception as erro:
        messagebox.showerror("Erro no banco de dados", f"Erro ao buscar no PostgreSQL:\n{erro}")
        return None

def atualizar_produto(cod_antigo, novos_dados):
    try:
        conexao = psycopg2.connect(
            host="localhost",
            database="Projetosexta",
            user="postgres",
            password="1234",
            port="5432"
        )
        cursor = conexao.cursor()
        cursor.execute("""
            UPDATE produtos SET
                nome_produto = %s,
                cod_produto = %s,
                validade = %s,
                fornecedor = %s,
                categoria = %s,
                unidade = %s,
                observacoes = %s
            WHERE cod_produto = %s
        """, (
            novos_dados["nome_produto"],
            novos_dados["cod_produto"],
            novos_dados["validade"],
            novos_dados["fornecedor"],
            novos_dados["categoria"],
            novos_dados["unidade"],
            novos_dados["observacoes"],
            cod_antigo
        ))
        conexao.commit()
        cursor.close()
        conexao.close()
        return True
    except Exception as erro:
        messagebox.showerror("Erro no banco de dados", f"Erro ao atualizar no PostgreSQL:\n{erro}")
        return False
    
def buscar_produto_por_termo(termo):
    try:
        conexao = psycopg2.connect(
            host="localhost",
            database="Projetosexta",
            user="postgres",
            password="1234",
            port="5432"
        )
        cursor = conexao.cursor()
        query = """
            SELECT nome_produto, cod_produto, validade, fornecedor, categoria, unidade, observacoes
            FROM produtos
            WHERE nome_produto ILIKE %s
               OR cod_produto ILIKE %s
               OR fornecedor ILIKE %s
        """
        like_termo = f"%{termo}%"
        cursor.execute(query, (like_termo, like_termo, like_termo))
        resultados = cursor.fetchall()
        cursor.close()
        conexao.close()
        return resultados
    except Exception as erro:
        messagebox.showerror("Erro no banco de dados", f"Erro ao buscar no PostgreSQL:\n{erro}")
        return []

