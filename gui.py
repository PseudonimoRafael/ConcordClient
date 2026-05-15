import tkinter as tk
from tkinter import messagebox
from comunication import Comunication
class ChatApp:
    def __init__(self, root):
        self.root = root
        self.root.title("WhatsApp da UFRPE")
        self.root.geometry("500x400")
        
        self.com = Comunication()
        self.com.on_message_callback = self.processar_pacote_recebido
        self.username = ""

        try:
            self.com.connect()
        except Exception:
            messagebox.showerror("Erro", "Servidor offline.")
            root.destroy()
            return

        self.tela_login()

    def tela_login(self):
        self.frame_login = tk.Frame(self.root)
        self.frame_login.pack(pady=50)

        tk.Label(self.frame_login, text="Nickname:").grid(row=0, column=0, pady=5)
        self.entry_user = tk.Entry(self.frame_login)
        self.entry_user.grid(row=0, column=1)

        tk.Label(self.frame_login, text="Senha:").grid(row=1, column=0, pady=5)
        self.entry_pass = tk.Entry(self.frame_login, show="*")
        self.entry_pass.grid(row=1, column=1)

        tk.Button(self.frame_login, text="Entrar", command=self.acao_login).grid(row=2, column=0, pady=15)
        tk.Button(self.frame_login, text="Registrar", command=self.acao_registrar).grid(row=2, column=1)

    def acao_login(self):
        user = self.entry_user.get()
        senha = self.entry_pass.get()
        self.username = user
        self.com.send_packet({"type": "LOGIN", "sender": user, "content": senha})

    def acao_registrar(self):
        user = self.entry_user.get()
        senha = self.entry_pass.get()
        self.com.send_packet({"type": "REGISTER", "sender": user, "content": senha})

    def tela_chat(self):
        self.frame_login.destroy()
        self.frame_chat = tk.Frame(self.root)
        self.frame_chat.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        tk.Label(self.frame_chat, text="Contatos (Selecione um)").grid(row=0, column=0)
        tk.Label(self.frame_chat, text="Mensagens").grid(row=0, column=1)

        # Lista de Contatos
        self.lista_contatos = tk.Listbox(self.frame_chat, width=20)
        self.lista_contatos.grid(row=1, column=0, sticky="ns", padx=5)

        # Histórico de Chat
        self.caixa_texto = tk.Text(self.frame_chat, state='disabled', width=40)
        self.caixa_texto.grid(row=1, column=1, sticky="nsew")

        # Área de Envio
        self.entry_msg = tk.Entry(self.frame_chat)
        self.entry_msg.grid(row=2, column=1, sticky="we", pady=5)
        tk.Button(self.frame_chat, text="Enviar", command=self.acao_enviar).grid(row=2, column=0)

    def acao_enviar(self):
        texto = self.entry_msg.get()
        selecao = self.lista_contatos.curselection()
        
        if not selecao:
            messagebox.showwarning("Aviso", "Selecione um contato na lista para enviar!")
            return
            
        contato_selecionado = self.lista_contatos.get(selecao[0]).split(":")[0] # Pega só o nick, ignora o status
        
        if texto:
            pacote = {"type": "MESSAGE", "sender": self.username, "receiver": contato_selecionado, "content": texto}
            self.com.send_packet(pacote)
            self.atualizar_chat(f"Você -> {contato_selecionado}: {texto}")
            self.entry_msg.delete(0, tk.END)

    def atualizar_chat(self, mensagem):
        self.caixa_texto.config(state='normal')
        self.caixa_texto.insert(tk.END, mensagem + "\n")
        self.caixa_texto.config(state='disabled')
        self.caixa_texto.see(tk.END)

    def processar_pacote_recebido(self, pacote):
        tipo = pacote.get("type")
        
        # O Tkinter precisa que atualizações de tela rodem na Thread principal (usando self.root.after)
        if tipo == "LOGIN_OK":
            self.root.after(0, self.tela_chat)
        elif tipo == "LOGIN_FAIL":
            self.root.after(0, lambda: messagebox.showerror("Erro", "Credenciais incorretas!"))
        elif tipo == "REGISTER_OK":
            self.root.after(0, lambda: messagebox.showinfo("Sucesso", "Registrado! Faça login."))
        elif tipo == "CONTACT_LIST":
            contatos = pacote.get("messageList", [])
            self.root.after(0, self.atualizar_lista_contatos, contatos)
        elif tipo == "MESSAGE":
            remetente = pacote.get("sender")
            conteudo = pacote.get("content")
            self.root.after(0, self.atualizar_chat, f"{remetente}: {conteudo}")

    def atualizar_lista_contatos(self, contatos):
        self.lista_contatos.delete(0, tk.END)
        for c in contatos:
            self.lista_contatos.insert(tk.END, c)

if __name__ == "__main__":
    root = tk.Tk()
    app = ChatApp(root)
    root.mainloop()