import customtkinter as ctk
from tkinter import messagebox
import psycopg2
import tkinter as tk

# Conexão com o banco PostgreSQL
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
    root.geometry("420x350")
    root.resizable(False, False)

    # Frame centralizado com visual mais elegante
    frame = ctk.CTkFrame(root, corner_radius=15, fg_color="#1e1e1e")
    frame.pack(expand=True, padx=40, pady=40)

    def fazer_login():
        usuario = usuario_var.get()
        senha = senha_var.get()
        if verificar_login(usuario, senha):
            messagebox.showinfo("Login", "Login realizado com sucesso!")
            root.destroy()

            from app import App
            app = App()
            app.mainloop()
        else:
            messagebox.showerror("Erro", "Usuário ou senha incorretos.")

    usuario_var = tk.StringVar()
    senha_var = tk.StringVar()

    # Título
    ctk.CTkLabel(frame, text="Login no Sistema", font=("Century Gothic", 22, "bold")).pack(pady=(10, 20))

    # Campo usuário
    ctk.CTkLabel(frame, text="Usuário:", font=("Century Gothic", 14)).pack(anchor="w", padx=10)
    ctk.CTkEntry(frame, textvariable=usuario_var, width=260).pack(pady=(0, 15))

    # Campo senha
    ctk.CTkLabel(frame, text="Senha:", font=("Century Gothic", 14)).pack(anchor="w", padx=10)
    ctk.CTkEntry(frame, show="*", textvariable=senha_var, width=260).pack(pady=(0, 20))

    # Botão entrar
    ctk.CTkButton(frame, text="Entrar", command=fazer_login, width=150, font=("Century Gothic", 14, "bold")).pack()

    root.mainloop()

if __name__ == "__main__":
    login()
