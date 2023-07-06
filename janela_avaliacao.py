from tkinter import *
from tkinter import ttk
import mysql.connector
from tkcalendar import DateEntry
from tkinter import messagebox

# Conectar ao banco de dados
mydb = mysql.connector.connect( #ligação á database
    host="localhost",
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
        # Insere cada avaliação na treeview
        for avaliacao in avaliacoes:
            avaliacao_list = list(avaliacao)
            avaliacao_list[4] = "Professor " + avaliacao_list[4]  # Adiciona o prefixo "Professor "
            tree.insert("", "end", values=avaliacao_list)


    def selecionar_avaliacao(event):
        # Obtem a avalição selecionada na treeview
        selected_item = tree.focus()
        # Verifica se alguma avaliação foi selecionada
        if selected_item:
            avaliacao = tree.item(selected_item)["values"]
            combo_alunos.delete(0, END)
            combo_alunos.insert(0, avaliacao[0])
            cal.delete(0, END)
            cal.insert(0, avaliacao[2])
            entry_nota.delete(0, END)
            entry_nota.insert(0, avaliacao[3])
            combo_professores.delete(0, END)
            combo_professores.insert(0, avaliacao[4].replace("Professor ", ""))# Remove o prefixo "Professor"

            # Define a opção selecionada na combobox de cursos
            if selected_course.get() == "Todos" or not selected_course.get():
                combo_curso.current(cursos.index(avaliacao[1]))
            else:
                combo_curso.current(cursos.index(selected_course.get()))
            # Faz update da combo_alunos para mostrar os alunos comforme o curso selecionado
            preencher_combobox_alunos(avaliacao[1])

    def selecionar_curso(event):
        selected_course.set(combo_curso.get())
        carregar_avaliacoes()
        preencher_combobox_alunos(selected_course.get())

    def preencher_combobox_professores():
        cursor = mydb.cursor()
        cursor.execute("SELECT utilizador_nome FROM q_utilizadores WHERE utilizador_perfil = 2")
        professores = [professor[0] for professor in cursor.fetchall()]
        combo_professores['values'] = professores


    def preencher_combobox_alunos(curso=None):
        cursor = mydb.cursor()

        # Verifica se um curso foi selecionado
        if curso is None or curso == "Todos":
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
            cursor.execute(query, (curso,))
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

            # Verifica se a nota é um número válido
            if nota.isnumeric() or (nota.count('.') == 1 and nota.replace('.', '').isnumeric()):
                nota = float(nota)
                if 0 <= nota <= 20:
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
                    messagebox.showinfo("Erro", "A nota deve ser um número de 0 a 20.")
            else:
                messagebox.showinfo("Erro", "A nota deve ser um valor numérico.")
        else:
            messagebox.showinfo("Erro", "Preencha todos os campos para inserir uma avaliação.")

    def editar_avaliacao():
        selected_item = tree.focus()
        if selected_item:
            avaliacao = tree.item(selected_item)["values"]
            id_avaliacao = avaliacao[5]

            # Verifica se todos os campos estão preenchidos
            if combo_alunos.get() and combo_curso.get() and entry_nota.get() and cal.get() and combo_professores.get():
                aluno = combo_alunos.get()
                curso = combo_curso.get()
                nota = entry_nota.get()
                data = cal.get()
                professor = combo_professores.get()

                # Verifica se a nota é um número válido
                if nota.isnumeric() or (nota.count('.') == 1 and nota.replace('.', '').isnumeric()):
                    nota = float(nota)
                    if 0 <= nota <= 20:
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
                    messagebox.showinfo("Erro", "A nota deve ser um número de 0 a 20.")
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

    def pesquisar_alunos(event):
        cursor = mydb.cursor()
        curso_selecionado = selected_course.get()
        # Verifica se nenhum curso foi selecionado ou se é "Todos"
        if curso_selecionado == "Todos" or not curso_selecionado:
            query = """
                SELECT utilizador_nome
                FROM q_utilizadores
                WHERE utilizador_perfil = 1
                    AND utilizador_nome LIKE %s;
            """
            cursor.execute(query, (combo_alunos.get() + '%',))
        else:
            query = """
                SELECT aluno.utilizador_nome
                FROM q_utilizadores AS aluno
                INNER JOIN q_alunos_cursos AS ac ON aluno.utilizador_id = ac.aluno_id
                INNER JOIN q_cursos AS c ON ac.curso_id = c.curso_id
                WHERE c.curso_desc = %s
                    AND aluno.utilizador_nome LIKE %s;
            """
            cursor.execute(query, (curso_selecionado, combo_alunos.get() + '%'))
            # Obtém os resultados da consulta SQL
        alunos = [aluno[0] for aluno in cursor.fetchall()]
        # Atualiza os valores do ComboBox com os nomes dos alunos encontrados
        combo_alunos['values'] = alunos

    def pesquisar_professores(event):
        cursor = mydb.cursor()
        query = """
            SELECT utilizador_nome
            FROM q_utilizadores
            WHERE utilizador_perfil = 2
                AND utilizador_nome LIKE %s;
        """
        cursor.execute(query, (combo_professores.get() + '%',))
        professores = [professor[0] for professor in cursor.fetchall()]
        # Atualiza os valores do ComboBox com os nomes dos Professores encontrados
        combo_professores['values'] = professores

    # Criação do frame para a gestão de avaliações
    frame_gestao_avaliacoes = Frame(content_frame, bg='white')
    frame_gestao_avaliacoes.pack()

    label = Label(frame_gestao_avaliacoes, text='Gestão de Avaliações', font=('Arial', 14), bg='white')
    label.pack(pady=5)

    label_nota = Label(content_frame, text="", bg='white')
    label_nota.pack(pady=1)

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

    # Configuração do "scroll" para a treeview
    scrollbar = ttk.Scrollbar(content_frame, orient="vertical", command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.pack(side="right", fill="y")
    tree.pack(expand=True, fill="both")

    tree.bind("<ButtonRelease-1>", selecionar_avaliacao)

    carregar_avaliacoes()

    label_nota = Label(content_frame, text="", bg='white')
    label_nota.pack(pady=1)
    label_nota = Label(content_frame, text="", bg='white')
    label_nota.pack(pady=1)

    combo_curso = ttk.Combobox(content_frame, values=cursos, textvariable=selected_course)
    combo_curso.current(0)
    combo_curso.bind("<<ComboboxSelected>>", selecionar_curso)
    combo_curso.pack(pady=5)

    # Combobox dos Alunos
    label_aluno = Label(content_frame, text="Aluno:")
    label_aluno.pack()
    combo_alunos = ttk.Combobox(content_frame)
    combo_alunos.pack(pady=5)
    preencher_combobox_alunos()
    combo_alunos.bind("<KeyRelease>", pesquisar_alunos)

    # DateEntry
    label_data = Label(content_frame, text="Data:")
    label_data.pack()
    cal = DateEntry(content_frame, width=12, background='grey', foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
    cal.pack()

    # Entry das Notas
    label_nota = Label(content_frame, text="Nota:")
    label_nota.pack()
    entry_nota = Entry(content_frame)
    entry_nota.pack(pady=5)

    # Combobox dos Professores
    label_professor = Label(content_frame, text="Professor:")
    label_professor.pack()
    combo_professores = ttk.Combobox(content_frame)
    combo_professores.pack(pady=5)
    preencher_combobox_professores()
    combo_professores.bind("<KeyRelease>", pesquisar_professores)

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
    limpar_campos()