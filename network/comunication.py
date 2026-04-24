"""
Obs: Seria muito bom se existisse um erro próprio para quando o canal
não estivesse aberto. já que a conexão pode ser perdida.
"""
import socket
import struct
from addres import (HOST, PORT)

class Comunication:
    chan = None

    @classmethod    
    def openComunication(cls):
        cls.chan = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        cls.chan.connect((HOST, PORT))

    @classmethod
    def closeComunication(cls):
        if cls.chan != None:
            cls.chan.close()
            cls.chan = None
 
    def __init__(self, message):
        self.message = bytearray(message, 'utf-8')
        self.answer = None
    
    @staticmethod
    def recv_all(sock, n):
    # 'n' é o tamanho da cadeia de bits que será recebido
        data = bytearray()
        while len(data) < n:
            try:
                packet = sock.recv(n - len(data))
                if not packet:
                    return None 
                data.extend(packet)
            except socket.error:
                return None
        return data
    
    def reciveMessage(self): #---
        header = self.recv_all(self.chan, 4)
        if header is None:
            self.answer = None
            # Por um erro aqui!!
            return

        msg_len = struct.unpack('>I', header)[0]
        payload = self.recv_all(self.chan, msg_len)
        if payload != None:
            self.answer = payload.decode('utf-8')
        else:
            self.answer = None
        
    def sendMesage(self): #---
        tam = len(self.message)
        header = struct.pack('>I', tam)
        try:
            self.chan.sendall(header + self.message)
        except socket.error as e:
            print(f"Erro ao enviar mensagem: {e}")

    ## Ainda não implementado
    def SendAndRecive(self):
        self.sendMesage()
        self.reciveMessage()
        return self.message 
