import customtkinter as ctk
from tkinter import messagebox
import psycopg2
import tkinter as tk

def conectar_banco():
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="Login",
            user="postgres",
            password="1234",
            port="5432"
        )
        return conn
    except Exception as e:
        messagebox.showerror("Erro de Conexão", f"Não foi possível conectar ao banco de dados:\n{e}")
        return None

def verificar_login(usuario, password):
    conn = conectar_banco()
    if conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM usuarios WHERE usuario=%s AND password=%s", (usuario, password))
        resultado = cur.fetchone()
        cur.close()
        conn.close()
        return resultado is not None
    return False

def login():
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    root = ctk.CTk()
    root.title("Login")
    root.geometry("420x400")
    root.resizable(False, False)

    frame = ctk.CTkFrame(root, corner_radius=15, fg_color="#1e1e1e")
    frame.pack(expand=True, padx=40, pady=40)

    sucesso = {'login': False}  # Usamos dicionário para modificar dentro da função interna

    def fazer_login(event=None):
        usuario = usuario_var.get()
        senha = senha_var.get()
        if verificar_login(usuario, senha):
            messagebox.showinfo("Login", "Login realizado com sucesso!")
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
    root.mainloop()

    return sucesso['login']
