import pandas as pd

# 各データファイル名をリストで指定
file_names = ['csv/akita_dent.csv', 'csv/akita_hos.csv', 'csv/aomori_dent.csv', 'csv/aomori_hos.csv', 'csv/fukushima_dent.csv', 'csv/fukushima_hos.csv', 'csv/hokkaidou_dent.csv', 'csv/hokkaidou_hos.csv', 'csv/iwate_dent.csv', 'csv/iwate_hos.csv', 'csv/miyagi_dent.csv', 'csv/miyagi_hos.csv', 'csv/yamagata_dent.csv', 'csv/yamagata_hos.csv'] # 実際のファイル名に合わせてください
output_file = 'hospital.csv'
department_name = '内科' 
all_data = []

for i, file_name in enumerate(file_names):
    try:
        df = pd.read_csv(file_name, header=None)
        if i == 0:
            df.iloc[0, 0] = department_name 
        all_data.append(df)
    except FileNotFoundError:
        print(f"警告: ファイル '{file_name}' が見つかりませんでした。スキップします。")
    except Exception as e:
        print(f"エラー: ファイル '{file_name}' の読み込み中に問題が発生しました: {e}")

if all_data:
    # 全てのデータを結合
    merged_df = pd.concat(all_data, ignore_index=True)

    # 最初の項目に診療科名を入れる処理が上記で不十分な場合、再度ここで設定
    # 例: merged_df.iloc[0, 0] = department_name

    # 結果を新しいCSVファイルに保存（インデックスなし）
    merged_df.to_csv(output_file, index=False, header=False)
    print(f"データが '{output_file}' に正常にまとめられました。")
else:
    print("処理するデータがありませんでした。")