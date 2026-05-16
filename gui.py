# Interface gráfica do cliente de chat

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
        self.historico = {}          # dicionário: contato -> lista de mensagens
        self.contato_ativo = None    # contato selecionado no momento

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

        self.lista_contatos = tk.Listbox(self.frame_chat, width=20)
        self.lista_contatos.grid(row=1, column=0, sticky="ns", padx=5)
        # ao clicar em um contato, chama selecionar_contato
        self.lista_contatos.bind("<<ListboxSelect>>", self.selecionar_contato)

        self.caixa_texto = tk.Text(self.frame_chat, state='disabled', width=40)
        self.caixa_texto.grid(row=1, column=1, sticky="nsew")

        self.entry_msg = tk.Entry(self.frame_chat)
        self.entry_msg.grid(row=2, column=1, sticky="we", pady=5)
        tk.Button(self.frame_chat, text="Enviar", command=self.acao_enviar).grid(row=2, column=0)

    def selecionar_contato(self, event):
        selecao = self.lista_contatos.curselection()
        if not selecao:
            return
        contato = self.lista_contatos.get(selecao[0]).split(":")[0]
        self.contato_ativo = contato

        # limpa a caixa e exibe o histórico do contato selecionado
        self.caixa_texto.config(state='normal')
        self.caixa_texto.delete(1.0, tk.END)
        if contato in self.historico:
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
            self.adicionar_ao_historico(self.contato_ativo, f"Você -> {self.contato_ativo}: {texto}")
            self.entry_msg.delete(0, tk.END)

    def adicionar_ao_historico(self, contato, mensagem):
        if contato not in self.historico:
            self.historico[contato] = []
        self.historico[contato].append(mensagem)

        # atualiza a caixa só se o contato estiver ativo
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
            self.root.after(0, self.adicionar_ao_historico, remetente, f"{remetente}: {conteudo}")
        elif tipo == "STATUS_UPDATE":
            pass

    def atualizar_lista_contatos(self, contatos):
        self.lista_contatos.delete(0, tk.END)
        for c in contatos:
            # não mostra o próprio usuário na lista
            if not c.startswith(self.username + ":"):
                self.lista_contatos.insert(tk.END, c)

if __name__ == "__main__":
    root = tk.Tk()
    app = ChatApp(root)
    root.mainloop()