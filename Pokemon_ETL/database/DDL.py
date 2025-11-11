import mysql.connector

def create_conn(username, pw):
    db = mysql.connector.connect(
        host = 'localhost',
        user = username,
        password = pw,
        database = 'ETL_db_Pokemon')
    return db

def create(username, pw):
    #Creating the database
    db = mysql.connector.connect(
        host = 'localhost',
        username = username,
        password = pw
                        )
    cursor = db.cursor()
    cursor.execute('CREATE DATABASE if not exists ETL_db_Pokemon')
    cursor.close()
    #Creating the tables
    cursor = db.cursor()
    db.close()
    db = create_conn(username, pw)
    cursor = db.cursor()
    cursor.execute("""
                CREATE TABLE if not exists Names (
                No SMALLINT UNSIGNED primary key,
                Name VARCHAR(50) NOT NULL
                )""")
    cursor.close()
    cursor = db.cursor()
    cursor.execute("""CREATE TABLE if not exists Types (
                No SMALLINT UNSIGNED PRIMARY KEY,
                Type1 VARCHAR(50) NOT NULL,
                Type2 VARCHAR(50) NOT NULL,
                FOREIGN KEY (No) REFERENCES Names (No))""")
    cursor.close()
    cursor = db.cursor()
    cursor.execute("""
                CREATE TABLE if not exists Measures (
                No SMALLINT UNSIGNED primary key,
                Height DECIMAL(10, 2) NOT NULL,
                Weight DECIMAL(10, 2) NOT NULL,
                Legendary VARCHAR(3) NOT NULL,
                CONSTRAINT condition_check CHECK (Weight > 0 AND Height > 0),
                FOREIGN KEY (No) REFERENCES Names (No)
                    )""")
    cursor.close()
    return db

def delete(username, pw):
    db = mysql.connector.connect(
        host = 'localhost',
        username = username,
        password = pw
    )
    cursor = db.cursor()
    cursor.execute('DROP DATABASE if exists etl_db_pokemon')
    cursor.close()
    db.close()