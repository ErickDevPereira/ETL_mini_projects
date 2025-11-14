import mysql.connector
from typing import Any

def define_conn(username: str, pw: str) -> Any:
    db: Any = mysql.connector.connect(
        host = 'localhost',
        username = username,
        password = pw,
        database = 'etl_movies'
    )
    return db

def rm_db(username: str, pw: str) -> None:
    db: Any = mysql.connector.connect(
        host = 'localhost',
        username = username,
        password = pw)
    cursor: Any = db.cursor()
    cursor.execute('DROP DATABASE if exists etl_movies')
    cursor.close()
    db.close()

def create_everything(username: str, pw: str) -> None:
    db: Any = mysql.connector.connect(
        host = 'localhost',
        username = username,
        password = pw
    )
    cursor: Any = db.cursor()
    cursor.execute('CREATE DATABASE if not exists etl_movies')
    cursor.close()
    db.close()
    db2: Any = define_conn(username, pw)
    cursor2: Any = db2.cursor()
    cursor2.execute("""
                    CREATE TABLE if not exists Movies (
                    imdbID VARCHAR(20) PRIMARY KEY,
                    Title VARCHAR(255) NOT NULL,
                    Year VARCHAR(4) NOT NULL,
                    Genre VARCHAR(255) NOT NULL,
                    Duration INT NOT NULL,
                    CONSTRAINT cond CHECK ( Duration >= 0 )
                   )""")
    cursor2.close()
    cursor3: Any = db2.cursor()
    cursor3.execute("""
                    CREATE TABLE if not exists Details (
                    imdbID VARCHAR(20) NOT NULL,
                    Release_date DATE NOT NULL,
                    Director VARCHAR(255) NOT NULL,
                    Actors VARCHAR(255) NOT NULL,
                    Writer VARCHAR(255) NOT NULL,
                    Language VARCHAR(255) NOT NULL,
                    Country VARCHAR(255) NOT NULL,
                    Score DECIMAL(5, 2) NOT NULL,
                    Votes INT UNSIGNED NOT NULL,
                    FOREIGN KEY (imdbID) REFERENCES Movies (imdbID)
                    )""")
    cursor3.close()
    db2.close()