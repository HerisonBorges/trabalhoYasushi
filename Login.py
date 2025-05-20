import customtkinter as ctk
from tkinter import messagebox
import tkinter as tk
import database

#Na parte de login, o usuário não precisa informar os dados do banco de dados, apenas o usuário e a senha que a gente decidiu para os adm (que seria Usuário: Admin Senha: 1234).

def login(master):
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    
    root = ctk.CTkToplevel(master)
    root.title("Login")
    
    #Centralizando a janela
    largura_janela = 420
    altura_janela = 400

    pos_x = int(root.winfo_screenwidth() / 2 - largura_janela / 2)
    pos_y = int(root.winfo_screenheight() / 2 - altura_janela / 2)

    root.geometry(f"{largura_janela}x{altura_janela}+{pos_x}+{pos_y}")
    root.resizable(False, False)

    frame = ctk.CTkFrame(root, corner_radius=15, fg_color="#1e1e1e")
    frame.pack(expand=True, padx=40, pady=40)

    def verificar_login(usuario, senha):
        usuarios_validos = {
            "Admin": "1234" #Nessa parte você pode adicionar mais usuários e senhas por comando(ainda não criado) ou manualmente
        }
        
        #Vai verificar cada usuário e senha presente no dicionário
        #Ainda não tem diferenciações entre adm e usuário comum
        for usuario_valido, senha_valida in usuarios_validos.items():
            if usuario == usuario_valido and senha == senha_valida:
                return True
        return False

    sucesso = {'login': False}

    def fazer_login(event=None):
        usuario = usuario_var.get()
        senha = senha_var.get()
        
        if verificar_login(usuario, senha):
            sucesso['login'] = True
            root.destroy()
        else:
            messagebox.showerror("Erro", "Usuário ou senha incorretos.")

    def toggle_senha():
        if entry_senha.cget("show") == "":
            entry_senha.configure(show="*")
            btn_mostrar.configure(text="Mostrar")
        else:
            entry_senha.configure(show="")
            btn_mostrar.configure(text="Ocultar")

    usuario_var = tk.StringVar()
    senha_var = tk.StringVar()

    ctk.CTkLabel(frame, text="Login no Sistema", font=("Century Gothic", 22, "bold")).pack(pady=(10, 20))
    ctk.CTkLabel(frame, text="Usuário:", font=("Century Gothic", 14)).pack(anchor="w", padx=10)
    ctk.CTkEntry(frame, textvariable=usuario_var, width=260).pack(pady=(0, 15))
    ctk.CTkLabel(frame, text="Senha:", font=("Century Gothic", 14)).pack(anchor="w", padx=10)
    
    senha_frame = ctk.CTkFrame(frame, fg_color="transparent")
    senha_frame.pack()
    
    entry_senha = ctk.CTkEntry(senha_frame, textvariable=senha_var, width=190, show="*")
    entry_senha.pack(side="left", pady=(0, 10), padx=(0, 10))
    
    btn_mostrar = ctk.CTkButton(senha_frame, text="Mostrar", width=60, command=toggle_senha)
    btn_mostrar.pack(side="left", pady=(0, 10))

    ctk.CTkButton(frame, text="Entrar", command=fazer_login, width=150, font=("Century Gothic", 14, "bold")).pack(pady=(10, 10))

    root.bind("<Return>", fazer_login)
    root.protocol("WM_DELETE_WINDOW", master.destroy)  # Fecha o programa se a janela de login for fechada

    master.wait_window(root)  # Espera o fechamento da janela de login
    return sucesso