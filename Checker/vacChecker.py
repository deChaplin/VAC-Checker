import Checker.database as database


def start_up():
    database.create_database()


def check_vac():
    database.get_vac_status(76561199078298677)

def add_account(steam_id, steam_name, steam_status, steam_vac):
    database.add_account(steam_id, steam_name, steam_status, steam_vac)

def remove_account(steam_id):
    database.remove_account(steam_id)