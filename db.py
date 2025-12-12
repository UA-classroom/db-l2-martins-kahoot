import psycopg2
from psycopg2 import errors, sql
from psycopg2.extras import RealDictCursor

"""
This file is responsible for making database queries, which your fastapi endpoints/routes can use.
The reason we split them up is to avoid clutter in the endpoints, so that the endpoints might focus on other tasks 

- Try to return results with cursor.fetchall() or cursor.fetchone() when possible
- Make sure you always give the user response if something went right or wrong, sometimes 
you might need to use the RETURNING keyword to garantuee that something went right / wrong
e.g when making DELETE or UPDATE queries
- No need to use a class here
- Try to raise exceptions to make them more reusable and work a lot with returns
- You will need to decide which parameters each function should receive. All functions 
start with a connection parameter.
- Below, a few inspirational functions exist - feel free to completely ignore how they are structured
- E.g, if you decide to use psycopg3, you'd be able to directly use pydantic models with the cursor, these examples are however using psycopg2 and RealDictCursor
"""


### THIS IS JUST AN EXAMPLE OF A FUNCTION FOR INSPIRATION FOR A LIST-OPERATION (FETCHING MANY ENTRIES)
# def get_items(con):
#     with con:
#         with con.cursor(cursor_factory=RealDictCursor) as cursor:
#             cursor.execute("SELECT * FROM items;")
#             items = cursor.fetchall()
#     return items

def get_users(con):
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT * FROM users;")
            users = cursor.fetchall()
    return users

def get_quizzes(con):
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT * FROM quizzes;")
            quizzes = cursor.fetchall()
    return quizzes

def get_sessions(con):
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT * FROM sessions;")
            sessions = cursor.fetchall()
    return sessions

def get_all_session_players(con):
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT * FROM session_players;")
            session_players = cursor.fetchall()
    return session_players

def get_session_players(con, session_id):
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("""SELECT * FROM session_players WHERE session_id = %s""", (session_id,))
            session_players = cursor.fetchall()
    return session_players

def get_questions(con):
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT * FROM questions;")
            questions = cursor.fetchall()
    return questions

def get_quiz_questions(con, quiz_id):
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("""SELECT * FROM questions WHERE quiz_id = %s""", (quiz_id,))
            quiz_questions = cursor.fetchall()
    return quiz_questions

def get_question_answer_alternatives(con, question_id):
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("""SELECT * FROM answer_alternatives WHERE question_id id = %s""", (question_id,))
            answer_alternatives = cursor.fetchall()
            return answer_alternatives

### THIS IS JUST INSPIRATION FOR A DETAIL OPERATION (FETCHING ONE ENTRY)
# def get_item(con, item_id):
#     with con:
#         with con.cursor(cursor_factory=RealDictCursor) as cursor:
#             cursor.execute("""SELECT * FROM items WHERE id = %s""", (item_id,))
#             item = cursor.fetchone()
#             return item

def get_user(con, user_id):
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("""SELECT * FROM users WHERE id = %s""", (user_id,))             
            user = cursor.fetchone()
            return user
        
def get_quiz(con, quiz_id):
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("""SELECT * FROM quizzes WHERE id = %s""", (quiz_id,))             
            quiz = cursor.fetchone()
            return quiz
        
def get_session(con, session_id):
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT * FROM sessions WHERE id = %s", (session_id))
            session = cursor.fetchone()
    return session

def get_session_player(con, session_player_id):
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("""SELECT * FROM session_players WHERE id = %s""", (session_player_id,))             
            session_player = cursor.fetchone()
            return session_player

def get_question(con, question_id):
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("""SELECT * FROM questions WHERE id = %s""", (question_id,))             
            question = cursor.fetchone()
            return question
        
def get_answer_alternative(con, answer_alternative_id):
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("""SELECT * FROM answer_alternatives WHERE id = %s""", (answer_alternative_id,))             
            answer_alternative = cursor.fetchone()
            return answer_alternative


