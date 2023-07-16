import ast
import csv
import json

import numpy as np
import pandas as pd


def drop_columns(df, columns_to_drop):
    df.drop(columns=columns_to_drop, inplace=True)


def album_date(df):
    # Convert 'release_date' column to datetime with format '%Y'
    df['release_date'] = pd.to_datetime(df['release_date'])

    # Extract year from 'release_date' column
    df['album_year'] = df['release_date'].dt.year

    # Group by 'album_id' and calculate maximum year
    max_year = df.groupby('album_id')['album_year'].transform('max')

    # Assign the maximum year to the 'album_year' column
    df['album_year'] = max_year
    # Return the modified DataFrame
    return df


def set_to_year(date_obj):
    return date_obj.strftime("%Y")


def standardize_values(value):
    try:
        value_list = ast.literal_eval(value)
        if isinstance(value_list, list):
            return ", ".join(value_list)
        else:
            return value_list.strip("'")
    except (SyntaxError, ValueError):
        return value


def sub_dataset(df):
    # Selezione del 30% degli album
    album_list = df['album'].unique()
    num_albums = len(album_list)
    num_selected_albums = int(10) #np.ceil(num_albums * 0.0001)
    selected_albums = pd.Series(album_list).sample(num_selected_albums)

    # Filtraggio delle canzoni degli album selezionati
    selected_songs = df[df['album'].isin(selected_albums)]

    return selected_songs


def song_date(df):
    # Filter rows based on release_date length less than 10 characters
    mask = df['release_date'].str.len() == 10
    filtered_df = df[mask]

    return filtered_df


def song_id(dataset):
    dataset['id'] = range(1, len(dataset) + 1)
    return dataset

def manage_dataset():
    csv_file_path = "tracks_features.csv"
    columns_to_drop = ["artist_ids", "track_number", "disc_number", "energy", "key", "loudness", "mode", "speechiness",
                       "acousticness", "valence", "time_signature", "year", "instrumentalness", "liveness", "tempo"]
    dataset = pd.read_csv(csv_file_path)
    dataset = sub_dataset(dataset)
    dataset = song_id(dataset)
    dataset = song_date(dataset)
    dataset = album_date(dataset)

    drop_columns(dataset, columns_to_drop)

    # Apply standardization function to 'artists'
    dataset['artists'] = dataset['artists'].apply(lambda x: standardize_values(x))

    dataset.to_csv("../spotify_dataset.csv", index=False)
    #print("csv modified")
    print(dataset.shape)


artists = {"placeholder": 0}

def get_artists():
    return artists

def artists_to_list(row) -> list[dict]:
    artists_list = []
    combined_name = ''.join(row)
    names = combined_name.split(', ')
    for name in names:
        if name in artists:
            artist_id = artists[name]
        else:
            artist_id = max(artists.values()) + 1
            artists[name] = artist_id
        artists_list.append({
            "artist_id": artist_id,
            "artist_name": name
        })
    return artists_list


def read_music_data():
    filepath = '../spotify_dataset.csv'
    music = []
    with open(filepath, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            song = {
                'id': row['id'],
                'name': row['name'],
                'album': row['album'],
                'album_id': row['album_id'],
                'artists': artists_to_list(row['artists']),
                'explicit': row['explicit'],
                'danceability': row['danceability'],
                'duration_ms': row['duration_ms'],
                'release_date': str(row['release_date']),
                'album_year': row['album_year'],
            }
            music.append(song)
    return music


if __name__ == "__main__":
    manage_dataset()