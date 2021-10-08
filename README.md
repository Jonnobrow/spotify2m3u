# spotify2m3u

Spotify2m3u is a simple tool to recreate spotify playlists in your local library
by querying your media collection and creating an m3u playlist file.

## Warning
- There is no overwrite protection or testing yet so if you accidentally
  overwrite a playlist you love and can't get it back I accept no responsibility
- You will see many copies of each track at the moment, this is not a bug but a
  limitation and will be improved upon ASAP

## Configuration

### Default Configuration

```
---
auto_mode: False
paths:
  music_dir: /media/music/
  beets_db: /media/music/beets.db
  playlist_dir: /media/music/playlists/
credentials:
  CLIENT_ID: 
  CLIENT_SECRET:
```

### Values

| Key  | Accepted Values   | Default   | Description |
|-------------- | -------------- | -------------- | -------------- |
| auto_mode    | true/false     | false     | The first match will be used, no user input for match selection |
| paths : music_dir | path | /media/music | The path to your music library |
| paths : beets_db | path | /media/music/beets.db | The path to your beets database | 
| paths : playlist_dir | path | /media/music/playlist/ | The path to write playlist files to |
| credentials : CLIENT_ID | string | "" | Your spotify client id |
| credentials : CLIENT_SECRET | string | "" | Your spotify client secret |
| log_level | [Python log levels](https://docs.python.org/3/library/logging.html#levels) | INFO | Log Level |

## Usage (for now)

1. Clone the repository
2. Create a config file at `$XDG_CONFIG_HOME/spotify2m3u/config.yaml`
3. Change directory to the repo and run:
    ```
    python -m virtualenv venv
    . venv/bin/activate
    pip install -r requirements.txt
    python -m spotify2m3u
    ```
4. Enter the playlist ID when prompted
5. *auto_mode == false*: Enter a number when prompted for each track
6. Marvel at the wonderful m3u file created at `playlist_dir/playlist_name.m3u`

## Changelog

#### v0.0.2: Wider search and tidier code
- Widened search to include album and artist only
- Refactored
  - Moved spotify stuff to a separate file and broke down
    into functions.
  - Implemented helper function to safely unpack a response
  - Refactored main to include separate functions for logical
    chunks of behaviour
  - Added requirements.txt easier development
- Correctly get paths rather than destination

#### v0.0.1: Basic Functionality
- Basic config file setup
- Logging setup
- Query spotify API for playlist for name
- Query spotify API for playlist items
- Find results in beets library for each item
- Ask user for best choice from items, or auto choose 1st
- Write results to playlist, absolute paths
