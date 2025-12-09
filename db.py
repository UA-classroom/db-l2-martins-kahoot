import psycopg2
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

def get_question_answer_alternatives(con, question_id):
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("""SELECT * FROM answer_alternatives WHERE question_id id = %s""", (question_id,))
            answer_alternatives = cursor.fetchall()
            return answer_alternatives

def get_player_answer_for_question(con, player_id, question_id):
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """SELECT * FROM player_answers 
                    WHERE player_id = %s AND question_id = %s""",
                    (player_id, question_id))
            player_answer = cursor.fetchone()
            return player_answer

def get_scoreboard_for_session(con, session_id):
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("""SELECT * FROM session_scoreboard WHERE session_id = %s""", (session_id))
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

# STATISKA VÄRDEN KAN INSERTAS I PGADMIN
# MER DYNAMISKA HÄR I METODERNA