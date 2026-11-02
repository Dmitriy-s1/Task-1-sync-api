import email

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
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS posts 
                (
                id INTEGER NOT NULL PRIMARY KEY ,
                user_id INTEGER NOT NULL,
                FOREIGN KEY(user_id) REFERENCES users(id),
                title TEXT NOT NULL,
                body TEXT NOT NULL
                )
            """)


def save_data_to_db(users:list, posts:list):
    with (closing(sqlite3.connect("app.db")) as connection):
        with connection:
            cursor = connection.cursor()

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











if __name__ == "__main__":
    test1 = make_request(USERS_URL)
    test2 = make_request(POSTS_URL)
    print(len(test1))
    print(test1[0]['name'])
    print(len(test2))