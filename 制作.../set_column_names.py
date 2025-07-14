import pandas as pd
import csv

column_names = [
    "id", "code", "name", "address", "prefecture", "tel", "corporation", "director", "established", "bed_type_and_count", "facility_type",
    "col12", "col13", "col14", "col15", "col16", "col17", "col18", "col19", "col20", "col21", "col22", "col23"
]
column_names += [f"col{i}" for i in range(24, 1114)]
column_names += [f"hospital{i}" for i in range(1, 44)]

csv_path = "/Users/oomuraruka/制作.../change/コード内容別医療機関一覧表（医科）r07072/yamagata_hos.csv"

df = pd.read_csv(csv_path, header=None, low_memory=False, on_bad_lines='skip')

if len(column_names) < len(df.columns):
    column_names += [f"extra_col{i}" for i in range(len(column_names) + 1, len(df.columns) + 1)]

df.columns = column_names[:len(df.columns)]
df.to_csv(csv_path, index=False)
print("カラム名を付与して保存しました")

with open(csv_path, encoding="utf-8") as f:
    reader = csv.reader(f)
    for i, row in enumerate(reader, 1):
        if len(row) != 24:
            print(f"{i}行目: {len(row)}列 -> {row}")