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


# STATISKA VÄRDEN KAN INSERTAS I PGADMIN
# MER DYNAMISKA HÄR I METODERNA