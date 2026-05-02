"""
Real-time Alert Generation Module
Author: Thành

This module is responsible for:
- Saving/loading the best Random Forest model
- Receiving a single network flow input
- Predicting whether the flow is BENIGN or attack
- Generating Suricata-style alert messages
- Optionally writing alerts to alerts.log
"""

from __future__ import annotations

import os
from datetime import datetime
from typing import Any, Dict, Tuple

import joblib
import numpy as np
import pandas as pd


PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODELS_DIR = os.path.join(PROJECT_ROOT, "models")
DEFAULT_MODEL_PATH = "models/best_model.pkl"
DEFAULT_ALERT_LOG = "alerts.log"
MODEL_NOT_FOUND_MESSAGE = (
    "Best model not found. Please train and save Random Forest model first."
)


SELECTED_FEATURES = [
    "Protocol", "Flow Duration", "Tot Fwd Pkts", "Tot Bwd Pkts",
    "TotLen Fwd Pkts", "TotLen Bwd Pkts", "Fwd Pkt Len Mean",
    "Bwd Pkt Len Mean", "Flow Byts/s", "Flow Pkts/s",
    "Pkt Len Mean", "Pkt Len Std", "SYN Flag Cnt",
    "ACK Flag Cnt", "FIN Flag Cnt", "RST Flag Cnt",
    "PSH Flag Cnt", "URG Flag Cnt"
]


def _resolve_project_path(path: str | os.PathLike[str]) -> str:
    """
    Resolve repository-relative paths while still accepting absolute paths.
    """
    path = os.fspath(path)
    if os.path.isabs(path):
        return path
    return os.path.join(PROJECT_ROOT, path)


def _resolve_model_path(model_path: str | os.PathLike[str]) -> str:
    """
    Resolve model paths. A bare filename is treated as inside models/.
    """
    model_path = os.fspath(model_path)
    if os.path.isabs(model_path):
        return model_path
    if os.path.dirname(model_path):
        return _resolve_project_path(model_path)
    return os.path.join(MODELS_DIR, model_path)


def save_best_model(
    model: Any,
    model_path: str | os.PathLike[str] = DEFAULT_MODEL_PATH,
    label_encoder: Any = None,
    scaler: Any = None,
    filename: str | os.PathLike[str] | None = None,
) -> str:
    """
    Save the trained best model bundle using joblib.

    The bundle may include:
    - model: trained Random Forest model
    - label_encoder: fitted LabelEncoder
    - scaler: fitted StandardScaler

    Backward compatible:
    - save_best_model(model, model_path="models/best_model.pkl")
    - save_best_model(model, label_encoder, scaler)
    - save_best_model(model, label_encoder, scaler, filename="best_model.pkl")
    """
    if not isinstance(model_path, (str, bytes, os.PathLike)):
        legacy_label_encoder = model_path
        legacy_scaler = label_encoder
        model_path = DEFAULT_MODEL_PATH
        label_encoder = legacy_label_encoder
        scaler = legacy_scaler

    if filename is not None:
        model_path = filename

    resolved_model_path = _resolve_model_path(model_path)
    os.makedirs(os.path.dirname(resolved_model_path), exist_ok=True)

    bundle = {
        "model": model,
        "label_encoder": label_encoder,
        "scaler": scaler,
    }

    joblib.dump(bundle, resolved_model_path)
    print(f"[INFO] Best model saved to: {resolved_model_path}")
    return resolved_model_path


def load_model(model_path: str = DEFAULT_MODEL_PATH) -> Any:
    """
    Load the saved best model.

    Raises:
        FileNotFoundError: if models/best_model.pkl does not exist.
    """
    resolved_model_path = _resolve_model_path(model_path)
    if not os.path.exists(resolved_model_path):
        raise FileNotFoundError(MODEL_NOT_FOUND_MESSAGE)

    return joblib.load(resolved_model_path)


def load_best_model(filename: str | os.PathLike[str] = DEFAULT_MODEL_PATH) -> Any:
    """
    Backward-compatible wrapper for the previous load_best_model(filename) API.
    """
    return load_model(filename)


