import pandas as pd
from sklearn.preprocessing import LabelEncoder

def select_core_features(df):
    """
    Nhiệm vụ: Chỉ giữ lại 18 cột quan trọng và cột Label.
    """
    selected_features = [
        'Protocol', 'Flow Duration', 'Tot Fwd Pkts', 'Tot Bwd Pkts',
        'TotLen Fwd Pkts', 'TotLen Bwd Pkts', 'Fwd Pkt Len Mean',
        'Bwd Pkt Len Mean', 'Flow Byts/s', 'Flow Pkts/s',
        'Pkt Len Mean', 'Pkt Len Std', 'SYN Flag Cnt',
        'ACK Flag Cnt', 'FIN Flag Cnt', 'RST Flag Cnt',
        'PSH Flag Cnt', 'URG Flag Cnt'
    ]
    
    # Kiểm tra xem cột Label có trong df không rồi mới lấy, tránh lỗi
    columns_to_keep = [col for col in selected_features if col in df.columns]
    if 'Label' in df.columns:
        columns_to_keep.append('Label')
        
    return df[columns_to_keep]

def encode_labels(df):
    """
    Nhiệm vụ: Chuyển đổi nhãn từ dạng chữ (Benign, Bot...) sang số (0, 1...).
    """
    if 'Label' in df.columns:
        le = LabelEncoder()
        df['Label'] = le.fit_transform(df['Label'])
        return df, le
    return df, None