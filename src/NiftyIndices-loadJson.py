import glob
import json
import os
from datetime import datetime

import pyodbc


JSON_FOLDER = r"C:\Test"
DB_CONNECTION = (
    'DRIVER={ODBC Driver 17 for SQL Server};'
    'SERVER=LAPTOP-IFK6D8L3\\SQLEXPRESS;'
    'DATABASE=Bse_Results;'
    'UID=sa;PWD=password'
)


def clean_value(value):
    if value is None:
        return None

    text = str(value).strip()
    if text in ('', '-', '--', 'None', 'null'):
        return None

    return text.replace(',', '')


def safe_sql_value(value):
    if value is None:
        return ''
    return str(value).replace("'", "''")


def format_sql_datetime(value):
    if value is None:
        return None

    if isinstance(value, datetime):
        return value.strftime('%d-%b-%Y %H:%M')

    text = str(value).strip()
    if not text:
        return None

    for fmt in ('%Y-%m-%d %H:%M:%S', '%Y-%m-%d %H:%M', '%d-%b-%Y %H:%M', '%d-%b-%Y %I:%M %p', '%d-%m-%Y %H:%M'):
        try:
            return datetime.strptime(text, fmt).strftime('%d-%b-%Y %H:%M')
        except ValueError:
            pass

    return text


def build_sql_from_item(item, file_timestamp):
    script_name = (item.get('indexName') or item.get('index') or '').strip()
    if not script_name:
        return None

    dt_value = file_timestamp or (item.get('timeVal') or item.get('timestamp') or item.get('dateTime') or item.get('time'))
    dt_value = format_sql_datetime(dt_value)
    if not dt_value:
        return None

    # Keep names within the existing SQL schema when needed, but preserve the exact value format.
    script_name = script_name[:15]

    last = clean_value(item.get('last'))
    perc_change = clean_value(item.get('percChange') if 'percChange' in item else item.get('percentChange'))
    open_value = clean_value(item.get('open'))
    high = clean_value(item.get('high'))
    low = clean_value(item.get('low'))
    previous_close = clean_value(item.get('previousClose'))

    if any(v is None for v in [last, perc_change, open_value, high, low, previous_close]):
        return None

    if str(previous_close).strip() == '-':
        return None

    script_name = safe_sql_value(script_name)
    dt_value = safe_sql_value(dt_value)
    sql = (
        "insert into Nifty_Ticker (Script_Name, [DateTime], SpotPrice, chg, IndOpen, IndHigh, IndLow, IndPreClose) "
        f"values ('{script_name}','{dt_value}','{last}','{perc_change}','{open_value}','{high}','{low}','{previous_close}')"
    )
    return sql


def process_json_file(file_path):
    conn = pyodbc.connect(DB_CONNECTION)
    cur = conn.cursor()

    try:
        with open(file_path, 'r', encoding='utf-8') as json_file:
            payload = json.load(json_file)

        data = payload.get('data')
        if not isinstance(data, list):
            print(f'No data array found in {file_path}')
            return

        file_timestamp = payload.get('timestamp')
        row_count = 0

        for item in data:
            if not isinstance(item, dict):
                continue

            sql = build_sql_from_item(item, file_timestamp)
            if not sql:
                continue

            row_count += 1
            print(sql)
            try:
                cur.execute(sql)
                conn.commit()
            except Exception as exc:
                print(f'Insert failed for {file_path}: {exc}')
                conn.rollback()

        print(f'Processed {row_count} rows from {file_path}')
    except Exception as exc:
        print(f'Error reading {file_path}: {exc}')
    finally:
        cur.close()
        conn.close()


def main():
    file_list = sorted(glob.glob(os.path.join(JSON_FOLDER, '*.json')))

    for file_path in file_list:
        print(f'Processing file: {file_path}')
        process_json_file(file_path)


if __name__ == '__main__':
    main()
