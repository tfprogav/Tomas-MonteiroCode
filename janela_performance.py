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
    aluno_curso = aluno[2]
    aluno_curso_id = aluno[3]

    cursor = mydb.cursor()

    # Média das notas do aluno no curso
    cursor.execute("""
    SELECT AVG(q_avaliacoes.avaliacao_nota)
    FROM q_alunos_cursos
    JOIN q_avaliacoes ON q_alunos_cursos.curso_id = q_avaliacoes.avaliacao_curso
    WHERE q_alunos_cursos.aluno_id = %s AND q_alunos_cursos.curso_id = %s
    """, (aluno_id, aluno_curso_id))
    aluno_media = cursor.fetchone()[0]

    # Média das notas do curso
    cursor.execute("""
    SELECT AVG(q_avaliacoes.avaliacao_nota)
    FROM q_avaliacoes
    WHERE q_avaliacoes.avaliacao_curso = %s
    """, (aluno_curso_id,))
    curso_media = cursor.fetchone()[0]

    # Nota máxima do curso
    cursor.execute("""
    SELECT MAX(q_avaliacoes.avaliacao_nota)
    FROM q_avaliacoes
    WHERE q_avaliacoes.avaliacao_curso = %s
    """, (aluno_curso_id,))
    nota_maxima = cursor.fetchone()[0]

    # Nota mínima do curso
    cursor.execute("""
    SELECT MIN(q_avaliacoes.avaliacao_nota)
    FROM q_avaliacoes
    WHERE q_avaliacoes.avaliacao_curso = %s
    """, (aluno_curso_id,))
    nota_minima = cursor.fetchone()[0]

    messagebox.showinfo("Informações do Aluno", f"ID do Usuário: {aluno_id}\nNome: {aluno_nome}\nCurso: {aluno_curso}\nMédia das Notas do Aluno: {aluno_media:.2f}\nMédia das Notas do Curso: {curso_media:.2f}\nNota Máxima do Curso: {nota_maxima:.2f}\nNota Mínima do Curso: {nota_minima:.2f}")

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

    for widget in content_frame.winfo_children():
        widget.destroy()

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
