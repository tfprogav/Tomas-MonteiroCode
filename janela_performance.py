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
    aluno_id = aluno[0]
    aluno_nome = aluno[1]
    curso_nome = aluno[2]
    aluno_curso_id = aluno[3]

    cursor = mydb.cursor()

    # Consulta para obter a média do aluno no curso
    cursor.execute(f"""
        SELECT AVG(avaliacao_nota) AS media_aluno_curso
        FROM q_avaliacoes
        WHERE avaliacao_aluno_id = {aluno_id} AND avaliacao_curso = {aluno_curso_id}
    """)
    media_aluno_curso = round(cursor.fetchone()[0], 2)

    # Consulta para obter a média do curso
    cursor.execute(f"""
        SELECT AVG(avaliacao_nota) AS media_curso
        FROM q_avaliacoes
        WHERE avaliacao_curso = {aluno_curso_id}
    """)
    media_curso = round(cursor.fetchone()[0], 2)

    # Consulta para obter a nota máxima do curso
    cursor.execute(f"""
        SELECT MAX(avaliacao_nota) AS nota_maxima
        FROM q_avaliacoes
        WHERE avaliacao_curso = {aluno_curso_id}
    """)
    nota_maxima = cursor.fetchone()[0]

    # Consulta para obter a nota mínima do curso
    cursor.execute(f"""
        SELECT MIN(avaliacao_nota) AS nota_minima
        FROM q_avaliacoes
        WHERE avaliacao_curso = {aluno_curso_id}
    """)
    nota_minima = cursor.fetchone()[0]

    messagebox.showinfo(
        "Informações do Aluno",
        f"ID do Usuário: {aluno_id}\n"
        f"Nome: {aluno_nome}\n"
        f"Curso: {curso_nome}\n"
        f"Média do Aluno no Curso: {media_aluno_curso}\n"
        f"Média do Curso: {media_curso}\n"
        f"Nota Máxima: {nota_maxima}\n"
        f"Nota Mínima: {nota_minima}"
    )


def gestao_performance(content_frame):
    def carregar_alunos():
        tree.delete(*tree.get_children())

        cursor = mydb.cursor()
        cursor.execute("""SELECT u.utilizador_id AS aluno_id, u.utilizador_nome AS aluno, c.curso_desc AS curso, c.curso_id, COUNT(*) AS num_avaliacoes
FROM q_avaliacoes a
JOIN q_utilizadores u ON a.avaliacao_aluno_id = u.utilizador_id
JOIN q_cursos c ON a.avaliacao_curso = c.curso_id
GROUP BY u.utilizador_id, u.utilizador_nome, c.curso_desc, c.curso_id
HAVING COUNT(*) >= 2
ORDER BY u.utilizador_nome;
""")
        alunos = cursor.fetchall()

        for aluno in alunos:
            tree.insert("", "end", values=aluno)  # Inserindo todas as colunas

    def selecionar_aluno():
        selected_item = tree.focus()
        if selected_item:
            aluno = tree.item(selected_item)["values"]
            mostrar_informacoes_aluno(aluno)
        else:
            messagebox.showwarning("Nenhum item selecionado", "Selecione um campo para visualizar a performance.")

    for widget in content_frame.winfo_children():
        widget.destroy()

    frame_ver_performance = Frame(content_frame)
    frame_ver_performance.pack()

    label = Label(frame_ver_performance, text='Visualização de Performance', font=('Arial', 14))
    label.pack(pady=5)

    tree = ttk.Treeview(content_frame, columns=("ID", "Nome", "Curso"), show="headings")
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
