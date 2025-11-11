def loadDBnames(db, /, *, No, Name):
    cursor = db.cursor()
    cursor.execute('INSERT INTO Names (No, Name) VALUES (%s, %s)', (No, Name))
    db.commit()
    cursor.close()
    
def loadDBtypes(db, /, *, No, type1, type2):
    cursor = db.cursor()
    cursor.execute("""
                    INSERT INTO Types (No, Type1, Type2)
                    VALUES (%s, %s, %s)
                    """, (No, type1, type2))
    db.commit()
    cursor.close()

def loadDBmeasures(db, /, *, No, legendary, height, weight):
    cursor = db.cursor()
    cursor.execute("""INSERT INTO Measures
                   VALUES (%s, %s, %s, %s)""",
                   (No, height, weight, legendary))
    db.commit()
    cursor.close()