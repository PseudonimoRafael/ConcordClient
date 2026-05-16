"""
Em resumo, quando o app precisar se comunicar com o banco de dados, é de bom tom que
use a palavra reservada With. É boa pratica. Que nem falar eu te amo para sua mãe
"""

from models import *

class DatabaseConnect:
    def __enter__(self):
        db.connect()
        db.create_tables([Usuario, Messages])

    def __exit__(self):
        pass

