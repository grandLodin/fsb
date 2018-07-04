from typing import Set


class Arena:
    """Arena Object"""

    def __init__(self):
        self.mGameLogger = GameLogger()
        self.mGameLogger.clearConsole()
        self.mGameLogger.addString("Game starts. Have fun!")
        self.mPlayerList: Set([Player()]) = set([])
        self.mNumberOfPlayers: int = self.howManyPlayers()
        self.mNexusHealth: int = self.setNexusHealth()
        self.mRing: set() = set([])
        self.mGraveyard: set() = set([])
        self.invitePlayers()
        self.mGameLogger.clearConsole()
        self.mFight = Fight(self)
    
    def howManyPlayers(self) -> int:
        """this method sets the number of players """

        try:
            numberOfPlayers = self.getInput_setPlayerNumber("How many players? ")
        except ValueError:
            print("Invalid Value. Value has to be a positive integer.")
            return self.howManyPlayers()
        if numberOfPlayers > 0:
            log = "This is a " + str(numberOfPlayers) + " player match"
            self.mGameLogger.addString(log)
            return numberOfPlayers
        else:
            print("Invalid number of players!")
            return self.howManyPlayers()

    def setNexusHealth(self) -> int:
        """Sets the starting Healthpoints of the Nexuses"""

        try:
            nexushealth = self.getInput_setNexusHealth("Set Nexus health for each player: ")
        except ValueError:
            print("Value has to be of type integer")
            return self.setNexusHealth()
        if nexushealth > 0:
            log = "Nexus health was set to " + str(nexushealth)
            self.mGameLogger.addString(log)
            return nexushealth
        else:
            print("Invalid Value. Value has to be a positive integer.")
            return self.setNexusHealth()

    def invitePlayers(self):
        """adds players to the arena"""
        i = 0
        while i < self.mNumberOfPlayers:
            self.mGameLogger.clearConsole()
            player = Player()
            player.setInitialPlayerHealth(self.mNexusHealth)
            player.setUniquePlayerName(self.mPlayerList)
            player.setDeck()
            self.mPlayerList.add(player)
            self.mRing.add(player)
            self.mGameLogger.addString(player.mGameLogger.mLogString)
            i += 1

    @property
    def noMinionsInRing(self) -> bool:
        """ returns True if no minion in the ring
        @:returns Boolean """
        
        minionsInRing = {item for item in self.mRing if isinstance(item, Minion)}
        return len(minionsInRing) == 0

    @property
    def noMinionsInHand(self) -> bool:
        """ returns True if no no Player has Minions left in hand to play
        @:returns Boolean """

        playersWithMinionsInHand = {player for player in self.mPlayerList if player.hasMinionsInHand()}
        return len(playersWithMinionsInHand) == 0


######## Getter for Inputs. Needed for Mocks ###########

    @staticmethod
    def getInput_setPlayerNumber(pText):
        return int(input(pText))

    @staticmethod
    def getInput_setNexusHealth(pText) -> int:
        return int(input(pText))


from common.main.minion import Minion
from server.main.gamelogger import GameLogger
from server.main.player import Player
from server.main.fight import Fight

