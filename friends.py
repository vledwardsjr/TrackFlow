"""CS 149 Project 3, Part C (recursion).

Author: VJ Edwards
Version: 12/6/24
"""
import json


def load_data(path):
    """Load data from a file and map user names to friends' names.

    Args:
        path (str): The file path to the JSON file containing the data.

    Returns:
        dict: Maps each user's name to a list of their friends' names
              or None if the user has no friends.
    """
    with open(path) as myfile:
        data = json.load(myfile)

    final = {}
    for dict in data:
        friends = dict.get("friends", [])
        name = dict['name']
        if friends is None:
            final[name] = None
        else:
            final[name] = friends
    return final


def influence(data, user, visited=None):
    """Count the number of unique friends reachable from a user.

    Args:
        data (dict): Maps each user's name to a list of their friends'
                     names or None if the user has no friends.
        user (str): Name of the user whose influence is to be counted.
        visited (set): Users already visited during recursion.

    Returns:
        int: The number of unique friends reachable from the user.
    """
    if visited is None:
        visited = set()
    if user in visited:
        return 0
    visited.add(user)
    friends = data.get(user, [])
    if not friends:
        return 0
    num = 0
    for i in friends:
        num += influence(data, i, visited)
    return num + len(friends)


def separation(data, user1, user2, visited=None, depth=0):
    """Find the degrees of separation between two users.

    Args:
        data (dict): Maps each user's name to a list of their friends'
                     names or None if the user has no friends.
        user1 (str): Name of the starting user.
        user2 (str): Name of the ending user.
        visited (set): Users already visited during recursion.
        depth (int): Current number of recursive calls.

    Returns:
        int: Degrees of separation between user1 and user2,
             or -1 if user2 is not reachable from user1.
    """
    if visited is None:
        visited = set()
    if user1 in visited:
        return -1
    visited.add(user1)
    if user1 == user2:
        return depth
    friends = data.get(user1)
    if friends is None:
        return -1
    for i in friends:
        final = separation(data, i, user2, visited, depth+1)
        if final != -1:
            return final
    return -1
