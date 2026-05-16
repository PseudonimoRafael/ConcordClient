from peewee import *

db = SqliteDatabase('concord.db')

class Usuario(Model):
    nickname = CharField(unique=True)
    nome = CharField()
    # last_seen = DateTimeField()

    class Meta:
        database = db

class Messages(Model):
    content = TextField()
    # datetime = DateTimeField()
    sender_id =  ForeignKeyField(Usuario, backref='sender_id' ) 
    reciver_id = ForeignKeyField(Usuario, backref='reciver_id')
    
    class Meta:
        database = db
