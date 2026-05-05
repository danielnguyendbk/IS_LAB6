import difflib

import pandas as pd


SELECTED_FEATURES = [
    "Protocol", "Flow Duration", "Tot Fwd Pkts", "Tot Bwd Pkts",
    "TotLen Fwd Pkts", "TotLen Bwd Pkts", "Fwd Pkt Len Mean",
    "Bwd Pkt Len Mean", "Flow Byts/s", "Flow Pkts/s",
    "Pkt Len Mean", "Pkt Len Std", "SYN Flag Cnt",
    "ACK Flag Cnt", "FIN Flag Cnt", "RST Flag Cnt",
    "PSH Flag Cnt", "URG Flag Cnt",
]

REQUIRED_FEATURES = [
    feature for feature in SELECTED_FEATURES if feature != "Protocol"
]

_ALIAS_MAP = {
    "Total Fwd Packets": "Tot Fwd Pkts",
    "Total Backward Packets": "Tot Bwd Pkts",
    "Total Length of Fwd Packets": "TotLen Fwd Pkts",
    "Total Length of Bwd Packets": "TotLen Bwd Pkts",
    "Fwd Packet Length Mean": "Fwd Pkt Len Mean",
    "Bwd Packet Length Mean": "Bwd Pkt Len Mean",
    "Flow Bytes/s": "Flow Byts/s",
    "Flow Packets/s": "Flow Pkts/s",
    "Packet Length Mean": "Pkt Len Mean",
    "Packet Length Std": "Pkt Len Std",
    "SYN Flag Count": "SYN Flag Cnt",
    "ACK Flag Count": "ACK Flag Cnt",
    "FIN Flag Count": "FIN Flag Cnt",
    "RST Flag Count": "RST Flag Cnt",
    "PSH Flag Count": "PSH Flag Cnt",
    "URG Flag Count": "URG Flag Cnt",
}


def _apply_aliases(df):
    return df.rename(columns=_ALIAS_MAP)


def resolve_core_features(df):
    df = _apply_aliases(df)

    protocol_missing = "Protocol" not in df.columns
    if protocol_missing:
        print(
            "[WARNING] `Protocol` column is not available in this "
            "CIC-IDS2017 CSV version. Using 17 core features instead."
        )

    feature_list = REQUIRED_FEATURES if protocol_missing else SELECTED_FEATURES
    missing = [col for col in feature_list if col not in df.columns]

    return df, feature_list, missing, protocol_missing


def select_core_features(df):
    """
    Nhiệm vụ: Chỉ giữ lại 18 cột quan trọng nhất từ 79 cột ban đầu.
    """
    df, feature_list, missing, _ = resolve_core_features(df)
    if missing:
        for feature in missing:
            candidates = difflib.get_close_matches(
                feature,
                list(df.columns),
                n=5,
                cutoff=0.6,
            )
            if candidates:
                print(f"[INFO] Closest columns for '{feature}': {candidates}")
        raise ValueError(f"Missing required features: {missing}")
    return df[feature_list]