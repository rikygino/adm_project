import pandas as pd


def drop_columns(csv_file_path, columns_to_drop):
    df = pd.read_csv(csv_file_path)
    df.drop(columns=columns_to_drop, inplace=True)

    df.to_csv("../spotify_dataset.csv", index=False)

    print("csv modified")

if __name__ == "__main__":
    csv_file_path = "dataset.csv"
    columns_to_drop = ["key","loudness","mode","speechiness","acousticness","valence","time_signature"]
    drop_columns(csv_file_path, columns_to_drop)
