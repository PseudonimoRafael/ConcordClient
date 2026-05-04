"""
Pequeno crud para adicionar e remover mensagens
"""

from models import *

def createMessage(content, sender_id, reciver_id):
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

def listHistory(user_a_id, user_b_id):
    return (Messages
            .select()
            .where(
                ((Messages.sender_id == user_a_id) & (Messages.reciver_id == user_b_id)) |
                ((Messages.sender_id == user_b_id) & (Messages.reciver_id == user_a_id))
            )
            .order_by(Messages.id.asc())) # Ordena por ordem de envio