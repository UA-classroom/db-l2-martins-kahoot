import psycopg2
from psycopg2 import errors, sql
from psycopg2.extras import RealDictCursor

"""
This file is responsible for making database queries, which the fastapi endpoints can use.
The reason we split them up is to avoid clutter in the endpoints, so that the endpoints might focus on other tasks 
"""


# --- Listing get-operations (fetching several entries) --- 

def get_users(con, limit: int):
    """Returns list of users from the database, based on the limit-parameter"""
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT * FROM users LIMIT %s", (limit,))
            users = cursor.fetchall()
    return users

def get_quizzes(con, limit: int):
    """Returns list of quizzes from the database, based on the limit-parameter"""
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT * FROM quizzes LIMIT %s", (limit,))
            quizzes = cursor.fetchall()
    return quizzes

def get_sessions(con, limit: int):
    
    """Returns list of sessions from the database, based on the limit-parameter"""
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT * FROM sessions LIMIT %s", (limit,))
            sessions = cursor.fetchall()
    return sessions

def get_all_session_players(con, limit: int):
    """Returns list of all session players from the database, based on the limit-parameter"""
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT * FROM session_players LIMIT %s", (limit,))
            session_players = cursor.fetchall()
    return session_players

def get_players_for_session(con, session_id, limit: int):
    """Returns list of players in a specific session, based on the limit-parameter"""
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT * FROM session_players WHERE session_id = %s LIMIT = %s", (session_id, limit),)
            session_players = cursor.fetchall()
    return session_players

def get_questions(con, limit: int):
    """Returns list of questions from the database, based on the limit-parameter"""
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT * FROM questions LIMIT %s;", (limit,))
            questions = cursor.fetchall()
    return questions

def get_quiz_questions(con, quiz_id, limit: int):
    """Returns list of questions for a specific quiz, based on the limit-parameter"""
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT * FROM questions WHERE quiz_id = %s LIMIT", (quiz_id, limit),)
            quiz_questions = cursor.fetchall()
    return quiz_questions

def get_question_answer_alternatives(con, question_id, limit: int):
    """Returns list of answer alternatives for a specific question, based on the limit-parameter"""
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT * FROM answer_alternatives WHERE question_id = %s LIMIT %s", (question_id, limit),)
            answer_alternatives = cursor.fetchall()
            return answer_alternatives
        
def get_all_player_answers(con, limit: int):
    """Returns list of player answers from the database, based on the limit-parameter"""
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT * FROM player_answers LIMIT %s", (limit,))
            all_player_answers = cursor.fetchall()
    return all_player_answers

def get_answers_by_player(con, session_player_id, limit: int):
    """Returns list of answes by a specific player from the database, based on the limit-parameter"""
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT * FROM player_answer WHERE question_id id = %s LIMIT %s", (session_player_id, limit),)
            player_answers = cursor.fetchall()
            return player_answers
        
def get_session_scoreboards(con, limit: int):
    """Returns list of session scoreboards from the database, based on the limit-parameter"""
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT * FROM session_scoreboards LIMIT %s", (limit,))
            scoreboards = cursor.fetchall()
    return scoreboards

# --- Detail get-operations (fetching one entry) ---

def get_user(con, user_id):
    """Returns the user with the given id from the database"""
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))             
            user = cursor.fetchone()
            return user
        
def get_quiz(con, quiz_id):
    """Returns the quiz with the given id from the database"""
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT * FROM quizzes WHERE id = %s", (quiz_id,))             
            quiz = cursor.fetchone()
            return quiz
        
def get_session(con, session_id):
    """Returns the session with the given id from the database"""
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT * FROM sessions WHERE id = %s", (session_id,))
            session = cursor.fetchone()
    return session

def get_session_player(con, session_player_id):
    """Returns the session player with the given id from the database"""
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT * FROM session_players WHERE id = %s", (session_player_id,))             
            session_player = cursor.fetchone()
            return session_player

