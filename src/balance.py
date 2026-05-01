from sklearn.preprocessing import LabelEncoder
from imblearn.over_sampling import SMOTE
from imblearn.under_sampling import RandomUnderSampler

def encode_labels(y):
    """
    Đổi tên cuộc tấn công (chữ) thành số (0, 1, 2...).
    """
    le = LabelEncoder()
    return le.fit_transform(y), le

def get_balancing_steps():
    """
    Tạo các bước cân bằng dữ liệu để ném vào Pipeline.
    """
    # SMOTE: Tự tạo thêm dữ liệu cho các lớp tấn công thiểu số (đạt 10% lớp đa số)
    over = SMOTE(sampling_strategy=0.1) 
    
    # RandomUnderSampler: Cắt bớt dữ liệu BENIGN (truy cập bình thường)
    under = RandomUnderSampler(sampling_strategy=0.5) 
    
    return over, under