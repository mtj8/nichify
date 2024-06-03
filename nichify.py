import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os
from dotenv import load_dotenv

def nichify():
    # use spotipy to authenticate request for client credential flow
    scope = "user-library-read"
    load_dotenv()

    auth_manager = SpotifyClientCredentials(client_id=os.getenv('CLIENT_ID'), client_secret=os.getenv('CLIENT_SECRET'))
    sp = spotipy.Spotify(auth_manager=auth_manager)
    
    # take artist id as input
    artist_id = input('Enter a Spotify artist ID: ')
    # print(artist)
    
    # output niche artists repeatedly (recursive?)
    niche_artist_list = []
    try:
        niche_finder(sp, artist_id, niche_artist_list, 50)
    except Exception as e:
        # print(e)
        print('fukt')



def niche_finder(sp, artist, artist_list, min_follower_threshold):
    # if artist is already in list, return
    artist_result = sp.artist(artist)
    if artist in artist_list:
        print('Hit a loop!')
        artist_dossier(artist_result)
        return
    elif artist_result['followers']['total'] <= min_follower_threshold:
        print('Mythical pull!')
        artist_dossier(artist_result)
        return
    else:
        artist_list += [artist]
        related_artists_results = sp.artist_related_artists(artist)
        print(f"Artists related to {artist_result['name']}: ")
        
        new_artist_dict = {}
        for i, new_artist in enumerate(related_artists_results['artists']):
            # print(f"{i}: {new_artist['name']}")
            new_artist_id = new_artist['id']
            new_artist_dict[new_artist_id] = new_artist['followers']['total']
        # print(artist_list)
        # print(new_artist_dict)
        
        new_niche_artist = min(new_artist_dict, key=new_artist_dict.get)
        # print(new_niche_artist)
        nichify(sp, new_niche_artist, artist_list, 50)
        
    # probably implement backoff strategies for api calling if necessary



def artist_dossier(artist_dict):
    print(f'Your niche artist is {artist_dict['name']} with {artist_dict['followers']['total']} followers.')
    print(artist_dict['external_urls']['spotify'])
    print(f'Genres (if any): {artist_dict['genres']}')

    
    
nichify()
    