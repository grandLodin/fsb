from fsb.server.main.gamelogger import GameLogger 
from fsb.server.main.player import Player
class Arena:
    """Arena Object"""

    def __init__(self):
        self.mGameLogger = GameLogger()
        self.mPlayerList = []
        self.mNumberOfPlayers = int
        self.mNexusHealth = int

        self.mGameLogger.addString("Game starts. Have fun!")
        self.howManyPlayers()
        self.setNexusHealth()
        self.invitePlayers()
    
    def howManyPlayers(self):
        """this method returns the number of players"""
        numberOfPlayers = 2
        if numberOfPlayers > 0 and type(numberOfPlayers) == int:
            self.mNumberOfPlayers = numberOfPlayers
            log = "This is a " + str(self.mNumberOfPlayers) + " player match"
            self.mGameLogger.addString(log)
        else:
            print("Invalide number of players!")
            self.howManyPlayers()

    def setNexusHealth(self):
        """Sets the starting Healthpoints of the Nexusses"""
        try:
            nexushealth = int(input("Set Nexus health for each player: "))
        except ValueError:
            print("Value has to be of type integer")
            nexushealth = 0        
        if nexushealth > 0 and type(nexushealth) == int:
            self.mNexusHealth = nexushealth
            log = "Nexus health was set to " + str(self.mNexusHealth)
            self.mGameLogger.addString(log)
        else:
            print("Invalide Value. Value has to be a positive integer.")
            self.setNexusHealth() 

    def invitePlayers(self):
        """adds players to the arena"""
        i = 0
        while i < self.mNumberOfPlayers:
            player = Player()
            player.setUniquePlayerName(self.mPlayerList)
            player.setDeck()
            self.mPlayerList.append(player)
            self.mGameLogger.addString(player.mGameLogger.mLogString)
            i += 1