def get_question(con, question_id):
    """Returns the question with the given id from the database"""
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT * FROM questions WHERE id = %s", (question_id,))             
            question = cursor.fetchone()
            return question
        
def get_answer_alternative(con, answer_alternative_id):
    """Returns the answer alternative with the given id from the database"""
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT * FROM answer_alternatives WHERE id = %s", (answer_alternative_id,))             
            answer_alternative = cursor.fetchone()
            return answer_alternative


def get_player_answer_for_question(con, player_id, question_id):
    """Returns the answer by a specfic player on a specific question"""
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """SELECT * FROM player_answers 
                    WHERE player_id = %s AND question_id = %s""",
                    (player_id, question_id),)
            player_answer = cursor.fetchone()
            return player_answer

def get_scoreboard_for_session(con, session_id):
    """Returns the scoreboard for a specific session"""
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT * FROM session_scoreboard WHERE session_id = %s", (session_id,))
            scoreboard = cursor.fetchone()
            return scoreboard
        
# -------------------------------------------------------------------------------------------------------
def get_item(con, table, item_id): # dålig säkerhet, måste fixas eller skitas i
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(f"""SELECT * FROM {table} WHERE id = %s""", (item_id,))             
            item = cursor.fetchone()
            return item

# --- POST/ADD OPERATIONS ---

def add_user(con, user_name, email, password, registration_date, user_status, birth_date):
    """Adds a new user to the database and returns its ID"""
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """INSERT INTO users (user_name, email, password, registration_date, user_status, birth_date)
                VALUES (%s, %s, %s, %s, %s, %s) RETURNING id;""",
                (user_name, email, password, registration_date, user_status, birth_date),
            )
            user_id = cursor.fetchone()["id"]
            con.commit()
    return user_id

def add_quiz(con, quiz_creator_id, quiz_title, quiz_description, intro_image, created_at, updated_at, is_public):
    """Adds a new quiz to the database and returns its ID"""
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """INSERT INTO quizzes (quiz_creator_id, quiz_title, quiz_description, intro_image, created_at, updated_at, is_public)
                VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING id;""",
                (quiz_creator_id, quiz_title, quiz_description, intro_image, created_at, updated_at, is_public),
            )
            quiz_id = cursor.fetchone()["id"]
            con.commit()
    return quiz_id

def add_question(con, quiz_id, question_text, question_order, time_limit, points, question_type, image):
    """Adds a new question to the database and returns its ID"""
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """INSERT INTO questions (quiz_id, question_text, question_order, time_limit, points, question_type, image)
                VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING id;""",
                (quiz_id, question_text, question_order, time_limit, points, question_type, image),
            )
            question_id = cursor.fetchone()["id"]
            con.commit()
    return question_id

def add_answer_alternative(con, question_id, answer_text, is_correct, answer_icon, answer_order):
    """Adds a new answer alternative to the database and returns its ID"""
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """INSERT INTO answer_alternatives (question_id, answer_text, is_correct, answer_icon, answer_order)
                VALUES (%s, %s, %s, %s, %s) RETURNING id;""",
                (question_id, answer_text, is_correct, answer_icon, answer_order),
            )
            answer_alternative_id = cursor.fetchone()["id"]
            con.commit()
    return answer_alternative_id

def add_player_answer(con, player_id, session_id, question_id, answer_id, response_time, points_earned, is_correct):
    """Adds a new player answer to the database and returns its ID"""
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """INSERT INTO player_answers (player_id, session_id, question_id, answer_id, response_time, points_earned, is_correct)
                VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING id;""",
                (player_id, session_id, question_id, answer_id, response_time, points_earned, is_correct),
            )
            player_answer = cursor.fetchone()["id"]
            con.commit()
            return player_answer

