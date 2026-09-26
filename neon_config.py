import os

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:  # pragma: no cover
    pass

try:
    import psycopg
except ImportError:  # pragma: no cover
    psycopg = None

try:
    import psycopg2
except ImportError:  # pragma: no cover
    psycopg2 = None


def build_neon_insert_values(record):
    if len(record) != 8:
        raise ValueError(f"Expected 8 values in API record, received {len(record)}")
    return tuple(str(value).replace(',', '') for value in record)


def get_neon_table_name(conn):
    if conn is None:
        return 'nifty_ticker'

    try:
        with conn.cursor() as cur:
            cur.execute("SELECT to_regclass(%s)", ('Nifty_Ticker',))
            quoted = cur.fetchone()
            if quoted and quoted[0]:
                return '"Nifty_Ticker"'

            cur.execute("SELECT to_regclass(%s)", ('nifty_ticker',))
            lowered = cur.fetchone()
            if lowered and lowered[0]:
                return 'nifty_ticker'
    except Exception:
        pass

    return 'nifty_ticker'


def ensure_neon_table(conn):
    table_name = get_neon_table_name(conn)
    if table_name in ('nifty_ticker', '"Nifty_Ticker"'):
        try:
            with conn.cursor() as cur:
                cur.execute(
                    '''
                    CREATE TABLE IF NOT EXISTS nifty_ticker (
                        script_name text,
                        datetime timestamp,
                        spotprice numeric,
                        chg numeric,
                        indopen numeric,
                        indhigh numeric,
                        indlow numeric,
                        indpreclose numeric
                    )
                    '''
                )
            conn.commit()
        except Exception:
            pass
        return 'nifty_ticker'
    return table_name


def get_neon_connection():
    dsn = os.getenv('NEON_DATABASE_URL')
    if not dsn:
        return None

    if psycopg is not None:
        return psycopg.connect(dsn, connect_timeout=10)

    if psycopg2 is not None:
        return psycopg2.connect(dsn, connect_timeout=10)

    raise RuntimeError('Install psycopg or psycopg2 to connect to Neon.')
