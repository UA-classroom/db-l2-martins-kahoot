import os

import psycopg2
from fastapi import FastAPI, HTTPException, status
from psycopg2 import errors
from psycopg2.extras import RealDictCursor

import db as db
import schemas as sc
from db_setup import get_connection

app = FastAPI()

"""
Endpoints for the API, organized by database-table.
"""

# --- Users Endpoints ---

@app.get("/users")
def list_users():
    """Fetch users from the database, max 10"""
    con = get_connection()
    users = db.get_users(con, limit=10)
    return users

@app.get("/users/{user_id}")
def get_user(user_id: int):
    """Fetch a specific user by ID"""
    con = get_connection()
    user = db.get_user(con, user_id=user_id)
    if not user:
            raise HTTPException(status_code=404, detail="User not found")
    return user

@app.post("/users")
def add_user(user_input: sc.UserCreate):
    """Adds a new user to the database, returns the new object and its ID"""
    con = get_connection()
    try:
        user_id = db.add_user(
            con, 
            user_input.user_name, 
            user_input.email, 
            user_input.password, 
            user_input.registration_date, 
            user_input.user_status, 
            user_input.birth_date
        )
    except psycopg2.errors.ForeignKeyViolation:
        raise HTTPException(status_code=400, detail="Invalid email")
    except psycopg2.errors.UniqueViolation:
        raise HTTPException(status_code=400, detail="Name already taken")
    return user_id

@app.put("/users/{user_id}", response_model=sc.UserResponse)
def put_update_user(user_id: int, user_update: sc.UserUpdate):
    """Updates a specific user and returns the whole object"""
    con = get_connection()
    try:
        updated_user = db.put_update_user(
            con, 
            user_id, 
            user_update.user_name, 
            user_update.email, 
            user_update.password, 
            user_update.registration_date, 
            user_update.user_status, 
            user_update.birth_date
        )
        if not updated_user:
            raise HTTPException(status_code=404, detail="User not found")
    except psycopg2.errors.ForeignKeyViolation:
        raise HTTPException(status_code=400, detail="Invalid email")
    except psycopg2.errors.UniqueViolation:
        raise HTTPException(status_code=400, detail="Name already taken")
    return updated_user

@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    """Delete a specific user and returns its ID"""
    con = get_connection()
    try:
        deleted_user_id = db.delete_user(con, user_id=user_id)
        if not deleted_user_id:
                raise HTTPException(status_code=404, detail="User not found")
    except psycopg2.errors.ForeignKeyViolation:
        raise HTTPException(status_code=400, detail="Cannot delete user due to foreign key constraints")
    return deleted_user_id

@app.patch("/users/{user_id}", response_model=sc.UserResponse)
def patch_update_user(user_id: int, user_patch: sc.UserPatch):
    update_data = user_patch.model_dump(exclude_unset=True)

    if not update_data:
        raise HTTPException(status_code=400, detail="No field to update")
    
    query, params = db.patch_update_table(update_data=update_data, table="users", pk="id")
    params[-1] = user_id
    con = get_connection()

    try:
        with con:
            with con.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(query, tuple(params))
                updated_user = cursor.fetchone()

                if not updated_user:
                    raise HTTPException(status_code=404, detail="User not found")
                
                return {
                    "id": updated_user["id"],
                    "user_name": updated_user.get("user_name"),
                    "email": updated_user.get("email"),
                    "registration_date": updated_user.get("registration_date"),
                    "user_status": updated_user.get("user_status"),
                    "birth_date": updated_user.get("birth_date")
                }
    except errors.UniqueViolation:
        raise HTTPException(status_code=409, detail="Unique constraint violation")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# --- Quizzes Endpoints ---

@app.get("/quizzes")
def list_quizzes():
    """Fetch quizzes from the database, max 10"""
    con = get_connection()
    quizzes = db.get_quizzes(con, limit=10)
    return quizzes

@app.get("/quizzes/{quiz_id}")
def get_quiz(quiz_id: int):
    """Fetch a specific quiz by ID"""
    con = get_connection()
    quiz = db.get_quiz(con, quiz_id=quiz_id)
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    return quiz

