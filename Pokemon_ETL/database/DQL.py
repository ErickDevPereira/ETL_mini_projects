#Mode as 0 means bellow average, any other value means above the average. Type = 2 means Type2 data, else, we have Type1 data.
def TypesRelAverage(db , /, *, mode, type = 2):
    cursor = db.cursor()
    cursor.execute(f"""
                    SELECT {'t.Type2' if type == 2 else 't.Type1'} as Pokemon_type,
                    CAST(FORMAT(AVG(m.Height), 2) AS DECIMAL(5, 2)) as Average_height
                    FROM Names as n INNER JOIN Types as t ON t.No = n.No
                    INNER JOIN Measures AS m ON m.No = n.No
                    GROUP BY {'t.Type2' if type == 2 else 't.Type1'}
                    HAVING AVG(m.Height) {'<' if mode == 0 else '>'} (SELECT AVG(Height) FROM measures)
                    ORDER BY Average_height
                    """)
    data = cursor.fetchall()
    dataset = {f'{'Type2' if type == 2 else 'Type1'}': [record[0] for record in data],
               'Average_height': [float(record[1]) for record in data]}
    cursor.close()
    return dataset

#Mode as 0 means bellow average, any other value means above the average. Type = 2 means Type2 data, else, we have Type1 data.
def TypesRelWeight(db, /, *, mode, type = 2):
    cursor = db.cursor()
    cursor.execute(
                f"""
                    SELECT {'t.Type2' if type == 2 else 't.Type1'} as Pokemon_type,
                    CAST(FORMAT(AVG(m.Weight), 2) AS DECIMAL(5, 2)) as Average_weight
                    FROM Names as n INNER JOIN Types as t ON t.No = n.No
                    INNER JOIN Measures AS m ON m.No = n.No
                    GROUP BY {'t.Type2' if type == 2 else 't.Type1'}
                    HAVING AVG(m.Weight) {'<' if mode == 0 else '>'} (SELECT AVG(Weight) FROM measures)
                    ORDER BY Average_weight;
                """)
    data = cursor.fetchall()
    dataset = {f'{'Type2' if type == 2 else 'Type1'}': [record[0] for record in data],
               'Average_weight': [float(record[1]) for record in data]}
    cursor.close()
    return dataset

def GetIMC(db):
    cursor = db.cursor()
    cursor.execute("""
                SELECT N.Name as Name,
                CAST(FORMAT(M.weight / (M.height * M.height), 2) AS DECIMAL(5, 2)) as IMC,
                M.Legendary as Legendary
                FROM Names as N INNER JOIN Measures as M
                ON M.No = N.No
                ORDER BY IMC ASC
                """)
    data = cursor.fetchall()
    dataset = {
            'Name': [record[0] for record in data],
            'IMC': [float(record[1]) for record in data],
            'Legendary': [record[2] for record in data]
            }
    cursor.close()
    return dataset

def GetLegendary(db):
    cursor = db.cursor()
    cursor.execute("""
                SELECT COUNT(*) as Quantity,
                FORMAT(AVG(M.Height), 2) as avg_height,
                FORMAT(AVG(M.Weight), 2) as avg_weight,
                M.Legendary as Legendary
                FROM Names as N INNER JOIN Types as T
                ON N.No = T.No INNER JOIN Measures as M
                ON M.No = N.No
                GROUP BY M.Legendary
                """)
    data = cursor.fetchall()
    cursor.close()
    dataset = {
        'Quantity': [record[0] for record in data],
        'avg_height': [float(record[1]) for record in data],
        'avg_weight': [float(record[2]) for record in data],
        'Legendary': [record[3] for record in data]
    }
    return dataset