def prepare_single_flow(flow_input: Dict[str, Any] | pd.DataFrame) -> pd.DataFrame:
    """
    Convert a single flow input into a DataFrame with the correct 18 features.

    Args:
        flow_input: dict or pandas DataFrame with one row.

    Returns:
        DataFrame with columns ordered by SELECTED_FEATURES.

    Raises:
        ValueError: if required features are missing or DataFrame has more than 1 row.
        TypeError: if input type is invalid.
    """
    if isinstance(flow_input, dict):
        df_flow = pd.DataFrame([flow_input])
    elif isinstance(flow_input, pd.DataFrame):
        df_flow = flow_input.copy()
    else:
        raise TypeError("flow_input must be a dict or a pandas DataFrame.")

    if len(df_flow) != 1:
        raise ValueError("flow_input must contain exactly one network flow.")

    missing_features = [col for col in SELECTED_FEATURES if col not in df_flow.columns]
    if missing_features:
        raise ValueError(
            "Missing required feature(s): "
            + ", ".join(missing_features)
        )

    df_flow = df_flow[SELECTED_FEATURES]

    df_flow = df_flow.replace([np.inf, -np.inf], np.nan)
    df_flow = df_flow.fillna(0)

    return df_flow


def _unpack_model_bundle(model_or_bundle: Any) -> Tuple[Any, Any, Any]:
    """
    Support both:
    - a raw sklearn model
    - a dict bundle: {"model": ..., "label_encoder": ..., "scaler": ...}
    """
    if isinstance(model_or_bundle, dict):
        model = model_or_bundle.get("model")
        label_encoder = model_or_bundle.get("label_encoder")
        scaler = model_or_bundle.get("scaler")
    else:
        model = model_or_bundle
        label_encoder = None
        scaler = None

    if model is None:
        raise ValueError("Model bundle does not contain a valid model.")

    return model, label_encoder, scaler


def _decode_prediction(prediction: Any, label_encoder: Any = None) -> str:
    """
    Convert encoded prediction back to original label if LabelEncoder is available.
    """
    if label_encoder is not None:
        try:
            if isinstance(prediction, (int, np.integer)):
                return str(label_encoder.inverse_transform([prediction])[0])
        except Exception:
            pass

    return str(prediction)


def _get_confidence(model: Any, X: Any) -> float | None:
    """
    Return max prediction probability if the model supports predict_proba.
    """
    if hasattr(model, "predict_proba"):
        try:
            probabilities = model.predict_proba(X)[0]
            return float(np.max(probabilities))
        except Exception:
            return None

    return None


def _flow_to_dict(flow_input: Dict[str, Any] | pd.DataFrame) -> Dict[str, Any]:
    if isinstance(flow_input, pd.DataFrame):
        if len(flow_input) != 1:
            raise ValueError("flow_input must contain exactly one network flow.")
        return flow_input.iloc[0].to_dict()
    if isinstance(flow_input, dict):
        return flow_input
    raise TypeError("flow_input must be a dict or a pandas DataFrame.")


def _get_destination_port(flow_input: Dict[str, Any] | pd.DataFrame) -> Any:
    raw_flow = _flow_to_dict(flow_input)
    for key in ("Destination Port", "Dst Port", "dst_port"):
        if key in raw_flow and not pd.isna(raw_flow[key]):
            return raw_flow[key]
    return "N/A"


def generate_alert(
    predicted_label: str | Dict[str, Any] | pd.DataFrame,
    flow_input: Dict[str, Any] | pd.DataFrame | str,
    confidence: float | None = None,
    log_file: str = DEFAULT_ALERT_LOG,
    write_log: bool = True,
    write_to_log: bool | None = None,
) -> str:
    """
    Generate a Suricata-style alert message.

    If predicted label is BENIGN, return an info message.
    If predicted label is not BENIGN, return and optionally log an alert.
    """
    if write_to_log is not None:
        write_log = write_to_log

    if isinstance(predicted_label, (dict, pd.DataFrame)) and isinstance(flow_input, str):
        predicted_label, flow_input = flow_input, predicted_label

    predicted_label = str(predicted_label)

    if predicted_label.strip().upper() == "BENIGN":
        message = "[INFO] Normal traffic detected."
        print(message)
        return message

    destination_port = _get_destination_port(flow_input)
    message = (
        f"[ALERT] Suspicious traffic detected: {predicted_label}. "
        f"Destination Port: {destination_port}."
    )

    print(message)

    if write_log:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        resolved_log_file = _resolve_project_path(log_file)
        os.makedirs(os.path.dirname(resolved_log_file), exist_ok=True)
        with open(resolved_log_file, "a", encoding="utf-8") as file:
            file.write(f"{timestamp} {message}\n")

    return message


