from MemoryStorage import ListStorage

class ListPresentation:
    # Qualuqer metodo que herde essa classe deve ter a habilidade de listar
    # instancias de sua classe de forma simples.
    #
    lista = ListStorage()

    def addToList(self, element):
        lista.addToList(element, self.myType)

    def present(self, end=10):
        elemnets = ListPresentation.lista.getList(self.myType)[-end:]
        for el in elemnets:
            print(elemnets) 

    def myType(self):
        return "ListPresentation"

class Messages(ListPresentation):
    def __init__(self, message, user, datetime):
        self.message = message
        self.user = user
        self.datetime = datetime

    def __str__(self):
        return f'{self.user} {self.datetime.date}\n -> {self.message}\n\n'

    def myType(self):
        return "Messages"

class Contacts(ListPresentation):
    def __init__(self, user):
        self.user = user
        self.last_message = "" # Ultima mensagem encontrada. Não implementado

    def __str__(self):
        return f"---\n{self.__user.name}\n\n---"

    def myType(self):
        return "Contacts"