try:
    import pkg_resources.py2_warn
except ImportError:
    pass

import csv
import datetime
import time

import spotipy

csv_columns = ["playList", "artist", "explicit", "id", "popularity", "title", "energy", "liveness", "tempo", "speechiness",
               "acousticness", "instrumentalness", "time_signature", "danceability", "key", "duration_ms", "loudness",
               "valence", "mode"]
csvfile = open('spotify-{}.csv'.format(datetime.datetime.now().date()), 'w', newline='', encoding="utf-8")
writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
writer.writeheader()

CLIENT_ID = "7e475c5008a3484d8350036385baed8f"
CLIENT_SECRET = "9ab3399040124ea89c196da8005c8326"
token = spotipy.oauth2.SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
cache_token = token.get_access_token()
sp = spotipy.Spotify(cache_token)
playlist_ids = ['6FKDzNYZ8IW1pvYVF4zUN2', '6yPiKpy7evrwvZodByKvM9', '0twlW4iDRhKXAJPopD8PP0', '4rnleEAOdmFAbRcNCgZMpY',
                '6ZlFKcTzJVslgjudScTX4G', '3crEbeyihVkc467poiIV03']


def refresh_token():
    new_token = spotipy.oauth2.SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
    new_cache_token = token.get_access_token()
    return spotipy.Spotify(cache_token)


for playlist_id in playlist_ids:
    for i in range(1, 100):
        try:
            items = sp.user_playlist_tracks("spotify", playlist_id, offset=i*100, limit=100)['items']
        except:
            sp = refresh_token()
            items = sp.user_playlist_tracks("spotify", playlist_id, offset=i * 100, limit=100)['items']
        for spotify_item in items:
            # time.sleep(2)
            item = dict()
            item['playList'] = playlist_id
            item['artist'] = ', '.join([artist['name'] for artist in spotify_item['track']['artists']])
            item['explicit'] = spotify_item['track']['explicit']
            item['id'] = spotify_item['track']['id']
            item['popularity'] = spotify_item['track']['popularity']
            item['title'] = spotify_item['track']['name']
            try:
                feature_data = sp.audio_features(spotify_item['track']['id'])[0]
            except:
                sp = refresh_token()
                feature_data = sp.audio_features(spotify_item['track']['id'])[0]

            item['energy'] = feature_data['energy']
            item['liveness'] = feature_data['liveness']
            item['tempo'] = feature_data['tempo']
            item['speechiness'] = feature_data['speechiness']
            item['acousticness'] = feature_data['acousticness']
            item['instrumentalness'] = feature_data['instrumentalness']
            item['time_signature'] = feature_data['time_signature']
            item['danceability'] = feature_data['danceability']
            item['key'] = feature_data['key']
            item['duration_ms'] = feature_data['duration_ms']
            item['loudness'] = feature_data['loudness']
            item['valence'] = feature_data['valence']
            item['mode'] = feature_data['mode']
            writer.writerow(item)
            csvfile.flush()




