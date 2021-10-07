import requests
import spotify2m3u
from spotify2m3u import find_matches, get_logger
import os

logger = get_logger(__name__)

if __name__ == "__main__":
    CLIENT_ID = os.getenv("S2M3U_CLIENT_ID",
                          spotify2m3u.config["credentials"]["CLIENT_ID"].get())
    CLIENT_SECRET = os.getenv("S2M3U_CLIENT_SECRET",
                          spotify2m3u.config["credentials"]["CLIENT_SECRET"].get())

    AUTH_URL = 'https://accounts.spotify.com/api/token'
    BASE_URL = 'https://api.spotify.com/v1/'

    auth_response = requests.post(AUTH_URL, {
        'grant_type': 'client_credentials',
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
    })
    access_token = auth_response.json()["access_token"]
    headers = {
        'Authorization': 'Bearer {token}'.format(token=access_token)
    }

    playlist_id = input("playlist id: ")

    r = requests.get(BASE_URL + 'playlists/' + playlist_id, headers=headers).json()
    playlist_name = r["name"]
    r = requests.get(BASE_URL + 'playlists/' + playlist_id + "/tracks?fields=items(track(name,artists(name),album(name,artists(name)))),name", headers=headers).json()

    matches = []
    for item in r["items"]:
        track = item["track"]
        track_name = track["name"]
        track_artists = ";".join(artist["name"] for artist in track["artists"])
        album = track["album"]
        album_name = album["name"]
        album_artists = ";".join(artist["name"] for artist in album["artists"])
        match = find_matches.find_match(track_name, album_name, track_artists+";"+album_artists)
        if match is not None:
            matches.append(match)

    playlist_file_path = os.path.join(spotify2m3u.config["paths"]["playlist_dir"].get(str), f"{playlist_name}.m3u")
    logger.info("Writing playlist to: %s", playlist_file_path)
    with open(playlist_file_path, 'w') as playlist_file:
        playlist_file.writelines(match.destination().decode("UTF-8") + "\n" for match in matches)
