import requests
from time import time

def get_time(func):
    def wrapper(*args, **kwargs):
        Ti = time()
        ret_val = func(*args, **kwargs)
        Tf = time()
        time_range = Tf - Ti
        return ret_val, time_range
    return wrapper

@get_time
def read_api(title):

    if not isinstance(title, str):
        raise TypeError('The title parameter must be a string, nothing else')
    
    URL = 'http://www.omdbapi.com/'
    key = '118afbf0'
    
    response = requests.get(URL, params = {'apikey': key, 't': title})
    if response.status_code == 200:
        data = response.json()
        if data['Response'] == 'False':
            if data['Error'] == 'Movie not found!':
                print(f"ERROR >> Movie '{title}' is not registered on omdbapi.com, the source of this program!\nThis movie will be ignored.")
                return None
        else:
            organized_data = {
                            'IMDB': data['imdbID'],
                            'Title': data['Title'],
                            'Year': data['Year'],
                            'Release data': data['Released'],
                            'Time': data['Runtime'],
                            'Genre': data['Genre'],
                            'Director': data['Director'],
                            'Actors': data['Actors'],
                            'Writer': data['Writer'],
                            'Language': data['Language'],
                            'Country': data['Country'],
                            'imdbRating': data['imdbRating'],
                            'imdbVotes': data['imdbVotes']
                                }
            return organized_data

if __name__ == '__main__':
    print(read_api('Chainsaw Massacre'))