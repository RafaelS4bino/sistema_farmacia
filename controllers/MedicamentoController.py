from Models.MedicamentoModel import Medicamento

class medicamento_controller:
    @staticmethod
    def cadastrar_medicamento(nome, categoria, preco, estoque):
        return Medicamento.cadastrar_medicamento(nome, categoria, preco, estoque)

    @staticmethod
    def listar_medicamentos():
        medicamentos = Medicamento.listar_medicamentos()
        if not medicamentos:
            print("Nenhum medicamento encontrado.")
        else:
            print("\n--- Medicamentos Cadastrados ---")
            for medicamento in medicamentos:
                print(medicamento)

    @staticmethod
    def buscar_medicamento(nome):
        medicamentos = Medicamento.buscar_medicamento(nome)
        if not medicamentos:
            print("Nenhum medicamento encontrado com esse nome.")
        else:
            print("\n--- Resultado da Busca ---")
            for medicamento in medicamentos:
                print(medicamento)

    @staticmethod
    def atualizar_estoque(nome, quantidade):
        return Medicamento.atualizar_estoque(nome, quantidade)

    @staticmethod
    def atualizar_preco(nome, preco):
        return Medicamento.atualizar_preco(nome, preco)

    @staticmethod
    def deletar_medicamento(id_medicamento):
        return Medicamento.deletar_medicamento(id_medicamento)
