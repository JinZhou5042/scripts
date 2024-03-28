import pandas as pd
import os.path as path

def parse_line(line):
    parts = line.strip().split()
    record_type = parts[2]  # MANAGER, WORKER, TASK, etc.
    return record_type, parts

def convert_columns_to_numeric(df):
    for column in df.columns:
        df[column] = pd.to_numeric(df[column], errors='coerce')
    return df

def main(log_file_path, output_excel_path):
    data = {
        'MANAGER': [],
        'WORKER': [],
        'TASK': [],
        'LIBRARY': [],
        # 其他可能的记录类型
    }

    with open(log_file_path, 'r') as file:
        for line in file:
            if line.startswith("#"):
                continue
            record_type, parts = parse_line(line)
            if record_type in data:
                data[record_type].append(parts)

    # 将数据写入Excel的不同工作表，并为每个表添加标题
    with pd.ExcelWriter(output_excel_path, engine='openpyxl') as writer:
        for record_type, records in data.items():
            # print(records)
            if records:
                df = pd.DataFrame(records)

                # 为每个工作表添加标题
                if record_type == 'TASK':
                    df.iloc[:, 3] = pd.to_numeric(df.iloc[:, 3], errors='coerce')
                df.to_excel(writer, sheet_name=record_type, index=False, header=False)


if __name__ == "__main__":
    base_dir = path.join(path.abspath('.'), "vine-run-info/most-recent/vine-logs")
    txn_log = path.join(base_dir, "transactions")
    opt_png = path.join(base_dir, "txn.xlsx")
    main(txn_log, opt_png)
