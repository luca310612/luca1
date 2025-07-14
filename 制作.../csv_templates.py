import pandas as pd
import csv

column_names = [
    "id", "code", "name", "address", "prefecture", "tel", "corporation", "director",
    "established", "bed_type_and_count", "facility_type",
    "col12", "col13", "col14", "col15", "col16", "col17", "col18", "col19", "col20", "col21", "col22", "col23", "col24"
]

input_csv = "csv/hokkaidou/hospital_hokkaidou_病院.csv" 
output_csv = "csv/hokkaidou/hospital_hokkaidou_病院.csv"

rows = []
with open(input_csv, encoding="utf-8") as f:
    reader = csv.reader(f)
    for row in reader:
        if len(row) < 24:
            row += [""] * (24 - len(row))
        elif len(row) > 24:
            row = row[:24]
        rows.append(row)

with open(output_csv, "w", encoding="utf-8-sig", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(column_names)
    writer.writerows(rows)

print(f"変換完了: {output_csv}")