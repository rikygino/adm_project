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

def date_to_BSON(date: str) -> dict:
    if date == "": return {}
    millis = datetime.datetime.strptime(date, '%Y-%m-%d').timestamp()*1000
    return {"$date": {"$numberLong": str(int(millis))}}

"""
CREATE SONG COLLECTION

"""

def collection_of_song() -> list[dict]:
    song_collection = []
    for row in songs_dataset:
        song = {}
        song['song_id'] = row['id'],
        song['title'] = row['name'],
        song['explicit'] = row['explicit'],
        song['danceability'] = row['danceability'],
        song['duration'] = row['duration_ms'],
        song['release_date'] = date_to_BSON(row['release_date']),
        song['album_id'] = row['album_id'],
        song['album_name'] = row['album'],
        song['year'] = row['album_year'],
        song['madeByArtists'] = row['artists'],

        song_collection.append(song)
        break
    return song_collection


"""
CREATE PLAYLIST COLLECTION

"""


def collection_of_playlist(coll_songs: list[dict]) -> list[dict]:
    playlist_collection = []
    for row in user_data:
        playlist = {}
        playlist['playlist_id'] = row['id']


        playlist_collection.append(playlist)

    return playlist_collection



"""
CREATE USERS COLLECTION

"""
def create_playlist_for_users_coll_random() -> list[dict]:
    max_elements=15
    list_size = random.randint(0, max_elements)
    playlist = []

    for _ in range(list_size):
        random_id = random.randint(0, len(songs_dataset) - 1)
        random_song = songs_dataset[random_id]
        random_pl_dict = {
            "song_id": random_song['id'],
        }
        if random_pl_dict in playlist:
            continue
        playlist.append(random_pl_dict)

    return playlist

def collection_of_users(coll_playlist: list[dict], coll_songs: list[dict]) -> list[dict]:
    user_collection = []
    for row in user_data:
        user = {}
        user['user_id'] = row['id']
        #user['playlist'] = playlist_of_users_rdn()
        #user['songs'] = playlist_of_users_rdn()

        user_collection.append(user)

    return user_collection

if __name__ == "__main__":
    song_collection = collection_of_song()
    print(song_collection)




