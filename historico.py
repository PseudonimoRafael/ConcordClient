# Gerencia o histórico de mensagens no banco de dados local

from models import db, Usuario, Messages
from peewee import IntegrityError
import datetime

def inicializar_banco(username):
    # Cada usuário terá seu próprio arquivo de banco de dados (ex: concord_teste1.db)
    db.init(f'concord_{username}.db')
    db.connect(reuse_if_open=True)
    db.create_tables([Usuario, Messages], safe=True)

def salvar_usuario(nickname):
    try:
        Usuario.get_or_create(nickname=nickname, defaults={"nome": nickname})
    except IntegrityError:
        pass

def salvar_mensagem(sender, receiver, content):
    salvar_usuario(sender)
    salvar_usuario(receiver)
    remetente = Usuario.get(Usuario.nickname == sender)
    destinatario = Usuario.get(Usuario.nickname == receiver)
    
    ultima_msg = (Messages
                  .select()
                  .where((Messages.sender_id == remetente) & (Messages.reciver_id == destinatario))
                  .order_by(Messages.id.desc())
                  .first())
    
    if ultima_msg and ultima_msg.content == content:
        agora = datetime.datetime.now()
        diferenca = (agora - ultima_msg.timestamp).total_seconds()
        
        if diferenca < 1.0:
            return

    Messages.create(
        content=content,
        sender_id=remetente,
        reciver_id=destinatario
    )

def buscar_historico(usuario1, usuario2):
    salvar_usuario(usuario1)
    salvar_usuario(usuario2)
    u1 = Usuario.get(Usuario.nickname == usuario1)
    u2 = Usuario.get(Usuario.nickname == usuario2)
    mensagens = (Messages
        .select()
        .where(
            ((Messages.sender_id == u1) & (Messages.reciver_id == u2)) |
            ((Messages.sender_id == u2) & (Messages.reciver_id == u1))
        )
        .order_by(Messages.id.asc())
    )
    resultado = []
    for msg in mensagens:
        sender_nick = msg.sender_id.nickname
        resultado.append((sender_nick, msg.content))
    return resultado