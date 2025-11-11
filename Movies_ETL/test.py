import pandas as pd

csv = pd.read_csv('data_source/data.csv')
csv.drop(columns = ['Genre','Description','Director','Actors','Year','Runtime (Minutes)','Rating','Votes','Revenue (Millions)','Metascore'], inplace = True)
csv.to_csv('data_source/new_data.csv', index = False)

