import pandas as pd
import re

csv_path = "/Users/oomuraruka/制作.../change/コード内容別医療機関一覧表（医科）r07072/miyagi_hos.csv"
df = pd.read_csv(csv_path, header=None, dtype=str)

def add_punctuation(address):
    if pd.isna(address):
        return address
    m = re.search(r'〒.{8}', address)
    if m:
        idx = m.end()
        return address[:idx] + ',' + address[idx:]
    return address

df[3] = df[3].apply(add_punctuation)

with open(csv_path, 'w', encoding='utf-8-sig') as f:
    for row in df.itertuples(index=False, name=None):
        f.write(','.join("" if pd.isna(x) else str(x) for x in row) + '\n')

print("郵便番号の9文字後ろにカンマのみ追加して保存しました")

