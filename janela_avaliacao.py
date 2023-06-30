from tkinter import *
from tkinter import ttk
import mysql.connector

mydb = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="",
    database="tf_prog_av"
)

def gestao_avaliacoes(content_frame):
    def carregar_avaliacoes():
        tree.delete(*tree.get_children())

        cursor = mydb.cursor()
        cursor.execute("""SELECT u.utilizador_nome AS nome_aluno, c.curso_desc AS nome_curso, a.avaliacao_data, a.avaliacao_nota
FROM q_avaliacoes a
JOIN q_utilizadores u ON a.avaliacao_aluno_id = u.utilizador_id
JOIN q_cursos c ON a.avaliacao_curso = c.curso_id
""")
        avaliacoes = cursor.fetchall()

        for avaliacao in avaliacoes:
            tree.insert("", "end", values=avaliacao)

    def adicionar_avaliacao():
        aluno = entry_aluno.get()
        disciplina = entry_disciplina.get()
        nota = entry_nota.get()
        data = entry_data.get()

        cursor = mydb.cursor()
        query = "INSERT INTO q_avaliacoes (avaliacao_aluno_id, avaliacao_curso, avaliacao_nota, avaliacao_data) VALUES (%s, %s, %s, %s)"
        values = (aluno, disciplina, nota, data)
        cursor.execute(query, values)
        mydb.commit()

        carregar_avaliacoes()

    def editar_avaliacao():
        selected_item = tree.focus()
        if selected_item:
            avaliacao = tree.item(selected_item)["values"]
            data, aluno, disciplina, nota = avaliacao

            id_avaliacao = avaliacao[0]

            aluno = entry_aluno.get()
            disciplina = entry_disciplina.get()
            nota = entry_nota.get()
            data = entry_data.get()

            cursor = mydb.cursor()
            query = "UPDATE q_avaliacoes SET avaliacao_aluno_id = %s, avaliacao_curso = %s, avaliacao_nota = %s, avaliacao_data = %s WHERE avaliacao_id = %s"
            values = (aluno, disciplina, nota, data, id_avaliacao)
            cursor.execute(query, values)
            mydb.commit()

            carregar_avaliacoes()

    def excluir_avaliacao():
        selected_item = tree.focus()
        if selected_item:
            avaliacao = tree.item(selected_item)["values"]
            id_avaliacao = avaliacao[0]

            cursor = mydb.cursor()
            query = "DELETE FROM q_avaliacoes WHERE avaliacao_id = %s"
            value = (id_avaliacao,)
            cursor.execute(query, value)
            mydb.commit()

            carregar_avaliacoes()

    for widget in content_frame.winfo_children():
        widget.destroy()

    tree = ttk.Treeview(content_frame, columns=("Aluno", "Curso", "Data", "Nota"), show="headings")
    tree.heading("Aluno", text="Aluno")
    tree.column("Aluno", width=150)
    tree.heading("Curso", text="Curso")
    tree.column("Curso", width=150)
    tree.heading("Data", text="Data")
    tree.column("Data", width=100)
    tree.heading("Nota", text="Nota")
    tree.column("Nota", width=50)

    scrollbar = ttk.Scrollbar(content_frame, orient="vertical", command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.pack(side="right", fill="y")
    tree.pack(expand=True, fill="both")

    carregar_avaliacoes()

    label_data = Label(content_frame, text="Data:")
    label_data.pack()
    entry_data = Entry(content_frame)
    entry_data.pack()

    label_aluno = Label(content_frame, text="Aluno:")
    label_aluno.pack()
    entry_aluno = Entry(content_frame)
    entry_aluno.pack()

    label_disciplina = Label(content_frame, text="Curso:")
    label_disciplina.pack()
    entry_disciplina = Entry(content_frame)
    entry_disciplina.pack()

    label_nota = Label(content_frame, text="Nota:")
    label_nota.pack()
    entry_nota = Entry(content_frame)
    entry_nota.pack()

    adicionar_button = Button(content_frame, text="Adicionar", command=adicionar_avaliacao)
    adicionar_button.pack(pady=5)

    editar_button = Button(content_frame, text="Editar", command=editar_avaliacao)
    editar_button.pack(pady=5)

    excluir_button = Button(content_frame, text="Excluir", command=excluir_avaliacao)
    excluir_button.pack(pady=5)
