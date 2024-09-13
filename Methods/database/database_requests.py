from psycopg2.pool import SimpleConnectionPool
from Methods.API_requests import parse_clan_members
from keys import keys
import os

if os.getenv('heroku'):
    database_name = 'players'
else:
    database_name = 'players_test'

def connect_to_database() -> SimpleConnectionPool:
    pool = SimpleConnectionPool(minconn=1, maxconn=20, dbname=keys.dbname, user=keys.user, password=keys.password, host=keys.host)
    return pool

#Functions for Scheduled.HiatusButton
def fetch_hiatus(conn, user_nickname):
    with conn.cursor() as cur:
        fetch_query = f'SELECT hiatus_num, is_hiatus FROM {database_name} WHERE name = %s'
        cur.execute(fetch_query, (user_nickname,))
        results = cur.fetchone()

    return results

def update_hiatus(conn, user_data_list : list) -> None:
    print(user_data_list)
    with conn.cursor() as cur:
        update_query = f'UPDATE {database_name} SET hiatus_num = %s, is_hiatus = %s WHERE name = %s'
        cur.executemany(update_query, user_data_list)
        conn.commit()

# Functions for Scheduled.DailyOnline
def daily_online_hiatus(conn):
    #Returns all users with is_hiatus set True and sets is_hiatus to False
    with conn.cursor() as cur:
        fetch_query = f'SELECT name, is_hiatus FROM {database_name}'
        cur.execute(fetch_query)
        results = cur.fetchall()
        update_query = f'UPDATE {database_name} SET is_hiatus = 0'
        cur.execute(update_query)
        conn.commit()

    return results

def increment_player_penalty(conn, players:list):
    with conn.cursor() as cur:
        data = [(100000, player) for player in players]
        update_penalty_query = f"UPDATE {database_name} SET penalty = penalty + %s WHERE name = %s AND NOT rank = 'RECRUIT'"
        cur.executemany(update_penalty_query, data)
        conn.commit()

#WIP WIP WIP WIP
def update_clan_members(conn):
    with conn.cursor() as cur:
        names, ranks = parse_clan_members()

        fetch_members_query = f"SELECT name FROM {database_name}"
        cur.execute(fetch_members_query)
        database_members = cur.fetchall()

        left, joined = find_missing_members(names, database_members)

        joined_ranks = [ranks[joined.index(joined_member)] for joined_member in joined]

        delete_users_query = f"DELETE FROM {database_name} WHERE name = %s"
        print(left)
        cur.executemany(delete_users_query, [(item,) for item in left])

        insert_users_qury = f"INSERT INTO {database_name} (name, rank, hiatus_num, is_hiatus, penalty) VALUES (%s, %s, %s, %s, %s)"
        data = [(name, rank, 2, 0, 0) for name, rank in zip(joined, joined_ranks)]
        cur.executemany(insert_users_qury, data)

        conn.commit()


def find_missing_members(new_members, old_members):
    left_clan_members = []
    joined_clan_members = []

    old_members = [old_member[0] for old_member in old_members]

    for i in range(len(old_members)):
        if old_members[i] not in new_members:
            left_clan_members.append(old_members[i])

    for i in range(len(new_members)):    
        if new_members[i] not in old_members:
            joined_clan_members.append(new_members[i])

    return left_clan_members, joined_clan_members

def reset_hiatus_status(conn):
    hiatus_num = 3
    penalty = 0 

    reset_hiatus_query = f"UPDATE {database_name} SET hiatus_num = %s, penalty = %s"

    with conn.cursor() as cur:
        cur.execute(reset_hiatus_query, (hiatus_num, penalty,))
        conn.commit()