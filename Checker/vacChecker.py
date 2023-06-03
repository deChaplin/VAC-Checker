import json
from collections import namedtuple

import Checker.database as database
import Checker.apiUtils as api


def start_up():
    database.create_database()


def check_vac(KEY, account):
    response = format_api_response(KEY, account, api.getBannedStatus(KEY, account))
    return response


def format_api_response(KEY, account, response):
    accountStatus = json.loads(response, object_hook=lambda d: namedtuple('X', d.keys())(
        *d.values()))  # Loads json for the account status

    for i in accountStatus.players:
        # Calls the function to get the account name passing through the current steamID
        nameResponse = api.getAccountName(KEY, account)
        accountData = json.loads(nameResponse, object_hook=lambda d: namedtuple('X', d.keys())(
            *d.values()))  # Loads the json for the account summaries

        # Checks if the steamIDs match and returns a name
        for x in accountData.response.players:
            if x.steamid == i.SteamId:
                name = x.personaname

        # Changes variables if the account is game banned
        if i.NumberOfGameBans > 0:
            game_banned = "Yes"
        else:
            game_banned = "No"

        # Changes variables if the account is VAC banned
        if i.VACBanned:
            vac_banned = "Yes"
        else:
            vac_banned = "No"

        # Add the account to the database
        add_account(i.SteamId, name, game_banned, i.NumberOfGameBans, vac_banned, i.NumberOfVACBans)

        # Print the account details
        return "---------------------------------------\n" + \
        "Steam Name: " + name + "\n" + \
        "Steam ID: " + i.SteamId + "\n" + \
        "Game Banned: " + game_banned + "\n" + \
        "Number of Game Bans: " + str(i.NumberOfGameBans) + "\n" + \
        "VAC Banned: " + vac_banned + "\n" + \
        "Number of VAC Bans: " + str(i.NumberOfVACBans) + "\n" + \
        "---------------------------------------\n"


def add_account(steam_id, steam_name, game_bans, num_game_bans, steam_vac, num_vac_bans):
    database.add_account(steam_id, steam_name, game_bans, num_game_bans, steam_vac, num_vac_bans)


def remove_account(steam_id):
    database.remove_account(steam_id)