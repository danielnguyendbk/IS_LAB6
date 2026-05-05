from imblearn.pipeline import Pipeline # Lưu ý dùng của imblearn để hỗ trợ SMOTE
from sklearn.preprocessing import StandardScaler

def build_preprocessing_pipeline(over, under):
    """
    Kết nối: Scaler -> SMOTE -> UnderSampler.
    """
    steps = [
        # 1. Chuẩn hóa số liệu về cùng một thang đo (giống như format lại tiền tệ)
        ('scaler', StandardScaler()),
    ]

    if over is not None:
        # 2. Tăng mẫu thiểu số (SMOTE)
        steps.append(('over', over))

    # 3. Giảm mẫu đa số (UnderSampler)[cite: 1]
    steps.append(('under', under))

    return Pipeline(steps=steps)