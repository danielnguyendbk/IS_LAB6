import pandas as pd
import numpy as np

def clean_column_names(df):
    """
    Xóa khoảng trắng ở đầu và cuối tên các cột trong DataFrame.
    """
    df.columns = df.columns.str.strip()
    return df

