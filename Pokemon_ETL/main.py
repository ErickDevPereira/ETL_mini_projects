import pandas as pd
import database.DDL as ddl
import database.DML as dml
import database.DQL as dql
import mysql.connector

class Solution:

    def __init__(self, username, password):
        self.username = username
        self.password = password
        ddl.delete(self.username, self.password)
        self.origin_df = pd.read_csv('database/data.csv')
        print(self.clean_data())
        self.split_dataset()
        self.first_export_csv()
        self.csv_to_db()
        print(self.transform_and_load())
    
    def __str__(self):
        return 'Object from class Solution, which reads, clean, proccess and export CSV data.'

    def clean_data(self):
        self.origin_df.dropna(inplace = True) #Dropping records with NaN or None
        self.origin_df.drop_duplicates(inplace = True) #Taking out duplications
        self.origin_df['Legendary'] = self.origin_df['Legendary'].astype(str) #Converting Legendary to string type
        for ind in self.origin_df.index:
            if self.origin_df.loc[ind, 'Height'] <= 0 or self.origin_df.loc[ind, 'Weight'] <= 0:
                self.origin_df.drop(ind, inplace = True) #Taking out records with negative weight/height
            if self.origin_df.loc[ind, 'Legendary'] == '0':
                self.origin_df.loc[ind, 'Legendary'] = 'No' #Setting No to zeros
            else:
                self.origin_df.loc[ind, 'Legendary'] = 'Yes' #Setting Yes to ones
        return 'Data cleaned successfully'
    
    def split_dataset(self):
        self.types_df = self.origin_df.loc[::1, ['No', 'Type1', 'Type2']] #Types DataFrame
        self.names_df = self.origin_df.loc[::1, ['No', 'Name']] #Names DataFrame
        self.measures_df = self.origin_df.loc[::1, ['No', 'Height', 'Weight', 'Legendary']] #Measures DataFrame

    def first_export_csv(self):
        self.origin_df.to_csv('New_data/full_data.csv', index = False) #Exporting the cleaned dataset. (COMPLETE)
        self.types_df.to_csv('database/intermediate_files/types.csv', index = False) #Exporting types DataFrame as csv4
        self.names_df.to_csv('database/intermediate_files/names.csv', index = False) #Exporting names DataFrame as csv
        self.measures_df.to_csv('database/intermediate_files/measures.csv', index = False) #Exporting measures DataFrame as csv
    
    def csv_to_db(self):
        db = ddl.create(self.username, self.password)
        self.types = pd.read_csv('database/intermediate_files/types.csv')
        self.names = pd.read_csv('database/intermediate_files/names.csv')
        self.measures = pd.read_csv('database/intermediate_files/measures.csv')
        for ind in self.names.index:
            dml.loadDBnames(db,
                            No = int(self.names.loc[ind, 'No']),
                            Name = str(self.names.loc[ind, 'Name']))
        for ind in self.types.index:
            dml.loadDBtypes(db,
                            No = int(self.types.loc[ind, 'No']),
                            type1 = str(self.types.loc[ind, 'Type1']),
                            type2 = str(self.types.loc[ind, 'Type2']))
        for ind in self.types.index:
            dml.loadDBmeasures(db,
                               No = int(self.measures.loc[ind, 'No']),
                               legendary = str(self.measures.loc[ind, 'Legendary']),
                               height = float(self.measures.loc[ind, 'Height']),
                               weight = float(self.measures.loc[ind, 'Weight']))
        db.close()
    
    def transform_and_load(self):
        db = ddl.create_conn(self.username, self.password)
        self.H_Type2_aboveDF = pd.DataFrame(dql.TypesRelAverage(db, mode = 1, type = 2))
        self.H_Type2_bellowDF = pd.DataFrame(dql.TypesRelAverage(db, mode = 0, type = 2))
        self.H_Type1_aboveDF = pd.DataFrame(dql.TypesRelAverage(db, mode = 1, type = 1))
        self.H_Type1_bellowDF = pd.DataFrame(dql.TypesRelAverage(db, mode = 0, type = 1))
        self.W_Type2_aboveDF = pd.DataFrame(dql.TypesRelWeight(db, mode = 1, type = 2))
        self.W_Type2_bellowDF = pd.DataFrame(dql.TypesRelWeight(db, mode = 0, type = 2))
        self.W_Type1_aboveDF = pd.DataFrame(dql.TypesRelWeight(db, mode = 1, type = 1))
        self.W_Type1_bellowDF = pd.DataFrame(dql.TypesRelWeight(db, mode = 0, type = 1))
        self.IMC = pd.DataFrame(dql.GetIMC(db))
        self.Legendary = pd.DataFrame(dql.GetLegendary(db))
        db.close()
        self.H_Type2_aboveDF.to_csv('New_data/type2_above_avg_height.csv', index = False)
        self.H_Type2_bellowDF.to_csv('New_data/type2_bellow_avg_height.csv', index = False)
        self.H_Type1_aboveDF.to_csv('New_data/type1_above_avg_height.csv', index = False)
        self.H_Type1_bellowDF.to_csv('New_data/type1_bellow_avg_height.csv', index = False)
        self.W_Type2_aboveDF.to_csv('New_data/type2_above_avg_weight.csv', index = False)
        self.W_Type2_bellowDF.to_csv('New_data/type2_bellow_avg_weight.csv', index = False)
        self.W_Type1_aboveDF.to_csv('New_data/type1_above_avg_weight.csv', index = False)
        self.W_Type1_bellowDF.to_csv('New_data/type1_bellow_avg_weight.csv', index = False)
        self.IMC.to_csv('New_data/Pokemon_IMC.csv', index = False)
        self.Legendary.to_csv('New_data/Legendary.csv', index = False)
        return 'Proccess Finished Successfully'

        
if __name__ == '__main__':
    try:
        username = input("MySQL Username >>  ")
        password = input("MySQL Password >>  ")
        solution = Solution(username, password)
    except mysql.connector.errors.ProgrammingError as err:
        print(err)