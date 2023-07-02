import mysql.connector

mydb = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="",
    database="tf_prog_av"
)

def obter_avaliacoes(curso):
    cursor = mydb.cursor()
    if curso == "Todos" or not curso:
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
                q_avaliacoes.avaliacao_curso = %s;
        """
        cursor.execute(query, (curso,))
    result = cursor.fetchall()
    return result

def obter_cursos():
    cursor = mydb.cursor()
    query = "SELECT curso_desc FROM q_cursos"
    cursor.execute(query)
    return cursor

def obter_alunos(curso):
    cursor = mydb.cursor()
    if curso == "Todos" or not curso:
        query = "SELECT utilizador_nome FROM q_utilizadores WHERE utilizador_tipo = 'Aluno'"
        cursor.execute(query)
    else:
        query = """
            SELECT 
                utilizador_nome 
            FROM 
                q_utilizadores 
            INNER JOIN 
                q_inscricoes ON q_utilizadores.utilizador_id = q_inscricoes.inscricao_aluno_id 
            WHERE 
                inscricao_curso_id = (SELECT curso_id FROM q_cursos WHERE curso_desc = %s);
        """
        cursor.execute(query, (curso,))
    result = cursor.fetchall()
    alunos = [aluno[0] for aluno in result]
    return alunos

def obter_professores():
    cursor = mydb.cursor()
    query = "SELECT utilizador_nome FROM q_utilizadores WHERE utilizador_tipo = 'Professor'"
    cursor.execute(query)
    result = cursor.fetchall()
    professores = [professor[0] for professor in result]
    return professores

def inserir_avaliacao(aluno, curso, nota, data, professor):
    cursor = mydb.cursor()
    query = """
        INSERT INTO q_avaliacoes 
            (avaliacao_aluno_id, avaliacao_curso, avaliacao_data, avaliacao_nota, avaliacao_prof_id) 
        VALUES 
            ((SELECT utilizador_id FROM q_utilizadores WHERE utilizador_nome = %s), 
            (SELECT curso_id FROM q_cursos WHERE curso_desc = %s), %s, %s, 
            (SELECT utilizador_id FROM q_utilizadores WHERE utilizador_nome = %s));
    """
    values = (aluno, curso, data, nota, professor)
    cursor.execute(query, values)
    mydb.commit()

def atualizar_avaliacao(id_avaliacao, aluno, curso, nota, data, professor):
    cursor = mydb.cursor()
    query = """
        UPDATE q_avaliacoes 
        SET 
            avaliacao_aluno_id = (SELECT utilizador_id FROM q_utilizadores WHERE utilizador_nome = %s),
            avaliacao_curso = (SELECT curso_id FROM q_cursos WHERE curso_desc = %s),
            avaliacao_data = %s,
            avaliacao_nota = %s,
            avaliacao_prof_id = (SELECT utilizador_id FROM q_utilizadores WHERE utilizador_nome = %s)
        WHERE 
            avaliacao_id = %s;
    """
    values = (aluno, curso, data, nota, professor, id_avaliacao)
    cursor.execute(query, values)
    mydb.commit()

def excluir_avaliacao(id_avaliacao):
    cursor = mydb.cursor()
    query = "DELETE FROM q_avaliacoes WHERE avaliacao_id = %s"
    cursor.execute(query, (id_avaliacao,))
    mydb.commit()