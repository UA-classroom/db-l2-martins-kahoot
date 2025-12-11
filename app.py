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
def update_user(user_id: int, user_update: sc.UserUpdate):
    con = get_connection()
    try:
        user = db.put_update_user(con, user_id, user_update.user_name, user_update.email, user_update.password, user_update.registration_date, user_update.user_status, user_update.birth_date)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
    except psycopg2.errors.ForeignKeyViolation:
        raise HTTPException(status_code=400, detail="Invalid email")
    except psycopg2.errors.UniqueViolation:
        raise HTTPException(status_code=400, detail="Name already taken")
    return user

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
def patch_user(user_id: int, user_patch: sc.UserPatch):
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
