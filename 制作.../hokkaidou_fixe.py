import pandas as pd
import re

def parse_code_column(code_str):
    """
    複雑なcode列を解析して分割する
    例: "01 / (05-1248 / 3214-9 / 6)" -> ["01", "1248", "6"]
    """
    if pd.isna(code_str) or code_str == "":
        return ["", "", ""]
    
    code_str = str(code_str).strip()
    
    pattern1 = r'(\d+)\s*/\s*\((\d+)-(\d+)\s*/\s*\d+-(\d+)\s*/\s*(\d+)\)'
    match1 = re.match(pattern1, code_str)
    if match1:
        code1 = match1.group(1)  # 01
        code2 = match1.group(3)  # 1248
        code3 = match1.group(5)  # 6
        return [code1, code2, code3]
    
    pattern2 = r'(\d+),(\d+),(\d+)'
    match2 = re.match(pattern2, code_str)
    if match2:
        return [match2.group(1), match2.group(2), match2.group(3)]
    
    pattern3 = r'^(\d+)$'
    match3 = re.match(pattern3, code_str)
    if match3:
        return [match3.group(1), "", ""]
    
    if ',' in code_str:
        parts = code_str.split(',')
        if len(parts) >= 3:
            return [parts[0].strip(), parts[1].strip(), parts[2].strip()]
        elif len(parts) == 2:
            return [parts[0].strip(), parts[1].strip(), ""]
        else:
            return [parts[0].strip(), "", ""]
    
    parts = re.findall(r'\d+', code_str)
    if len(parts) >= 3:
        return [parts[0], parts[1], parts[2]]
    elif len(parts) == 2:
        return [parts[0], parts[1], ""]
    elif len(parts) == 1:
        return [parts[0], "", ""]
    else:
        return ["", "", ""]

def clean_csv_data(input_file, output_file=None):
    """
    CSVデータを読み込み、code列を分割して整理する
    """
    df = pd.read_csv(input_file, dtype=str)
    
    if 'code' in df.columns:
        code_parts = df['code'].apply(parse_code_column)
        
        df['code_1'] = [parts[0] for parts in code_parts]
        df['code_2'] = [parts[1] for parts in code_parts]
        df['code_3'] = [parts[2] for parts in code_parts]
        
        df = df.drop('code', axis=1)
        
        cols = df.columns.tolist()
        if 'id' in cols:
            id_idx = cols.index('id')
            new_cols = cols[:id_idx+1] + ['code_1', 'code_2', 'code_3'] + [col for col in cols[id_idx+1:] if col not in ['code_1', 'code_2', 'code_3']]
            df = df[new_cols]
    
    # 結果を保存
    if output_file:
        df.to_csv(output_file, index=False, encoding='utf-8')
        print(f"整理されたデータを {output_file} に保存しました")
    
    return df

def process_sample_data():
    """
    サンプルデータでテスト
    """
    sample_data = [
        "01 / (05-1248 / 3214-9 / 6)",
        "01,1274,5",
        "01,1342,0",
        "01,1353,7",
        "01,1368,5",
        "01,1371,9",
        "01,1398,2"
    ]
    
    print("サンプルデータの変換テスト:")
    print("-" * 50)
    for code in sample_data:
        result = parse_code_column(code)
        print(f"入力: {code}")
        print(f"出力: {result[0]}, {result[1]}, {result[2]}")
        print()

#example
if __name__ == "__main__":
    process_sample_data()

    csv_path = "/Users/oomuraruka/制作.../csv/hokkaidou_hos.csv"

def clean_hospital_data(df):
    """
    病院データのcode列を整理する（DataFrame用）
    """
    if 'code' in df.columns:
        code_parts = df['code'].apply(parse_code_column)
        df['code_1'] = [parts[0] for parts in code_parts]
        df['code_2'] = [parts[1] for parts in code_parts]
        df['code_3'] = [parts[2] for parts in code_parts]
        df = df.drop('code', axis=1)
        
        cols = df.columns.tolist()
        if 'id' in cols:
            id_idx = cols.index('id')
            new_cols = cols[:id_idx+1] + ['code_1', 'code_2', 'code_3'] + [col for col in cols[id_idx+1:] if col not in ['code_1', 'code_2', 'code_3']]
            df = df[new_cols]
    
    return df