def predict_single_flow(
    flow_input: Dict[str, Any] | pd.DataFrame,
    model: Any = None,
    model_path: str = DEFAULT_MODEL_PATH,
    write_log: bool = True,
) -> Tuple[str, str]:
    """
    Predict one real-time network flow.

    Args:
        flow_input: dict or DataFrame containing one network flow.
        model: optional model or model bundle. If None, load from model_path.
        model_path: path to best_model.pkl.
        write_log: whether to append attack alerts to alerts.log.

    Returns:
        predicted_label, alert/info message
    """
    model_or_bundle = model if model is not None else load_model(model_path)
    clf, label_encoder, scaler = _unpack_model_bundle(model_or_bundle)

    df_flow = prepare_single_flow(flow_input)

    X = scaler.transform(df_flow) if scaler is not None else df_flow

    raw_prediction = clf.predict(X)[0]
    predicted_label = _decode_prediction(raw_prediction, label_encoder)

    confidence = _get_confidence(clf, X)

    message = generate_alert(
        predicted_label=predicted_label,
        flow_input=flow_input,
        confidence=confidence,
        write_log=write_log,
    )

    return predicted_label, message


def demo_realtime_prediction() -> None:
    """
    Demo function for real-time IDS prediction.
    Run with:
        python -m src.realtime_alert
    """
    sample_flow = {
        "Protocol": 6,
        "Flow Duration": 120000,
        "Tot Fwd Pkts": 10,
        "Tot Bwd Pkts": 8,
        "TotLen Fwd Pkts": 500,
        "TotLen Bwd Pkts": 300,
        "Fwd Pkt Len Mean": 50.0,
        "Bwd Pkt Len Mean": 37.5,
        "Flow Byts/s": 6666.7,
        "Flow Pkts/s": 150.0,
        "Pkt Len Mean": 44.4,
        "Pkt Len Std": 12.5,
        "SYN Flag Cnt": 1,
        "ACK Flag Cnt": 8,
        "FIN Flag Cnt": 0,
        "RST Flag Cnt": 0,
        "PSH Flag Cnt": 2,
        "URG Flag Cnt": 0,
        "Destination Port": 80,
    }

    try:
        predicted_label, message = predict_single_flow(sample_flow, write_log=True)
        print("\nPrediction result:")
        print(f"Label: {predicted_label}")
        print(f"Message: {message}")
    except FileNotFoundError as error:
        print(f"[ERROR] {error}")
        print("Please run the training pipeline first and save the Random Forest model.")
    except Exception as error:
        print(f"[ERROR] Real-time prediction failed: {error}")


# Backward-compatible demo name if README or main.py already imports this
def run_realtime_demo(model_bundle=None, n_samples: int = 5, write_to_log: bool = True) -> None:
    """
    Simulate multiple real-time network flows.
    """
    for i in range(n_samples):
        print(f"\n[Flow #{i + 1}]")
        sample_flow = {
            "Protocol": 6,
            "Flow Duration": 120000 + i * 1000,
            "Tot Fwd Pkts": 10,
            "Tot Bwd Pkts": 8,
            "TotLen Fwd Pkts": 500,
            "TotLen Bwd Pkts": 300,
            "Fwd Pkt Len Mean": 50.0,
            "Bwd Pkt Len Mean": 37.5,
            "Flow Byts/s": 6666.7,
            "Flow Pkts/s": 150.0,
            "Pkt Len Mean": 44.4,
            "Pkt Len Std": 12.5,
            "SYN Flag Cnt": 1,
            "ACK Flag Cnt": 8,
            "FIN Flag Cnt": 0,
            "RST Flag Cnt": 0,
            "PSH Flag Cnt": 2,
            "URG Flag Cnt": 0,
            "Destination Port": 80,
        }

        predict_single_flow(
            sample_flow,
            model=model_bundle,
            write_log=write_to_log,
        )


if __name__ == "__main__":
    demo_realtime_prediction()
