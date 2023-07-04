from tkinter import *
from tkinter import ttk
import mysql.connector
from tkcalendar import DateEntry
from tkinter import messagebox

# Conectar ao banco de dados
mydb = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="",
    database="tf_prog_av"
)

def gestao_avaliacoes(content_frame):
    selected_course = StringVar()

    # Limpa o conteúdo do frame
    for widget in content_frame.winfo_children():
        widget.destroy()

    def carregar_avaliacoes():
        # Limpa as avaliações existentes na treeview
        tree.delete(*tree.get_children())
        cursor = mydb.cursor()
        # Verifica se um curso foi selecionado
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
            # Consulta SQL para selecionar avaliações de um curso específico
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
        # Obtem todas as avaliações retornadas pela consulta
        avaliacoes = cursor.fetchall()
        # Insere cada avaliação na treeview
        for avaliacao in avaliacoes:
            tree.insert("", "end", values=avaliacao)

    def selecionar_avaliacao(event):
        # Obtem o item selecionado na treeview
        selected_item = tree.focus()
        # Verifica se algum item foi selecionado
        if selected_item:
            avaliacao = tree.item(selected_item)["values"]
            combo_alunos.delete(0, END)
            combo_alunos.insert(0, avaliacao[0])
            cal.delete(0, END)
            cal.insert(0, avaliacao[2])
            entry_nota.delete(0, END)
            entry_nota.insert(0, avaliacao[3])
            combo_professores.delete(0, END)
            combo_professores.insert(0, avaliacao[4])

            # Define a opção selecionada na combobox de cursos
            if selected_course.get() == "Todos" or not selected_course.get():
                combo_curso.current(cursos.index(avaliacao[1]))
            else:
                combo_curso.current(cursos.index(selected_course.get()))

    def selecionar_curso(event):
        carregar_avaliacoes()
        preencher_combobox_alunos()

    def preencher_combobox_professores():
        cursor = mydb.cursor()
        cursor.execute("SELECT utilizador_nome FROM q_utilizadores WHERE utilizador_perfil = 2")
        professores = [professor[0] for professor in cursor.fetchall()]
        combo_professores['values'] = professores

    def preencher_combobox_alunos():
        cursor = mydb.cursor()

        # Verifica se um curso foi selecionado
        if selected_course.get() == "Todos" or not selected_course.get():
            cursor.execute("SELECT utilizador_nome FROM q_utilizadores WHERE utilizador_perfil = 1")
        else:
            # Consulta SQL para selecionar os alunos do curso selecionado
            query = """
                SELECT 
                    aluno.utilizador_nome
                FROM 
                    q_utilizadores AS aluno
                INNER JOIN 
                    q_alunos_cursos AS ac ON aluno.utilizador_id = ac.aluno_id
                INNER JOIN 
                    q_cursos AS c ON ac.curso_id = c.curso_id
                WHERE 
                    c.curso_desc = %s;
            """
            cursor.execute(query, (selected_course.get(),))
        alunos = [aluno[0] for aluno in cursor.fetchall()]
        combo_alunos['values'] = alunos

    def limpar_campos():
        combo_alunos.delete(0, END)
        cal.delete(0, END)
        entry_nota.delete(0, END)
        combo_professores.delete(0, END)

    def adicionar_avaliacao():
        # Verifica se todos os campos estão preenchidos
        if combo_alunos.get() and combo_curso.get() and entry_nota.get() and cal.get() and combo_professores.get():
            aluno = combo_alunos.get()
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
        else:
            messagebox.showinfo("Erro", "Preencha todos os campos para inserir uma avaliação.")

    def editar_avaliacao():
        selected_item = tree.focus()
        if selected_item:
            avaliacao = tree.item(selected_item)["values"]
            id_avaliacao = avaliacao[5]
            if combo_alunos.get() and combo_curso.get() and entry_nota.get() and cal.get() and combo_professores.get():
                aluno = combo_alunos.get()
                curso = combo_curso.get()
                nota = entry_nota.get()
                data = cal.get()
                professor = combo_professores.get()

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
                               SELECT prof.utilizador_id
                               FROM q_utilizadores prof
                               WHERE prof.utilizador_nome = %s
                           )
                       WHERE avaliacao_id = %s
               """
                values = (aluno, curso, nota, data, professor, id_avaliacao)
                cursor.execute(query, values)
                mydb.commit()

                carregar_avaliacoes()
                limpar_campos()
            else:
                messagebox.showinfo("Erro", "Preencha todos os campos para editar uma avaliação.")
        else:
            messagebox.showinfo("Erro", "Selecione uma avaliação para editar.")

    def excluir_avaliacao():
        selected_item = tree.focus()
        if selected_item:
            result = messagebox.askyesno("Excluir", "Tem certeza que deseja excluir a avaliação selecionada?")
            if result:
                avaliacao = tree.item(selected_item)["values"]
                id_avaliacao = avaliacao[5]

                cursor = mydb.cursor()
                query = "DELETE FROM q_avaliacoes WHERE avaliacao_id = %s"
                values = (id_avaliacao,)
                cursor.execute(query, values)
                mydb.commit()

                carregar_avaliacoes()
                limpar_campos()
        else:
            messagebox.showinfo("Erro", "Selecione uma avaliação para excluir.")

    # Criação do frame para a gestão de avaliações
    frame_gestao_avaliacoes = Frame(content_frame)
    frame_gestao_avaliacoes.pack()

    label = Label(frame_gestao_avaliacoes, text='Gestão de Avaliações', font=('Arial', 14))
    label.pack(pady=5)

    # Criação da árvore (treeview) para exibir as avaliações
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

    # Configuração do scroll para a treeview
    scrollbar = ttk.Scrollbar(content_frame, orient="vertical", command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.pack(side="right", fill="y")
    tree.pack(expand=True, fill="both")

    tree.bind("<ButtonRelease-1>", selecionar_avaliacao)

    carregar_avaliacoes()

    label_nota = Label(content_frame, text="")
    label_nota.pack(pady=1)
    label_nota = Label(content_frame, text="")
    label_nota.pack(pady=1)

    combo_curso = ttk.Combobox(content_frame, values=cursos, textvariable=selected_course)
    combo_curso.current(0)
    combo_curso.bind("<<ComboboxSelected>>", selecionar_curso)
    combo_curso.pack(pady=5)


    label_aluno = Label(content_frame, text="Aluno:")
    label_aluno.pack()
    combo_alunos = ttk.Combobox(content_frame)
    combo_alunos.pack(pady=5)
    preencher_combobox_alunos()

    label_data = Label(content_frame, text="Data:")
    label_data.pack()
    cal = DateEntry(content_frame, width=12, background='grey', foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
    cal.pack()

    label_nota = Label(content_frame, text="Nota:")
    label_nota.pack()
    entry_nota = Entry(content_frame)
    entry_nota.pack(pady=5)

    label_professor = Label(content_frame, text="Professor:")
    label_professor.pack()
    combo_professores = ttk.Combobox(content_frame)
    combo_professores.pack(pady=5)
    preencher_combobox_professores()

    frame_botoes = Frame(content_frame, bg='white')
    frame_botoes.pack(pady=5)
    frame_gestao_avaliacoes = Frame(content_frame)
    frame_gestao_avaliacoes.pack(anchor='center')

    btn_inserir = Button(frame_botoes, text="Inserir", command=adicionar_avaliacao)
    btn_inserir.pack(side='left', padx=5)

    btn_atualizar = Button(frame_botoes, text="Editar", command=editar_avaliacao)
    btn_atualizar.pack(side='left', padx=5)

    btn_apagar = Button(frame_botoes, text="Apagar", command=excluir_avaliacao)
    btn_apagar.pack(side='left', padx=5)

    btn_limpar = Button(frame_botoes, text="Limpar Campos", command=limpar_campos)
    btn_limpar.pack(side='left', padx=5)

    frame_gestao_avaliacoes.pack(fill='y', pady=50)