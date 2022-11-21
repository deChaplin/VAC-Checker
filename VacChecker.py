from asyncio.base_subprocess import ReadSubprocessPipeProto
from collections import namedtuple
import json
import time
from playerClass import *
import ApiUtils

from colorama import init, Fore, Back, Style
init()

def timeLoop():
    while True:
        VacChecker()
        time.sleep(1)

def VacChecker():
    key = ""    # Key generated from steam
    accountsList = ""
    players = []

    # open json file
    with open("accounts.json", "r") as accounts:
        accounts = json.load(accounts)

    # Filters through the given accounts and adds the steamID to a string
    for SteamID in accounts["accountDetails"]:
        accountsList = accountsList + SteamID["SteamID"] + ","

    banResponse = ApiUtils.getBannedStatus(key, accountsList)

    accountStatus = json.loads(banResponse, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))   # Loads json for the account status

    for i in accountStatus.players:

        nameResponse = ApiUtils.getAccountName(key, accountsList)   # Calls the function to get the account name passing through the current steamID
        accountData = json.loads(nameResponse, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))    # Loads the json for the account summaries

        # Checks if the steamIDs match and returns a name
        for x in accountData.response.players:
            if x.steamid == i.SteamId:
                name = x.personaname

        tempPlayer = Player(steamid=i.SteamId, communityStatus=i.CommunityBanned, vacStatus=i.VACBanned, steamName=name)
        players.append(tempPlayer)

    bannedAccount = ""
    print("---------------------------------------\n")
    # Checks the VAC status of the account and returns the steam name
    for i in players:
        if i.getVacStatus():
            print('\033[31m' + i.getSteamName() + " Has been VAC Banned\n")
            print('\033[39m')
            bannedAccount = i.getSteamName() + " Has been VAC Banned" + ", " + bannedAccount
            # Deleting VAC banned accounts
            #for SteamID in accounts["accountDetails"]:
            #    if SteamID["SteamID"] == i.getSteamid():
            #        del SteamID["SteamID"]

            #        with open("accounts.json", "w") as accounts:
            #            json.dump(SteamID, accounts)
        else:
            print('\033[32m' + i.getSteamName() + " Has NOT been VAC Banned\n")
            print('\033[39m')
            #print("Account Name: " + i.getSteamName() + " SteamID: " + i.getSteamid() + " has been removed from the check list!")

    print("---------------------------------------\n")
    return bannedAccount

#if __name__ == "__main__":
    #while True:
       #VacChecker()
        #time.sleep(30*60)   # Executes the code every 30 minutes