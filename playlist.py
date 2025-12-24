"""CS 149 Project 3, Part B (nested data).

Author: VJ Edwards
Version: 11/21/24
"""
import sys
import os
import json


def process_args():  # pragma: no cover
    """
    Check the number and validity of the command-line arguments.

    There must be 2 arguments: the tags filename and the tracks filename.
    Print the required error message and exit if the number of arguments is
    incorrect or if either filename does not exist.

    Returns:
        tuple: (tagsfilename, tracksfilename)
    """
    if len(sys.argv) != 3:
        print("Usage: python playlist.py tagfile trackfile")
        sys.exit(1)
    tagfile = sys.argv[1]
    trackfile = sys.argv[2]
    if not os.path.exists(tagfile):
        print(f"Input file {tagfile} does not exist")
        sys.exit(1)
    if not os.path.exists(trackfile):
        print(f"Input file {trackfile} does not exist")
        sys.exit(1)
    return (tagfile, trackfile)


def load_json(filename):  # pragma: no cover
    """
    Load the given JSON file and return the data.

    Arguments:
        filename(str): the filename of the JSON file to load

    Returns:
        list: the data from the JSON file assuming the top level is a list
    """
    with open(filename, 'r') as myfile:
        data = json.load(myfile)
    return data


def clean_tags(tags, exclude, limit=None):
    """
    Return a list of tag names, excluding any in the exclude list or whose
    count exceeds the limit.

    Arguments:
        tags(list): A list of tag dictionaries
        exclude(list): A list of tag name strings to be excluded
        limit(int): OPTIONAL - exclude tags whose count is equal to or
                                below the limit

    Returns:
        list: a list of lowercase strings that are acceptable tag names
    """
    valid_tags = []
    for tag in tags:
        if tag['name'].lower() not in exclude:
            if limit is None or tag['count'] > limit:
                valid_tags.append(tag['name'].lower())
    return valid_tags


def format_tags(tags):
    """
    Format the list of tag names into 3 columns for display.

    Arguments:
        tags(list): a list of tag name strings

    Returns:
        string: a single string that will display the tags in 3 columns
    """
    formatted_str = ""
    for i in range(0, len(tags), 3):
        group = tags[i:i+3]
        row = ""
        for tag in group:
            row += tag + " " * (25 - len(tag))
        formatted_str += row + "\n"
    return formatted_str


def add_tag_to_set(name, tags, tagset):
    """
    Add the tag name to the tagset only if it appears in tags list,
    regardless of case.

    Also handle the special hip-hop issue.

    Arguments:
        name(str): the tag name to add to the set
        tags(list): a list of all tag names in lowercase
        tagset(set): add name to this set if it is a valid name
    """
    normal_name = name.lower()
    if normal_name in ["hip hop", "hip-hop"]:
        if "hip hop" in tags:
            tagset.add("hip hop")
        if "hip-hop" in tags:
            tagset.add("hip-hop")
    elif normal_name in tags:
        tagset.add(normal_name)


def clean_durations(tracks, default_duration=300):
    """
    Clean the tracks' duration attribute: update its type & fix inconsistencies.

    Arguments:
        tracks(list): a list of track dictionaries
        default_duration: OPTIONAL: the value for missing durations; set to 300
                        seconds unless another value is provided.
    """
    for track in tracks:
        duration = track.get("duration", "")
        try:
            duration = int(float(duration))
        except (ValueError, TypeError):
            duration = 0
        if duration % 1000 == 0 and duration != 0:
            duration //= 1000
        if duration == 0:
            duration = default_duration
        track["duration"] = duration


def tags_match(track, tagset):
    """
    Return True if any of a track's tag names are in the given tag set.

    Arguments:
        track(dictionary): a single track dictionary
        tagset(set): a set of tag names

    Returns:
        bool: True only if one of the track's tag names is in the tag set
    """
    for tag in track['toptags']['tag']:
        if tag['name'].lower() in tagset:
            return True
    return False


def create_playlist(tracks, tagset, minutes):
    """
    Search the list of tracks and compile a new list of ones which match the tags
    and fit within the desired playlist length in minutes.

    Arguments:
        tracks(list): a list of track dictionaries
        tagset(set): a set of tag names
        minutes(int): the desired playlist length

    Returns:
        list: a list of track dictionaries for the songs in the playlist.
    """
    tracks_list = []
    total_seconds = 0
    clean_durations(tracks)
    for track in tracks:
        if tags_match(track, tagset):
            if total_seconds + int(track['duration']) <= minutes * 60:
                tracks_list.append(track)
                total_seconds += int(track['duration'])
    return tracks_list


def format_playlist(playlist):
    """
    Format a playlist as a string.

    Arguments:
        playlist(list): a list of track dictionaries

    Returns:
        str: a single string suitable for printing
    """
    clean_durations(playlist)
    formatted_playlist = f"{'TRACK NAME':50s}{'ARTIST NAME':30s}LENGTH (min)\n"
    for track in playlist:
        formatted_playlist += f"{track['name']:50s}"
        formatted_playlist += f"{track['artist']['name']:30s}"
        formatted_playlist += f"{int(track['duration']) / 60:.1f}\n"
    formatted_playlist += '\n'
    formatted_playlist += 'DETAILS\n'
    for track in playlist:
        formatted_playlist += track['wiki']['summary'] + '\n\n'
    return formatted_playlist


def main():  # pragma: no cover
    """
    Given the 2 JSON data files on the command-line, have the user build a playlist.
    """
    # process the command line arguments
    tagfile, trackfile = process_args()
    # load the top 50 tags
    tags = load_json(tagfile)

    # remove the tags that are not really like genres,
    # optionally limit by popularity
    # get a new list of just tag names
    tags = clean_tags(tags, ["seen live", "chillout"])

    # format and show the tag names in 3 columns
    print("\nThese are the top tags, select as many as you want, enter 'stop' to end:\n")
    print(format_tags(tags))

    # let the user select a set of tags they are interested in
    ts = set()
    while (s := input("Enter a tag (or 'stop' to stop): ")) != 'stop':
        add_tag_to_set(s, tags, ts)
        # display the set as its being updated
        print(ts)

    # load the list of top tracks from the input file
    tracks = load_json(trackfile)

    # clean the duration attributes, optionally change the default duration
    clean_durations(tracks)

    # ask the user for a playlist length
    minutes = int(input("\nEnter your desired playlist length in minutes: "))
    # create the playlist
    playlist = create_playlist(tracks, ts, minutes)
    # display the playlist
    print("\nHere is your playlist created from the top 50 tracks on last.fm:")
    print(format_playlist(playlist))


if __name__ == "__main__":  # pragma: no cover
    main()
