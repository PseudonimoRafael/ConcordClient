import socket
import struct
import json
import threading
from addres import HOST, PORT

class Comunication:
    def __init__(self):
        self.chan = None
        self.on_message_callback = None

    def connect(self):
        self.chan = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.chan.connect((HOST, PORT))
        
        # Inicia uma Thread rodando em background só para escutar o servidor
        thread_escuta = threading.Thread(target=self._listen, daemon=True)
        thread_escuta.start()

    def _listen(self):
        while True:
            try:
                # Lê a linha JSON diretamente do servidor Java
                arquivo_socket = self.chan.makefile('r', encoding='utf-8')
                linha_json = arquivo_socket.readline()
                
                if not linha_json: break
                
                pacote_dict = json.loads(linha_json)
                
                if self.on_message_callback:
                    self.on_message_callback(pacote_dict)
                    
            except Exception as e:
                print("Conexão perdida:", e)
                break

    def send_packet(self, packet_dict):
        # Transforma o dicionário em string JSON e envia
        msg_json = json.dumps(packet_dict) + "\n"
        try:
            self.chan.sendall(msg_json.encode('utf-8'))
        except socket.error as e:
            print(f"Erro ao enviar mensagem: {e}")