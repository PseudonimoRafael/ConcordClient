"""
Pequeno crud para adicionar e remover usuarios
"""

from models import *

def createUser(nickname, nome): 
    try:
        return Usuario.create(nickname=nickname, nome=nome)
    except IntegrityError:
        print(f"Erro: Nickname '{nickname}' já existe.")
        return None

def readUser(nickname):
    return Usuario.get_or_none(Usuario.nickname == nickname)

def deleteUser(nickname):
    query = Usuario.delete().where(Usuario.nickname == nickname)
    return query.execute()  # Retorna o número de linhas deletadas

# Carrega uma lista de usuarios especificada pela quantidade passada no argumento
def loadUsers(len=10):
    # Retorna um dicionario
    # return Usuario.select().limit(tam).dicts()
    return Usuario.select().limit(tam)
