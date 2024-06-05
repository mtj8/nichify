import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os
from dotenv import load_dotenv

MIN_FOLLOWER_THRESHOLD = 50 # adjust as necessary

def nichify(artist_id):
    # use spotipy to authenticate request for client credential flow
    scope = "user-library-read"
    load_dotenv()

    auth_manager = SpotifyClientCredentials(client_id=os.getenv('CLIENT_ID'), client_secret=os.getenv('CLIENT_SECRET'))
    sp = spotipy.Spotify(auth_manager=auth_manager)
    
    # take artist id as input
    # output niche artists repeatedly (recursive?)
    niche_artist_list = []
    try:
        niche_list = niche_finder(sp, artist_id, niche_artist_list, MIN_FOLLOWER_THRESHOLD)
        return niche_list
    except Exception as e:
        print(e)



def niche_finder(sp, artist, artist_list, min_follower_threshold):
    # if artist is already in list, return
    artist_result = sp.artist(artist)
    for artist_entry in artist_list:
        if artist_result['id'] == artist_entry['id']:
            print('Hit a loop!')
            # artist_dossier(artist_result)
            return artist_list
    if artist_result['followers']['total'] <= min_follower_threshold:
        print('Mythical pull!')
        # artist_dossier(artist_result)
        return artist_list
    
    else:
        artist_list += [artist_result]
        related_artists_results = sp.artist_related_artists(artist)
        print(f"{artist_result['name']}")
        
        new_artists_dict = {}
        for i, new_artist in enumerate(related_artists_results['artists']):
            # print(f"{i}: {new_artist['name']}")
            new_artist_id = new_artist['id']
            new_artists_dict[new_artist_id] = new_artist['followers']['total']
        # print(artist_list)
        # print(new_artist_dict)
        
        new_niche_artist = min(new_artists_dict, key=new_artists_dict.get)
        # print(new_niche_artist)
        
        return niche_finder(sp, new_niche_artist, artist_list, MIN_FOLLOWER_THRESHOLD)
        
    # probably implement backoff strategies for api calling if necessary



# def artist_dossier(artist_dict):
#     print(f'Your niche artist is {artist_dict['name']} with {artist_dict['followers']['total']} followers.')
#     print(artist_dict['external_urls']['spotify'])
#     print(f'Genres (if any): {artist_dict['genres']}')
    
# test: yeat - returns Kanni with 41 followers
# print(nichify('3qiHUAX7zY4Qnjx8TNUzVx'))

# test: yoasobi - hits loop, returns ゲネラル・パウゼ with 235 followers
# print(nichify('64tJ2EAv1R6UaZqc4iOCyj'))