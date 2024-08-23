from psycopg2.pool import SimpleConnectionPool
from db_key import user, dbname, password, host
from Methods.API_requests import retrieve_clan_members

def connect_to_database() -> SimpleConnectionPool:
    pool = SimpleConnectionPool(minconn=1, maxconn=10, dbname=dbname, user=user, password=password, host=host)
    return pool

def fetch_hiatus(conn, user_nickname):
    with conn.cursor() as cur:
        fetch_query = 'SELECT hiatus_num, is_hiatus FROM players WHERE name = %s'
        cur.execute(fetch_query, (user_nickname,))
        results = cur.fetchone()

    return results

def update_hiatus(conn, user_data_list : list):
    with conn.cursor() as cur:
        update_query = 'UPDATE players SET hiatus_num = %s, is_hiatus = %s WHERE name = %s'
        print(user_data_list)
        cur.executemany(update_query, user_data_list)
        conn.commit()

    