from typing import Any

def load_Movies(db: Any, /, *, idbmID: str, Title: str, Year: str, Genre: str, Duration: int) -> None:

    cursor: Any = db.cursor()
    cursor.execute("INSERT INTO Movies VALUES (%s, %s, %s, %s, %s)",
                    (idbmID, Title, Year, Genre, Duration))
    db.commit()
    cursor.close()

def load_Details(db: Any, /, *, idbmID: str, Release_date: str, Director: str, Actors: str, Writer: str,
                Language: str, Country: str, Score: float, Votes: int) -> None:

    cursor: Any = db.cursor()
    cursor.execute("INSERT INTO Details VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                (idbmID, Release_date, Director, Actors, Writer, Language, Country, Score, Votes))
    db.commit()
    cursor.close()