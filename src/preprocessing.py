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

def drop_duplicates_and_zero_variance(df):
    """
    Xóa các dòng dữ liệu trùng lặp và các cột có phương sai bằng 0.
    """
    df = df.drop_duplicates()

    cols_to_keep = df.nunique() > 1
    df = df.loc[:, cols_to_keep]
    
    return df

def downcast_dtypes(df):
    """
    Ép kiểu dữ liệu (downcast) số nguyên và số thực để giảm thiểu mức tiêu thụ RAM.
    """
    for column in df.columns:
        if df[column].dtype == 'float64':
            df[column] = pd.to_numeric(df[column], downcast='float')
        elif df[column].dtype == 'int64':
            df[column] = pd.to_numeric(df[column], downcast='integer')
    return df

def run_preprocessing(df):
    """
    Hàm tổng hợp chạy toàn bộ pipeline làm sạch dữ liệu.
    """
    print("Bắt đầu chuẩn hóa tên cột...")
    df = clean_column_names(df)
    
    print("Bắt đầu xử lý giá trị inf và NaN...")
    df = handle_missing_values(df)
    
    print("Bắt đầu xóa dữ liệu trùng lặp và zero-variance...")
    df = drop_duplicates_and_zero_variance(df)
    
    print("Bắt đầu ép kiểu dữ liệu để giảm RAM...")
    df = downcast_dtypes(df)
    
    print("Tiền xử lý dữ liệu hoàn tất!")
    return df