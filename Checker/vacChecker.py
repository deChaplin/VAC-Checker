import json
from collections import namedtuple

import Checker.database as database
import Checker.apiUtils as api


def start_up():
    database.create_database()


def check_vac(KEY, account, discord_id):
    steamID, name, game_banned, game_bans, vac_banned, vac_bans = format_api_response(KEY, account, api.getBannedStatus(KEY, account))

    # Add the account to the database
    database.add_account(steamID, name, game_banned, game_bans, vac_banned, vac_bans, discord_id)

    message = ""
    message += "---------------------------------------\n" + \
                "Steam Name: " + name + "\n" + \
                "Steam ID: " + steamID + "\n" + \
                "Game Banned: " + game_banned + "\n" + \
                "Number of Game Bans: " + game_bans + "\n" + \
                "VAC Banned: " + vac_banned + "\n" + \
                "Number of VAC Bans: " + vac_bans + "\n" + \
                "---------------------------------------\n"

    return message


def get_discord_id():
    # Returns the number of discord IDs in the database
    return database.get_num_discord_id()


def check_all(KEY, discord_id):
    accounts = database.get_steamid_from_discord(discord_id)

    print("Discord Id - " + discord_id)
    message = ""
    for i in accounts:
        print("Steam Id - " + i)
        steamID, name, game_banned, game_bans, vac_banned, vac_bans = format_api_response(KEY, i, api.getBannedStatus(KEY, i))

        if game_banned == "Yes" or vac_banned == "Yes":
            message += "---------------------------------------\n" + \
            "Steam Name: " + name + "\n" + \
            "Steam ID: " + steamID + "\n" + \
            "Game Banned: " + game_banned + "\n" + \
            "Number of Game Bans: " + game_bans + "\n" + \
            "VAC Banned: " + vac_banned + "\n" + \
            "Number of VAC Bans: " + vac_bans + "\n" + \
            "---------------------------------------\n"

            return message
        else:
            return None


def add_account(KEY, account, discord_id):
    steamID, name, game_banned, game_bans, vac_banned, vac_bans = format_api_response(KEY, account, api.getBannedStatus(KEY, account))
    database.add_account(steamID, name, game_banned, game_bans, vac_banned, vac_bans, discord_id)
    return name


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

        return i.SteamId, name, game_banned, str(i.NumberOfGameBans), vac_banned, str(i.NumberOfVACBans)


def remove_account(steam_id):
    database.remove_account(steam_id)