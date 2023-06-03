import sqlite3


def create_database():
    # Connect to the database
    conn = sqlite3.connect('database.db')
    # Create a cursor
    c = conn.cursor()
    # Create a table
    c.execute("""CREATE TABLE IF NOT EXISTS accounts (
        steam_id text PRIMARY KEY,
        steam_name text,
        steam_status text,
        steam_vac text
    )""")
    # commit our command
    conn.commit()
    # close our connection
    conn.close()

# add a steam account to the database
def add_account(steam_id, steam_name, steam_status, steam_vac):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    # Create a table
    c.execute("INSERT INTO accounts VALUES (?, ?, ?, ?)", (steam_id, steam_name, steam_status, steam_vac))
    conn.commit()
    conn.close()

# remove a steam account from the database
def remove_account(steam_id):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    # Create a table
    c.execute("DELETE FROM accounts WHERE steam_id=?", (steam_id,))
    conn.commit()
    conn.close()

def get_steamid(steam_name):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    # Create a table
    c.execute("SELECT steam_id FROM users WHERE steam_name=?", (steam_name,))
    row = c.fetchone()
    conn.close()

    if row:
        return row[0]
    else:
        return None

def get_vac_status(steam_id):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    # Create a table
    c.execute("SELECT steam_vac FROM users WHERE steam_id=?", (steam_id,))
    row = c.fetchone()
    conn.close()

    if row:
        return row[0]
    else:
        return None

def get_game_status(steam_id):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    # Create a table
    c.execute("SELECT steam_status FROM users WHERE steam_id=?", (steam_id,))
    row = c.fetchone()
    conn.close()

    if row:
        return row[0]
    else:
        return None