"""CS 149 Project 3, Part A (testing).

You are not required to test process_args(), load_json(), or main().
To prevent needless suffering, test_format_playlist() is provided.

Author: VJ Edwards
Version: 11/21/24
"""

from copy import deepcopy
from sample_data import TAGS, TRACKS

from playlist import clean_tags, format_tags, add_tag_to_set, \
    clean_durations, tags_match, create_playlist, format_playlist


def test_clean_tags():
    tags = clean_tags(TAGS, ["seen live", "seen dead"])
    assert tags == ["rock", "electronic", "alternative", "indie"]

    tags2 = clean_tags(TAGS, ["rock"], 2150000)
    assert tags2 == ["electronic", "seen live"]

    tags3 = clean_tags(TAGS, ["great"], 2250000)
    assert tags3 == ["rock", "electronic"]


def test_format_tags():
    tags = ["a", "b", "c", "d"]
    assert format_tags(tags) == (
        "a                        b                        c                        \n"
        "d                        \n"
    )
    # TODO try testing with more and less output
    tags = ["a", "b", "c", "d", "e", "f", "g", "h", "i"]
    assert format_tags(tags) == (
        "a                        b                        c                        \n"
        "d                        e                        f                        \n"
        "g                        h                        i                        \n"
    )
    tags = ["a", "b", "c"]
    assert format_tags(tags) == (
        "a                        b                        c                        \n"
    )
    tags = ["a"]
    assert format_tags(tags) == (
        "a                        \n"
    )


def test_add_tag_to_set():
    tags = ["rock", "classical", "hip hop", "hip-hop"]
    s = set()
    add_tag_to_set("rock", tags, s)
    assert s == {"rock"}
    # TODO don't forget to test the hip hop cases
    s = set()
    add_tag_to_set("rock", tags, s)
    add_tag_to_set("classical", tags, s)
    assert s == {"rock", "classical"}
    s = set()
    add_tag_to_set("hip hop", tags, s)
    assert s == {"hip hop", "hip-hop"}
    s = set()
    add_tag_to_set("hip-hop", tags, s)
    assert s == {"hip hop", "hip-hop"}
    s = set()
    add_tag_to_set("pop", tags, s)
    assert s == {}
    add_tag_to_set("", tags, s)
    assert s == {}
    s = set()
    add_tag_to_set("rock", tags, s)
    add_tag_to_set("rock", tags, s)
    assert s == {"rock"}
    s = set()
    add_tag_to_set("rock", "hip-hop", tags, s)
    assert s == {"rock", "hip-hop"}


def test_clean_durations():
    tracks = [
        {"name": "A", "duration": "135000"},
    ]
    clean_durations(tracks)
    assert tracks == [
        {"name": "A", "duration": 135},
    ]
    tracks = [
        {"name": "B", "duration": None},
    ]
    clean_durations(tracks)
    assert tracks == [
        {"name": "B", "duration": 300},
    ]
    tracks = [
        {"name": "C", "duration": ""},
    ]
    clean_durations(tracks)
    assert tracks == [
        {"name": "C", "duration": 300},
    ]
    tracks = [
        {"name": "D", "duration": 135},
    ]
    clean_durations(tracks)
    assert tracks == [
        {"name": "D", "duration": 135},
    ]
    tracks = [
        {"name": "D", "duration": "invalid"},
    ]
    clean_durations(tracks)
    assert tracks == [
        {"name": "D", "duration": 300},
    ]
        


def test_tags_match():
    assert tags_match(TRACKS[0], {"hip hop", "Neo-Soul"})
    # TODO at least one test should be "assert not"
    assert not tags_match(TRACKS[0], {"classical", "alternative"})
    assert tags_match(TRACKS[1], {"hip hop", "classical"})
    assert not tags_match(TRACKS[2], set())
    assert not tags_match(TRACKS[0], {"Hip Hop"})


def test_create_playlist():
    tracks = deepcopy(TRACKS)
    tracks[0]["duration"] = 100
    tracks[1]["duration"] = 120
    tracks[2]["duration"] = 140
    playlist = create_playlist(tracks, {"wonky"}, 5)
    assert playlist == [tracks[1]]
    # TODO try creating playlists of length 2 and 3
    playlist = create_playlist(tracks, {"hip hop"}, 2)
    assert playlist == [tracks[2]]
    playlist = create_playlist(tracks, {"classical"}, 3)
    assert playlist == [tracks[0]]


def test_format_playlist():
    tracks = deepcopy(TRACKS)
    tracks[0]["duration"] = 100
    tracks[1]["duration"] = 120
    tracks[2]["duration"] = 140
    assert format_playlist([]) == (
        'TRACK NAME                                        ARTIST NAME                   LENGTH (min)\n'
        '\n'
        'DETAILS\n'
    )
    assert format_playlist(tracks[1:2]) == (
        'TRACK NAME                                        ARTIST NAME                   LENGTH (min)\n'
        'Rah Tah Tah                                       Tyler, the Creator            2.0\n'
        '\n'
        'DETAILS\n'
        '“Rah Tah Tah” is one of the few songs teased in a CHROMAKOPIA promotional video, uploaded to Tyler’s channel on October 22, 2024, where a 12-second part of the song was featured in a medley of different CHROMAKOPIA snippets.\n\nThis track portrays the chaotic side of the album, featuring Tyler’s well-known aggressive rapping style, with the production following suit and sounding just as menacing.\n\n+28 <a href="http://www.last.fm/music/Tyler,+the+Creator/_/Rah+Tah+Tah">Read more on Last.fm</a>.\n\n'
    )
    assert format_playlist(tracks[1:3]) == (
        'TRACK NAME                                        ARTIST NAME                   LENGTH (min)\n'
        'Rah Tah Tah                                       Tyler, the Creator            2.0\n'
        'Good Luck, Babe!                                  Chappell Roan                 2.3\n'
        '\n'
        'DETAILS\n'
        '“Rah Tah Tah” is one of the few songs teased in a CHROMAKOPIA promotional video, uploaded to Tyler’s channel on October 22, 2024, where a 12-second part of the song was featured in a medley of different CHROMAKOPIA snippets.\n\nThis track portrays the chaotic side of the album, featuring Tyler’s well-known aggressive rapping style, with the production following suit and sounding just as menacing.\n\n+28 <a href="http://www.last.fm/music/Tyler,+the+Creator/_/Rah+Tah+Tah">Read more on Last.fm</a>.\n\n'
        '“Good Luck, Babe!“ entails a relationship Chappell Roan had with a woman who struggled with compulsory heterosexuality, the conflict eventually causing their split.\n\nRoan teased this song a month prior to its release by sharing a minute-long snippet. Additionally, she further teased the track by performing it live before its initial release date. <a href="http://www.last.fm/music/Chappell+Roan/_/Good+Luck,+Babe%21">Read more on Last.fm</a>.\n\n'
    )
