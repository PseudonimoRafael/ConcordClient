"""
Essa classe é responsável por fazer as mensagens terem permanencia no computador.
Seja com banco de dados seja anotando tudo em um bloco de notas.
"""

class ListStorage:
    def __init__(self):
        # Em um futuro breve essa lista deve ser uma lista de tuplas
        self.Message = []
        self.Contacts = []

    def addToList(self, element, type):
        if type == "Message":
            self.Message.append(element)
        elif type == "Contact":
            self.Contacts.append(element)
        else:
            raise TypeError("That type is not valid")

    def getList(self, type):
        if type == "Messages":
            return self.Message
        elif type == "Contacts":
            return self.Contacts
        else:
            raise TypeError("That type is not valid")