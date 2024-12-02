from config.database import criar_conexao, fechar_conexao


class Venda:
    def __init__(self, cpf_cliente=None, id_colaborador=None, itens=None):
        self.cpf_cliente = cpf_cliente
        self.id_colaborador = id_colaborador
        self.itens = itens or []

    def registrar_venda(self):
        conn = criar_conexao()
        try:
            with conn.cursor() as cursor:
                total = 0

                for item in self.itens:
                    sql_busca = "SELECT ID_medicamento, preco, estoque FROM Medicamentos WHERE nome = %s"
                    cursor.execute(sql_busca, (item['nome_medicamento'],))
                    medicamento = cursor.fetchone()

                    if not medicamento:
                        raise ValueError(f"Medicamento '{item['nome_medicamento']}' não encontrado.")

                    id_medicamento, preco_unitario, estoque_atual = medicamento

                    if estoque_atual < item['quantidade']:
                        raise ValueError(f"Estoque insuficiente para o medicamento '{item['nome_medicamento']}'.")

                    subtotal = preco_unitario * item['quantidade']
                    total += subtotal

                    item['id_medicamento'] = id_medicamento
                    item['preco_unitario'] = preco_unitario

                sql_venda = """
                INSERT INTO Vendas (data_venda, total, ID_colaborador, cpf)
                VALUES (CURRENT_DATE, %s, %s, %s) RETURNING ID_venda
                """
                cursor.execute(sql_venda, (total, self.id_colaborador, self.cpf_cliente))
                id_venda = cursor.fetchone()[0]

                sql_item_venda = """
                INSERT INTO Item_Venda (ID_venda, ID_medicamento, quantidade, preco_unitario)
                VALUES (%s, %s, %s, %s)
                """
                for item in self.itens:
                    cursor.execute(sql_item_venda, (id_venda, item['id_medicamento'], item['quantidade'], item['preco_unitario']))

                    novo_estoque = estoque_atual - item['quantidade']
                    sql_atualiza_estoque = "UPDATE Medicamentos SET estoque = %s WHERE ID_medicamento = %s"
                    cursor.execute(sql_atualiza_estoque, (novo_estoque, item['id_medicamento']))

                conn.commit()
                print(f"Venda registrada com sucesso! ID da Venda: {id_venda}")
                return id_venda
        except ValueError as ve:
            print(f"Erro: {ve}")
            conn.rollback()
            return None
        except Exception as e:
            print(f"Erro ao registrar venda: {e}")
            conn.rollback()
            return None
        finally:
            if conn:
                fechar_conexao(conn)

    @staticmethod
    def listar_vendas():
        """
        Lista todas as vendas, incluindo seus itens.
        """
        conn = criar_conexao()
        try:
            with conn.cursor() as cursor:
                sql_vendas = """
                SELECT v.ID_venda, v.data_venda, v.total, c.nome AS cliente, col.nome AS colaborador
                FROM Vendas v
                INNER JOIN Clientes c ON v.cpf = c.cpf
                INNER JOIN Colaboradores col ON v.ID_colaborador = col.ID_colaborador
                ORDER BY v.data_venda DESC
                """
                cursor.execute(sql_vendas)
                vendas = cursor.fetchall()

                if vendas:
                    print("\n--- Lista de Vendas ---")
                    for venda in vendas:
                        print(f"\nVenda ID: {venda[0]}, Data: {venda[1]}, Total: R$ {venda[2]:.2f}")
                        print(f"Cliente: {venda[3]}, Colaborador: {venda[4]}")

                        sql_itens = """
                        SELECT iv.ID_item_venda, m.nome AS medicamento, iv.quantidade, iv.preco_unitario
                        FROM Item_Venda iv
                        INNER JOIN Medicamentos m ON iv.ID_medicamento = m.ID_medicamento
                        WHERE iv.ID_venda = %s
                        """
                        cursor.execute(sql_itens, (venda[0],))
                        itens = cursor.fetchall()

                        print("Itens da Venda:")
                        print(f"{'ID':<5} {'Medicamento':<20} {'Qtd':<5} {'Preço Unitário':<15}")
                        for item in itens:
                            print(f"{item[0]:<5} {item[1]:<20} {item[2]:<5} R$ {item[3]:<10.2f}")
                else:
                    print("Nenhuma venda encontrada.")
        except Exception as e:
            print(f"Erro ao listar vendas: {e}")
        finally:
            if conn:
                fechar_conexao(conn)

    @staticmethod
    def buscar_venda_por_id(id_venda):
        conn = criar_conexao()
        try:
            with conn.cursor() as cursor:
                sql_venda = """
                SELECT v.ID_venda, v.data_venda, v.total, c.nome AS cliente, col.nome AS colaborador
                FROM Vendas v
                INNER JOIN Clientes c ON v.cpf = c.cpf
                INNER JOIN Colaboradores col ON v.ID_colaborador = col.ID_colaborador
                WHERE v.ID_venda = %s
                """
                cursor.execute(sql_venda, (id_venda,))
                venda = cursor.fetchone()

                if venda:
                    print(f"\n--- Detalhes da Venda ---\n")
                    print(f"ID da Venda: {venda[0]}")
                    print(f"Data da Venda: {venda[1]}")
                    print(f"Total: R$ {venda[2]:.2f}")
                    print(f"Cliente: {venda[3]}")
                    print(f"Colaborador: {venda[4]}")

                    sql_itens = """
                    SELECT iv.ID_item_venda, m.nome AS medicamento, iv.quantidade, iv.preco_unitario
                    FROM Item_Venda iv
                    INNER JOIN Medicamentos m ON iv.ID_medicamento = m.ID_medicamento
                    WHERE iv.ID_venda = %s
                    """
                    cursor.execute(sql_itens, (id_venda,))
                    itens = cursor.fetchall()

                    print("\nItens da Venda:")
                    print(f"{'ID':<5} {'Medicamento':<20} {'Qtd':<5} {'Preço Unitário':<15}")
                    for item in itens:
                        print(f"{item[0]:<5} {item[1]:<20} {item[2]:<5} R$ {item[3]:<10.2f}")
                    return venda
                else:
                    print("Venda não encontrada.")
                    return None
        except Exception as e:
            print(f"Erro ao buscar venda: {e}")
            return None
        finally:
            if conn:
                fechar_conexao(conn)

    @staticmethod
    def historico_compras_cliente(cpf_cliente):
        conn = criar_conexao()
        try:
            with conn.cursor() as cursor:
                sql = """
                SELECT v.ID_venda, v.data_venda, v.total, col.nome AS colaborador
                FROM Vendas v
                INNER JOIN Colaboradores col ON v.ID_colaborador = col.ID_colaborador
                WHERE v.cpf = %s
                ORDER BY v.data_venda DESC
                """
                cursor.execute(sql, (cpf_cliente,))
                vendas = cursor.fetchall()

                if vendas:
                    print(f"\n--- Histórico de Compras do Cliente ({cpf_cliente}) ---")
                    print(f"{'ID':<5} {'Data':<12} {'Total':<10} {'Colaborador':<20}")
                    print("-" * 60)
                    for venda in vendas:
                        print(f"{venda[0]:<5} {venda[1]:<12} R$ {venda[2]:<10.2f} {venda[3]:<20}")
                    return vendas
                else:
                    print("Nenhum histórico de compras encontrado para este cliente.")
                    return []
        except Exception as e:
            print(f"Erro ao buscar histórico de compras: {e}")
            return []
        finally:
            if conn:
                fechar_conexao(conn)

    @staticmethod
    def historico_vendas_colaborador(id_colaborador):
        conn = criar_conexao()
        try:
            with conn.cursor() as cursor:
                sql = """
                SELECT v.ID_venda, v.data_venda, v.total, c.nome AS cliente
                FROM Vendas v
                INNER JOIN Clientes c ON v.cpf = c.cpf
                WHERE v.ID_colaborador = %s
                ORDER BY v.data_venda DESC
                """
                cursor.execute(sql, (id_colaborador,))
                vendas = cursor.fetchall()

                if vendas:
                    print(f"\n--- Histórico de Vendas do Colaborador (ID: {id_colaborador}) ---")
                    print(f"{'ID':<5} {'Data':<12} {'Total':<10} {'Cliente':<20}")
                    print("-" * 60)
                    for venda in vendas:
                        print(f"{venda[0]:<5} {venda[1]:<12} R$ {venda[2]:<10.2f} {venda[3]:<20}")
                    return vendas
                else:
                    print("Nenhum histórico de vendas encontrado para este colaborador.")
                    return []
        except Exception as e:
            print(f"Erro ao buscar histórico de vendas: {e}")
            return []
        finally:
            if conn:
                fechar_conexao(conn)

    @staticmethod
    def atualizar_quantidade_itens(id_item_venda, nova_quantidade):
        conn = criar_conexao()
        try:
            with conn.cursor() as cursor:
                sql = """
                UPDATE Item_Venda
                SET quantidade = %s
                WHERE ID_item_venda = %s
                """
                cursor.execute(sql, (nova_quantidade, id_item_venda))
                conn.commit()
                print("Quantidade do item atualizada com sucesso.")
                return True
        except Exception as e:
            print(f"Erro ao atualizar quantidade do item: {e}")
            return False
        finally:
            if conn:
                fechar_conexao(conn)

    @staticmethod
    def atualizar_preco_estoque(id_item_venda, novo_preco_unitario):
        conn = criar_conexao()
        try:
            with conn.cursor() as cursor:
                sql = """
                UPDATE Item_Venda
                SET preco_unitario = %s
                WHERE ID_item_venda = %s
                """
                cursor.execute(sql, (novo_preco_unitario, id_item_venda))
                conn.commit()
                print("Preço do item atualizado com sucesso.")
                return True
        except Exception as e:
            print(f"Erro ao atualizar preço do item: {e}")
            return False
        finally:
            if conn:
                fechar_conexao(conn)

    @staticmethod
    def deletar_venda(id_venda):
        conn = criar_conexao()
        try:
            with conn.cursor() as cursor:
                sql_itens = """
                DELETE FROM Item_Venda
                WHERE ID_venda = %s
                """
                cursor.execute(sql_itens, (id_venda,))

                sql_venda = """
                DELETE FROM Vendas
                WHERE ID_venda = %s
                """
                cursor.execute(sql_venda, (id_venda,))
                conn.commit()
                print("Venda e itens relacionados removidos com sucesso.")
                return True
        except Exception as e:
            print(f"Erro ao deletar venda: {e}")
            return False
        finally:
            if conn:
                fechar_conexao(conn)
        