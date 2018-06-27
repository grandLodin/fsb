from typing import List

from common.minion import Minion
from server.main.gamelogger import GameLogger
from server.main.player import Player


class Arena:
    """Arena Object"""

    def __init__(self):
        self.mGameLogger: GameLogger() = GameLogger()
        self.mGameLogger.addString("Game starts. Have fun!")
        self.mPlayerList: List[Player()] = []
        self.mNumberOfPlayers: int = self.howManyPlayers()
        self.mNexusHealth: int = self.setNexusHealth()
        self.mRing: List = []
        self.mGraveyard: List = []
        self.invitePlayers()
    
    def howManyPlayers(self) -> int:
        """this method sets the number of players """

        global numberOfPlayers
        try:
            numberOfPlayers = self.getInput_setPlayerNumber("How many players? ")
        except ValueError:
            print("Invalid Value. Value has to be a positive integer.")
            self.howManyPlayers()
        if numberOfPlayers > 0 and type(numberOfPlayers) == int:
            log = "This is a " + str(numberOfPlayers) + " player match"
            self.mGameLogger.addString(log)
            return numberOfPlayers
        else:
            print("Invalid number of players!")
            self.howManyPlayers()

    def setNexusHealth(self) -> int:
        """Sets the starting Healthpoints of the Nexuses"""
        global nexushealth
        try:
            nexushealth = self.getInput_setNexusHealth("Set Nexus health for each player: ")
        except ValueError:
            print("Value has to be of type integer")
            nexushealth = 0        
        if nexushealth > 0 and type(nexushealth) == int:
            log = "Nexus health was set to " + str(nexushealth)
            self.mGameLogger.addString(log)
            return nexushealth
        else:
            print("Invalid Value. Value has to be a positive integer.")
            self.setNexusHealth()

    def invitePlayers(self):
        """adds players to the arena"""
        i = 0
        while i < self.mNumberOfPlayers:
            player = Player()
            player.setInitialPlayerHealth(self.mNexusHealth)
            player.setUniquePlayerName(self.mPlayerList)
            player.setDeck()
            self.mPlayerList.append(player)
            self.mRing.append(player)
            self.mGameLogger.addString(player.mGameLogger.mLogString)
            i += 1

    def noMinionsInRing(self) -> int:
        """ returns True if no minion in the ring
        @:returns number of Players as int """
        
        minionsInRing: List[Minion()] = []
        for item in self.mRing:
            if item.__class__.__name__ == "Minion":
                minionsInRing.append(item)
        return len(minionsInRing) == 0


######## Getter for Inputs. Needed for Mocks ###########

    @staticmethod
    def getInput_setPlayerNumber(pText):
        return int(input(pText))

    @staticmethod
    def getInput_setNexusHealth(pText) -> int:
        return int(input(pText))
