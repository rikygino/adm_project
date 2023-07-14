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


#def playlist_of_users_rdn() -> list[dict]:


def collection_of_users(coll_playlist: list[dict], coll_songs: list[dict]) -> list[dict]:
    user_collection = []
    for row in user_data:
        user = {}
        user['user_id'] = row['id']
        user['birthdate'] = date_to_BSON(row['birthday'])
        user['playlist'] = playlist_of_users_rdn()

        user_collection.append(user)

    return user_collection

def collection_of_playlist(coll_songs: list[dict]) -> list[dict]:
    playlist_collection = []
    for row in user_data:
        playlist = {}
        playlist['playlist_id'] = row['id']


        playlist_collection.append(playlist)

    return playlist_collection