from datetime import date, datetime, time
from typing import Optional

from pydantic import BaseModel, EmailStr, Field

# Add Pydantic schemas here that you'll use in your routes / endpoints
# Pydantic schemas are used to validate data that you receive, or to make sure that whatever data
# you send back to the client follows a certain structure

class UserCreate(BaseModel):
    user_name: str = Field(min_lenght=3, max_length=50)
    email: EmailStr 
    password: str = Field(min_length=8, max_length=50)
    registration_date: datetime
    user_status: int 
    birth_date: date

class UserResponse(BaseModel):
    id: int
    user_name: str
    email: str
    registration_date: datetime
    user_status: int
    birth_date: date

class UserUpdate(BaseModel):
    user_name: str = Field(min_lenght=3, max_length=50)
    email: EmailStr 
    password: str = Field(min_lenght=8, max_length=50)
    registration_date: datetime
    user_status: int 
    birth_date: date

class UserPatch(BaseModel):
    user_name: str | None = Field(None, min_length=3, max_length=50)
    email: EmailStr | None = None
    password: str | None = Field(None, min_length=8, max_length=50)
    registration_date: datetime | None = None
    user_status: int | None = None
    birth_date: date | None = None

class QuizCreate(BaseModel):
    quiz_creator_id: int
    quiz_title: str = Field(min_length=3, max_length=255)
    quiz_description: str = Field(max_length=1000)
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
    quiz_title: str = Field(min_length=3, max_length=255)
    quiz_description: str = Field(max_length=1000)
    intro_image: int
    created_at: datetime
    updated_at: datetime
    is_public: bool

class QuizPatch(BaseModel):
    quiz_creator_id: int | None = None
    quiz_title: str | None = Field(None, min_length=3, max_length=255)
    quiz_description: str | None = Field(None, max_length=1000)
    intro_image: int | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
    is_public: bool | None = None

class QuestionCreate(BaseModel):
    quiz_id: int
    question_text: str = Field(min_length=3, max_length=500)
    question_order: int
    time_limit: int
    points: int
    question_type: int
    image: int

class QuestionResponse(BaseModel):
    quiz_id: int
    question_text: str
    question_order: int
    time_limit: int
    points: int
    question_type: int
    image: int

class QuestionUpdate(BaseModel):
    quiz_id: int
    question_text: str = Field(min_length=3, max_length=500)
    question_order: int
    time_limit: int
    points: int
    question_type: int
    image: int

class QuestionPatch(BaseModel):
    quiz_id: int | None = None
    question_text: str | None = Field(None, min_length=3, max_length=500)
    question_order: int | None = None
    time_limit: int | None = None
    points: int | None = None
    question_type: int | None = None
    image: int | None = None

class AnswerAlternativeCreate(BaseModel):
    question_id: int
    answer_text: str = Field(min_length=3, max_length=255)
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
    answer_text: str = Field(min_length=3, max_length=255)
    is_correct: bool
    answer_icon: int
    answer_order: int

class SessionCreate(BaseModel):
    session_name: str = Field(min_length=3, max_length=255)
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
    session_name: str = Field(min_length=3, max_length=255)
    host_user_id: int
    active_quiz: int
    qr_code_id: int
    session_status: int
    started_at: datetime
    ended_at: datetime
    current_question_id: int
    session_code: int

class SessionPlayerCreate(BaseModel):
    session_id: int
    display_name: str = Field(min_length=3, max_length=255)
    user_id: int | None = None
    joined_at: datetime
    player_points: int

class SessionPlayerResponse(BaseModel):
    session_id: int
    display_name: str
    user_id: int
    joined_at: datetime
    player_points: int

class SessionPlayerUpdate(BaseModel):
    session_id: int
    display_name: str = Field(min_length=3, max_length=255)
    user_id: int | None = None
    joined_at: datetime
    player_points: int

class PlayerAnswerCreate(BaseModel):
    player_id: int
    session_id: int
    question_id: int
    answer_id: int
    response_time: int
    points_earned: int
    is_correct: bool

class PlayerAnswerResponse(BaseModel):
    player_id: int
    session_id: int
    question_id: int
    answer_id: int
    response_time: int
    points_earned: int
    is_correct: bool

class PlayerAnswerUpdate(BaseModel):
    player_id: int
    session_id: int
    question_id: int
    answer_id: int
    response_time: int
    points_earned: int
    is_correct: bool

class ScoreboardCreate(BaseModel):
    session_id: int 
    player_id: int 
    total_score: int 
    correct_answers: bool 
    rank: int

class ScoreboardResponse(BaseModel):
    session_id: int 
    player_id: int 
    total_score: int 
    correct_answers: bool 
    rank: int

class ScoreboardUpdate(BaseModel):
    session_id: int 
    player_id: int 
    total_score: int 
    correct_answers: bool 
    rank: int