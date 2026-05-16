from peewee import *
import datetime

# Inicia o banco vazio. Ele receberá o nome correto após o login.
db = SqliteDatabase(None)

class BaseModel(Model):
    class Meta:
        database = db

class Usuario(BaseModel):
    nickname = CharField(unique=True)
    nome = CharField()

class Messages(BaseModel):
    content = TextField()
    timestamp = DateTimeField(default=datetime.datetime.now)
    sender_id = ForeignKeyField(Usuario, backref='sender_id') 
    reciver_id = ForeignKeyField(Usuario, backref='reciver_id')