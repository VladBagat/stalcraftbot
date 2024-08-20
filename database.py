import psycopg2 as psycopg
from db_key import user, dbname, password, host
from Methods.API_requests import retrieve_clan_members

#SHOULD BE EXECUTED ONCE
def create_players_table(conn):
    cur = conn.cursor()
    table_arguments = '(id serial PRIMARY KEY, name text, rank text, brawl_skip integer, tournament_skip integer, hiatus_num integer, is_hiatus integer)'
    create_players_table = f"CREATE TABLE IF NOT EXISTS players {table_arguments}"
    cur.execute(create_players_table)
    conn.commit()
    cur.close()

def prepare_players_data():
    names, ranks = prepare_players()
    data = [(name, rank, 0, 0, 2, 0) for name, rank in zip(names, ranks)]
    return data

def initiate_database():
    with connect_to_database() as conn:
        create_players_table(conn)
        data = prepare_players_data()
        insert_players(conn, data)

#RUNS DYNAMICALLY
def connect_to_database():
    conn = psycopg.connect(dbname=dbname, user=user, password=password, host=host)
    return conn

def prepare_players():
    names = []
    ranks = []

    players = retrieve_clan_members()

    for i in range(0, 30):
        names.append(players[i].get("name"))
        ranks.append(players[i].get("rank"))

    return names, ranks

def refresh_players():
    pass

def insert_players(conn, data):
    cur = conn.cursor()
    cur.executemany("INSERT INTO players (name, rank, brawl_skip, tournament_skip, hiatus_num, is_hiatus) VALUES (%s, %s, %s, %s, %s, %s)", data)
    conn.commit()
    cur.close()

initiate_database()

