import mysql.connector

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