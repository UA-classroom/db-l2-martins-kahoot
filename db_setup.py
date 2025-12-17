import os

import psycopg2
from dotenv import load_dotenv

load_dotenv(override=True)

DATABASE_NAME = os.getenv("DATABASE_NAME")
PASSWORD = os.getenv("PASSWORD")


def get_connection():
    """
    Function that returns a single connection.
    """
    try:
        conn = psycopg2.connect(
            dbname=DATABASE_NAME,
            user="thomasdeming",  # change if needed
            password=PASSWORD,
            host="localhost",  # change if needed
            port="5432",  # change if needed
        )
        print("Successful connection")
        return conn
    except psycopg2.Error as e:
        print(f"Error: {e}")


def create_tables():
    """
    A function to create the necessary tables for the project.
    """
    
    con = get_connection()

    commands = (
    """ CREATE TABLE IF NOT EXISTS user_statuses (
            id SERIAL PRIMARY KEY,
            user_status VARCHAR NOT NULL
            )
    """,
    """
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        user_name VARCHAR(50) UNIQUE NOT NULL, 
        email VARCHAR(50) UNIQUE NOT NULL,
        password VARCHAR(50) UNIQUE NOT NULL,
        registration_date DATE NOT NULL DEFAULT CURRENT_DATE,
        user_status INT REFERENCES user_statuses(id) NOT NULL,
        birth_date DATE NOT NULL DEFAULT CURRENT_DATE
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS creators (
        id SERIAL PRIMARY KEY,
        name VARCHAR(50) UNIQUE NOT NULL,
        user_id INT NOT NULL REFERENCES users(id)
        )
    """,
    """ CREATE TABLE IF NOT EXISTS qr_codes (
            id SERIAL PRIMARY KEY,
            qr_link VARCHAR(50) NOT NULL
            )
    """,
    """ CREATE TABLE IF NOT EXISTS images (
            id SERIAL PRIMARY KEY,
            image_url VARCHAR(255) NOT NULL
            )
    """,
    """
    CREATE TABLE IF NOT EXISTS quizzes (
        id SERIAL PRIMARY KEY,
        quiz_creator_id INT NOT NULL REFERENCES creators(id),
        quiz_title VARCHAR(255) NOT NULL,
        quiz_description TEXT, 
        intro_image INT REFERENCES images(id),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP,
        is_public BOOLEAN
        )
    """,
    """
    CREATE TABLE IF NOT EXISTS hashtags (
        id SERIAL PRIMARY KEY,
        hashtag_name VARCHAR(255) NOT NULL
        )
    """,
    """
    CREATE TABLE IF NOT EXISTS quiz_hashtags (
        quiz_id INT NOT NULL REFERENCES quizzes(id),
        hashtag_id NOT NULL REFERENCES hashtags(id),
        PRIMARY KEY (quiz_id, hashtag_id)
        )
    """,
    """ CREATE TABLE question_types (
            id SERIAL PRIMARY KEY,
            question_type VARCHAR(255) UNIQUE NOT NULL
            )
    """,
    """
    CREATE TABLE IF NOT EXISTS questions (
        id SERIAL PRIMARY KEY,
        quiz_id INT NOT NULL REFERENCES quizzes(id),
        question_text VARCHAR(500) NOT NULL,
        question_order INT,
        time_limit INT NOT NULL,
        points INT DEFAULT 100,
        question_type INT NOT NULL REFERENCES question_types(id),
        image INT NOT NULL REFERENCES images(id)
        )
    """,
    """ CREATE TABLE IF NOT EXISTS answer_icons (
        id SERIAL PRIMARY KEY,
        icon_image INT NOT NULL REFERENCES images(id)
        )
    """,
    """
    CREATE TABLE IF NOT EXISTS answer_alternatives (
        id SERIAL PRIMARY KEY,
        question_id INT NOT NULL REFERENCES questions(id),
        answer_text VARCHAR(255) NOT NULL,
        correct_status BOOLEAN NOT NULL,
        answer_icon INT NOT NULL REFERENCES answer_icons(id),
        answer_order INT
        )
    """,
    """ CREATE TABLE IF NOT EXISTS session_statuses (
        id SERIAL PRIMARY KEY,
        status_type VARCHAR(255) UNIQUE NOT NULL
        )
    """,
    """
    CREATE TABLE IF NOT EXISTS sessions (
        id SERIAL PRIMARY KEY,
        session_name VARCHAR(255) NOT NULL,
        host_user_id INT NOT NULL REFERENCES users(id),
        active_quiz INT REFERENCES quizzes(id),
        qr_code_id INT REFERENCES qr_codes(id),
        session_status INT NOT NULL REFERENCES session_statuses(id),
        started_at TIMESTAMP,
        ended_at TIMESTAMP,
        current_question_id INT REFERENCES questions(id),
        session_code INT UNIQUE NOT NULL
        )
    """,
    """
    CREATE TABLE IF NOT EXISTS session_players (
        id SERIAL PRIMARY KEY,
        display_name VARCHAR(255) UNIQUE NOT NULL,
        session_id INT NOT NULL REFERENCES sessions(id),
        user_id INT REFERENCES users(id),
        joined_at TIMESTAMP,
        player_points INT DEFAULT 0
        )
    """,
    """
    CREATE TABLE IF NOT EXISTS session_scoreboards (
        id SERIAL PRIMARY KEY,
        session_id INT NOT NULL REFERENCES sessions(id),
        player_id INT NOT NULL REFERENCES session_players(id),
        total_score INT DEFAULT 0,
        correct_answers INT DEFAULT 0,
        rank INT
        )
    """,
    """
    CREATE TABLE IF NOT EXISTS player_answers (
        id SERIAL PRIMARY KEY,
        player_id INT NOT NULL REFERENCES session_players(id),
        session_id INT NOT NULL REFERENCES sessions(id),
        question_id INT NOT NULL REFERENCES questions(id),
        answer_id INT NOT NULL REFERENCES answer_alternatives(id),
        response_time INT NOT NULL,
        points_earned INT DEFAULT 0,
        is_correct BOOLEAN
        )
    """,
    """
    CREATE TABLE IF NOT EXISTS courses (
        id SERIAL PRIMARY KEY,
        creator_id INT NOT NULL REFERENCES creators(id),
        course_name VARCHAR(255) UNIQUE NOT NULL,
        description TEXT
        )
    """,
    """
    CREATE TABLE IF NOT EXISTS course_quizzes (
        course_id INT NOT NULL REFERENCES courses(id),
        quiz_id INT NOT NULL REFERENCES quizzes(id),
        PRIMARY KEY (course_id, quiz_id)
        )
    """,
    """
    CREATE TABLE IF NOT EXISTS course_hashtags (
        course_id INT NOT NULL REFERENCES courses(id),
        hashtag_id NOT NULL REFERENCES hashtags(id),
        PRIMARY KEY (course_id, hashtag_id)
        )
    """,
    """
    CREATE TABLE IF NOT EXISTS channels (
        id SERIAL PRIMARY KEY,
        creator_id INT NOT NULL REFERENCES creators(id),
        name VARCHAR(255) UNIQUE NOT NULL,
        description TEXT,
        )
    """,
    """
    CREATE TABLE IF NOT EXISTS channel_quizzes (
        channel_id INT NOT NULL REFERENCES channels(id),
        quiz_id INT NOT NULL REFERENCES quizzes(id),
        PRIMARY KEY (channel_id, quiz_id)
        )
    """,
    """
    CREATE TABLE IF NOT EXISTS channel_courses (
        channel_id INT NOT NULL REFERENCES channel(id),
        course_id INT NOT NULL REFERENCES courses(id),
        PRIMARY KEY (channel_id, course_id)
        )
    """,
    """ CREATE TABLE IF NOT EXISTS creator_profiles (
        id SERIAL PRIMARY KEY,
        creator_id INT NOT NULL REFERENCES creators(id),
        name VARCHAR(100) NOT NULL,
        description TEXT NOT NULL, 
        profile_picture INT REFERENCES images
        )
    """)

    try:
        with con.cursor() as cur:
            for command in commands:
                cur.execute(command)
            con.commit()
        print("Tables created successfully.")
    
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)
        con.rollback()

    finally:
        con.close()

if __name__ == "__main__":
    # Only reason to execute this file would be to create new tables, meaning it serves a migration file
    create_tables()
