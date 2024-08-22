from psycopg2.pool import SimpleConnectionPool
from db_key import user, dbname, password, host
from Methods.API_requests import retrieve_clan_members

def connect_to_database() -> SimpleConnectionPool:
    pool = SimpleConnectionPool(minconn=1, maxconn=10, dbname=dbname, user=user, password=password, host=host)
    return pool

def fetch_hiatus(conn, user_nickname):
    cur = conn.cursor()

    fetch_query = 'SELECT hiatus_num, is_hiatus FROM players WHERE name = %s'

    cur.execute(fetch_query, (user_nickname,))

    results = cur.fetchone()

    return results

def fetch_hiatus(conn, user_nickname):
    with conn.cursor() as cur:
        fetch_query = 'SELECT hiatus_num, is_hiatus FROM players WHERE name = %s'
        cur.execute(fetch_query, (user_nickname,))
        results = cur.fetchone()

    return results

def insert_hiatus(conn, hiatus_num, is_hiatus, user_nickname):
    with conn.cursor() as cur:
        insert_query = 'INSERT INTO players (hiatus_num, is_hiatus) VALUES (%s, %s) WHERE name = %s'
        cur.execute(insert_query, (hiatus_num, is_hiatus, user_nickname))
        conn.commit()

    