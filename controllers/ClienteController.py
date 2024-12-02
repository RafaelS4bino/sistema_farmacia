from Models.ClienteModel import Cliente

class cliente_controller:

    @staticmethod
    def criar_cliente(nome, cpf, telefone):
        return Cliente.criar_cliente(nome, cpf, telefone)

    @staticmethod
    def listar_clientes():
        clientes = Cliente.listar_clientes()
        if not clientes:
            print("Nenhum cliente encontrado.")
            return []
        print("\n--- Clientes Cadastrados ---")
        for cliente in clientes:
            print(cliente)
        return clientes

    @staticmethod
    def buscar_cliente(nome):
        clientes = Cliente.buscar_cliente(nome)
        if not clientes:
            print("Nenhum cliente encontrado com esse nome.")
        else:
            print("\n--- Resultado da Busca ---")
            for cliente in clientes:
                print(cliente)
        return clientes

    @staticmethod
    def atualizar_telefone(cpf, telefone):
        return Cliente.atualizar_telefone(cpf, telefone)

    @staticmethod
    def deletar_cliente(cpf):
        return Cliente.deletar_cliente(cpf)
