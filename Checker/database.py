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
        game_bans text,
        num_game_bans text,
        steam_vac text,
        num_vac_bans text
    )""")
    # commit our command
    conn.commit()
    # close our connection
    conn.close()

# add a steam account to the database
def add_account(steam_id, steam_name, game_bans, num_game_bans, steam_vac, num_vac_bans):

    if check_account(steam_id):
        update_status(steam_id, steam_name, game_bans, num_game_bans, steam_vac, num_vac_bans)
    else:
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        # Create a table
        c.execute("INSERT INTO accounts VALUES (?, ?, ?, ?, ?, ?)", (steam_id, steam_name, game_bans, num_game_bans, steam_vac, num_vac_bans))
        conn.commit()
        conn.close()

# Check if steam account is in the database
def check_account(steam_id):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    # Create a table
    c.execute("SELECT steam_id FROM accounts WHERE steam_id=?", (steam_id,))
    row = c.fetchone()
    conn.close()

    if row:
        return True
    else:
        return False

# Update the status of a steam account
def update_status(steam_id, steam_name, game_bans, num_game_bans, steam_vac, num_vac_bans):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    # Create a table
    c.execute("UPDATE accounts SET steam_name=?, game_bans=?, num_game_bans=?, steam_vac=?, num_vac_bans=? "
              "WHERE steam_id=?", (steam_name, game_bans, num_game_bans, steam_vac, num_vac_bans, steam_id))
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

def get_game_bans(steam_id):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    # Create a table
    c.execute("SELECT game_bans FROM users WHERE steam_id=?", (steam_id,))
    row = c.fetchone()
    conn.close()

    if row:
        return row[0]
    else:
        return None