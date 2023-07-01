from tkinter import *
from tkinter import ttk
import mysql.connector
from tkcalendar import DateEntry

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
                    professor.utilizador_nome AS professor_info,
                    q_avaliacoes.avaliacao_id,
                    q_avaliacoes.avaliacao_curso,
                    aluno.utilizador_id AS aluno_id,
                    professor.utilizador_id AS professor_id
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
                    professor.utilizador_nome AS professor_info,
                    q_avaliacoes.avaliacao_id,
                    q_avaliacoes.avaliacao_curso,
                    aluno.utilizador_id AS aluno_id,
                    professor.utilizador_id AS professor_id
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
            tree.insert("", "end", values=avaliacao)

    def selecionar_avaliacao(event):
        selected_item = tree.focus()
        if selected_item:
            avaliacao = tree.item(selected_item)["values"]
            entry_aluno.delete(0, END)
            entry_aluno.insert(0, avaliacao[0])
            cal.delete(0, END)
            cal.insert(0, avaliacao[2])
            entry_nota.delete(0, END)
            entry_nota.insert(0, avaliacao[3])
            combo_professores.delete(0, END)
            combo_professores.insert(0, avaliacao[4])
            print(avaliacao[0])
            print(avaliacao[1])
            print(avaliacao[2])
            print(avaliacao[3])
            print(avaliacao[4])
            print(avaliacao[5])
            print(avaliacao[6])
            print(avaliacao[7])
            print(avaliacao[8])

    def selecionar_curso(event):
        carregar_avaliacoes()

    def preencher_combobox_professores():
        cursor = mydb.cursor()
        cursor.execute("SELECT utilizador_nome FROM q_utilizadores WHERE utilizador_perfil = 2")
        professores = [professor[0] for professor in cursor.fetchall()]
        combo_professores['values'] = professores

    def limpar_campos():
        entry_aluno.delete(0, END)
        cal.delete(0, END)
        entry_nota.delete(0, END)
        combo_professores.delete(0, END)

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

    cursor = mydb.cursor()
    cursor.execute("SELECT curso_desc FROM q_cursos")
    cursos = [curso[0] for curso in cursor.fetchall()]
    cursos.insert(0, "Todos")

    scrollbar = ttk.Scrollbar(content_frame, orient="vertical", command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.pack(side="right", fill="y")
    tree.pack(expand=True, fill="both")

    tree.bind("<ButtonRelease-1>", selecionar_avaliacao)

    carregar_avaliacoes()

    combo_curso = ttk.Combobox(content_frame, values=cursos, textvariable=selected_course)
    combo_curso.current(0)
    combo_curso.bind("<<ComboboxSelected>>", selecionar_curso)
    combo_curso.pack(pady=5)


    label_aluno = Label(content_frame, text="Aluno:")
    label_aluno.pack()
    entry_aluno = Entry(content_frame)
    entry_aluno.pack()

    label_data = Label(content_frame, text="Data:")
    label_data.pack()
    cal = DateEntry(content_frame, width=12, background='darkblue', foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
    cal.pack()

    label_nota = Label(content_frame, text="Nota:")
    label_nota.pack()
    entry_nota = Entry(content_frame)
    entry_nota.pack()

    label_professor = Label(content_frame, text="Professor:")
    label_professor.pack()
    combo_professores = ttk.Combobox(content_frame)
    combo_professores.pack(pady=5)
    preencher_combobox_professores()

    def adicionar_avaliacao():
        aluno = entry_aluno.get()
        curso = combo_curso.get()
        nota = entry_nota.get()
        data = cal.get()
        professor = combo_professores.get()

        cursor = mydb.cursor()
        query = """
            INSERT INTO q_avaliacoes (avaliacao_aluno_id, avaliacao_prof_id, avaliacao_curso, avaliacao_data, avaliacao_nota)
            SELECT 
                (SELECT utilizador_id FROM q_utilizadores WHERE utilizador_nome = %s),
                (SELECT utilizador_id FROM q_utilizadores WHERE utilizador_nome = %s),
                (SELECT curso_id FROM q_cursos WHERE curso_desc = %s),
                %s, %s
        """
        values = (aluno, professor, curso, data, nota)
        cursor.execute(query, values)
        mydb.commit()

        carregar_avaliacoes()
        limpar_campos()

    def editar_avaliacao():
        selected_item = tree.focus()
        if selected_item:
            avaliacao = tree.item(selected_item)["values"]
            id_avaliacao = avaliacao[5]

            aluno = entry_aluno.get()
            curso = combo_curso.get()
            nota = entry_nota.get()
            data = cal.get()
            professor = combo_professores.get()
            print(aluno)
            print(curso)
            print(nota)
            print(data)
            print(professor)

            cursor = mydb.cursor()
            query = """
                UPDATE q_avaliacoes SET 
                    avaliacao_aluno_id = (
                        SELECT aluno.utilizador_id
                        FROM q_utilizadores aluno
                        WHERE aluno.utilizador_nome = %s
                    ),
                    avaliacao_curso = (
                        SELECT c.curso_id
                        FROM q_cursos c
                        WHERE c.curso_desc = %s
                    ),
                    avaliacao_nota = %s,
                    avaliacao_data = %s,
                    avaliacao_prof_id = (
                        SELECT professor.utilizador_id
                        FROM q_utilizadores professor
                        WHERE professor.utilizador_nome = %s
                    )
                WHERE avaliacao_id = %s
            """
            values = (aluno, curso, nota, data, professor, id_avaliacao)
            cursor.execute(query, values)
            mydb.commit()

            carregar_avaliacoes()
            limpar_campos()

    excluir_button = Button(content_frame, text="Criar", command=adicionar_avaliacao)
    excluir_button.pack(pady=5)

    editar_button = Button(content_frame, text="Editar", command=editar_avaliacao)
    editar_button.pack(pady=5)

    def excluir_avaliacao():
        selected_item = tree.focus()
        if selected_item:
            avaliacao = tree.item(selected_item)["values"]
            id_avaliacao = avaliacao[5]

            cursor = mydb.cursor()
            query = "DELETE FROM q_avaliacoes WHERE avaliacao_id = %s"
            value = (id_avaliacao,)
            cursor.execute(query, value)
            mydb.commit()

            carregar_avaliacoes()


    excluir_button = Button(content_frame, text="Excluir", command=excluir_avaliacao)
    excluir_button.pack(pady=5)

    limpar_button = Button(content_frame, text="Limpar Campos", command=limpar_campos)
    limpar_button.pack(pady=5)
