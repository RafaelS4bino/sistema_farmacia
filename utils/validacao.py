from config.database import criar_conexao, fechar_conexao


def validar_cpf(cpf):
    cpf = ''.join(filter(str.isdigit, cpf))
    if len(cpf) != 11 or cpf == cpf[0] * 11:
        return False
    
    soma1 = sum(int(cpf[i]) * (10 - i) for i in range(9))
    digito1 = (soma1 * 10) % 11
    if digito1 == 10:
        digito1 = 0
    
    soma2 = sum(int(cpf[i]) * (11 - i) for i in range(10))
    digito2 = (soma2 * 10) % 11
    if digito2 == 10:
        digito2 = 0
    if int(cpf[9]) == digito1 and int(cpf[10]) == digito2:
        return True
    
    return False


def validar_cargo(cpf):
    cpf = ''.join(filter(str.isdigit, cpf))
    try:
        conn = criar_conexao()
        with conn.cursor() as cursor:
            sql = "SELECT cargo FROM Colaboradores WHERE CPF_colaborador = %s"
            cursor.execute(sql, (cpf,))
            result = cursor.fetchone()
            if not result:
                print("Colaborador não encontrado.")
                return None
            return result[0]
    except Exception as e:
        print(f"Erro ao verificar cargo: {e}")
        return None
    finally:
        fechar_conexao(conn)