@app.post("/quizzes")
def add_quiz(quiz_input: sc.QuizCreate):
    """Adds a new quiz to the database, returns the new object and its ID"""
    con = get_connection()
    try:
        quiz_id = db.add_quiz(
            con, 
            quiz_input.quiz_creator_id, 
            quiz_input.quiz_title, 
            quiz_input.quiz_description, 
            quiz_input.intro_image, 
            quiz_input.created_at, 
            quiz_input.updated_at, 
            quiz_input.is_public
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return quiz_id

@app.put("/quizzes/{quiz_id}", response_model=sc.QuizResponse)
def put_update_quiz(quiz_id: int, quiz_update: sc.QuizUpdate):
    """Updates a specific quiz and returns the whole object"""
    con = get_connection()
    try:
        updated_quiz = db.put_update_quiz(
            con, 
            quiz_id, 
            quiz_update.quiz_creator_id, 
            quiz_update.quiz_title, 
            quiz_update.quiz_description, 
            quiz_update.intro_image, 
            quiz_update.created_at, 
            quiz_update.updated_at, 
            quiz_update.is_public
        )
        if not updated_quiz:
            raise HTTPException(status_code=404, detail="Quiz not found")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return updated_quiz

@app.delete("/quizzes/{quiz_id}")
def delete_quiz(quiz_id: int):
    """Delete a specific quiz and returns its ID"""
    con = get_connection()
    try:
        deleted_quiz_id = db.delete_quiz(con, quiz_id=quiz_id)
        if not deleted_quiz_id:
            raise HTTPException(status_code=404, detail="Quiz not found")
    except psycopg2.errors.ForeignKeyViolation:
        raise HTTPException(status_code=400, detail="Cannot delete quiz due to foreign key constraints")
    return deleted_quiz_id

@app.patch("/quizzes/{quiz_id}", response_model=sc.QuizResponse)
def patch_update_quiz(quiz_id: int, quiz_patch: sc.QuizPatch):
    update_data = quiz_patch.model_dump(exclude_unset=True)

    if not update_data:
        raise HTTPException(status_code=400, detail="No field to update")
    
    query, params = db.patch_update_table(update_data=update_data, table="quizzes", pk="id")
    params[-1] = quiz_id
    con = get_connection()

    try:
        with con:
            with con.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(query, tuple(params))
                updated_quiz = cursor.fetchone()

                if not updated_quiz:
                    raise HTTPException(status_code=404, detail="Quiz not found")
                
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
    except errors.UniqueViolation:
        raise HTTPException(status_code=409, detail="Unique constraint violation")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# --- Questions Endpoints ---

@app.get("/questions")
def list_questions():
    """Fetch questions from the database, max 10"""
    con = get_connection()
    questions = db.get_questions(con, limit=10)
    return questions

@app.get("/questions/{question_id}")
def get_question(question_id: int):
    """Fetch a specific question by ID"""
    con = get_connection()
    question = db.get_question(con, question_id=question_id)
    if not question:
            raise HTTPException(status_code=404, detail="Question not found")
    return question

@app.get("/questions/{quiz_id}")
def get_quiz_questions(con, quiz_id: int):
    con = get_connection()
    quiz_questions = db.get_quiz_questions(con, quiz_id=quiz_id, limit=10)
    if not quiz_questions:
            raise HTTPException(status_code=404, detail="Quiz not found")
    return quiz_questions

@app.post("/questions")
def add_question(question_input: sc.QuestionCreate):
    """Adds a new question to the database, returns the new object and its ID"""
    con = get_connection()
    try:
        question_id = db.add_question(
            con, 
            question_input.quiz_id, 
            question_input.question_text, 
            question_input.question_order, 
            question_input.time_limit, 
            question_input.points, 
            question_input.question_type, 
            question_input.image
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return question_id

@app.put("/questions/{question_id}", response_model=sc.QuestionResponse)
def put_update_question(question_id: int, question_update: sc.QuestionUpdate):
    """Updates a specific questoin and returns the whole object"""
    con = get_connection()
    try:
        updated_question = db.put_update_question(
            con, 
            question_id, 
            question_update.qiuz_id, 
            question_update.question_text, 
            question_update.question_order, 
            question_update.time_limit, 
            question_update.points, 
            question_update.question_type,
            question_update.image
        )
        if not updated_question:
            raise HTTPException(status_code=404, detail="Question not found")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return updated_question

@app.delete("/questions/{question_id}")
def delete_question(question_id: int):
    """Delete a specific question and returns its ID"""
    con = get_connection()
    try:
        deleted_question_id = db.delete_question(con, question_id=question_id)
        if not deleted_question_id:
            raise HTTPException(status_code=404, detail="Question not found")
    except psycopg2.errors.ForeignKeyViolation:
        raise HTTPException(status_code=400, detail="Cannot delete question due to foreign key constraints")
    return deleted_question_id

@app.patch("/questions/{question_id}", response_model=sc.QuestionResponse)
def patch_update_question(question_id: int, question_patch: sc.QuestionPatch):
    update_data = question_patch.model_dump(exclude_unset=True)

    if not update_data:
        raise HTTPException(status_code=400, detail="No field to update")
    
    query, params = db.patch_update_table(update_data=update_data, table="questions", pk="id")
    params[-1] = question_id
    con = get_connection()

    try:
        with con:
            with con.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(query, tuple(params))
                updated_question = cursor.fetchone()

                if not updated_question:
                    raise HTTPException(status_code=404, detail="Question not found")
                
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
    except errors.UniqueViolation:
        raise HTTPException(status_code=409, detail="Unique constraint violation")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# --- Answer alternatives Endpoints ---

@app.get("/answer_alternatives/{question_id}")
def get_question_answer_alternatives(question_id: int):
    """Fetch answer alternatives for a specific question"""
    con = get_connection()
    answer_alternatives = db.get_question_answer_alternatives(con, question_id=question_id, limit=10)
    if not answer_alternatives:
        raise HTTPException(status_code=404, detail="Question not found")
    return answer_alternatives

@app.get("/answer_alternatives/{answer_alternative_id}")
def get_answer_alternative(answer_alternative_id: int):
    """Fetch a specific answer alternative by ID"""
    con = get_connection()
    answer_alternative = db.get_answer_alternative(con, answer_alternative_id=answer_alternative_id)
    if not answer_alternative:
            raise HTTPException(status_code=404, detail="Answer not found")
    return answer_alternative

@app.post("/answer_alternatives")
def add_answer_alternative(answer_input: sc.AnswerAlternativeCreate):
    """Adds a new answer alternative to the database, returns the new object and its ID"""
    con = get_connection()
    try:
        answer_alternative_id = db.add_answer_alternative(
            con, 
            answer_input.question_id, 
            answer_input.answer_text, 
            answer_input.is_correct, 
            answer_input.answer_icon, 
            answer_input.answer_order
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return answer_alternative_id

@app.put("/answer_alternatives/{answer_alternative_id}", response_model=sc.AnswerAlternativeResponse)
def put_update_answer_alternative(answer_alternative_id: int, answer_update: sc.AnswerAlternativeUpdate):
    """Updates a specific answer alternative and returns the whole object"""
    con = get_connection()
    try:
        updated_answer = db.put_update_answer_alternative(
            con, 
            answer_alternative_id, 
            answer_update.question_id, 
            answer_update.answer_text, 
            answer_update.is_correct, 
            answer_update.answer_icon
        )
        if not updated_answer:
            raise HTTPException(status_code=404, detail="Answer not found")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return updated_answer

@app.delete("/answer_alternatives/{answer_alternative_id}")
def delete_answer_alternative(answer_alternative_id: int):
    """Delete a specific asnwer alternative and returns its ID"""
    con = get_connection()
    try:
        deleted_answer_id = db.delete_answer_alternative(con, answer_alternative_id=answer_alternative_id)
        if not deleted_answer_id:
            raise HTTPException(status_code=404, detail="Answer not found")
    except psycopg2.errors.ForeignKeyViolation:
        raise HTTPException(status_code=400, detail="Cannot delete answer due to foreign key constraints")
    return deleted_answer_id

# --- Sessions Endpoints ---

@app.get("/sessions")
def list_sessions():
    """Fetch sessions from the database, max 10"""
    con = get_connection()
    sessions = db.get_sessions(con, limit=10)
    return sessions

@app.get("/sessions/{session_id}")
def get_session(session_id: int):
    """Fetch a specific session by ID"""
    con = get_connection()
    session = db.get_session(con, session_id=session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session

@app.post("/sessions")
def add_session(session_input: sc.SessionCreate):
    """Adds a new session to the database, returns the new object and its ID"""
    con = get_connection()
    try:
        session_id = db.add_session(
            con, 
            session_input.session_name, 
            session_input.host_user_id, 
            session_input.active_quiz, 
            session_input.qr_code_id, 
            session_input.session_status, 
            session_input.started_at, 
            session_input.current_question_id, 
            session_input.session_code
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return session_id

@app.put("/sessions/{session_id}", response_model=sc.SessionResponse)
def put_update_session(session_id: int, session_update: sc.SessionUpdate):
    """Updates a specific session and returns the whole object"""
    con = get_connection()
    try:
        updated_session = db.put_update_session(
            con, 
            session_id, 
            session_update.session_name, 
            session_update.host_user_id, 
            session_update.active_quiz, 
            session_update.qr_code_id, 
            session_update.session_status, 
            session_update.started_at, 
            session_update.current_question_id, 
            session_update.session_code
        )
        if not updated_session:
            raise HTTPException(status_code=404, detail="Session not found")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return updated_session

@app.delete("/sessions/{session_id}")
def delete_session(session_id: int):
    """Delete a specific session and returns its ID"""
    con = get_connection()
    try:
        deleted_session_id = db.delete_session(con, session_id=session_id)
        if not deleted_session_id:
            raise HTTPException(status_code=404, detail="Session not found")
    except psycopg2.errors.ForeignKeyViolation:
        raise HTTPException(status_code=400, detail="Cannot delete session due to foreign key constraints")
    return deleted_session_id

# --- Session players Endpoints ---

@app.get("/session_players")
def list_all_session_players():
    """Fetch session players from the database, max 10"""
    con = get_connection()
    all_session_players = db.get_all_session_players(con, limit=10)
    return all_session_players

@app.get("/session_players/{session_id}")
def get_players_for_session(con, session_id: int):
    """Fetch players for a specific session"""
    con = get_connection()
    players = db.get_players_for_session(con, session_id=session_id)
    if not players:
        raise HTTPException(status_code=404, detail="Session not found")
    return players

@app.get("/session_players/{session_player_id}")
def get_session_player(session_player_id: int):
    """Fetch a specific session player by ID"""
    con = get_connection()
    player = db.get_session_player(con, session_player_id=session_player_id)
    if not player:
        raise HTTPException(status_code=404, detail="Session player not found")
    return player

@app.post("/session_players")
def add_session_player(player_input: sc.SessionPlayerCreate):
    """Adds a new session player to the database, returns the new object and its ID"""
    con = get_connection()
    try:
        player_id = db.add_session_player(
            con, 
            player_input.session_id, 
            player_input.display_name, 
            player_input.user_id, 
            player_input.joined_at, 
            player_input.player_points
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return player_id

@app.put("/session_player/{session_player_id}", response_model=sc.SessionPlayerResponse)
def put_update_session_player(session_player_id: int, player_update: sc.SessionPlayerUpdate):
    """Updates a specific session player and returns the whole object"""
    con = get_connection()
    try:
        updated_player = db.put_update_session_player(
            con, 
            session_player_id, 
            player_update.session_id, 
            player_update.display_name,
            player_update.user_id, 
            player_update.joined_at, 
            player_update.player_points
        )
        if not updated_player:
            raise HTTPException(status_code=404, detail="Session player not found")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return updated_player

@app.delete("/session_players/{session_player_id}")
def delete_session_player(session_player_id: int):
    """Delete a specific session player and returns its ID"""
    con = get_connection()
    try:
        deleted_player_id = db.delete_session_player(con, session_player_id=session_player_id)
        if not deleted_player_id:
            raise HTTPException(status_code=404, detail="Session player not found")
    except psycopg2.errors.ForeignKeyViolation:
        raise HTTPException(status_code=400, detail="Cannot delete player due to foreign key constraints")
    return deleted_player_id

# --- Player answers Endpoints --- 

@app.get("/player_answers")
def list_all_player_answers():
    """Fetch player asnwers from the database, max 10"""
    con = get_connection()
    all_player_answers = db.get_all_player_answers(con, limit=10)
    return all_player_answers

@app.get("/player_answers/{session_player_id}")
def list_answers_by_player(session_player_id: int):
    """Fetch answers by a specific session player based on their ID"""
    con = get_connection()
    player_answers = db.get_answers_by_player(con, session_player_id=session_player_id, limit=10)
    if not player_answers:
            raise HTTPException(status_code=404, detail="Session player not found")
    return player_answers

@app.get("/player_answers/{session_player_id}/{question_id}")
def get_player_answer_for_question(session_player_id: int, question_id: int):
    """Fetch answer by a specific player for a specific question"""
    con = get_connection()
    player_answer = db.get_player_answer_for_question(con, player_id=session_player_id, question_id=question_id)
    if not player_answer:
            raise HTTPException(status_code=404, detail="Player answer not found")
    return player_answer

@app.post("/player_answers")
def add_player_answer(answer_input: sc.PlayerAnswerCreate):
    """Adds a new player answer to the database, returns the new object and its ID"""
    con = get_connection()
    try:
        answer_id = db.add_player_answer(
            con, 
            answer_input.player_id, 
            answer_input.session_id, 
            answer_input.question_id, 
            answer_input.answer_id, 
            answer_input.response_time, 
            answer_input.points_earned, 
            answer_input.is_correct
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return answer_id

@app.put("/player_answers/{player_answer_id}", response_model=sc.PlayerAnswerResponse)
def put_update_player_answer(player_answer_id: int, answer_update: sc.PlayerAnswerUpdate):
    """Updates a specific player answer and returns the whole object"""
    con = get_connection()
    try:
        updated_answer = db.put_update_player_answer(
            con, 
            player_answer_id, 
            answer_update.player_id, 
            answer_update.session_id, 
            answer_update.question_id, 
            answer_update.answer_id, 
            answer_update.response_time, 
            answer_update.points_earned, 
            answer_update.is_correct
        )
        if not updated_answer:
            raise HTTPException(status_code=404, detail="Answer not found")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return updated_answer

@app.delete("/player_answers/{player_answer_id}")
def delete_player_answer(player_answer_id: int):
    """Delete a specific player answer and returns its ID"""
    con = get_connection()
    try:
        deleted_answer_id = db.delete_player_answer(con, player_answer_id=player_answer_id)
        if not deleted_answer_id:
            raise HTTPException(status_code=404, detail="Answer not found")
    except psycopg2.errors.ForeignKeyViolation:
        raise HTTPException(status_code=400, detail="Cannot delete answer due to foreign key constraints")
    return deleted_answer_id

# --- Session scoreboards Endpoints ---

@app.get("/session_scoreboards")
def list_session_scoreboards():
    """Fetch session scoreboards from the database, max 10"""
    con = get_connection()
    scoreboards = db.get_session_scoreboards(con, limit=10)
    return scoreboards

@app.get("/session_scoreboards/{session_id}")
def get_scoreboard_for_session(session_id: int):
    """Fetch a scoreboard for a specific session based on the session's ID"""
    con = get_connection()
    scoreboard = db.get_scoreboard_for_session(con, session_id=session_id)
    if not scoreboard:
        raise HTTPException(status_code=404, detail="Scoreboard not found")
    return scoreboard

@app.post("/session_scoreboards")
def add_session_scoreboard(scoreboard_input: sc.ScoreboardCreate):
    """Adds a new session scoreboard to the database, returns the new object and its ID"""
    con = get_connection()
    try:
        scoreboard_id = db.add_session_scoreboard(
            con, 
            scoreboard_input.session_id, 
            scoreboard_input.player_id, 
            scoreboard_input.total_score, 
            scoreboard_input.correct_answers, 
            scoreboard_input.rank
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return scoreboard_id

@app.put("/session_scoreboards/{session_scoreboard_id}", response_model=sc.ScoreboardResponse)
def put_update_session_scoreboard(session_scoreboard_id: int, scoreboard_update: sc.ScoreboardUpdate):
    """Updates a specific session scoreboard and returns the whole object"""
    con = get_connection()
    try:
        updated_scoreboard = db.put_update_session_scoreboard(
            con, 
            session_scoreboard_id, 
            scoreboard_update.session_id, 
            scoreboard_update.player_id, 
            scoreboard_update.total_score, 
            scoreboard_update.correct_answers, 
            scoreboard_update.rank
        )
        if not updated_scoreboard:
            raise HTTPException(status_code=404, detail="Scoreboard not found")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return updated_scoreboard

@app.delete("/session_scoreboards/{session_scoreboard_id}")
def delete_session_scoreboard(session_scoreboard_id: int):
    """Delete a specific session scoreboard and returns its ID"""
    con = get_connection()
    try:
        deleted_scoreboard_id = db.delete_session_scoreboard(con, session_scoreboard_id=session_scoreboard_id)
        if not deleted_scoreboard_id:
            raise HTTPException(status_code=404, detail="Scoreboard not found")
    except psycopg2.errors.ForeignKeyViolation:
        raise HTTPException(status_code=400, detail="Cannot delete scoreboard due to foreign key constraints")
    return deleted_scoreboard_id