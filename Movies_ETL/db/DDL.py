import mysql.connector

def define_conn(username, pw):
    db = mysql.connector.connect(
        host = 'localhost',
        username = username,
        password = pw,
        database = 'etl_movies'
    )
    return db

def rm_db(username, pw):
    db = mysql.connector.connect(
        host = 'localhost',
        username = username,
        password = pw)
    cursor = db.cursor()
    cursor.execute('DROP DATABASE if exists etl_movies')
    cursor.close()
    db.close()

def create_everything(username, pw):
    db = mysql.connector.connect(
        host = 'localhost',
        username = username,
        password = pw
    )
    cursor = db.cursor()
    cursor.execute('CREATE DATABASE if not exists etl_movies')
    cursor.close()
    db.close()
    db = define_conn(username, pw)
    cursor = db.cursor()
    cursor.execute("""
                    CREATE TABLE if not exists Movies (
                    imdbID VARCHAR(20) PRIMARY KEY,
                    Title VARCHAR(255) NOT NULL,
                    Year VARCHAR(4) NOT NULL,
                    Genre VARCHAR(255) NOT NULL,
                    Duration INT NOT NULL,
                    CONSTRAINT cond CHECK ( Duration >= 0 )
                   )""")
    cursor.close()
    cursor = db.cursor()
    cursor.execute("""
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
    cursor.close()
    db.close()