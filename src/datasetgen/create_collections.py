import time

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

artists = manipulation_dataset.get_artists()
artists.pop("placeholder")


def format_date(date: str) -> dict:
    if date == "": return {}
    millis = datetime.datetime.strptime(date, '%Y-%m-%d').timestamp() * 1000
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
            'users': liked_songs_from_users_random()
        }
        song_collection.append(song)
    return song_collection


def liked_songs_from_users_random() -> list[dict]:
    max_elements = 6
    users_likes = []
    list_size = random.randint(0, max_elements)
    for _ in range(list_size):
        random_id = random.randint(0, len(user_data) - 1)
        random_user = user_data[random_id]
        random_likes = {
            "user_id": random_user['id'],
            'birthdate': format_date(random_user['birthdate']),
        }
        if random_likes in users_likes:
            continue
        users_likes.append(random_likes)

    return users_likes


"""
CREATE PLAYLIST COLLECTION

"""


def song_of_playlist_random() -> list[dict]:
    max_elements = 6
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
    max_elements = 3
    playlist_id = 0
    playlist_collection = []
    for row in user_data:
        number_of_playlists = random.randint(0, max_elements)
        for index in range(number_of_playlists):
            playlist = {
                'playlist_id': playlist_id,
                'user_id': row['id'],
                'username': row['username'],
                'songs': song_of_playlist_random(),
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
            name_playlist = playlist['username'] + "_" + str(playlist['playlist_id'])
            playlist_user = {
                'playlist_id': playlist['playlist_id'],
                'playlist_name': name_playlist,
                'songs': get_songs(playlist['songs']),
            }
            playlist_of_users.append(playlist_user)

    return playlist_of_users


def get_liked_songs_from_user(coll_songs: list[dict], row) -> list[dict]:
    liked_songs = []
    for song in coll_songs:
        for id_user in song['users']:
            if row['id'] == id_user['user_id']:
                song_liked = {
                    'song_id': song['song_id'],
                    'title': song['title'],
                }
                liked_songs.append(song_liked)

    return liked_songs



def collection_of_users(coll_playlist: list[dict], coll_songs: list[dict]) -> list[dict]:
    user_collection = []

    for row in user_data:
        user = {
            'user_id': row['id'],
            'playlists': playlist_of_users_random(coll_playlist, row),
            'likedSongs': get_liked_songs_from_user(coll_songs, row),
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
    return (7 * account_id + 1) % len(account_data)


def assign_left_users(coll_user_copy: list[dict], account_collection: list[dict]):
    while len(coll_user_copy) > 0:
        for user in coll_user_copy:
            account_user = {
                "user_id": user['user_id'],
                "username": get_username(user['user_id']),
                "playlists": user['playlists'],
            }
            account_random = random.choice(account_collection)
            if len(account_random['users']) < 4:
                account_random['users'].append(account_user)
                coll_user_copy.remove(user)

def get_username(user_id):
    for user in user_data:
        if user['id'] == user_id:
            return user['username']


def get_account_users(coll_users: list[dict]) -> list[dict]:
    min_users = 1
    max_users = 2
    account_user_number = random.randint(min_users, max_users)
    account_users = []
    for _ in range(account_user_number):
        random_user_index = random.randint(0, len(coll_users) - 1)
        random_user = coll_users.pop(random_user_index)
        account_user = {
            'user_id': random_user['user_id'],
            'username': get_username(random_user['user_id']),
            'playlists': random_user['playlists'],
        }
        account_users.append(account_user)

    return account_users


def gen_subscription_type() -> str:
    subscription_types = {
        1: "Free",
        2: "Standard",
        3: "Premium",
    }
    return subscription_types[random.randint(1, 3)]


def collection_of_accounts(coll_users: list[dict]) -> list[dict]:
    coll_user_copy = coll_users.copy()
    account_collection = []
    for row in account_data:
        account = {
            'account_id': row['id'],
            'email': row['email'],
            'sub_id': gen_subscription_id(row['id']),
            'start_date': format_date(generate_random_date("2020-01-01", "2023-07-10")),
            'subscription_type': gen_subscription_type(),
            'users': get_account_users(coll_user_copy),
        }
        account_collection.append(account)
    assign_left_users(coll_user_copy, account_collection)

    return account_collection


"""
CREATE SUBSCRIPTION COLLECTION

"""


def get_profile(account_id):
    for row in account_data:
        if row['id'] == account_id:
            name = row['name']
            surname = row['surname']
    return name, surname


def get_expiration_date(startingdate):
    value = int(startingdate['$date']['$numberLong'])
    timestamp = value / 1000
    dt = datetime.datetime.fromtimestamp(timestamp)

    interval = random.choice(['month', '6months', 'year'])

    if interval == 'month':
        new_date = dt + datetime.timedelta(days=30)
    elif interval == '6months':
        new_date = dt + datetime.timedelta(days=180)
    elif interval == 'year':
        new_date = dt + datetime.timedelta(days=365)

    formatted_date = new_date.strftime("%Y-%m-%d")
    dt = dt.strftime("%Y-%m-%d")

    return dt + " " + formatted_date


def collection_of_subscriptions(coll_accounts: list[dict]) -> list[dict]:
    subscriptions_collection = []
    for account in coll_accounts:
        acc_name, acc_surname = get_profile(account['account_id'])
        subscription = {
            'account_id': account['account_id'],
            'expiration_date': get_expiration_date(account['start_date']),
            'name': acc_name,
            'surname': acc_surname,
        }
        subscriptions_collection.append(subscription)
    return subscriptions_collection


"""
CREATE ARTIST COLLECTION

"""


def get_songs_artist(coll_songs: list[dict], id):
    artists_songs = []
    for song in coll_songs:
        for art in song['madeByArtists']:
            if id == art['artist_id']:
                song_of_artist = {
                    'song_id': song['song_id'],
                    'title': song['title'],
                    'album_id': song['album_id'],
                    'album_name': song['album_name'],
                    'year': song['year'],
                    'users': song['users']
                }
                artists_songs.append(song_of_artist)
    return artists_songs


def collection_of_artists(coll_songs: list[dict]) -> list[dict]:
    artists_collection = []
    for id in artists.values():
        artist = {
            'artist_id': id,
            'songs': get_songs_artist(coll_songs, id)
        }
        artists_collection.append(artist)
    return artists_collection


"""
CREATE ALBUM COLLECTION

"""


def get_songs_of_album(coll_songs, row):
    songs_of_album = []
    for song in coll_songs:
        if row['album_id'] == song['album_id']:
            song = {
                'song_id': song['song_id'],
                'title': song['title'],
                'duration': song['duration'],
                'createdByArtists': song['madeByArtists'],
            }
            songs_of_album.append(song)

    return songs_of_album


def collection_of_albums(coll_songs: list[dict]) -> list[dict]:
    albums_collection = []
    for row in songs_dataset:
        album = {
            'album_id': row['album_id'],
            'songs': get_songs_of_album(coll_songs, row)
        }
        albums_collection.append(album)
    return albums_collection


def convert_collection_to_json(collection: list[dict], filename: str) -> None:
    with open(filename, 'w') as jsonfile:
        jsonfile.write(json.dumps(collection))


def calculate_execution_time(start_time, end_time):
    execution_time = end_time - start_time

    minutes = int(execution_time // 60)
    seconds = int(execution_time % 60)

    return minutes, seconds


def collections_to_json(songs_collection, playlists_collection, users_collection, accounts_collection,
                        subscriptions_collection, artists_collection, albums_collection):

    print("Conversions to JSON started!")
    convert_collection_to_json(songs_collection, "songs_collection.json")
    convert_collection_to_json(playlists_collection, "playlists_collection.json")
    convert_collection_to_json(users_collection, "users_collection.json")
    convert_collection_to_json(accounts_collection, "accounts_collection.json")
    convert_collection_to_json(subscriptions_collection, "subscriptions_collection.json")
    convert_collection_to_json(artists_collection, "artists_collection.json")
    convert_collection_to_json(albums_collection, "albums_collection.json")
    print("Conversions to JSON done!")

if __name__ == "__main__":
    print("Creating songs_collection")
    start_time1 = time.time()
    songs_collection = collection_of_song()
    end_time1 = time.time()
    print("--> songs_collection created with time:", calculate_execution_time(start_time1, end_time1))

    print("Creating playlists_collection")
    start_time2 = time.time()
    playlists_collection = collection_of_playlist()
    end_time2 = time.time()
    print("--> playlists_collection created with time:", calculate_execution_time(start_time2, end_time2))

    print("Creating users_collection")
    start_time3 = time.time()
    users_collection = collection_of_users(playlists_collection, songs_collection)
    end_time3 = time.time()
    print("--> users_collection created with time:", calculate_execution_time(start_time3, end_time3))

    print("Creating accounts_collection")
    start_time4 = time.time()
    accounts_collection = collection_of_accounts(users_collection)
    end_time4 = time.time()
    print("--> accounts_collection created with time:", calculate_execution_time(start_time4, end_time4))

    print("Creating subscriptions_collection")
    start_time5 = time.time()
    subscriptions_collection = collection_of_subscriptions(accounts_collection)
    end_time5 = time.time()
    print("--> subscriptions_collection created with time:", calculate_execution_time(start_time5, end_time5))

    print("Creating artists_collection")
    start_time6 = time.time()
    artists_collection = collection_of_artists(songs_collection)
    end_time6 = time.time()
    print("--> artists_collection created with time:", calculate_execution_time(start_time6, end_time6))

    print("Creating albums_collection")
    start_time7 = time.time()
    albums_collection = collection_of_albums(songs_collection)
    end_time7 = time.time()
    print("--> albums_collection created with time:", calculate_execution_time(start_time7, end_time7))

    collections_to_json(songs_collection, playlists_collection, users_collection,
                        accounts_collection, subscriptions_collection, artists_collection, albums_collection)
