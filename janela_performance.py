from tkinter import *
from tkinter import ttk
import mysql.connector
from tkinter import messagebox

mydb = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="",
    database="tf_prog_av"
)

def mostrar_informacoes_aluno(aluno):
    messagebox.showinfo("Informações do Aluno", f"ID do Usuário: {aluno[0]}\nNome: {aluno[1]}\nCurso: {aluno[2]}")

def gestao_performance(content_frame):
    def carregar_alunos():
        tree.delete(*tree.get_children())

        cursor = mydb.cursor()
        cursor.execute("SELECT * FROM q_utilizadores")
        alunos = cursor.fetchall()

        for aluno in alunos:
            tree.insert("", "end", values=aluno)  # Inserindo todas as colunas

    def selecionar_aluno():
        selected_item = tree.focus()
        if selected_item:
            aluno = tree.item(selected_item)["values"]
            mostrar_informacoes_aluno(aluno)

    for widget in content_frame.winfo_children():
        widget.destroy()

    tree = ttk.Treeview(content_frame, columns=("ID", "Nome", "Curso"))
    tree.heading("#0", text="ID")
    tree.column("#0", width=50)
    tree.heading("ID", text="ID")
    tree.column("ID", width=100)
    tree.heading("Nome", text="Nome")
    tree.column("Nome", width=150)
    tree.heading("Curso", text="Curso")
    tree.column("Curso", width=150)

    scrollbar = ttk.Scrollbar(content_frame, orient="vertical", command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.pack(side="right", fill="y")
    tree.pack(expand=True, fill="both")

    carregar_alunos()

    selecionar_button = Button(content_frame, text="Selecionar Aluno", command=selecionar_aluno)
    selecionar_button.pack(pady=10)
