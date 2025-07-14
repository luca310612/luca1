import pandas as pd
import csv

def extract_hospital_data(csv_paths):
    hospital_data = []
    valid_departments = ["内", "外", "整", "小", "呼", "リハ", "精神", "糖尿病", "循環器", "消化器",
                         "脳外", "心外", "皮", "ひ", "産婦", "眼", "耳い", "放", "麻", "歯", "形", "病理"]

    for csv_path in csv_paths:
        df = pd.read_csv(
    csv_path,
    header=0,
    skip_blank_lines=True,
    low_memory=False,
    dtype=str,
    on_bad_lines='skip'
)
        df.rename(columns={
            "病院名": "name",
            "住所": "address",
            "診療科": "established",
            "レビューの数": "review"
        }, inplace=True)

        for _, row in df.iterrows():
            if pd.isna(row.get("name")) or pd.isna(row.get("address")) or pd.isna(row.get("established")):
                continue

            departments = row.get("established", "").split(",")
            filtered_departments = [dept.strip() for dept in departments if any(keyword in dept for keyword in valid_departments)]

            hospital = {
                "name": str(row.get("name", "")).strip(),
                "address": str(row.get("address", "")).strip(),
                "established": ", ".join(filtered_departments),
                "reviews": int(row.get("review", 0)) if pd.notna(row.get("review")) else 0,
            }
            hospital_data.append(hospital)
    return hospital_data

if __name__ == "__main__":
    csv_file_paths = [
    'csv/fukushima_hos.csv',
    'csv/hokkaidou_dent.csv',
    'csv/yamagata_hos.csv',
    'csv/yamagata_dent.csv',
    'csv/miyagi_hos.csv',
    'csv/miyagi_dent.csv',
    'csv/iwate_hos.csv',
    'csv/iwate_dent.csv',
    'csv/fukushima_hos.csv',
    'csv/fukushima_dent.csv',
    'csv/aomori_hos.csv',
    'csv/aomori_dent.csv',
]
    hospital_data = extract_hospital_data(csv_file_paths)
    print(hospital_data)