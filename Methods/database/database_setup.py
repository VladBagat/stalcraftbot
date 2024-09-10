import psycopg2 as psycopg
from Methods.API_requests import retrieve_clan_members
from keys import keys


#SHOULD BE EXECUTED ONCE
def create_players_table(conn):
    cur = conn.cursor()
    table_arguments = '''(
        id serial PRIMARY KEY,
        name text,
        rank text,
        brawl_skip integer,
        tournament_skip integer,
        hiatus_num integer,
        is_hiatus integer, 
        penalty integer
    )'''
    create_players_table = f"CREATE TABLE IF NOT EXISTS players {table_arguments}"
    cur.execute(create_players_table)
    conn.commit()

    cur.execute("SELECT name, is_hiatus FROM players")
    result = cur.fetchone()

    cur.close()

    return result

def prepare_players_data():
    names, ranks = prepare_players()
    data = [(name, rank, 0, 0, 2, 0, 0) for name, rank in zip(names, ranks)]
    return data

def initiate_database():
    with connect_to_database() as conn:
        result = create_players_table(conn)
        if not result:
            data = prepare_players_data()
            insert_players(conn, data)
            clone_database(conn)

#RUNS DYNAMICALLY
def connect_to_database():
    conn = psycopg.connect(dbname=keys.dbname, user=keys.user, password=keys.password, host=keys.host)
    return conn

def prepare_players():
    names = []
    ranks = []

    players = retrieve_clan_members()

    for i in range(len(players)):
        names.append(players[i].get("name"))
        ranks.append(players[i].get("rank"))

    return names, ranks

def refresh_players():
    pass

def insert_players(conn, data):
    cur = conn.cursor()
    cur.executemany("INSERT INTO players (name, rank, brawl_skip, tournament_skip, hiatus_num, is_hiatus, penalty) VALUES (%s, %s, %s, %s, %s, %s, %s)", data)
    conn.commit()
    cur.close()

def clone_database(conn):
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS players_test AS TABLE players WITH DATA")
    #cur.execute("INSERT INTO nplayers_test SELECT * FROM players")
    conn.commit()
    cur.close()
