import bcrypt

def criptografar(senha):

    senha_bytes = senha.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(senha_bytes, salt)
    return hashed