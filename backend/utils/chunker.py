import pandas as pd
import os

def split_csv(file_path, chunk_size=1000):

    os.makedirs(
        "chunks",
        exist_ok=True
    )

    df = pd.read_csv(file_path)

    chunk_files = []

    for i in range(
        0,
        len(df),
        chunk_size
    ):

        chunk = df.iloc[
            i:i + chunk_size
        ]

        chunk_name = (
            f"chunks/chunk_{i//chunk_size + 1}.csv"
        )

        chunk.to_csv(
            chunk_name,
            index=False
        )

        chunk_files.append(
            chunk_name
        )

    return chunk_files