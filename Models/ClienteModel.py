import psycopg2
from config.database import criar_conexao, fechar_conexao

class Cliente:
    @staticmethod
    def criar_cliente(nome, cpf, telefone):
        try:
            conn = criar_conexao()
            with conn:
                with conn.cursor() as cursor:
                    query = """
                    INSERT INTO Clientes (nome, CPF, telefone)
                    VALUES (%s, %s, %s)
                    """
                    cursor.execute(query, (nome, cpf, telefone))
                    conn.commit()
                    return True
        except psycopg2.Error as e:
            print(f"Erro ao criar cliente: {e}")
            return False
        finally:
            conn.close()

    @staticmethod
    def listar_clientes():
        try:
            conn = criar_conexao()
            with conn:
                with conn.cursor() as cursor:
                    query = "SELECT * FROM Clientes"
                    cursor.execute(query)
                    return cursor.fetchall()
        except psycopg2.Error as e:
            print(f"Erro ao listar clientes: {e}")
            return []
        finally:
            conn.close()

    @staticmethod
    def buscar_cliente(nome):
        try:
            conn = criar_conexao()
            with conn:
                with conn.cursor() as cursor:
                    query = "SELECT * FROM Clientes WHERE nome ILIKE %s"
                    cursor.execute(query, ('%' + nome + '%',))
                    return cursor.fetchall()
        except psycopg2.Error as e:
            print(f"Erro ao buscar cliente: {e}")
            return []
        finally:
            conn.close()

    @staticmethod
    def atualizar_telefone(cpf, telefone):
        try:
            conn = criar_conexao()
            with conn:
                with conn.cursor() as cursor:
                    query = "UPDATE Clientes SET telefone = %s WHERE CPF = %s"
                    cursor.execute(query, (telefone, cpf))
                    conn.commit()
                    return cursor.rowcount > 0
        except psycopg2.Error as e:
            print(f"Erro ao atualizar telefone: {e}")
            return False
        finally:
            conn.close()
            
    @staticmethod
    def deletar_cliente(cpf):
        try:
            conn = criar_conexao()
            with conn:
                with conn.cursor() as cursor:
                    query = "DELETE FROM Clientes WHERE CPF = %s"
                    cursor.execute(query, (cpf,))
                    conn.commit()
                    return cursor.rowcount > 0
        except psycopg2.Error as e:
            print(f"Erro ao deletar cliente: {e}")
            return False
        finally:
            conn.close()