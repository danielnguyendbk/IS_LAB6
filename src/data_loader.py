# src/data_loader.py

import pandas as pd
import os
from src.config import DATA_DIR, DATA_FILES, MERGED_FILE


def load_single_file(file_path):
    print(f"[INFO] Loading: {file_path}")
    df = pd.read_csv(file_path)

    # Strip column names
    df.columns = df.columns.str.strip()

    return df


def load_and_merge_data():
    dataframes = []

    for file in DATA_FILES:
        file_path = os.path.join(DATA_DIR, file)

        if not os.path.exists(file_path):
            print(f"[WARNING] File not found: {file_path}")
            continue

        df = load_single_file(file_path)
        dataframes.append(df)

    print("[INFO] Merging all files...")
    merged_df = pd.concat(dataframes, ignore_index=True)

    print(f"[INFO] Final shape: {merged_df.shape}")

    return merged_df


def save_merged_data(df):
    df.to_csv(MERGED_FILE, index=False)
    print(f"[INFO] Saved merged file to {MERGED_FILE}")