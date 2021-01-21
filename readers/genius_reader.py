import pandas as pd
import lyricsgenius as genius
from readers.base_reader import DataFrameManager


class GeniusReader(DataFrameManager):

    def __init__(self, client_token, artist_name):
        #  self.excluded_terms = ["(Remix)", "(Live)"]
        #  self.remove_section_headers = True
        self.__client_token = client_token
        self.artist_name = artist_name
        self.artist_dataframe = pd.DataFrame()
        self.wanted_columns = ['title', 'album', 'year', 'lyrics', 'image']
        self.unwanted_columns = ['image']
        self.api = self._api_setup()
        DataFrameManager.__init__(self, artist_name=self.artist_name, file_lastname='lyrics')

    def _api_setup(self):
        try:
            api = genius.Genius(self.__client_token)
        except Exception as e:
            print(f'Error in your client token:{self.__client_token} exception {str(e)}')
        return api

    def artist_reader(self):
        try:
            artist = self.api.search_artist(self.artist_name)
        except Exception as e:
            print(f'Error with your artist:{self.artist_name} exception {str(e)}')

        return artist

    def read_artist_songs(self):
        artist = self.artist_reader()
        return [song.to_dict() for song in artist.songs]

    def build_dataframe(self):
        self.artist_dataframe = pd.DataFrame(self.read_artist_songs())

        for column in self.artist_dataframe.columns:
            if column in self.wanted_columns:
                pass
            else:
                print(f'Warning column {column} has changed, check the lyricsgenius documentation')

        for unwanted_field in self.unwanted_columns:
            if unwanted_field in self.artist_dataframe.columns:
                del self.artist_dataframe[unwanted_field]
            else:
                print(f'Column {unwanted_field} does not exist')

        return self.artist_dataframe

    def __call__(self, *args, **kwargs):
        self.artist_dataframe = self.get_data_frame()

        return self.artist_dataframe


if __name__ == "__main__":

    CLIENT_TOKEN = 'c1RFgHXaEPOu77nhaIi85DhEqzL7yN4ryIx6Mid2_YZ7r-8VnV6OjDL_dvXGoMHH'
    # https://genius.com/artists/Draco-rosa
    ARTIST = 'Draco-rosa'
    artist_data = GeniusReader(client_token=CLIENT_TOKEN, artist_name=ARTIST)
    df_artist = artist_data()
