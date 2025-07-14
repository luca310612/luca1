import csv
import re
import pandas as pd

csv_path = "/Users/oomuraruka/制作.../csv/yamagata/山形県-表1.csv"

# dialect検出＋読み込み（最初からこれを使う）
with open(csv_path, newline='', encoding='utf-8-sig') as csvfile:
    dialect = csv.Sniffer().sniff(csvfile.read(1024))
    csvfile.seek(0)
    df = pd.read_csv(csvfile, header=None, dtype=str, dialect=dialect)

def add_commas_before_zip(address):
    if pd.isna(address):
        return address
    m = re.search(r'〒', address)
    if m:
        idx = m.start()
        return address[:idx] + ',,,,,,,' + address[idx:]
    return address

df[3] = df[3].apply(add_commas_before_zip)

print("郵便番号の前にカンマを追加しました")