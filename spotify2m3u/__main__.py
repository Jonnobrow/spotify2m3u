import spotify2m3u
from spotify2m3u import find_matches, get_logger
from spotify2m3u.spotify import get_playlist
import os
import sys

logger = get_logger(__name__)


def _get_matches(tracks):
    matches = []
    misses = []
    for item in tracks:
        track = item["track"]
        track_name = track["name"]
        track_artists = ";".join(artist["name"]
                                 for artist in track["artists"])

        album = track["album"]
        album_name = album["name"]
        album_artists = ";".join(artist["name"]
                                 for artist in album["artists"])

        match = find_matches.find_match(track_name, album_name,
                                        track_artists+";"+album_artists)

        if match is not None:
            matches.append(match.get('path'))
        else:
            misses.append(f"{track_artists} - {album_name}"
                          " - {track_name}")
    return matches, misses


def _write_playlist(matches, playlist_name):
    playlist_file_path = os.path.join(
            str(spotify2m3u.config["paths"]["playlist_dir"].get(str)),
            f"{playlist_name}.m3u")
    logger.info("Writing playlist to: %s", playlist_file_path)
    with open(playlist_file_path, 'w') as playlist_file:
        playlist_file.writelines(match.decode("UTF-8") + "\n"
                                 for match in matches)


def main():
    playlist_id = input("Enter playlist id: ")
    tracks, name = get_playlist(playlist_id)
    if tracks is None:
        sys.exit(0)
    if name is None:
        name = input("Enter a name for the playlist: ")

    matches, misses = _get_matches(tracks)

    if len(matches) == 0:
        logger.warning("No tracks were matched,"
                       " no playlist will be created")

    if len(misses) == 0:
        logger.info("All tracks matched")
    else:
        print("Failed to matche these tracks: ")
        for miss in misses:
            print("- " + miss)

    _write_playlist(matches, name)


if __name__ == "__main__":
    main()
    