def add_session(con, session_name, host_user_id, active_quiz, qr_code_id, session_status, started_at, current_question_id, session_code):
    """Adds a new session to the database and returns its ID"""
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """INSERT INTO sessions (session_name, host_user_id, active_quiz, qr_code_id, session_status, started_at, current_question_id, session_code)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING id;""",
                (session_name, host_user_id, active_quiz, qr_code_id, session_status, started_at, current_question_id, session_code),
            )
            session_id = cursor.fetchone()["id"]
            con.commit()
            return session_id
        
def add_session_player(con, session_id, display_name, user_id, joined_at, player_points):
    """Adds a new session player to the database and returns its ID"""
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """INSERT INTO session_players (session_id, display_name, user_id, joined_at, player_points)
                VALUES (%s, %s, %s, %s, %s) RETURNING id;""",
                (session_id, display_name, user_id, joined_at, player_points),
            )
            player_id = cursor.fetchone()["id"]
            con.commit()
            return player_id

def add_session_scoreboard(con, session_id, player_id, total_score, correct_answers, rank):
    """Adds a new scoreboard to the database and returns its ID"""
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """INSERT INTO session_scoreboards (session_id, player_id, total_score, correct_answers, rank)
                VALUES (%s, %s, %s, %s, %s) RETURNING id;""",
                (session_id, player_id, total_score, correct_answers, rank),
            )
            scoreboard_id = cursor.fetchone()["id"]
            con.commit()
            return scoreboard_id
        
# -------- PUT OPERATIONS -------------

def put_update_user(con, user_id, user_name, email, password, registration_date, user_status, birth_date):
    """Updates a specfic user and returns it"""
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """UPDATE users SET user_name = %s, email = %s, password = %s, registration_date = %s, user_status = %s, birth_date = %s
                WHERE id = %s RETURNING *;""",
                (user_name, email, password, registration_date, user_status, birth_date, user_id),
            )
            updated_user = cursor.fetchone()
            con.commit()
    return {
                    "id": updated_user["id"],
                    "user_name": updated_user.get("user_name"),
                    "email": updated_user.get("email"),
                    "registration_date": updated_user.get("registration_date"),
                    "user_status": updated_user.get("user_status"),
                    "birth_date": updated_user.get("birth_date")
                }

def put_update_quiz(con, quiz_id, quiz_creator_id, quiz_title, quiz_description, intro_image, created_at, updated_at, is_public):
    """Updates a specfic quiz and returns it"""
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """UPDATE quizzes SET quiz_creator_id = %s, quiz_title = %s, quiz_description = %s, intro_image %s, created_at =%s, updated_at = %s, is_public = %s
                WHERE id = %s RETURNING *;""",
                (quiz_creator_id, quiz_title, quiz_description, intro_image, created_at, updated_at, is_public, quiz_id),
            )
            updated_quiz = cursor.fetchone()
            con.commit()
    return {
        "id": updated_quiz["id"],
        "quiz_creator_id": updated_quiz.get("quiz_creator_id"), 
        "quiz_title": updated_quiz.get("quiz_title"), 
        "quiz_description": updated_quiz.get("quiz_description"), 
        "intro_image": updated_quiz.get("intro_image"), 
        "created_at": updated_quiz.get("created_at"), 
        "updated_at": updated_quiz.get("updated_at"), 
        "is_public": updated_quiz.get("is_public")
    }

def put_update_question(con, question_id, quiz_id, question_text, question_order, time_limit, points, question_type, image):
    """Updates a specfic question and returns it"""
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """UPDATE questions SET quiz_id = %s, question_text = %s, question_order = %s, time_limit = %s, points = %s, question_type = %s, image = %s
                WHERE id = %s RETURNING *;""",
                (quiz_id, question_text, question_order, time_limit, points, question_type, image, question_id),
            )
            updated_question = cursor.fetchone()
            con.commit()
    return {
        "id": updated_question["id"],
        "quiz_id": updated_question.get("quiz_id"),
        "question_text": updated_question.get("question_text"),
        "question_order": updated_question.get("question_order"),
        "time_limit": updated_question.get("time_limit"),
        "points": updated_question.get("points"),
        "question_type": updated_question.get("question_type"),
        "image": updated_question.get("image")
    }

