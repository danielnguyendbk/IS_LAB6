import pandas as pd
import numpy as np

def clean_column_names(df):
    """
    Xóa khoảng trắng ở đầu và cuối tên các cột trong DataFrame.
    """
    df.columns = df.columns.str.strip()
    return df

def handle_missing_values(df):
    """
    Thay thế các giá trị vô cực (np.inf) và thiếu (NaN) bằng median của từng cột.
    """
    df = df.replace([np.inf, -np.inf], np.nan)

    numeric_cols = df.select_dtypes(include=[np.number]).columns
    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].median())
    
    return df