import csv
import os

folder_path = 'change'

def is_id_cell(s):
    if s is None:
        return False
    s = s.strip()
    if not s:
        return False
    try:
        float(s)
        return True
    except ValueError:
        return False

for filename in os.listdir(folder_path):
    if filename.endswith('.csv'):
        file_path = os.path.join(folder_path, filename)
        
        with open(file_path, newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            all_rows = list(reader)

        if not all_rows:
            continue

        header = all_rows[0]
        merged_rows = []
        current_row = None

        for row in all_rows[1:]:
            if len(row) > 0 and is_id_cell(row[0]):
                if current_row:
                    merged_rows.append(current_row)
                try:
                    id_num = float(row[0])
                    if id_num.is_integer():
                        row[0] = f"{int(id_num)}.0"
                    else:
                        row[0] = str(id_num)
                except:
                    row[0] = row[0] + '.0'

                if len(row) > 1:
                    row[1] = row[1].replace('・', '-')

                current_row = row
            else:
                if current_row is None:
                    continue
                for i, val in enumerate(row):
                    if val.strip():
                        if len(current_row) <= i:
                            current_row.extend([''] * (i - len(current_row) + 1))
                        if current_row[i].strip():
                            current_row[i] += ' / ' + val.strip()
                        else:
                            current_row[i] = val.strip()

        if current_row:
            merged_rows.append(current_row)

        with open(file_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(header)
            writer.writerows(merged_rows)

        print(f"編集完了: {filename}")