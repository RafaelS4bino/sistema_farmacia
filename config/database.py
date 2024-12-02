import psycopg2

def criar_conexao():
    try:
        conn = psycopg2.connect(
            dbname = 'farmacia',
            user = 'postgres',
            password = '12345',
            host = 'localhost',
            port = '5432'
        )
        with conn.cursor() as cursor:
            cursor.execute("SET search_path TO farmacia;")
        return conn
    except Exception as e:
        print (f"Erro ao conectar com o banco de dados: {e}")
        return e

def fechar_conexao(conn):
    try:
        if conn:
            conn.close()
        else:
            print("Nenhuma conexão ativa para fechar.")
    except Exception as e:
        print(f"Erro ao fechar a conexão: {e}")