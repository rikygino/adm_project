import ast

import pandas as pd

import accounts_generator
import users_generator
import manipulation_dataset
import random
import datetime
import json


# creating and initializing the variables
accounts_generator.generate_accounts()
account_data = accounts_generator.read_account_from_csv()

users_generator.generate_users()
user_data = users_generator.read_users_from_csv()

manipulation_dataset.manage_dataset()
songs_dataset = manipulation_dataset.read_music_data()

def format_date(date: str) -> dict:
    if date == "": return {}
    millis = datetime.datetime.strptime(date, '%Y-%m-%d').timestamp()*1000
    return {"$date": {"$numberLong": str(int(millis))}}

"""
CREATE SONG COLLECTION

"""

def collection_of_song() -> list[dict]:
    song_collection = []
    for row in songs_dataset:
        song = {
        'song_id': row['id'],
        'title': row['name'],
        'explicit': row['explicit'],
        'danceability': row['danceability'],
        'duration': row['duration_ms'],
        'release_date': format_date(row['release_date']),
        'album_id': row['album_id'],
        'album_name': row['album'],
        'year': row['album_year'],
        'madeByArtists': row['artists'],
        }
        song_collection.append(song)
    return song_collection


"""
CREATE PLAYLIST COLLECTION

"""
def create_a_playlist_random() -> list[dict]:
    max_elements=10
    list_size = random.randint(1, max_elements)
    playlist = []

    for _ in range(list_size):
        random_id = random.randint(0, len(songs_dataset) - 1)
        random_song = songs_dataset[random_id]
        random_pl_dict = {
            "song_id": random_song['id'],
            'title': random_song['name'],
            'danceability': random_song['danceability'],
            'duration': random_song['duration_ms'],
        }
        if random_pl_dict in playlist:
            continue
        playlist.append(random_pl_dict)

    return playlist

playlists_group = {"placeholder": 0}

def collection_of_playlist() -> list[dict]:
    max_elements = 6
    playlist_id = 0
    playlist_collection = []
    for row in user_data:
        number_of_playlists = random.randint(0, max_elements)
        for index in range(number_of_playlists):
            playlist = {
                'playlist_id': playlist_id,
                'user_id': row['id'],
                'username': row['username'],
                'songs': create_a_playlist_random(),
            }
            playlist_id = playlist_id + 1
            playlist_collection.append(playlist)

    return playlist_collection



"""
CREATE USERS COLLECTION

"""

def get_songs(playlist) -> list[dict]:
    songs_ids = []
    for songs in playlist:
        song = {
            'song_id': songs['song_id'],
            'title': songs['title'],
        }
        songs_ids.append(song)

    return songs_ids

def playlist_of_users_random(coll_playlist: list[dict], row) -> list[dict]:
    playlist_of_users = []
    for playlist in coll_playlist:
        if playlist['user_id'] == row['id']:
            name_playlist = playlist['username']+"_"+str(playlist['playlist_id'])
            playlist_user = {
                'playlist_id': playlist['playlist_id'],
                'playlist_name': name_playlist,
                'songs': get_songs(playlist['songs']),
            }
            playlist_of_users.append(playlist_user)

    return playlist_of_users

def collection_of_users(coll_playlist: list[dict]) -> list[dict]:
    user_collection = []

    for row in user_data:
        user = {
            'user_id': row['id'],
            'playlists': playlist_of_users_random(coll_playlist, row),
        }
        user_collection.append(user)

    return user_collection


"""
CREATE ACCOUNT COLLECTION

"""
def generate_random_date(from_date: str, to_date: str) -> str:
    start_date = datetime.datetime.strptime(from_date.strip(), '%Y-%m-%d')
    end_date = datetime.datetime.strptime(to_date.strip(), '%Y-%m-%d')

    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days

    random_number_of_days = random.randrange(days_between_dates)
    random_date = start_date + datetime.timedelta(days=random_number_of_days)

    return random_date.strftime('%Y-%m-%d')

def gen_subscription_id(account_id: int) -> int:
    return (7*account_id+1) % len(account_data)

def get_account_users(coll_playlist: list[dict]) -> list[dict]:
    min_users = 1
    max_users = 4
    account_user_number = random.randint(min_users, max_users)
    account_users = []
    for _ in range(account_user_number):
        random_user_index = random.randint(0, len(user_data) - 1)
        random_user = user_data.pop(random_user_index)
        account_user = {
            "userId": random_user['id'],
            "username": random_user['username'],
            "playlists": playlist_of_users_random(coll_playlist, random_user)
        }
        account_users.append(account_user)

    return account_users



def gen_subscription_type() -> str:
    subscription_types = {
        1: "Free",
        2: "Duo",
        3: "Premium",
    }
    return subscription_types[random.randint(1, 3)]

def collection_of_accounts() -> list[dict]:
    account_collection = []
    for row in account_data:
        account = {
            'account_id': row['id'],
            'email': row['email'],
            'sub_id': gen_subscription_id(row['id']),
            'start_date': format_date(generate_random_date("2018-01-01","2023-01-01")),
            'subscription_type': gen_subscription_type(),
            'users': get_account_users(),
        }
        account_collection.append(account)
    return account_collection

"""
CREATE SUBSCRIPTION COLLECTION

"""



if __name__ == "__main__":
    #song_collection = collection_of_song()
    #print(song_collection)

    #print(create_a_playlist_random())

    playlist_collection = collection_of_playlist()
    for i in range(0,100):
        print(playlist_collection[i])

    #user_collection = collection_of_users(playlist_collection)
    #print(user_collection)



