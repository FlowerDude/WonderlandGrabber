import spotipy
import yaml
import spotipy.util as util
import urllib.request
from pprint import pprint
from bs4 import BeautifulSoup


def load_config():
    global user_config
    stream = open('config.yaml')
    user_config = yaml.load(stream, Loader=yaml.FullLoader)


def getWonderlandArtists():
    autists = []
    response = urllib.request.urlopen("https://www.waldfrieden.net/en/wonderland/")
    readeted = response.read()
    s = BeautifulSoup(readeted, 'html.parser')
    lineupanchor = s.find_all('div', attrs={'data-anchor': 'lineup'})
    for anchor in lineupanchor:
        artistLinks = BeautifulSoup(anchor.__str__(), 'html.parser')
        links = artistLinks.find_all('a', attrs={'href': True})
        for link in links:
            autists.append(link.text)
    return autists


def getSongs(artists):
    songIds = []
    for artist in artists:
        pprint(artist)
        result = sp.search(q='artist:' + artist, type='artist', limit=1)
        artistItem = result['artists']['items']
        if len(artistItem) == 0:
            print('Artist not found - ' + artist)
            continue
        artist_id = artistItem[0]['id']
        artist_top_tracks = sp.artist_top_tracks(artist_id)
        if len(artist_top_tracks) < 1 or len(artist_top_tracks['tracks']) < 1:
            print('No Top-Track found for Artist - ' + artist)
            continue
        songIds.append(artist_top_tracks['tracks'][00]['id'])
    return songIds


if __name__ == '__main__':
    global sp
    global user_config
    load_config()
    token = util.prompt_for_user_token(
        user_config['username'], scope='playlist-modify-private,playlist-modify-public', client_id=user_config[
            'client_id'], client_secret=user_config['client_secret'], redirect_uri=user_config['redirect_uri'])
    if not token:
        print("Can't get token for", user_config['username'])
        exit()
    sp = spotipy.Spotify(auth=token)
    songIds = getSongs(getWonderlandArtists())
    sp.playlist_add_items(playlist_id=user_config['playlist_id'], items=songIds)
