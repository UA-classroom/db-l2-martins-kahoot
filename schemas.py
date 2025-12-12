from datetime import date, datetime, time
from typing import Optional

from pydantic import BaseModel, EmailStr, Field

# Add Pydantic schemas here that you'll use in your routes / endpoints
# Pydantic schemas are used to validate data that you receive, or to make sure that whatever data
# you send back to the client follows a certain structure

class UserCreate(BaseModel):
    user_name: str 
    email: EmailStr 
    password: str 
    registration_date: datetime
    user_status: int 
    birth_date: date

class UserResponse(BaseModel):
    user_name: str = Field(max_lenght=50)
    email: str
    password: str = Field(min_lenght=8)
    registration_date: datetime
    user_status: int
    birth_date: date

class UserUpdate(BaseModel):
    user_name: str 
    email: EmailStr 
    password: str 
    registration_date: datetime
    user_status: int 
    birth_date: date

class UserPatch(BaseModel):
    user_name: Optional[str] = Field(None, max_lenght=50)
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(None, min_lenght=8)
    registration_date: Optional[datetime] = None
    user_status: Optional[int] = None
    birth_date: Optional[date] = None

class QuizCreate(BaseModel):
    quiz_creator_id: int
    quiz_title: str
    quiz_description: str
    intro_image: int
    created_at: datetime
    updated_at: datetime
    is_public: bool

class QuizResponse(BaseModel):
    quiz_creator_id: int
    quiz_title: str
    quiz_description: str
    intro_image: int
    created_at: datetime
    updated_at: datetime
    is_public: bool

class QuizUpdate(BaseModel):
    quiz_creator_id: int
    quiz_title: str
    quiz_description: str
    intro_image: int
    created_at: datetime
    updated_at: datetime
    is_public: bool

class QuestionCreate(BaseModel):
    qiuz_id: int
    question_text: str
    question_order: int
    time_limit: int
    points: int
    question_type: int
    image: int

class QuestionResponse(BaseModel):
    qiuz_id: int
    question_text: str
    question_order: int
    time_limit: int
    points: int
    question_type: int
    image: int

class QuestionUpdate(BaseModel):
    qiuz_id: int
    question_text: str
    question_order: int
    time_limit: int
    points: int
    question_type: int
    image: int

class AnswerAlternativeCreate(BaseModel):
    question_id: int
    answer_text: str
    is_correct: bool
    answer_icon: int
    answer_order: int

class AnswerAlternativeResponse(BaseModel):
    question_id: int
    answer_text: str
    is_correct: bool
    answer_icon: int
    answer_order: int

class AnswerAlternativeUpdate(BaseModel):
    question_id: int
    answer_text: str
    is_correct: bool
    answer_icon: int
    answer_order: int

class SessionCreate(BaseModel):
    session_name: str
    host_user_id: int
    active_quiz: int
    qr_code_id: int
    session_status: int
    started_at: datetime
    ended_at: datetime
    current_question_id: int
    session_code: int

class SessionResponse(BaseModel):
    session_name: str
    host_user_id: int
    active_quiz: int
    qr_code_id: int
    session_status: int
    started_at: datetime
    ended_at: datetime
    current_question_id: int
    session_code: int

class SessionUpdate(BaseModel):
    session_name: str
    host_user_id: int
    active_quiz: int
    qr_code_id: int
    session_status: int
    started_at: datetime
    ended_at: datetime
    current_question_id: int
    session_code: int