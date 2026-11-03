import requests
import sqlite3
from contextlib import closing

USERS_URL = "https://jsonplaceholder.typicode.com/users"
POSTS_URL = "https://jsonplaceholder.typicode.com/posts"


def make_request(url:str) -> list :
    response = requests.get(url,timeout=5)
    response.raise_for_status()
    return response.json()


def init_database() -> None:
    with closing(sqlite3.connect("app.db")) as connection:
        with connection:
            cursor = connection.cursor()
            cursor.execute("PRAGMA foreign_keys = ON")

            cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS users 
                (
                id INTEGER NOT NULL PRIMARY KEY ,
                name TEXT NOT NULL,
                username TEXT NOT NULL,
                email TEXT NOT NULL
                )
            """)
            cursor.execute("""CREATE TABLE IF NOT EXISTS posts 
                (
                id INTEGER NOT NULL PRIMARY KEY ,
                userId INTEGER NOT NULL,
                title TEXT NOT NULL,
                body TEXT NOT NULL,
                FOREIGN KEY(userId) REFERENCES users(id)
                )
            """)


def save_data_to_db(users:list, posts:list):
    with (closing(sqlite3.connect("app.db")) as connection):
        with connection:
            cursor = connection.cursor()
            cursor.execute("PRAGMA foreign_keys = ON")

            cursor.executemany("""
            INSERT OR IGNORE INTO users(id, name, username, email) 
            VALUES (?,?,?,?)
                """,
            ((user['id'], user["name"], user["username"], user["email"]) for user in users)
            )

            cursor.executemany("""
            INSERT OR IGNORE INTO posts(id, userId, title, body) 
            VALUES (?,?,?,?)
                """,
            ((post["id"], post["userId"], post["title"], post["body"]) for post in posts)
            )


def check_database() -> None:
    with closing(sqlite3.connect("app.db")) as connection:
        with connection:
            cursor = connection.cursor()
            u = cursor.execute("""SELECT COUNT(*) FROM users""").fetchone()[0]
            p = cursor.execute("""SELECT COUNT(*) FROM posts""").fetchone()[0]
            print(f"количество записей в таблице users: {u}")
            print(f"количество записей в таблице posts: {p}")




if __name__ == "__main__":
    init_database()
    users = make_request(USERS_URL)
    posts = make_request(POSTS_URL)
    save_data_to_db(users, posts)
    check_database()