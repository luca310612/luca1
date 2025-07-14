import pandas as pd
import csv
import re
from pathlib import Path
import time

def clean_medical_data(csv_paths):
    """
    医療データCSVから不要な情報を一括削除
    - 複数の形式を統一化
    - 電話番号から「/ 常勤:...」以降を削除
    - 各列から医師数などの情報を削除
    - 大量データに対応した高速処理
    """
    
    # 削除対象パターン（正規表現）
    patterns_to_remove = [
        r'/ 常　勤:.*',      # 常勤情報以降を削除
        r'/ 非常勤:.*',      # 非常勤情報以降を削除
        r'/ \(医.*?\)',      # 医師数情報を削除
        r'/ \(歯.*?\)',      # 歯科医師数情報を削除
        r'/ \(薬.*?\)',      # 薬剤師数情報を削除
        r'/ 新規.*',         # 新規情報以降を削除
        r'/ 交代.*',         # 交代情報以降を削除
        r'/ 組織変更.*',     # 組織変更情報以降を削除
        r'/ 令\d+\..*',      # 令和年月日以降を削除
        r'/ 平\d+\..*',      # 平成年月日以降を削除
        r'/ 昭\d+\..*',      # 昭和年月日以降を削除
        r'/ 現存.*',         # 現存情報以降を削除
        r'/ 療養病床.*',     # 療養病床情報以降を削除
    ]
    
    def clean_code_column(text):
        """code列専用：複雑な形式を単純化"""
        if pd.isna(text) or text == '':
            return text
        
        text = str(text)
        
        # パターン1: "01 / (01 / 山医1,1001 / 3001,7 / 1)" → "01"
        pattern1 = r'^(\d+)\s*/\s*\([^)]+\)$'
        match1 = re.match(pattern1, text)
        if match1:
            return match1.group(1)
        
        # パターン2: "01 / (05,1248 / 3214,9 / 6)" → "01"
        pattern2 = r'^(\d+)\s*/\s*\([^)]+\)$'
        match2 = re.match(pattern2, text)
        if match2:
            return match2.group(1)
        
        # パターン3: "01 / 山医17,1017,3" → "01"
        pattern3 = r'^(\d+)\s*/\s*.*$'
        match3 = re.match(pattern3, text)
        if match3:
            return match3.group(1)
        
        # パターン4: 単純な数値や既にクリーンな場合
        if re.match(r'^\d+$', text):
            return text
        
        # その他の場合は通常のクリーニング
        return clean_text(text)
    
    def clean_text(text):
        """テキストから不要な情報を削除"""
        if pd.isna(text) or text == '':
            return text
        
        # 文字列として処理
        text = str(text)
        
        # 各パターンを順次削除
        for pattern in patterns_to_remove:
            text = re.sub(pattern, '', text, flags=re.IGNORECASE)
        
        # 最後の「/」があれば削除してトリム
        text = re.sub(r'/\s*$', '', text)
        return text.strip()
    
    def clean_tel_with_comma(text):
        """電話番号専用：クリーニング後にカンマを追加"""
        if pd.isna(text) or text == '':
            return text
        
        # まず通常のクリーニング
        cleaned = clean_text(text)
        
        # 電話番号パターンにマッチする場合のみカンマを追加
        # 日本の電話番号形式: 0XX-XXX-XXXX, 0XXX-XX-XXXX など
        tel_pattern = r'^\d{2,4}-\d{2,4}-\d{4}$'
        if re.match(tel_pattern, cleaned):
            return cleaned + ','
        
        # 既にカンマが付いている場合は何もしない
        if cleaned.endswith(','):
            return cleaned
        
        # 電話番号らしい文字列の場合もカンマを追加
        # (数字とハイフンのみで構成されている場合)
        if re.match(r'^[\d\-]+$', cleaned) and '-' in cleaned:
            return cleaned + ','
        
        return cleaned
    
    def clean_name_column(text):
        """name列専用：施設名から不要情報を削除"""
        if pd.isna(text) or text == '':
            return text
        
        text = str(text)
        
        # 医師数情報などを削除
        text = re.sub(r'/ \(医.*?\)', '', text)
        text = re.sub(r'/ \(歯.*?\)', '', text)
        text = re.sub(r'/ \(薬.*?\)', '', text)
        text = re.sub(r'/ 常　勤:.*', '', text)
        text = re.sub(r'/ 非常勤:.*', '', text)
        
        return text.strip()
    
    def clean_address_column(text):
        """address列専用：住所から不要情報を削除"""
        if pd.isna(text) or text == '':
            return text
        
        text = str(text)
        
        # 常勤情報以降を削除
        text = re.sub(r'/ 常　勤:.*', '', text)
        
        return text.strip()
    
    def clean_corporation_column(text):
        """corporation列専用：法人情報から不要情報を削除"""
        if pd.isna(text) or text == '':
            return text
        
        text = str(text)
        
        # 診療科目情報以降を削除（長い診療科目リストが含まれているため）
        # 典型的な診療科目の開始パターンを検出
        medical_dept_patterns = [
            r'/ 内[　\s]',
            r'/ 外[　\s]',
            r'/ 精[　\s]',
            r'/ 小[　\s]',
            r'/ 産婦[　\s]',
            r'/ 眼[　\s]',
            r'/ 耳[　\s]',
            r'/ 皮[　\s]',
            r'/ リハ[　\s]',
            r'/ 放[　\s]',
            r'/ 麻[　\s]',
            r'/ 整外[　\s]',
            r'/ 脳外[　\s]',
            r'/ 心外[　\s]',
            r'/ 呼内[　\s]',
            r'/ 循環器',
            r'/ 消化器',
            r'/ 内科',
            r'/ 外科',
            r'/ 精神',
        ]
        
        for pattern in medical_dept_patterns:
            text = re.sub(pattern + r'.*', '', text, flags=re.IGNORECASE)
        
        return text.strip()
    
    def clean_director_column(text):
        """director列専用：院長情報から不要情報を削除"""
        if pd.isna(text) or text == '':
            return text
        
        text = str(text)
        
        # 新規、現存、交代などの情報を削除
        text = re.sub(r'/ 新規.*', '', text)
        text = re.sub(r'/ 現存.*', '', text)
        text = re.sub(r'/ 交代.*', '', text)
        text = re.sub(r'/ 組織変更.*', '', text)
        
        return text.strip()
    
    def clean_established_column(text):
        """established列専用：設立日から不要情報を削除"""
        if pd.isna(text) or text == '':
            return text
        
        text = str(text)
        
        # 診療科目情報以降を削除
        # 年月日の後に続く診療科目情報を削除
        text = re.sub(r'(昭\d+\.\s*\d+\.\s*\d+|平\d+\.\s*\d+\.\s*\d+|令\d+\.\s*\d+\.\s*\d+)\s*/\s*.*', r'\1', text)
        
        return text.strip()
    
    def clean_bed_column(text):
        """bed_type_and_count列専用：ベッド情報から不要情報を削除"""
        if pd.isna(text) or text == '':
            return text
        
        text = str(text)
        
        # 現存情報以降を削除
        text = re.sub(r'/ 現存.*', '', text)
        text = re.sub(r'/ 療養病床.*', '', text)
        
        return text.strip()
    
    # 処理対象の主要列とその専用関数
    column_cleaners = {
        'code': clean_code_column,
        'name': clean_name_column,
        'address': clean_address_column,
        'tel': clean_tel_with_comma,
        'corporation': clean_corporation_column,
        'director': clean_director_column,
        'established': clean_established_column,
        'bed_type_and_count': clean_bed_column,
    }
    
    total_files = len(csv_paths)
    
    for file_idx, csv_path in enumerate(csv_paths, 1):
        print(f"\n{'='*60}")
        print(f"処理中 ({file_idx}/{total_files}): {csv_path}")
        print(f"{'='*60}")
        
        start_time = time.time()
        
        try:
            # ファイル存在確認
            if not Path(csv_path).exists():
                print(f"❌ ファイルが見つかりません: {csv_path}")
                continue
                
            # CSVファイル読み込み（複数の方法を試行）
            df = None
            read_methods = [
                # 方法1: 標準的な読み込み
                lambda: pd.read_csv(csv_path, dtype=str, encoding='utf-8-sig'),
                # 方法2: 問題行をスキップ
                lambda: pd.read_csv(csv_path, dtype=str, encoding='utf-8-sig', on_bad_lines='skip'),
                # 方法3: Pythonエンジンを使用
                lambda: pd.read_csv(csv_path, dtype=str, encoding='utf-8-sig', engine='python', on_bad_lines='skip'),
                # 方法4: 区切り文字を明示的に指定
                lambda: pd.read_csv(csv_path, dtype=str, encoding='utf-8-sig', sep=',', engine='python', on_bad_lines='skip'),
            ]
            
            for method_idx, read_method in enumerate(read_methods, 1):
                try:
                    df = read_method()
                    print(f"✅ 読み込み成功 (方法{method_idx}): {len(df):,}行, {len(df.columns)}列")
                    break
                except Exception as e:
                    print(f"❌ 読み込み方法{method_idx}失敗: {str(e)[:100]}...")
                    continue
            
            if df is None:
                print(f"❌ 全ての読み込み方法が失敗しました: {csv_path}")
                continue
            
            # データクリーニング実行
            print(f"🔄 データクリーニング開始...")
            
            # 各列の処理前例を表示
            print(f"\n📋 処理前の例:")
            for col in ['code', 'name', 'address', 'tel']:
                if col in df.columns and len(df) > 0 and pd.notna(df[col].iloc[0]):
                    example = str(df[col].iloc[0])
                    print(f"   {col}: {example[:100]}...")
            
            # 全列をクリーニング
            cleaned_count = 0
            for col in df.columns:
                original_values = df[col].copy()
                
                if col in column_cleaners:
                    # 専用クリーニング関数を使用
                    df[col] = df[col].apply(column_cleaners[col])
                    print(f"   🔧 {col}: 専用クリーニング実行")
                else:
                    # その他の列は軽くクリーニング
                    df[col] = df[col].apply(lambda x: clean_text(x) if isinstance(x, str) and any(pattern in x for pattern in ['常　勤:', '非常勤:', '新規', '現存']) else x)
                
                # 変更された行数をカウント
                changed = (original_values != df[col]).sum()
                if changed > 0:
                    cleaned_count += changed
                    print(f"   ✅ {col}: {changed:,}行をクリーニング")
            
            # 列順を変えずに「address」と「prefecture」の中身だけを入れ替え
            if 'address' in df.columns and 'prefecture' in df.columns:
                df[['address', 'prefecture']] = df[['prefecture', 'address']].values
                print("🔄 『address』と『prefecture』の中身を入れ替えました（列順はそのまま）")

            # 処理後の例を表示
            print(f"\n📋 処理後の例:")
            for col in ['code', 'name', 'address', 'tel']:
                if col in df.columns and len(df) > 0 and pd.notna(df[col].iloc[0]):
                    example = str(df[col].iloc[0])
                    print(f"   {col}: {example}")

            # 「code」列に連番（1234, 1235, 1236…）を挿入
            if 'code' in df.columns:
                df['code'] = [str(1234 + i) for i in range(len(df))]
                print("🔢 『code』列に連番（1234〜）を挿入しました")

            # バックアップ作成
            backup_path = csv_path + '.backup'
            if not Path(backup_path).exists():
                Path(csv_path).rename(backup_path)
                print(f"💾 バックアップ作成: {backup_path}")
            
            # ファイル保存
            df.to_csv(csv_path, index=False, encoding='utf-8-sig', quoting=csv.QUOTE_MINIMAL)
            
            # 処理時間計算
            elapsed_time = time.time() - start_time
            
            print(f"\n✅ 処理完了!")
            print(f"   📊 総クリーニング数: {cleaned_count:,}箇所")
            print(f"   ⏱️  処理時間: {elapsed_time:.2f}秒")
            print(f"   💾 保存完了: {csv_path}")
            
        except Exception as e:
            print(f"❌ 予期しないエラー: {csv_path}")
            print(f"   エラー詳細: {str(e)}")
            import traceback
            traceback.print_exc()
    
    print(f"\n{'='*60}")
    print(f"🎉 全体処理完了! ({total_files}ファイル)")
    print(f"{'='*60}")

# 使用例
if __name__ == "__main__":
    # 処理対象ファイルのリスト
    csv_file_paths = [
        'csv/yamagata_hos.csv',
    ]
    
    print("🚀 大量データ CSV クリーニング開始（形式統一版）")
    print(f"📁 処理対象ファイル数: {len(csv_file_paths)}")
    
    clean_medical_data(csv_file_paths)