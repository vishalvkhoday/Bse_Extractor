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
  AND convert(date, [DateTime]) in ('2026-11-04','2026-10-28','2026-10-23','2026-10-16')
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

    neon_conn = get_neon_connection()
    if neon_conn is None:
        raise RuntimeError('Neon connection is not configured; set NEON_DATABASE_URL.')

    inserted_count = 0
    try:
        table_name = get_neon_table_name(neon_conn)
        insert_sql = f'''
            INSERT INTO nifty_ticker (
                script_name, datetime, spotprice, chg, indopen, indhigh, indlow, indpreclose
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (script_name, datetime) DO NOTHING
        '''
        with neon_conn.cursor() as cursor:
            for record in records:
                if len(record) != 8:
                    raise ValueError(
                        f'Expected 8 MSSQL columns for Neon insert, received {len(record)}.'
                    )
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
                print(insert_sql)
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

    print(f'Sync complete: inserted {inserted_count} of {len(records)} MSSQL records.')
    return inserted_count


if __name__ == '__main__':
    sync_nifty_ticker()
