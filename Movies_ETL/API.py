import requests
from time import time
from typing import Callable, Dict, Any

def get_time(func: Callable[[str], Dict[str, str] | None]) -> Dict[str, str] | float  | None:
    def wrapper(*args, **kwargs) -> Dict[str, str] | float  | None:
        Ti: float = time()
        ret_val: Dict[str, str] | None = func(*args, **kwargs)
        Tf: float = time()
        time_range: float = Tf - Ti
        return ret_val, time_range
    return wrapper

@get_time
def read_api(title: str) -> Dict[str, str] | None:

    if not isinstance(title, str):
        raise TypeError('The title parameter must be a string, nothing else')
    
    URL: str = 'http://www.omdbapi.com/'
    key: str = '118afbf0'
    
    response: Any = requests.get(URL, params = {'apikey': key, 't': title})
    if response.status_code == 200:
        data: Any = response.json()
        if data['Response'] == 'False':
            if data['Error'] == 'Movie not found!':
                print(f"ERROR >> Movie '{title}' is not registered on omdbapi.com, the source of this program!\nThis movie will be ignored.")
                return None
        else:
            organized_data: Dict[str, str] = {
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