from readers.genius_reader import GeniusReader
from readers.spotify_reader import SpotifyReader

# https://genius.com/artists/Draco-rosa
# https://open.spotify.com/artist/4Vo7jk7sjpIFMk14dedex5

spotify_client_id = '0a156b494d2847bf9ba024531ff42d56'
spotify_client_secret = '4c03fa9f23c44e9d9351ef67aac05c7e'
spotify_artist_name = 'draco-rosa'
genius_client_token = 'c1RFgHXaEPOu77nhaIi85DhEqzL7yN4ryIx6Mid2_YZ7r-8VnV6OjDL_dvXGoMHH'
genius_artist_name = 'Draco-rosa'

spr = SpotifyReader(client_id=spotify_client_id, client_secret=spotify_client_secret, artist_name=spotify_artist_name)
df_spotify = spr()
artist_data = GeniusReader(client_token=genius_client_token, artist_name=genius_artist_name)
df_genius = artist_data()

