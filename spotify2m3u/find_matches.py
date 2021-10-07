import beets.library
import spotify2m3u
from spotify2m3u import get_logger
import sys

logger = get_logger(__name__)
beets_db_path = spotify2m3u.config["paths"]["beets_db"].get()
music_dir_path = spotify2m3u.config["paths"]["music_dir"].get()
auto_mode = spotify2m3u.config["auto_mode"].get(False)
try:
    logger.info("Instatiating beets library") 
    lib = beets.library.Library(beets_db_path, music_dir_path)
    logger.debug("Successfully instantiated beet library") 
except:
    logger.critical("Failed to instantiate beets library")
    logger.info("Check paths:beets_db and paths:music_dir are valid")
    logger.debug(f"spotify2m3u:paths:beets_db => {beets_db_path}")
    logger.debug(f"spotify2m3u:paths:music_dir => {music_dir_path}")
    sys.exit(1)


def find_match(title: str, album: str, artists: str):
    results = _find_matches_by_album_and_title(title, album)
    results.extend(_find_matches_by_artist_and_title(title, artists))
    results = list(set(results))
    if len(results) == 0:
        logger.info("No results found for %s - %s - %s",
                    artists, album, title)
        logger.warning("Searching by title only"
                       "- may lead to a large number of results")
        results.extend(_find_matches_by_title_only(title))
        if len(results) == 0:
            logger.info("No additional results found, track skipped")
    for result in results:
        logger.debug("Found Result: %s at %s",
                     result, result.destination())
    return _choose_best_match(results, title, album, artists)


def _find_matches_by_album_and_title(title: str, album: str):
    logger.debug("Finding results by album and track title")
    results = lib.items(f"album:{album} title:'{title}'")
    logger.debug("Found %d results" % len(results))
    return list(results)


def _find_matches_by_artist_and_title(title: str, artists: str):
    logger.debug("Finding results by album and track title")
    results = []
    for artist in artists.split(";"):
        results.extend(
                list(lib.items(f"artist:{artist} title:'{title}'")))
    logger.debug("Found %d results" % len(results))
    return results


def _find_matches_by_title_only(title: str):
    logger.debug("Finding results by track title only")
    results = lib.items(f"title:'{title}'")
    logger.debug("Found %d results" % len(results))
    return list(results)


def _choose_best_match(results: list, title: str,
                       album: str, artists: str):

    if len(results) == 0:
        return None
    if auto_mode:
        return results[0]

    print(f"Matches for track with info\n"
          f"Title: {title}\n"
          f"Album: {album}\n"
          f"Artist(s): {artists}\n")

    print("Enter the number of the best match, or 0 to skip")
    for i in range(len(results)):
        result = results[i]
        print(f"{i+1}) - {result} at {result.destination()}")

    choice = -1
    while choice < 0:
        try:
            choice = int(input("Choice: "))
            if choice < 0 or choice > len(results):
                print("Invalid choice: {choice}"
                      ", must be between 0 and {len(results)}")
        except (ValueError, TypeError):
            print("Invalid choice, must be integer")
        except (KeyboardInterrupt):
            logger.info("Exiting due to keyboard interrupt")
            sys.exit(1)
    return None if choice == 0 else results[choice-1]