def get_player_answer_for_question(con, player_id, question_id):
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """SELECT * FROM player_answers 
                    WHERE player_id = %s AND question_id = %s""",
                    (player_id, question_id),)
            player_answer = cursor.fetchone()
            return player_answer

def get_scoreboard_for_session(con, session_id):
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("""SELECT * FROM session_scoreboard WHERE session_id = %s""", (session_id,))
            scoreboard = cursor.fetchone()
            return scoreboard
        
# -------------------------------------------------------------------------------------------------------
def get_item(con, table, item_id): # dålig säkerhet, måste fixas eller skitas i
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(f"""SELECT * FROM {table} WHERE id = %s""", (item_id,))             
            item = cursor.fetchone()
            return item


### THIS IS JUST INSPIRATION FOR A CREATE-OPERATION
# def add_item(con, title, description):
#     with con:
#         with con.cursor(cursor_factory=RealDictCursor) as cursor:
#             cursor.execute(
#                 "INSERT INTO items (title, description) VALUES (%s, %s) RETURNING id;",
#                 (title, description),
#             )
#             item_id = cursor.fetchone()["id"]
#     return item_id

def add_user(con, user_name, email, password, registration_date, user_status, birth_date):
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

def add_quiz(con, quiz_creator_id, quiz_title, quiz_description, intro_image, created_at, is_public):
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """INSERT INTO quizzes (quiz_creator_id, quiz_title, quiz_description, intro_image, created_at, is_public)
                VALUES (%s, %s, %s, %s, %s, %s) RETURNING id;""",
                (quiz_creator_id, quiz_title, quiz_description, intro_image, created_at, is_public),
            )
            quiz_id = cursor.fetchone()["id"]
            con.commit()
    return quiz_id

def add_question(con, quiz_id, question_text, question_order, time_limit, points, question_type, image):
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

def add_session_scoreboard(con, session_id, player_id, total_score, correct_answers, rank):
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """INSERT INTO session_scoreboard (session_id, player_id, total_score, correct_answers, rank)
                VALUES (%s, %s, %s, %s, %s) RETURNING id;"""
                (session_id, player_id, total_score, correct_answers, rank),
            )
            scoreboard_id = cursor.fetchone()["id"]
            con.commit()
            return scoreboard_id
        
# -------- PUT FUNCTIONS -------------

def put_update_user(con, user_id, user_name, email, password, registration_date, user_status, birth_date):
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
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """UPDATE quizzes SET quiz_creator_id = %s, quiz_title = %s, quiz_description = %s, intro_image %s, created_at =%s, updated_at = %s, is_public = %s
                WHERE id = %s RETURNING *,""",
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

# ----------- DELETE FUNCTIONS ---------

def delete_user(con, user_id):
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                "DELETE FROM users WHERE id = %s RETURNING id;", (user_id,))
            deleted_user_id = cursor.fetchone()
            con.commit()
    return deleted_user_id

def delete_quiz(con, quiz_id):
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                "DELETE FROM quizzes WHERE id = %s RETURNINNG id;", (quiz_id,))
            deleted_quiz_id = cursor.fetchone()
            con.commit()
    return deleted_quiz_id

def delete_question(con, question_id):
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                "DELETE FROM questions WHERE id = %s RETURNING id;", (question_id,))
            deleted_question_id = cursor.fetchone()
            con.commit()
    return deleted_question_id

def delete_answer_alternative(con, answer_alternative_id):
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(
                    "DELETE FROM answer_alternatives WHERE id = %s RETURNING id;", (answer_alternative_id,))
                deleted_answer_id = cursor.fetchone()
                con.commit()
    return deleted_answer_id

def delete_session(con, session_id):
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(
                    "DELETE FROM sessions WHERE id = %s RETURNING id;", (session_id,))
                deleted_session_id = cursor.fetchone()
                con.commit()
    return deleted_session_id

#----- PATCH FUNCTIONS ------

def patch_update_user(update_data: dict, table: str, pk: str = "id"):
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

# STATISKA VÄRDEN KAN INSERTAS I PGADMIN
# MER DYNAMISKA HÄR I METODERNA