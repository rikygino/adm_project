import ast
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

    df['release_date'] = pd.to_datetime(df['release_date'])
    df['release_date'] = df['release_date'].dt.strftime("%d-%m-%Y")
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
    # Selezione del 40% degli album
    album_list = df['album'].unique()
    num_albums = len(album_list)
    num_selected_albums = int(num_albums * 0.03)
    selected_albums = df[df['album'].isin(pd.Series(album_list).sample(num_selected_albums))]

    # Visualizzazione dei risultati
    print(selected_albums)

    return selected_albums


def song_date(df):
    # Filter rows based on release_date length less than 10 characters
    mask = df['release_date'].str.len() == 10
    filtered_df = df[mask]
    print(filtered_df.shape)
    # Drop rows with duplicate album_id values
    filtered_df = filtered_df.drop_duplicates(subset=['album_id'])
    filtered_df['release_date'] = pd.to_datetime(filtered_df['release_date'])
    filtered_df['release_date'] = filtered_df['release_date'].dt.strftime("%m/%d/%Y")

    return filtered_df


if __name__ == "__main__":
    csv_file_path = "tracks_features.csv"
    columns_to_drop = ["track_number", "disc_number", "energy", "key", "loudness", "mode", "speechiness",
                       "acousticness", "valence", "time_signature", "year", "instrumentalness", "liveness", "tempo"]
    dataset = pd.read_csv(csv_file_path)
    dataset = song_date(dataset)
    dataset = album_date(dataset)
    drop_columns(dataset, columns_to_drop)
    # Apply standardization function to 'artists_ids' column and 'artists'
    dataset['artists'] = dataset['artists'].apply(lambda x: standardize_values(x))
    dataset['artist_ids'] = dataset['artist_ids'].apply(lambda x: standardize_values(x))

    dataset = sub_dataset(dataset)
    dataset.to_csv("../spotify_dataset.csv", index=False)
    print("csv modified")
    print(dataset.shape)
