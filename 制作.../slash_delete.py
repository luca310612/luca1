import pandas as pd
import csv
import re
from pathlib import Path
import time

def clean_medical_data(csv_paths):
    """
    医療データCSVから不要な情報を一括削除
    - ID形式「数値,コード / 文字列,数値,数値,」を保持
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
        r'/ 令\d+\..*',      # 令和年月日以降を削除
        r'/ 平\d+\..*',      # 平成年月日以降を削除
        r'/ 昭\d+\..*',      # 昭和年月日以降を削除
        r'/ 現存.*',         # 現存情報以降を削除
    ]
    
    def preserve_id_format(text):
        """ID形式「数値,コード / 文字列,数値,数値,」を保持"""
        if pd.isna(text) or text == '':
            return text
        
        text = str(text)
        
        # ID形式のパターンを検出
        # 例: "4.0,01 / 山医17,1017,3,"
        id_pattern = r'^(\d+(?:\.\d+)?,\d+\s*/\s*[^,]+,\d+,\d+,?)(.*)$'
        match = re.match(id_pattern, text)
        
        if match:
            # ID部分と残りの部分を分離
            id_part = match.group(1)
            remaining_part = match.group(2)
            
            # 残りの部分から不要な情報を削除
            cleaned_remaining = clean_text(remaining_part)
            
            # ID部分を保持して結合
            if cleaned_remaining.strip():
                return f"{id_part}{cleaned_remaining}"
            else:
                return id_part
        else:
            # ID形式でない場合は通常のクリーニング
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
    
    def is_likely_id_column(column_name, sample_values):
        """列がID形式を含む可能性が高いかを判定"""
        if not column_name or len(sample_values) == 0:
            return False
        
        # 列名がIDっぽい
        if column_name.lower() in ['id', 'code', 'name']:
            return True
        
        # サンプル値をチェック
        id_pattern = r'\d+(?:\.\d+)?,\d+\s*/\s*[^,]+,\d+,\d+'
        for value in sample_values[:5]:  # 最初の5つをチェック
            if pd.notna(value) and re.search(id_pattern, str(value)):
                return True
        
        return False
    
    # 処理対象の主要列（これらの列を重点的にクリーニング）
    target_columns = [
        'tel', 'name', 'address', 'corporation', 'director', 
        'established', 'bed_type_and_count', 'facility_type'
    ]
    
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
            for col in df.columns[:3]:  # 最初の3列を表示
                if len(df) > 0 and pd.notna(df[col].iloc[0]):
                    example = str(df[col].iloc[0])
                    print(f"   {col}: {example[:100]}...")
            
            # 全列をクリーニング
            cleaned_count = 0
            for col in df.columns:
                original_values = df[col].copy()
                
                # 列の性質を判定
                sample_values = df[col].dropna().head(10).tolist()
                is_id_col = is_likely_id_column(col, sample_values)
                
                if col == 'tel':
                    # 電話番号列は専用関数でクリーニング（カンマ付き）
                    df[col] = df[col].apply(clean_tel_with_comma)
                elif is_id_col:
                    # ID形式を含む列は専用関数でクリーニング
                    df[col] = df[col].apply(preserve_id_format)
                    print(f"   🔢 {col}: ID形式保持モードで処理")
                elif col in target_columns:
                    # 重要な列は確実にクリーニング
                    df[col] = df[col].apply(clean_text)
                else:
                    # その他の列も軽くクリーニング
                    df[col] = df[col].apply(lambda x: clean_text(x) if isinstance(x, str) and ('常　勤:' in x or '非常勤:' in x) else x)
                
                # 変更された行数をカウント
                changed = (original_values != df[col]).sum()
                if changed > 0:
                    cleaned_count += changed
                    print(f"   ✅ {col}: {changed:,}行をクリーニング")
            
            # 処理後の例を表示
            print(f"\n📋 処理後の例:")
            for col in df.columns[:3]:  # 最初の3列を表示
                if len(df) > 0 and pd.notna(df[col].iloc[0]):
                    example = str(df[col].iloc[0])
                    print(f"   {col}: {example}")
            
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
        # 他のファイルがある場合はここに追加
        # 'csv/other_file1.csv',
        # 'csv/other_file2.csv',
    ]
    
    print("🚀 大量データ CSV クリーニング開始（ID形式保持版）")
    print(f"📁 処理対象ファイル数: {len(csv_file_paths)}")
    
    clean_medical_data(csv_file_paths)