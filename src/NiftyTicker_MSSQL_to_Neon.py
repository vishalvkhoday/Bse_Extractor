import os
import sys

if __package__ in (None, ''):
    sys.path.insert(0, os.path.dirname(__file__))
    sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from DB_Operation import DB_Operation
from neon_config import (
    build_neon_insert_values,
    get_neon_connection,
    get_neon_table_name,
)


MSSQL_QUERY = '''
SELECT
    [Script_Name],
    [DateTime],
    [SpotPrice],
    [chg],
    [IndOpen],
    [IndHigh],
    [IndLow],
    [IndPreClose]
FROM Nifty_Ticker
WHERE Script_Name IN ('NIFTY 50', 'INDIA VIX', 'NIFTY BANK')
  AND convert(date, [DateTime]) > ('2026-10-01')
'''


def fetch_mssql_records():
    mssql_conn = DB_Operation().db_ConnectionObject()
    try:
        cursor = mssql_conn.cursor()
        try:
            cursor.execute(MSSQL_QUERY)
            return [tuple(row) for row in cursor.fetchall()]
        finally:
            cursor.close()
    finally:
        mssql_conn.close()


def sync_nifty_ticker():
    records = fetch_mssql_records()
    if not records:
        print('No matching MSSQL records found for the specified date.')
        return 0

    for record in records:
        if len(record) != 8:
            raise ValueError(
                f'Expected 8 MSSQL columns for Neon insert, received {len(record)}.'
            )

    neon_conn = get_neon_connection()
    if neon_conn is None:
        raise RuntimeError('Neon connection is not configured; set NEON_DATABASE_URL.')

    inserted_count = 0
    try:
        table_name = get_neon_table_name(neon_conn)
        record_keys = list(dict.fromkeys((record[0], record[1]) for record in records))
        existing_keys = set()
        with neon_conn.cursor() as cursor:
            for start in range(0, len(record_keys), 500):
                key_batch = record_keys[start:start + 500]
                placeholders = ', '.join(['(%s, %s)'] * len(key_batch))
                cursor.execute(
                    f'''
                    SELECT script_name, datetime
                    FROM {table_name}
                    WHERE (script_name, datetime) IN ({placeholders})
                    ''',
                    tuple(value for key in key_batch for value in key),
                )
                existing_keys.update(cursor.fetchall())

        missing_records = []
        seen_keys = set(existing_keys)
        for record in records:
            record_key = (record[0], record[1])
            if record_key not in seen_keys:
                missing_records.append(record)
                seen_keys.add(record_key)
        insert_sql = f'''
            INSERT INTO {table_name} (
                script_name, datetime, spotprice, chg, indopen, indhigh, indlow, indpreclose
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (script_name, datetime) DO NOTHING
        '''
        with neon_conn.cursor() as cursor:
            for record in missing_records:
                script_name, date_time, spot_price, change, ind_open, ind_high, ind_low, ind_preclose = record
                neon_record = (
                    script_name,
                    date_time,
                    spot_price,
                    change,
                    ind_open,
                    ind_high,
                    ind_low,
                    ind_preclose,
                )
                neon_values = build_neon_insert_values(neon_record)
                print(f'Inserting MSSQL values into Neon: {neon_values!r}')
                cursor.execute(insert_sql, neon_values)
                if cursor.rowcount > 0:
                    inserted_count += cursor.rowcount
        neon_conn.commit()
    except Exception:
        neon_conn.rollback()
        raise
    finally:
        neon_conn.close()

    print(
        f'Sync complete: inserted {inserted_count} missing records '
        f'from {len(records)} MSSQL records.'
    )
    return inserted_count


if __name__ == '__main__':
    sync_nifty_ticker()
