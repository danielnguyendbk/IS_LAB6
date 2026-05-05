import os

import pandas as pd

from src.config import DATA_FILES, DATA_RAW_DIR, MERGED_FILE
from src.data_loader import load_single_file, merge_raw_csvs
from src.features import resolve_core_features


def _raw_csvs_complete():
    raw_paths = [os.path.join(DATA_RAW_DIR, file) for file in DATA_FILES]
    return all(os.path.exists(path) for path in raw_paths)


def validate_dataframe(df, source_label="dataset"):
    print(f"[INFO] Validating columns for {source_label}...")

    print(f"[INFO] Rows: {len(df)} | Columns: {len(df.columns)}")

    if "Label" not in df.columns:
        print("[FAIL] Missing required column: Label")
        return False

    _, feature_list, missing, protocol_missing = resolve_core_features(df)
    if protocol_missing:
        print(
            "[WARNING] `Protocol` column is not available in this "
            "CIC-IDS2017 CSV version. Using 17 core features instead."
        )

    if missing:
        print(f"[FAIL] Missing required features: {missing}")
        return False

    print(f"[PASS] Required features present: {len(feature_list)}")
    return True


def main():
    print("===== DATASET VALIDATION =====")

    if _raw_csvs_complete():
        print("[INFO] Raw CSVs detected in data/raw/. Merging to data/merged_dataset.csv...")
        merged_df = merge_raw_csvs(MERGED_FILE)
        if merged_df is None:
            print("[FAIL] Could not merge raw CSV files.")
            return
        validate_dataframe(merged_df, source_label="data/merged_dataset.csv")
        return

    if os.path.exists(MERGED_FILE):
        df = load_single_file(MERGED_FILE)
        validate_dataframe(df, source_label="data/merged_dataset.csv")
        return

    print(
        "[FAIL] No dataset found. Please place the 8 raw CIC-IDS2017 CSV files in "
        "data/raw/ or provide data/merged_dataset.csv."
    )


if __name__ == "__main__":
    main()
