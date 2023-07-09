import ast
import pandas as pd

def drop_columns(df, columns_to_drop):
    df.drop(columns=columns_to_drop, inplace=True)

def album_date(df):
    df['year'] = pd.to_datetime(df['year'])
    df['year'] = df['year'].apply(set_to_year)
    df['album_year'] = pd.NaT
    df['album_year'] = df.groupby('album')['year'].transform('max')

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
    # Selezione del 40% degli album
    album_list = df['album'].unique()
    num_albums = len(album_list)
    num_selected_albums = int(num_albums * 0.05)
    selected_albums = df[df['album'].isin(pd.Series(album_list).sample(num_selected_albums))]

    # Visualizzazione dei risultati
    print(selected_albums)

    return selected_albums

if __name__ == "__main__":
    csv_file_path = "tracks_features.csv"
    columns_to_drop = ["track_number", "disc_number", "energy", "key", "loudness", "mode", "speechiness",
                       "acousticness", "valence", "time_signature", "year", "release_date"]
    dataset = pd.read_csv(csv_file_path)
    album_date(dataset)
    drop_columns(dataset, columns_to_drop)
    # Apply standardization function to 'artists_ids' column and 'artists'
    dataset['artists'] = dataset['artists'].apply(lambda x: standardize_values(x))
    dataset['artist_ids'] = dataset['artist_ids'].apply(lambda x: standardize_values(x))

    dataset = sub_dataset(dataset)
    dataset.to_csv("../spotify_dataset.csv", index=False)
    print("csv modified")
    print(dataset.shape)
