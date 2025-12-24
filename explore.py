"""Downloads the full data of a numerous number of tracks.
This program downlads data from a numerous amount of tracks. It does
that by fetching
top tracks from the Last.fm
API and stores metadata for each track. The fetch_top_tracks function
calls the chart.gettoptracks method to
retrieve a list of top tracks and saves the data to a toptracks.json
file. For each track, the program calls
track.getinfo to retrieve detailed metadata, including
artist information and track details. This metadata is
stored in
fulltracks.json. The program
ensures compliance with Last.fm's API rate
limits by pausing for 2 seconds between requests.
The API key must be added in the API_KEY
variable for the program to deliver its desired result.


Author: VJ Edwards
Version: 12/6/2024
"""

import json
import time
import requests
import os  # For accessing environment variables

# Fetch the API key from the environment variable
API_KEY = os.getenv("API_KEY")  # Make sure to set this environment variable
API_URL = "https://ws.audioscrobbler.com/2.0/"


def fetch_track_info(artist_name, track_name):
    """Get the metadata for a track on Last.fm.

    Args:
        artist_name (str): The artist name.
        track_name (str): The track name.

    Returns:
        dict: JSON response from Last.fm API or None if an error occurs.
    """
    params = {
        "method": "track.getinfo",
        "api_key": API_KEY,
        "format": "json",
        "artist": artist_name,
        "track": track_name,
    }

    try:
        response = requests.get(API_URL, params)
        # Check if the response was successful
        response.raise_for_status()
        data = response.json()
        return data.get("track")
    except (requests.exceptions.RequestException, ValueError) as e:
        print(f"Error fetching track info for {artist_name} - {track_name}: {e}")
        return None


def fetch_top_tracks():
    """Store the top tracks in a json file."""
    # Get the top tracks chart
    params = {
        "method": "chart.gettoptracks",
        "api_key": API_KEY,
        "format": "json"
    }

    try:
        response = requests.get(API_URL, params)
        # Check if the response was successful
        response.raise_for_status()
        data = response.json()
        tracks = data["tracks"]["track"]
        print("Received", len(tracks), "tracks")  # This print might be removed for Gradescope

        # Save the top tracks to a file
        with open("toptracks.json", "w") as file:
            json.dump(tracks, file, indent=4)

        # Get full info about each track
        fulltracks = []
        for track in tracks:
            artist_name = track["artist"]["name"]
            track_name = track["name"]
            info = fetch_track_info(artist_name, track_name)
            if info:
                fulltracks.append(info)
            # Wait 2 seconds between requests to avoid being blocked
            time.sleep(2)

        # Save the full tracks to a file
        with open("fulltracks.json", "w") as file:
            json.dump(fulltracks, file, indent=4)

    except (requests.exceptions.RequestException, ValueError) as e:
        print(f"Error fetching top tracks: {e}")


if __name__ == "__main__":
    fetch_top_tracks()
