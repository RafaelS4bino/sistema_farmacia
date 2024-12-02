from Models.VendaModel import Venda

class venda_controller:
    def __init__(self):
        self.VendaModel = Venda()

    def registrar_venda(self, cpf_cliente, id_colaborador, itens):
        try:
            venda = Venda(cpf_cliente=cpf_cliente, id_colaborador=id_colaborador, itens=itens)
            id_venda = venda.registrar_venda()
            return id_venda
        except Exception as e:
            print(f"Erro ao registrar venda: {e}")
            return None
    
    def listar_vendas(self):
        try:
            return Venda.listar_vendas()
        except Exception as e:
            print(f"Erro ao listar vendas: {e}")
            return []
        
    def buscar_venda(self, id_venda):
        try:
            return Venda.buscar_venda_por_id(id_venda)
        except Exception as e:
            print(f"Erro ao buscar venda: {e}")
            return None
        
    def historico_compras_cliente(self, cpf_cliente):
        try:
            return Venda.historico_compras_cliente(cpf_cliente)
        except Exception as e:
            print(f"Erro ao buscar histórico de compras do cliente: {e}")
            return []
    
    def historico_vendas_colaborador(self, id_colaborador):
        try:
            return Venda.historico_vendas_colaborador(id_colaborador)
        except Exception as e:
            print(f"Erro ao buscar histórico de vendas do colaborador: {e}")
            return []
        
    def atualizar_quantidade_itens(self, id_item_venda, nova_quantidade):
        try:
            return Venda.atualizar_quantidade_itens(id_item_venda, nova_quantidade)
        except Exception as e:
            print(f"Erro ao atualizar quantidade do item: {e}")
            return False
    def atualizar_preco_itens(self, id_item_venda, novo_preco_unitario):
        try:
            return Venda.atualizar_preco_estoque(id_item_venda, novo_preco_unitario)
        except Exception as e:
            print(f"Erro ao atualizar preço do item: {e}")
            return False
    
    def deletar_venda(self, id_venda):
        try:
            return Venda.deletar_venda(id_venda)
        except Exception as e:
            print(f"Erro ao deletar venda: {e}")
            return False