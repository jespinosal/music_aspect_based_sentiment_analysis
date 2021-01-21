import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from readers.base_reader import DataFrameManager


class SpotifyReader(DataFrameManager):

    def __init__(self, client_id, client_secret, artist_name):

        self.__client_id = client_id
        self.__client_secret = client_secret
        self.artist_name = artist_name
        self.__ccm, self.__sp = self.__setup()
        self.song_features_dataframe = pd.DataFrame()
        DataFrameManager.__init__(self, artist_name=self.artist_name, file_lastname='songs-features')

    def __setup(self):
        _ccm = SpotifyClientCredentials(client_id=self.__client_id,
                                        client_secret=self.__client_secret)
        _sp = spotipy.Spotify(client_credentials_manager=_ccm)
        return _ccm, _sp

    def artist_id_get(self):
        _results = self.__sp.search(f'artist:{self.artist_name.lower()}')
        return _results['tracks']['items'][0]['artists'][0]['uri']

    def _tracts_get(self, album_id):
        return self.__sp.album_tracks(album_id=album_id, limit=50).get('items')

    def _albums_get(self, artist_id):
        return self.__sp.artist_albums(artist_id=artist_id, country="US", limit=50).get('items')

    @staticmethod
    def _album_feature_extraction(album):
        return {
            'album_name': album.get('name'),
            'release_date': album.get('release_date'),
            'total_tracks': album.get('total_tracks')
               }

    @staticmethod
    def track_get_meta_info_extraction(track):
        return {
            'track_name': track.get('name'),
            'track_duration': track.get('duration_ms'),
            'track_number': track.get('disc_number')
               }

    def track_audio_features_extraction(self, track_id):
        track_features = self.__sp.audio_analysis(track_id=track_id).get('track')
        return {
            'feature_duration': track_features.get('duration'),
            'feature_loudness': track_features.get('duration'),
            'feature_tempo': track_features.get('tempo')
               }

    def build_dataframe(self):

        albums_track_data_list = []

        artist_id = self.artist_id_get()

        albums = self._albums_get(artist_id=artist_id)

        for _album in albums:

            album_id = _album.get('uri')

            albums_features_dict = self._album_feature_extraction(_album)

            _tracks = self._tracts_get(album_id=album_id)

            for _track in _tracks:

                track_fields = {}

                track_id = _track.get('id')

                track_meta_dict = self.track_get_meta_info_extraction(track=_track)
                track_fields.update(track_meta_dict)

                tract_features_dict = self.track_audio_features_extraction(track_id=track_id)
                track_fields.update(tract_features_dict)

                track_fields.update(albums_features_dict)

                albums_track_data_list.append(track_fields)

        return pd.DataFrame(albums_track_data_list)

    def __call__(self, *args, **kwargs):

        self.song_features_dataframe = self.get_data_frame()

        return self.song_features_dataframe


if __name__ == "__main__":

    client_id = '0a156b494d2847bf9ba024531ff42d56'
    client_secret = '4c03fa9f23c44e9d9351ef67aac05c7e'
    spr = SpotifyReader(client_id=client_id, client_secret=client_secret, artist_name='draco-rosa')
    df_spotify = spr()

