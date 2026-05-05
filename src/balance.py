from collections import Counter

from imblearn.over_sampling import SMOTE
from imblearn.under_sampling import RandomUnderSampler
from sklearn.preprocessing import LabelEncoder

def encode_labels(y):
    """
    Đổi tên cuộc tấn công (chữ) thành số (0, 1, 2...).
    """
    le = LabelEncoder()
    return le.fit_transform(y), le

def get_balancing_steps(y, random_state=42):
    """
    Tạo các bước cân bằng dữ liệu để ném vào Pipeline.
    """
    class_counts = Counter(y)
    min_class_count = min(class_counts.values())

    over = None
    if min_class_count >= 2:
        k_neighbors = min(5, min_class_count - 1)
        over = SMOTE(
            sampling_strategy="not majority",
            random_state=random_state,
            k_neighbors=k_neighbors,
        )
    else:
        print("[WARNING] Too few samples in a class for SMOTE. Skipping oversampling.")

    # RandomUnderSampler: Cắt bớt dữ liệu lớp đa số (thường là BENIGN)
    under = RandomUnderSampler(
        sampling_strategy="not minority",
        random_state=random_state,
    )
    
    return over, under