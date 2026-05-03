import pandas as pd
import numpy as np
from src.features import select_core_features, encode_labels
from src.balance import scale_features, balance_data

def preprocess_pipeline(df_train, df_test):
    """
    Pipeline xử lý dữ liệu chuẩn từ A-Z.
    Đảm bảo tính nhất quán giữa Train và Test.
    """
    # 1. Xử lý giá trị vô cực hoặc lỗi (thường gặp trong dữ liệu mạng)
    df_train = df_train.replace([np.inf, -np.inf], np.nan).dropna()
    df_test = df_test.replace([np.inf, -np.inf], np.nan).dropna()

    # 2. Lọc 18 Core Features
    df_train = select_core_features(df_train)
    df_test = select_core_features(df_test)

    # 3. Mã hóa nhãn (Label Encoder)
    # Fit encoder trên tập Train và transform trên cả Train và Test
    df_train, le = encode_labels(df_train)
    
    if 'Label' in df_test.columns:
        df_test['Label'] = le.transform(df_test['Label'])

    # 4. Tách Features (X) và Target (y)
    X_train = df_train.drop(columns=['Label'])
    y_train = df_train['Label']
    
    X_test = df_test.drop(columns=['Label']) if 'Label' in df_test.columns else df_test
    y_test = df_test['Label'] if 'Label' in df_test.columns else None

    # 5. Cân bằng dữ liệu (Chỉ áp dụng trên tập Train!)
    X_train_balanced, y_train_balanced = balance_data(X_train, y_train)

    # 6. Chuẩn hóa dữ liệu (Scaling)
    X_train_final, X_test_final, scaler = scale_features(X_train_balanced, X_test)

    return X_train_final, y_train_balanced, X_test_final, y_test, le, scaler