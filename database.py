import pymysql
import config

def get_db():
    return pymysql.connect(host=config.DB_HOST, user=config.DB_USER, password=config.DB_PASS, database=config.DB_NAME, cursorclass=pymysql.cursors.DictCursor)

def get_all_users():
    conn = get_db()
    users = []
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM users ORDER BY id DESC")
            users = cursor.fetchall()
    finally:
        conn.close()
    return users

def add_user(username, password):
    conn = get_db()
    try:
        with conn.cursor() as cursor:
            cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
        conn.commit()
    finally:
        conn.close()

def get_username(user_id):
    conn = get_db()
    username = None
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT username FROM users WHERE id = %s", (user_id,))
            result = cursor.fetchone()
            if result: username = result['username']
    finally:
        conn.close()
    return username

def delete_user(user_id):
    conn = get_db()
    try:
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
        conn.commit()
    finally:
        conn.close()