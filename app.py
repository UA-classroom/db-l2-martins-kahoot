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
ADD ENDPOINTS FOR FASTAPI HERE
Make sure to do the following:
- Use the correct HTTP method (e.g get, post, put, delete)
- Use correct STATUS CODES, e.g 200, 400, 401 etc. when returning a result to the user
- Use pydantic models whenever you receive user data and need to validate the structure and data types (VG)
This means you need some error handling that determine what should be returned to the user
Read more: https://www.geeksforgeeks.org/10-most-common-http-status-codes/
- Use correct URL paths the resource, e.g some endpoints should be located at the exact same URL, 
but will have different HTTP-verbs.
"""


# INSPIRATION FOR A LIST-ENDPOINT - Not necessary to use pydantic models, but we could to ascertain that we return the correct values
# @app.get("/items/")
# def read_items():
#     con = get_connection()
#     items = get_items(con)
#     return {"items": items}


# INSPIRATION FOR A POST-ENDPOINT, uses a pydantic model to validate
# @app.post("/validation_items/")
# def create_item_validation(item: ItemCreate):
#     con = get_connection()
#     item_id = add_item_validation(con, item)
#     return {"item_id": item_id}


# IMPLEMENT THE ACTUAL ENDPOINTS! Feel free to remove

# --- User Endpoints ---

@app.get("/users")
def list_users():
    con = get_connection()
    users = db.get_users(con)
    return users

@app.get("/users/{user_id}")
def get_user(user_id: int):
    con = get_connection()
    user = db.get_user(con, user_id=user_id)
    if not user:
            raise HTTPException(status_code=404, detail="User not found")
    return user

@app.post("/users")
def add_user(user_input: sc.UserCreate):
    con = get_connection()
    try:
        user_id = db.add_user(con, user_input.user_name, user_input.email, user_input.password, user_input.registration_date, user_input.user_status, user_input.birth_date)
    except psycopg2.errors.ForeignKeyViolation:
        raise HTTPException(status_code=400, detail="Invalid email")
    except psycopg2.errors.UniqueViolation:
        raise HTTPException(status_code=400, detail="Name already taken")
    return user_id

@app.put("/users/{user_id}", response_model=sc.UserResponse)
def put_update_user(user_id: int, user_update: sc.UserUpdate):
    con = get_connection()
    try:
        updated_user = db.put_update_user(con, user_update.user_name, user_update.email, user_update.password, user_update.registration_date, user_update.user_status, user_update.birth_date, user_id=user_id)
        if not updated_user:
            raise HTTPException(status_code=404, detail="User not found")
    except psycopg2.errors.ForeignKeyViolation:
        raise HTTPException(status_code=400, detail="Invalid email")
    except psycopg2.errors.UniqueViolation:
        raise HTTPException(status_code=400, detail="Name already taken")
    return updated_user

@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    con = get_connection()
    try:
        deleted_user_id = db.delete_user(con, user_id=user_id)
        if not deleted_user_id:
                raise HTTPException(status_code=404, detail="User not found")
    except psycopg2.errors.ForeignKeyViolation:
        raise HTTPException(status_code=400, detail="Cannot delete user due to foreign key constraints")
    return deleted_user_id

@app.patch("/users/{user_id}")
def patch_update_user(user_id: int, user_patch: sc.UserPatch):
    update_data = user_patch.model_dump(exclude_unset=True)

    if not update_data:
        raise HTTPException(status_code=400, detail="No field to update")
    
    query, params = db.patch_update_user(update_data=update_data, table="users", pk="id")
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

# --- Quizzes endpoints ---

@app.get("/quizzes")
def list_quizzes():
    con = get_connection()
    quizzes = db.get_quizzes(con)
    return quizzes

@app.get("/quizzes/{quiz_id}")
def get_quiz(quiz_id: int):
    con = get_connection()
    quiz = db.get_quiz(con, quiz_id=quiz_id)
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    return quiz

@app.post("/quizzes")
def add_quiz(quiz_input: sc.QuizCreate):
    con = get_connection()
    try:
        quiz_id = db.add_quiz(con, quiz_input.quiz_creator_id, quiz_input.quiz_title, quiz_input.quiz_description, quiz_input.intro_image, quiz_input.created_at, quiz_input.updated_at, quiz_input.is_public)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return quiz_id

@app.put("/quizzes/{quiz_id}", response_model=sc.QuizResponse)
def put_update_quiz(quiz_id: int, quiz_update: sc.QuizUpdate):
    con = get_connection()
    try:
        updated_quiz = db.put_update_quiz(con, quiz_update.quiz_creator_id, quiz_update.quiz_title, quiz_update.quiz_description, quiz_update.intro_image, quiz_update.created_at, quiz_update.updated_at, quiz_update.is_public, quiz_id=quiz_id)
        if not updated_quiz:
            raise HTTPException(status_code=404, detail="Quiz not found")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return updated_quiz

@app.delete("/quizzes/{quiz_id}")
def delete_quiz(quiz_id: int):
    con = get_connection()
    try:
        deleted_quiz_id = db.delete_quiz(con, quiz_id=quiz_id)
        if not deleted_quiz_id:
            raise HTTPException(status_code=404, detail="Quiz not found")
    except psycopg2.errors.ForeignKeyViolation:
        raise HTTPException(status_code=400, detail="Cannot delete quiz due to foreign key constraints")
    return deleted_quiz_id

# --- Question Endpoints ---

@app.get("/questions")
def list_questions():
    con = get_connection()
    questions = db.get_questions(con)
    return questions

@app.get("/questions/{question_id}")
def get_question(question_id: int):
    con = get_connection()
    question = db.get_question(con, question_id=question_id)
    if not question:
            raise HTTPException(status_code=404, detail="Question not found")
    return question

@app.get("/questions/{quiz_id}")
def get_quiz_questions(con, quiz_id: int):
    con = get_connection()
    quiz_questions = db.get_quiz_questions(con, quiz_id=quiz_id)
    if not quiz_questions:
            raise HTTPException(status_code=404, detail="Quiz not found")
    return quiz_questions

@app.post("/questions")
def add_question(question_input: sc.QuestionCreate):
    con = get_connection()
    try:
        question_id = db.add_question(con, question_input.qiuz_id, question_input.question_text, question_input.question_order, question_input.time_limit, question_input.points, question_input.question_type, question_input.image)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return question_id

@app.put("/questions/{question_id}", response_model=sc.QuestionResponse)
def put_update_question(question_id: int, question_update: sc.QuestionUpdate):
    con = get_connection()
    try:
        updated_question = db.put_update_question(con, question_update.qiuz_id, question_update.question_text, question_update.question_order, question_update.time_limit, question_update.points, question_update.question_type, question_update.image, question_id=question_id)
        if not updated_question:
            raise HTTPException(status_code=404, detail="Question not found")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return updated_question

@app.delete("/questions/{question_id}")
def delete_question(question_id: int):
    con = get_connection()
    try:
        deleted_question_id = db.delete_question(con, question_id=question_id)
        if not deleted_question_id:
            raise HTTPException(status_code=404, detail="Question not found")
    except psycopg2.errors.ForeignKeyViolation:
        raise HTTPException(status_code=400, detail="Cannot delete question due to foreign key constraints")
    return deleted_question_id

