import os
import pandas as pd


def main():
    files_list = [
        file_name for file_name in os.listdir('test_case')
        if file_name.endswith('.xlsx')
    ]
    sheet_name = pd.ExcelFile(f"test_case/{files_list[0]}").sheet_names[0]
    columns = ''
    all_rows = {}
    result = []
    for xlsx_file in files_list:
        df = pd.read_excel(f"test_case/{xlsx_file}", sheet_name=sheet_name)
        if not columns:
            columns = list(df.columns.values)
        for i in range(len(df)):
            if df["Номер"][i] not in all_rows:
                all_rows[df["Номер"][i]] = []
            row_data = []
            for column in columns:
                row_data.append(df[column][i])
            all_rows[df["Номер"][i]].append(row_data)
    for num in sorted(all_rows.keys()):
        for _ in all_rows[num]:
            result.append(_)

    new_df = pd.DataFrame(columns=columns, data=result)
    new_df.to_excel("result.xlsx", index=False)


if __name__ == '__main__':
    main()
