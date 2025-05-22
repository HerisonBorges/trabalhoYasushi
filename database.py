# Importa o psycopg2 para trabalhar com PostgreSQL e messagebox para exibir mensagens de erro
import psycopg2
from tkinter import messagebox

def conectarBancoDeDados():
    try:
        # Conecta ao banco de dados PostgreSQL
        conexao = psycopg2.connect(
            host="localhost",
            database="produtos_db",
            user="postgres",
            password="0l0k1nh0123",
        )
        return conexao
    except Exception as erro:
        # Mostra mensagem de erro caso a conexão falhe
        messagebox.showerror("Erro no banco de dados", f"Erro ao conectar ao PostgreSQL\n{erro}")
        return None

# Função para inserir um novo produto no banco de dados
def insert(nome_produto, cod_produto, validade, fornecedor, categoria, unidade, obs):
        conexao = conectarBancoDeDados()
        cursor = conexao.cursor()
        
        # Executa o comando de inserção (INSERT)
        cursor.execute("""
            INSERT INTO produtos (nome_produto, cod_produto, validade, fornecedor, categoria, unidade, observacoes)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (nome_produto, cod_produto, validade, fornecedor, categoria, unidade, obs))
        
        # Confirma a inserção no banco
        conexao.commit() #Salva as alterações
        cursor.close() # Fecha o QueryTool

def selectAll():
    conexao = conectarBancoDeDados()
    cursor = conexao.cursor()

    # Executa o comando SELECT para buscar todos os produtos
    cursor.execute("""
        SELECT nome_produto, cod_produto, validade, fornecedor, categoria, unidade, observacoes
        FROM produtos
    """)
    
    # Retorna todos os resultados encontrados
    resultados = cursor.fetchall()
    cursor.close()
    conexao.close()

    return resultados

# Função para buscar um único produto com base em um campo específico
def selectCampo(campo, valor):
        conexao = conectarBancoDeDados()
        cursor = conexao.cursor()

        # Monta dinamicamente a consulta SQL usando o nome do campo (ex: cod_produto, nome_produto, etc)
        query = f"""
            SELECT nome_produto, cod_produto, validade, fornecedor, categoria, unidade, observacoes
            FROM produtos
            WHERE {campo} = %s
        """
        cursor.execute(query, (valor,))
        resultado = cursor.fetchone()  # Retorna apenas um resultado
        cursor.close()

        return resultado
# Função para buscar produtos com base em um termo que pode estar no nome, código ou fornecedor
def selectSpecific(termo):
        conexao = conectarBancoDeDados()
        cursor = conexao.cursor()
        
        # Consulta usando ILIKE para busca insensível a maiúsculas/minúsculas
        query = """
            SELECT nome_produto, cod_produto, validade, fornecedor, categoria, unidade, observacoes
            FROM produtos
            WHERE nome_produto ILIKE %s
               OR cod_produto ILIKE %s
               OR fornecedor ILIKE %s
               OR categoria ILIKE %s
        """
        like_termo = f"%{termo}%"  # Formata o termo para busca parcial
        cursor.execute(query, (like_termo, like_termo, like_termo, like_termo))
        
        resultados = cursor.fetchall()  # Retorna todos os resultados encontrados
        cursor.close()
        return resultados

# Função para atualizar os dados de um produto já existente
def update(cod_antigo, novos_dados):
        conexao = conectarBancoDeDados()
        cursor = conexao.cursor()
        
        # Comando UPDATE, usando o código antigo para localizar o registro correto
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

        return True  # Retorna True se a operação for bem-sucedida