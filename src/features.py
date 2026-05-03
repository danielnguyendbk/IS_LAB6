import pandas as pd

def select_core_features(df):
    """
    Nhiệm vụ: Chỉ giữ lại 18 cột quan trọng nhất từ 79 cột ban đầu.
    """
    selected_features = [
        'Protocol', 'Flow Duration', 'Tot Fwd Pkts', 'Tot Bwd Pkts',
        'TotLen Fwd Pkts', 'TotLen Bwd Pkts', 'Fwd Pkt Len Mean',
        'Bwd Pkt Len Mean', 'Flow Byts/s', 'Flow Pkts/s',
        'Pkt Len Mean', 'Pkt Len Std', 'SYN Flag Cnt',
        'ACK Flag Cnt', 'FIN Flag Cnt', 'RST Flag Cnt',
        'PSH Flag Cnt', 'URG Flag Cnt'
    ]
    return df[selected_features]