def put_update_answer_alternative(con, answer_alternative_id, question_id, answer_text, is_correct, answer_icon, answer_order):
    """Updates a specfic answer alternative and returns it"""
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """UPDATE answer_alternatives SET question_id = %s, answer_text = %s, is_correct = %s, answer_icon = %s, answer_order = %s
                WHERE id = %s RETURNING *;""",
                (question_id, answer_text, is_correct, answer_icon, answer_order, answer_alternative_id),
            )
            updated_answer_alternative = cursor.fetchone()
            con.commit()
    return {
        "id": updated_answer_alternative["id"], 
        "question_id": updated_answer_alternative.get("question_id"), 
        "answer_text": updated_answer_alternative.get("answer_text"), 
        "is_correct": updated_answer_alternative.get("is_correct"), 
        "answer_icon": updated_answer_alternative.get("answer_icon"), 
        "answer_order": updated_answer_alternative.get("answer_order")
    }

def put_update_session(con, session_id, session_name, host_user_id, active_quiz, qr_code_id, session_status, started_at, current_question_id, session_code):
    """Updates a specfic session and returns it"""
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """UPDATE sessions SET session_name = %s, host_user_id = %s, active_quiz = %s, qr_code_id = %s, session_status = %s, started_at = %s, current_question_id = %s, session_code = %s
                WHERE id = %s RETURNING *;""",
                (session_name, host_user_id, active_quiz, qr_code_id, session_status, started_at, current_question_id, session_code, session_id),
            )
            updated_session = cursor.fetchone()
            con.commit()
    return {
        "id": updated_session["id"],
        "session_name": updated_session.get("session_name"), 
        "host_user_id": updated_session.get("host_user_id"), 
        "active_quiz": updated_session.get("active_quiz"), 
        "qr_code_id": updated_session.get("qr_code_id"), 
        "session_status": updated_session.get("session_status"),
        "started_at": updated_session.get("started_at"), 
        "current_question_id": updated_session.get("current_question_id"), 
        "session_code": updated_session.get("session_code")
    }

def put_update_session_player(con, session_player_id, session_id, display_name, user_id, joined_at, player_points):
    """Updates a specfic session player and returns it"""
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """UPDATE session_players SET session_id = %s, display_name = %s, user_id = %s, joined_at = %s, player_points = %s
                WHERE id = %s RETURNING *;""",
                (session_id, display_name, user_id, joined_at, player_points, session_player_id),
            )
            updated_player = cursor.fetchone()
            con.commit()
    return {
        "id": updated_player["id"],
        "session_id": updated_player.get("sessoin_id"), 
        "display_name": updated_player.get("display_name"), 
        "user_id": updated_player.get("user_id"), 
        "joined_at": updated_player.get("joined_at"), 
        "player_points": updated_player.get("player_points")
    }

def put_update_player_answer(con, player_answer_id, player_id, session_id, question_id, answer_id, response_time, points_earned, is_correct):
    """Updates a specfic player answer and returns it"""
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """UPDATE player_answers SET player_id = %s, session_id = %s, question_id = %s, answer_id = %s, response_time = %s, points_earned = %s, is_correct = %s
                WHERE id = %s RETURNING *;""",
                (player_id, session_id, question_id, answer_id, response_time, points_earned, is_correct, player_answer_id),
            )
            updated_answer = con.fetchone()
            con.commit()
    return {
        "id": updated_answer["id"],
        "player_id": updated_answer.get("player_id"), 
        "session_id": updated_answer.get("session_id"), 
        "question_id": updated_answer.get("question_id"), 
        "answer_id": updated_answer.get("answer_id"), 
        "response_time": updated_answer.get("response_time"), 
        "points_earned": updated_answer.get("points_earned"), 
        "is_correct": updated_answer.get("is_correct")
    }

