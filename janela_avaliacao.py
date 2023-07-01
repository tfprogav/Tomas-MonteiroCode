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
    selected_course = StringVar()

    for widget in content_frame.winfo_children():
        widget.destroy()

    def carregar_avaliacoes():
        tree.delete(*tree.get_children())
        cursor = mydb.cursor()
        if selected_course.get() == "Todos" or not selected_course.get():
            query = """
                SELECT 
                    aluno.utilizador_nome AS aluno_info,
                    q_cursos.curso_desc AS nome_curso,
                    q_avaliacoes.avaliacao_data,
                    q_avaliacoes.avaliacao_nota,  
                    q_avaliacoes.avaliacao_id,
                    q_avaliacoes.avaliacao_curso,
                    aluno.utilizador_id AS aluno_id,
                    professor.utilizador_id AS professor_id,
                    professor.utilizador_nome AS professor_info 
                FROM 
                    q_avaliacoes 
                INNER JOIN 
                    q_utilizadores AS aluno ON q_avaliacoes.avaliacao_aluno_id = aluno.utilizador_id 
                INNER JOIN 
                    q_utilizadores AS professor ON q_avaliacoes.avaliacao_prof_id = professor.utilizador_id
                INNER JOIN
                    q_cursos ON q_avaliacoes.avaliacao_curso = q_cursos.curso_id;
            """
            cursor.execute(query)
        else:
            query = """
                SELECT 
                    aluno.utilizador_nome AS aluno_info,
                    q_cursos.curso_desc AS nome_curso,
                    q_avaliacoes.avaliacao_data,
                    q_avaliacoes.avaliacao_nota,
                    q_avaliacoes.avaliacao_id,
                    q_avaliacoes.avaliacao_curso,
                    aluno.utilizador_id AS aluno_id,
                    professor.utilizador_id AS professor_id,
                    professor.utilizador_nome AS professor_info 
                FROM 
                    q_avaliacoes 
                INNER JOIN 
                    q_utilizadores AS aluno ON q_avaliacoes.avaliacao_aluno_id = aluno.utilizador_id 
                INNER JOIN 
                    q_utilizadores AS professor ON q_avaliacoes.avaliacao_prof_id = professor.utilizador_id
                INNER JOIN
                    q_cursos ON q_avaliacoes.avaliacao_curso = q_cursos.curso_id
                WHERE 
                    q_cursos.curso_desc = %s;
            """
            cursor.execute(query, (selected_course.get(),))
        avaliacoes = cursor.fetchall()
        for avaliacao in avaliacoes:
            tree.insert("", "end", values=avaliacao[0:4] + (avaliacao[8],))

    def selecionar_avaliacao(event):
        selected_item = tree.focus()
        if selected_item:
            avaliacao = tree.item(selected_item)["values"]
            entry_aluno.delete(0, END)
            entry_aluno.insert(0, avaliacao[0])
            entry_disciplina.delete(0, END)
            entry_disciplina.insert(0, avaliacao[1])
            entry_data.delete(0, END)
            entry_data.insert(0, avaliacao[2])
            entry_nota.delete(0, END)
            entry_nota.insert(0, avaliacao[3])
            combo_professores.delete(0, END)
            combo_professores.insert(0, avaliacao[4])

    def selecionar_curso(event):
        carregar_avaliacoes()

    tree = ttk.Treeview(content_frame, columns=("Aluno", "Curso", "Data", "Nota", "Professor"), show="headings")
    tree.heading("Aluno", text="Aluno")
    tree.column("Aluno", width=150)
    tree.heading("Curso", text="Curso")
    tree.column("Curso", width=150)
    tree.heading("Data", text="Data")
    tree.column("Data", width=100)
    tree.heading("Nota", text="Nota")
    tree.column("Nota", width=50)
    tree.heading("Professor", text="Professor")
    tree.column("Professor", width=150)

    scrollbar = ttk.Scrollbar(content_frame, orient="vertical", command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.pack(side="right", fill="y")
    tree.pack(expand=True, fill="both")

    tree.bind("<ButtonRelease-1>", selecionar_avaliacao)

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

    def adicionar_avaliacao():
        aluno = entry_aluno.get()
        disciplina = entry_disciplina.get()
        nota = entry_nota.get()
        data = entry_data.get()

        cursor = mydb.cursor()
        query = """
            INSERT INTO q_avaliacoes (avaliacao_aluno_id, avaliacao_curso, avaliacao_nota, avaliacao_data)
            SELECT %s, c.curso_id, %s, %s
            FROM q_cursos c
            WHERE c.curso_desc = %s
        """
        values = (aluno, nota, data, disciplina)
        cursor.execute(query, values)
        mydb.commit()

        carregar_avaliacoes()

    adicionar_button = Button(content_frame, text="Adicionar", command=adicionar_avaliacao)
    adicionar_button.pack(pady=5)

    def editar_avaliacao():
        selected_item = tree.focus()
        if selected_item:
            avaliacao = tree.item(selected_item)["values"]
            id_avaliacao = avaliacao[4]

            aluno = entry_aluno.get()
            disciplina = entry_disciplina.get()
            nota = entry_nota.get()
            data = entry_data.get()

            cursor = mydb.cursor()
            query = "UPDATE q_avaliacoes SET avaliacao_aluno_id = %s, avaliacao_curso = (SELECT curso_id FROM q_cursos WHERE curso_desc = %s), avaliacao_nota = %s, avaliacao_data = %s WHERE avaliacao_id = %s"
            values = (aluno, disciplina, nota, data, id_avaliacao)
            cursor.execute(query, values)
            mydb.commit()

            carregar_avaliacoes()

    editar_button = Button(content_frame, text="Editar", command=editar_avaliacao)
    editar_button.pack(pady=5)

    def excluir_avaliacao():
        selected_item = tree.focus()
        if selected_item:
            avaliacao = tree.item(selected_item)["values"]
            id_avaliacao = avaliacao[4]

            cursor = mydb.cursor()
            query = "DELETE FROM q_avaliacoes WHERE avaliacao_id = %s"
            value = (id_avaliacao,)
            cursor.execute(query, value)
            mydb.commit()

            carregar_avaliacoes()

    def preencher_combobox_professores():
        cursor = mydb.cursor()
        cursor.execute("SELECT utilizador_nome FROM q_utilizadores WHERE utilizador_perfil = 2")
        professores = [professor[0] for professor in cursor.fetchall()]
        combo_professores['values'] = professores

    excluir_button = Button(content_frame, text="Excluir", command=excluir_avaliacao)
    excluir_button.pack(pady=5)

    cursor = mydb.cursor()
    cursor.execute("SELECT curso_desc FROM q_cursos")
    cursos = [curso[0] for curso in cursor.fetchall()]
    cursos.insert(0, "Todos")

    combo_curso = ttk.Combobox(content_frame, values=cursos, textvariable=selected_course)
    combo_curso.current(0)
    combo_curso.bind("<<ComboboxSelected>>", selecionar_curso)
    combo_curso.pack(pady=5)

    combo_professores = ttk.Combobox(content_frame)
    combo_professores.pack(pady=5)
    preencher_combobox_professores()
