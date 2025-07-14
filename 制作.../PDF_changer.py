import camelot
import pandas as pd

pages = input("抽出したいページ番号を指定してください（例: 1-5 または 1,3,5）: ")

pdf_path = "/Users/oomuraruka/制作.../csv/hokkaidou.pdf"
tables = camelot.read_pdf(pdf_path, pages=pages, flavor="stream")

if tables.n > 0:
    df_list = []
    columns = None
    for i, table in enumerate(tables):
        df = table.df
        if i == 0:
            columns = df.iloc[0]
            df.columns = columns
            df = df[1:]
            df_list.append(df)
        else:
            if df.shape[1] == len(columns):
                df.columns = columns
                df = df[1:]
                df_list.append(df)
            else:
                print(f"Warning: {i+1}番目のテーブルのカラム数が一致しません。スキップします。")
    if df_list:
        export_data = pd.concat(df_list, ignore_index=True)
        export_data.to_csv("/Users/oomuraruka/制作.../csv/hospital_hokkaidou_診療所.csv", index=False, encoding="utf-8-sig")
        print("データを hospital_deta_iwate.csv に保存しました。")
    else:
        print("有効なテーブルがありませんでした。")
else:
    print("No tables found in the PDF.")