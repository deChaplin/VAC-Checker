from typing import List


class Player:
    def __init__(self, steamid, communityStatus, vacStatus, steamName) -> None:
        self.steamid = steamid
        self.communityStatus = communityStatus
        self.vacStatus = vacStatus
        self.steamName = steamName

    def getSteamid(self):
        return self.steamid

    def setSteamid(self, inSteamid):
        self.steamid = inSteamid

    def getCommunityStatus(self):
        return self.communityStatus

    def setCommunityStatus(self, isCommunityBanned):
        self.communityStatus = isCommunityBanned

    def getVacStatus(self):
        return self.vacStatus

    def setVacStatus(self, isVacBanned):
        self.vacStatus = isVacBanned

    def getSteamName(self):
        return self.steamName

    def setSteamName(self, name):
        self.steamName = name