def put_update_session_scoreboard(con, session_scoreboard_id, session_id, player_id, total_score, correct_answers, rank):
    """Updates a specfic session scoreboard and returns it"""
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """UPDATE session_scoreboards SET session_id = %s, player_id = %s, total_score = %s, correct_answers = %s, rank = %s
                WHERE id = %s RETURNING *;""",
                (session_id, player_id, total_score, correct_answers, rank, session_scoreboard_id),
            )
            updated_scoreboard = cursor.fetchone()
            con.commit()
    return {
        "id": updated_scoreboard["id"],
        "session_id": updated_scoreboard.get("session_id"), 
        "player_id": updated_scoreboard.get("player_id"), 
        "total_score": updated_scoreboard.get("total_score"), 
        "correct_answers": updated_scoreboard.get("correct_answers"), 
        "rank": updated_scoreboard.get("rank")
    }

# ----------- DELETE OPERATIONS ---------

def delete_user(con, user_id):
    "Deletes a specific user and returns its ID"
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                "DELETE FROM users WHERE id = %s RETURNING id;", (user_id,))
            deleted_user_id = cursor.fetchone()
            con.commit()
    return deleted_user_id

def delete_quiz(con, quiz_id):
    "Deletes a specific quiz and returns its ID"
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                "DELETE FROM quizzes WHERE id = %s RETURNINNG id;", (quiz_id,))
            deleted_quiz_id = cursor.fetchone()
            con.commit()
    return deleted_quiz_id

def delete_question(con, question_id):
    "Deletes a specific question and returns its ID"
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                "DELETE FROM questions WHERE id = %s RETURNING id;", (question_id,))
            deleted_question_id = cursor.fetchone()
            con.commit()
    return deleted_question_id

def delete_answer_alternative(con, answer_alternative_id):
    "Deletes a specific answer alternative and returns its ID"
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(
                    "DELETE FROM answer_alternatives WHERE id = %s RETURNING id;", (answer_alternative_id,))
                deleted_answer_id = cursor.fetchone()
                con.commit()
    return deleted_answer_id

def delete_session(con, session_id):
    "Deletes a specific session and returns its ID"
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(
                    "DELETE FROM sessions WHERE id = %s RETURNING id;", (session_id,))
                deleted_session_id = cursor.fetchone()
                con.commit()
    return deleted_session_id

def delete_session_player(con, session_player_id):
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                "DELETE FROM session_players WHERE id = %s RETURNING id;", (session_player_id,))
            deleted_player_id = cursor.fetchone()
            con.commit()
    return deleted_player_id

def delete_player_answer(con, player_answer_id):
    "Deletes a specific player answer and returns its ID"
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                "DELETE FROM player_answers WHERE id = %s RETURNING id;", (player_answer_id,))
            deleted_answer_id = cursor.fetchone()
            con.commit()
    return deleted_answer_id

def delete_session_scoreboard(con, session_scoreboard_id):
    "Deletes a specific session scoreboard and returns its ID"
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                "DELETE FROM session_scoreboards WHERE id = %s RETURNING id;", (session_scoreboard_id,))
            deleted_scoreboard_id = cursor.fetchone()
            con.commit()
    return deleted_scoreboard_id

#----- PATCH OPERATION ------

def patch_update_table(update_data: dict, table: str, pk: str = "id"):
    """Updates specific fields of a specific table"""
    set_clauses = []
    params = []

    for column_name, value in update_data.items():
        set_clauses.append(sql.SQL("{} = %s").format(sql.Identifier(column_name)))
        params.append(value)

    if not set_clauses:
        return None, None
    
    query = sql.SQL("""
        UPDATE {table}
        SET {set_clause}
        WHERE {pk} = %s
        RETURNING *
    """).format(
        table=sql.Identifier(table),
        set_clause=sql.SQL(", ").join(set_clauses),
        pk=sql.Identifier(pk),
    )

    params.append(None)

    return query, params