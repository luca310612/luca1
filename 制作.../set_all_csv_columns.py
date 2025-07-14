import pandas as pd
import glob
import os

# 統一したいカラム名（24列分）
column_names = [
    "id", "code", "name", "address", "prefecture", "tel", "corporation", "director",
    "established", "bed_type_and_count", "facility_type",
    "col12", "col13", "col14", "col15", "col16", "col17", "col18", "col19", "col20", "col21", "col22", "col23", "col24"
]

# 対象ディレクトリ（必要に応じて変更）
target_dirs = [
    "csv/akita", "csv/yamagata", "csv/miyagi", "csv/iwate", "csv/hukusima", "csv/aomori", "csv/hokkaidou"
]
base_dir = os.path.dirname(__file__)

for tdir in target_dirs:
    csv_files = glob.glob(os.path.join(base_dir, tdir, "*.csv"))
    for csv_path in csv_files:
        # 列数が違う行はスキップ
        df = pd.read_csv(csv_path, header=None, dtype=str, encoding="utf-8", low_memory=False, on_bad_lines='skip')
        if len(df.columns) < 24:
            df = df.reindex(columns=range(24), fill_value="")
        elif len(df.columns) > 24:
            df = df.iloc[:, :24]
        df.columns = column_names
        df.to_csv(csv_path, index=False, encoding="utf-8-sig")
        print(f"{csv_path} をカラム統一・保存しました")