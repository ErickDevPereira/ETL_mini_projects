def load_Movies(db, /, *, idbmID, Title, Year, Genre, Duration):

    cursor = db.cursor()
    cursor.execute("INSERT INTO Movies VALUES (%s, %s, %s, %s, %s)",
                    (idbmID, Title, Year, Genre, Duration))
    db.commit()
    cursor.close()

def load_Details(db, /, *, idbmID, Release_date, Director, Actors, Writer, Language, Country, Score, Votes):

    cursor = db.cursor()
    cursor.execute("INSERT INTO Details VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                (idbmID, Release_date, Director, Actors, Writer, Language, Country, Score, Votes))
    db.commit()
    cursor.close()