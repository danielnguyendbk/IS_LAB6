# src/config.py

import os

# Root directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Data folder
DATA_DIR = os.path.join(BASE_DIR, "data")

# List of 8 CSV files (bạn sửa lại đúng tên file)
DATA_FILES = [
    "Friday-WorkingHours-Afternoon-DDos.pcap_ISCX.csv",
    "Friday-WorkingHours-Afternoon-PortScan.pcap_ISCX.csv",
    "Friday-WorkingHours-Morning.pcap_ISCX.csv",
    "Monday-WorkingHours.pcap_ISCX.csv",
    "Thursday-WorkingHours-Afternoon-Infilteration.pcap_ISCX.csv",
    "Thursday-WorkingHours-Morning-WebAttacks.pcap_ISCX.csv",
    "Tuesday-WorkingHours.pcap_ISCX.csv",
    "Wednesday-workingHours.pcap_ISCX.csv"
]

# Output merged file
MERGED_FILE = os.path.join(DATA_DIR, "merged_data.csv")