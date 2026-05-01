from imblearn.pipeline import Pipeline # Lưu ý dùng của imblearn để hỗ trợ SMOTE
from sklearn.preprocessing import StandardScaler

def build_preprocessing_pipeline(over, under):
    """
    Kết nối: Scaler -> SMOTE -> UnderSampler.
    """
    pipeline = Pipeline(steps=[
        # 1. Chuẩn hóa số liệu về cùng một thang đo (giống như format lại tiền tệ)
        ('scaler', StandardScaler()),
        
        # 2. Tăng mẫu thiểu số (SMOTE)
        ('over', over),
        
        # 3. Giảm mẫu đa số (UnderSampler)[cite: 1]
        ('under', under)
    ])
    return pipeline