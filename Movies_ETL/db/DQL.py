def get_genre_data(db):
    cursor = db.cursor()
    cursor.execute("""
                    SELECT 
                        M.Genre as Genre, COUNT(*) as Quantity, FORMAT(AVG(D.score), 2) as Score
                    FROM
                        Movies as M INNER JOIN Details as D
                        ON M.imdbID = D.imdbID
                    GROUP BY
                        M.Genre
                    ORDER BY 
                        COUNT(*) DESC
                    """)
    data = cursor.fetchall()
    organized_dataset = {'Genre': [record[0] for record in data],
                        'Quantity': [record[1] for record in data],
                        'Score': [float(record[2]) for record in data]}
    cursor.close()
    return organized_dataset

def get_top10_scores(db):
    cursor = db.cursor()
    cursor.execute("""
                    SELECT
                        M.imdbID as IMDB, M.Title as Title, D.Score as Score
                    FROM
                        Movies as M INNER JOIN Details as D
                        ON M.imdbID = D.imdbID
                    ORDER BY
                        D.Score DESC
                    LIMIT 10
                    """)
    data = cursor.fetchall()
    dataset = {'IMDB': [record[0] for record in data],
               'Title': [record[1] for record in data],
               'Score': [record[2] for record in data]}
    cursor.close()
    return dataset

def get_year_data(db):
    cursor = db.cursor()
    cursor.execute("""
                    SELECT
                        COUNT(*) as Quantity, M.Year as Year, CAST(FORMAT(AVG(Score), 2) AS DECIMAL(5, 2)) as avg_score
                    FROM
                        Movies as M INNER JOIN Details as D
                        ON M.imdbID = D.imdbID
                    GROUP BY
                        M.Year
                    ORDER BY Quantity DESC
                    """)
    data = cursor.fetchall()
    dataset = {
        'Quantity': [record[0] for record in data],
        'Year': [record[1] for record in data],
        'avg_score': [record[2] for record in data]
    }
    return dataset

def get_month_data(db):
    cursor = db.cursor()
    cursor.execute('''
                    SELECT
                        CASE
                            WHEN MONTH(D.release_date) = '1' THEN 'January'
                            WHEN MONTH(D.release_date) = '2' THEN 'February'
                            WHEN MONTH(D.release_date) = '3' THEN 'May'
                            WHEN MONTH(D.release_date) = '4' THEN 'April'
                            WHEN MONTH(D.release_date) = '5' THEN 'March'
                            WHEN MONTH(D.release_date) = '6' THEN 'June'
                            WHEN MONTH(D.release_date) = '7' THEN 'July'
                            WHEN MONTH(D.release_date) = '8' THEN 'August'
                            WHEN MONTH(D.release_date) = '9' THEN 'September'
                            WHEN MONTH(D.release_date) = '10' THEN 'October'
                            WHEN MONTH(D.release_date) = '11' THEN 'November'
                            WHEN MONTH(D.release_date) = '12' THEN 'December'
                        END as Month,
                        COUNT(*) as Quantity,
                        CAST(FORMAT(AVG(D.Score), 2) as DECIMAL(5, 2)) as avg_score
                    FROM
                        Movies as M INNER JOIN Details as D
                        ON D.imdbID = M.imdbID
                    GROUP BY
                        Month
                    ORDER BY
                        AVG(D.Score) DESC, Quantity DESC
                ''')
    data = cursor.fetchall()
    dataset = {
            'Month': [record[0] for record in data],
            'Quantity': [record[1] for record in data],
            'avg_score': [record[2] for record in data]
    }
    return dataset

def get_everything(db):
    cursor = db.cursor()
    cursor.execute("""
                SELECT
                    M.imdbID as IMDB,
                    M.Title as Title,
                    D.Release_date as Release_date,
                    M.Duration as Duration,
                    M.Genre as Genre,
                    FORMAT(D.Score, 2) as Score,
                    D.Director as Director,
                    D.Writer as Writer,
                    D.Language as Language,
                    D.Country as Country,
                    D.Votes as Votes
                FROM
                    Movies as M INNER JOIN Details as D
                    ON M.imdbID = D.imdbID
                """)
    data = cursor.fetchall()
    dataset = {
        'IMDB': [record[0] for record in data],
        'Title': [record[1] for record in data],
        'Release_date': [record[2] for record in data],
        'Duration': [str(record[3]) + ' min' for record in data],
        'Genre': [record[4] for record in data],
        'Score': [record[5] for record in data],
        'Director': [record[6] for record in data],
        'Writer': [record[7] for record in data],
        'Language': [record[8] for record in data],
        'Country': [record[9] for record in data],
        'Votes': [record[10] for record in data]
    }
    cursor.close()
    return dataset