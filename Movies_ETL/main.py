import pandas as pd
import API
import utils
import db.DDL as ddl
import db.DML as dml
import db.DQL as dql
import time

class Solution:

    def __init__(self, MySQL_username, MySQL_password):
        self.username = MySQL_username
        self.password = MySQL_password
        self.namesDF = pd.read_csv('data_source/data.csv')
        self.namesDF.dropna(subset = ['Title'], inplace = True)
        self.from_api_to_DF()
        self.export_DF_to_DB()
        self.execute_queries_and_export_to_csv()
    
    def from_api_to_DF(self):
        self.dataset_list = list()
        count = 1
        t_start = time.time()
        for ind in self.namesDF.index:
            print(f'{count} - Downloading data about the movie >> {self.namesDF.loc[ind, 'Title']}')
            data, range_of_time = API.read_api(self.namesDF.loc[ind, 'Title'])
            if data is not None:
                self.dataset_list.append(data)
                print(f"{count} - '{self.namesDF.loc[ind, 'Title']}' was downloaded succesfully (Download has taken {range_of_time:.2f} sec)\n...")
                count += 1
        t_end = time.time()
        print(f'Time to download data from internet >> {t_end - t_start:.2f} seconds')
        self.Data = {
            'imdbID': [record['IMDB'] for record in self.dataset_list],
            'Title': [record['Title'] for record in self.dataset_list],
            'Year': [str(record['Year']) for record in self.dataset_list],
            'Genre': [record['Genre'] for record in self.dataset_list],
            'Duration': [str(record['Time']) for record in self.dataset_list],
            'imdbID': [record['IMDB'] for record in self.dataset_list],
            'Release_date': [utils.cleanDate(record['Release data']) for record in self.dataset_list],
            'Director': [record['Director'] for record in self.dataset_list],
            'Actors': [record['Actors'] for record in self.dataset_list],
            'Writer': [record['Writer'] for record in self.dataset_list],
            'Language': [record['Language'] for record in self.dataset_list],
            'Country': [record['Country'] for record in self.dataset_list],
            'Score': [float(record['imdbRating']) for record in self.dataset_list],
            'Votes': [utils.cleanNumber(record['imdbVotes']) for record in self.dataset_list]
        }
        self.DataFrame = pd.DataFrame(self.Data)
        self.DataFrame.dropna(inplace = True)
        self.MoviesDF = self.DataFrame.loc[::1, ['imdbID', 'Title', 'Year', 'Genre', 'Duration']]
        self.DetailsDF = self.DataFrame.loc[::1, ['imdbID', 'Release_date', 'Director', 'Actors', 'Writer', 'Language', 'Country', 'Score', 'Votes']]
        for ind in self.MoviesDF.index:
            self.MoviesDF.loc[ind, 'Duration'] = self.MoviesDF.loc[ind, 'Duration'].split()[0]
        self.MoviesDF['Duration'] = self.MoviesDF['Duration'].astype(int)
        for ind in self.MoviesDF.index:
            if self.MoviesDF.loc[ind, 'Duration'] < 0:
                self.MoviesDF.loc[ind, 'Duration'] = 0
        for ind in self.DetailsDF.index:
            if self.DetailsDF.loc[ind, 'Votes'] < 0:
                self.DetailsDF.loc[ind, 'Votes'] = 0
    
    def export_DF_to_DB(self):
        ddl.rm_db(self.username, self.password)
        ddl.create_everything(self.username, self.password)
        self.db = ddl.define_conn(self.username, self.password)
        for ind in self.MoviesDF.index:
            dml.load_Movies(self.db, idbmID = self.MoviesDF.loc[ind, 'imdbID'],
                                Title = self.MoviesDF.loc[ind, 'Title'],
                                Year = self.MoviesDF.loc[ind, 'Year'],
                                Genre = self.MoviesDF.loc[ind, 'Genre'],
                                Duration= int(self.MoviesDF.loc[ind, 'Duration']))
        for ind in self.DetailsDF.index:
            dml.load_Details(self.db, idbmID = self.DetailsDF.loc[ind, 'imdbID'],
                                Release_date = self.DetailsDF.loc[ind, 'Release_date'],
                                Director = self.DetailsDF.loc[ind, 'Director'],
                                Actors = self.DetailsDF.loc[ind, 'Actors'],
                                Writer = self.DetailsDF.loc[ind, 'Writer'],
                                Language = self.DetailsDF.loc[ind, 'Language'],
                                Country = self.DetailsDF.loc[ind, 'Country'],
                                Score = self.DetailsDF.loc[ind, 'Score'],
                                Votes = int(self.DetailsDF.loc[ind, 'Votes']))

    def send_from_DB_to_CSV_per_unit(self, *, csv_path, dict_data):
        self.DF = pd.DataFrame(dict_data)
        self.DF.to_csv(csv_path, index = False)

    def execute_queries_and_export_to_csv(self):
        self.send_from_DB_to_CSV_per_unit(csv_path='CSV_file_will_be_here/genre_data.csv',
                                          dict_data = dql.get_genre_data(self.db))
        self.send_from_DB_to_CSV_per_unit(csv_path='CSV_file_will_be_here/top10_scores.csv',
                                        dict_data = dql.get_top10_scores(self.db))
        self.send_from_DB_to_CSV_per_unit(csv_path = 'CSV_file_will_be_here/year_data.csv',
                                        dict_data = dql.get_year_data(self.db))
        self.send_from_DB_to_CSV_per_unit(csv_path = 'CSV_file_will_be_here/month_data.csv',
                                        dict_data = dql.get_month_data(self.db))
        self.send_from_DB_to_CSV_per_unit(csv_path = 'CSV_file_will_be_here/everything.csv',
                                        dict_data = dql.get_everything(self.db))
        print('\nProccess finished successfully\n Link to the API >> https://www.omdbapi.com/')

if __name__ == '__main__':
    username = input('MySQL Username >>  ')
    password = input('MySQL Password >>  ')
    try:
        solution = Solution(username, password)
    except Exception as e:
        print(f"ATTENTION: Proccess wasn't finished do to an error:\n{e}")