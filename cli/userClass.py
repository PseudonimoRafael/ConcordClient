class User:
    def __init__(self, name, nickname):
        self.__name = name
        self.__nickname = nickname

    @property
    def name(self):
        return __name

    @property
    def nickname(self):
        return __nickname

class MainUser(User):
    # Cada cliente pode ter apenas um Usuario prinicpal logado por vez 
    # Equnato não exsitir a opção de trocar o usuario essa classe deve
    # garantir a unicidade dele.
    def __init__(self, name, mickname, password):
        self.__password = password
        super().__init__(name, nickname)