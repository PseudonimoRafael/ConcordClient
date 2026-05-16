# Interface gráfica do cliente de chat

import tkinter as tk
from tkinter import messagebox
from comunication import Comunication
from historico import inicializar_banco, salvar_mensagem, buscar_historico

ASCII_ART = """
  _    _              ____         _ 
 | |  | |     /\     |  _ \       | |
 | |  | |    /  \    | |_) |      | |
 | |  | |   / /\ \   |  _ <   _   | |
 | |__| |  / ____ \  | |_) | | |__| |
  \____/  /_/    \_\ |____/   \____/ 
                             
"""

class ChatApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Concord — UABJ")
        self.root.resizable(False, False)

        self.com = Comunication()
        self.com.on_message_callback = self.processar_pacote_recebido
        self.username = ""
        self.historico = {}
        self.contato_ativo = None
        self.typing_timer = None
        self.estou_digitando = False

        inicializar_banco()

        try:
            self.com.connect()
        except Exception:
            messagebox.showerror("Erro", "Servidor offline.")
            root.destroy()
            return

        self.tela_login()

    def tela_login(self):
        self.root.geometry("320x420")
        self.frame_login = tk.Frame(self.root, bg="#f0f0f0")
        self.frame_login.pack(fill=tk.BOTH, expand=True)

        frame_topo = tk.Frame(self.frame_login, bg="#f0f0f0", pady=20)
        frame_topo.pack(fill=tk.X)

        tk.Label(
            frame_topo,
            text=ASCII_ART,
            font=("Courier", 10, "bold"),
            fg="#555555",
            bg="#f0f0f0",
            justify="center"
        ).pack()

        tk.Label(
            frame_topo,
            text="ZapZap",
            font=("Arial", 9),
            fg="#888888",
            bg="#f0f0f0"
        ).pack()

        frame_campos = tk.Frame(self.frame_login, bg="#f0f0f0", pady=20, padx=30)
        frame_campos.pack(fill=tk.BOTH, expand=True)

        tk.Label(frame_campos, text="Nickname", bg="#f0f0f0", anchor="w").pack(fill=tk.X)
        self.entry_user = tk.Entry(frame_campos, width=30)
        self.entry_user.pack(fill=tk.X, pady=(2, 12))

        tk.Label(frame_campos, text="Senha", bg="#f0f0f0", anchor="w").pack(fill=tk.X)
        self.entry_pass = tk.Entry(frame_campos, show="*", width=30)
        self.entry_pass.pack(fill=tk.X, pady=(2, 20))

        frame_botoes = tk.Frame(frame_campos, bg="#f0f0f0")
        frame_botoes.pack(fill=tk.X)

        tk.Button(
            frame_botoes,
            text="Entrar",
            command=self.acao_login,
            bg="#555555",
            fg="white",
            width=10
        ).pack(side=tk.LEFT)

        tk.Button(
            frame_botoes,
            text="Registrar",
            command=self.acao_registrar,
            bg="#f0f0f0",
            width=10
        ).pack(side=tk.RIGHT)

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
        self.root.geometry("600x500")
        self.root.resizable(True, True)
        self.frame_login.destroy()
        self.frame_chat = tk.Frame(self.root)
        self.frame_chat.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.frame_chat.columnconfigure(1, weight=1)
        self.frame_chat.rowconfigure(1, weight=1)

        tk.Label(self.frame_chat, text="Contatos").grid(row=0, column=0)
        tk.Label(self.frame_chat, text="Mensagens").grid(row=0, column=1)

        self.lista_contatos = tk.Listbox(self.frame_chat, width=20)
        self.lista_contatos.grid(row=1, column=0, sticky="ns", padx=5)
        self.lista_contatos.bind("<<ListboxSelect>>", self.selecionar_contato)

        self.caixa_texto = tk.Text(self.frame_chat, state='disabled')
        self.caixa_texto.grid(row=1, column=1, sticky="nsew")

        self.label_digitando = tk.Label(self.frame_chat, text="", fg="gray", font=("Arial", 8, "italic"))
        self.label_digitando.grid(row=2, column=1, sticky="w")

        frame_envio = tk.Frame(self.frame_chat)
        frame_envio.grid(row=3, column=0, columnspan=2, sticky="we", pady=5)
        frame_envio.columnconfigure(0, weight=1)

        self.entry_msg = tk.Entry(frame_envio)
        self.entry_msg.grid(row=0, column=0, sticky="we", padx=5)
        self.entry_msg.bind("<KeyRelease>", self.ao_digitar)

        tk.Button(frame_envio, text="Enviar", command=self.acao_enviar).grid(row=0, column=1, padx=5)

    def ao_digitar(self, event):
        if not self.contato_ativo:
            return
        if not self.estou_digitando:
            self.estou_digitando = True
            self.com.send_packet({
                "type": "TYPING_START",
                "sender": self.username,
                "receiver": self.contato_ativo
            })
        if self.typing_timer:
            self.root.after_cancel(self.typing_timer)
        self.typing_timer = self.root.after(2000, self.parou_de_digitar)

    def parou_de_digitar(self):
        if self.estou_digitando and self.contato_ativo:
            self.estou_digitando = False
            self.com.send_packet({
                "type": "TYPING_STOP",
                "sender": self.username,
                "receiver": self.contato_ativo
            })

    def selecionar_contato(self, event):
        selecao = self.lista_contatos.curselection()
        if not selecao:
            return
        contato = self.lista_contatos.get(selecao[0]).split(":")[0]
        self.contato_ativo = contato

        msgs_banco = buscar_historico(self.username, contato)
        self.historico[contato] = []
        for sender_nick, content in msgs_banco:
            if sender_nick == self.username:
                self.historico[contato].append(f"Você -> {contato}: {content}")
            else:
                self.historico[contato].append(f"{sender_nick}: {content}")

        self.caixa_texto.config(state='normal')
        self.caixa_texto.delete(1.0, tk.END)
        for msg in self.historico[contato]:
            self.caixa_texto.insert(tk.END, msg + "\n")
        self.caixa_texto.config(state='disabled')
        self.caixa_texto.see(tk.END)

    def acao_enviar(self):
        texto = self.entry_msg.get()
        if not self.contato_ativo:
            messagebox.showwarning("Aviso", "Selecione um contato!")
            return
        if texto:
            pacote = {"type": "MESSAGE", "sender": self.username, "receiver": self.contato_ativo, "content": texto}
            self.com.send_packet(pacote)
            salvar_mensagem(self.username, self.contato_ativo, texto)
            self.adicionar_ao_historico(self.contato_ativo, f"Você -> {self.contato_ativo}: {texto}")
            self.entry_msg.delete(0, tk.END)
            self.parou_de_digitar()

    def adicionar_ao_historico(self, contato, mensagem):
        if contato not in self.historico:
            self.historico[contato] = []
        self.historico[contato].append(mensagem)

        if contato == self.contato_ativo:
            self.caixa_texto.config(state='normal')
            self.caixa_texto.insert(tk.END, mensagem + "\n")
            self.caixa_texto.config(state='disabled')
            self.caixa_texto.see(tk.END)

    def processar_pacote_recebido(self, pacote):
        tipo = pacote.get("type")

        if tipo == "LOGIN_OK":
            self.root.after(0, self.tela_chat)
        elif tipo == "LOGIN_FAIL":
            self.root.after(0, lambda: messagebox.showerror("Erro", "Credenciais incorretas!"))
        elif tipo == "REGISTER_OK":
            self.root.after(0, lambda: messagebox.showinfo("Sucesso", "Registrado! Faça login."))
        elif tipo == "REGISTER_FAIL":
            self.root.after(0, lambda: messagebox.showerror("Erro", "Nickname já existe!"))
        elif tipo == "CONTACT_LIST":
            contatos = pacote.get("messageList", [])
            self.root.after(0, self.atualizar_lista_contatos, contatos)
        elif tipo == "MESSAGE":
            remetente = pacote.get("sender")
            conteudo = pacote.get("content")
            salvar_mensagem(remetente, self.username, conteudo)
            self.root.after(0, self.adicionar_ao_historico, remetente, f"{remetente}: {conteudo}")
        elif tipo == "TYPING_START":
            remetente = pacote.get("sender")
            self.root.after(0, self.mostrar_digitando, remetente)
        elif tipo == "TYPING_STOP":
            self.root.after(0, self.esconder_digitando)
        elif tipo == "STATUS_UPDATE":
            pass

    def mostrar_digitando(self, nickname):
        self.label_digitando.config(text=f"{nickname} está digitando...")

    def esconder_digitando(self):
        self.label_digitando.config(text="")

    def atualizar_lista_contatos(self, contatos):
        self.lista_contatos.delete(0, tk.END)
        for c in contatos:
            if not c.startswith(self.username + ":"):
                self.lista_contatos.insert(tk.END, c)

if __name__ == "__main__":
    root = tk.Tk()
    app = ChatApp(root)
    root.mainloop()