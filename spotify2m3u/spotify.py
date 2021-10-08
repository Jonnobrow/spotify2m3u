import requests
import os
from spotify2m3u import config, get_logger
try:
    from simplejson.errors import JSONDecodeError
except ImportError:
    from json.decoder import JSONDecodeError

logger = get_logger(__name__)

CLIENT_ID = os.getenv("S2M3U_CLIENT_ID",
                      config["credentials"]["CLIENT_ID"].get())
CLIENT_SECRET = os.getenv("S2M3U_CLIENT_SECRET",
                          config["credentials"]["CLIENT_SECRET"].get())

AUTH_URL = 'https://accounts.spotify.com/api/token'
BASE_URL = 'https://api.spotify.com/v1/'


def _safe_unpack_response(response, key):
    logger.debug("Unpacking response")
    value = None
    if response.ok:
        try:
            logger.debug("Getting JSONified response")
            json_response = response.json()
            if key in json_response.keys():
                logger.debug(f"Getting key '{key}' from response")
                value = json_response[key]
            else:
                logger.error(f"Failed to get key '{key}' from response")
        except JSONDecodeError:
            logger.error("Response body did not contain JSON")
    else:
        logger.error(f"Response status code was {response.status_code}")
        logger.info("Check credentials")
    return value


def _headers(token):
    logger.debug("Generating request headers")
    return {
        'Authorization': 'Bearer {token}'.format(token=token)
    }


def _get_access_token():
    logger.debug("Getting access token")
    access_token = None
    try:
        auth_response = requests.post(AUTH_URL, {
            'grant_type': 'client_credentials',
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
        })
        access_token = _safe_unpack_response(auth_response,
                                             "access_token")
    except ConnectionError:
        logger.exception("Failed to connect to spotify API")
        logger.info("Check your credentials and network connection")
    return access_token


def _get_playlist_name(headers, playlist_id):
    name = None
    try:
        logger.debug("Getting playlist information")
        response = requests.get(BASE_URL + 'playlists/' + playlist_id,
                                headers=headers)
        name = _safe_unpack_response(response, "name")
        logger.debug(f"Got playlist information for '{name}'")
    except ConnectionError:
        logger.exception("Failed to connect to spotify API")
        logger.info("Check your credentials and network connection")
    return name


def _get_playlist_tracks(headers, playlist_id):
    tracks = []
    try:
        logger.debug("Getting playlist tracks")
        response = requests.get(BASE_URL + 'playlists/' + playlist_id +
                                "/tracks?fields=items(track(name,"
                                "artists(name),album(name,"
                                "artists(name)))),name",
                                headers=headers)
        tracks = _safe_unpack_response(response, "items")
        if tracks is not None:
            logger.debug(f"Got {len(tracks)} tracks")
        else:
            logger.warning("Got no tracks for playlist")
    except ConnectionError:
        logger.exception("Failed to connect to spotify API")
        logger.info("Check your credentials and network connection")
    return tracks


def get_playlist(playlist_id):
    access_token = _get_access_token()
    if access_token is None:
        logger.error("Failed to get access token for spotify")
        return None

    headers = _headers(access_token)

    name = _get_playlist_name(headers, playlist_id)
    if name is None:
        logger.error("Failed to get name for playlist")

    tracks = _get_playlist_tracks(headers, playlist_id)
    if tracks is None or len(tracks) == 0:
        logger.error("Failed to get tracks for playlist")
        tracks = None

    return tracks, name
