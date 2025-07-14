import pandas as pd

column_names = [
    "id", "code", "name", "address", "tel", "corporation", "director", "established", "bed_type_and_count", "facility_type"
]
column_names += [f"col{i}" for i in range(len(column_names), 1179)]

input_csv = "/Users/oomuraruka/制作.../csv/hospital_deta_aomori.csv"
output_csv = "/Users/oomuraruka/制作.../csv/hospital_deta_aomori.csv"
df = pd.read_csv(input_csv, header=None, low_memory=False)

df.columns = column_names[:len(df.columns)]
df.to_csv(output_csv, index=False)
print("カラム名を付与して保存しました")