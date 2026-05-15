"""
Pequeno crud para adicionar e remover mensagens
"""

from models import *
from crudUser import (
    readUser,
)

def convertFromNick(func):
    def reciveNick(nick1, nick2, argument):
        user1 = readUser(nick1)
        user2 = readUser(nick2)

        if user1 != None and user2 != None:
            return func(user1, user2, argument)
        else:
            return None

    return reciveNick
        
@convertFromNick
def createMessage(sender_id, reciver_id, content):
    return Messages.create(
        content=content,
        sender_id = sender_id,
        reciver_id = reciver_id,
        )

def deleteMessage(messageID):
    try:
        return Message.get_by_id(messageID).delete_instance()
    except DoesNotExist:
        print(f"Aviso: Mensagem {messageID} não encontrada.")

def deleteChat(user_a_id, user_b_id):
    query = Messages.delete().where(
        ((Messages.sender_id == user_a_id) & (Messages.reciver_id == user_b_id)) |
        ((Messages.sender_id == user_b_id) & (Messages.reciver_id == user_a_id))
    )
    return query.execute()

@convertFromNick
def listHistory(user_a_id, user_b_id, tam):
    return (Messages
            .select()
            .where(
                ((Messages.sender_id == user_a_id) & (Messages.reciver_id == user_b_id)) |
                ((Messages.sender_id == user_b_id) & (Messages.reciver_id == user_a_id))
            )
            .order_by(Messages.id.asc()).limit(tam)) # Ordena por ordem de escrita no banco 