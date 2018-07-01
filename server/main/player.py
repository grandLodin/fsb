

class Player:
    """Class for Entity Player"""

    def __init__(self):
        self.mGameLogger = GameLogger()
        self.mPlayerName = str 
        self.mDeck = Deck()

        self.mPlayerHealth = int
        self.mCurrentHealthPoints = int
        self.mDead = False

    def setUniquePlayerName(self, pPlayerlist):
        """Checks if Player Name has already been choosen"""

        playerNumber = len(pPlayerlist)+1
        name = str(input("Player" + str(playerNumber) + " choose your Name:\n"))
        isNameUnique = True
        for item in pPlayerlist:
            if item.mPlayerName == name:
                isNameUnique = False
        if not isNameUnique:
            print("This Name is not available")
            self.setUniquePlayerName(pPlayerlist)
        else:
            self.mPlayerName = name            
            log = "Name of Player"+str(playerNumber)+" was set to: " + self.mPlayerName
            self.mGameLogger.addString(log)
        
    def setInitialPlayerHealth(self, pNexusHealth):
        """ """
        self.mPlayerHealth = pNexusHealth
        self.mCurrentHealthPoints = self.mPlayerHealth
    
    def setDeck(self):
        """set the mDeck member for Class Player"""

        deckDict = Deck.selectDeck()
        self.mDeck = Deck().parseDeck(deckDict, self.mPlayerName)

        log = "\t" + self.mPlayerName + " selected the deck: " + deckDict['filename']
        log += Deck.printDeck(deckDict)
        self.mGameLogger.addString(log)

    def findEnemyMinions(self, pMinionList):
        """Looks throug a List of Minions and adds them to a List if enemy
        param: a List of Minions
        returns a List of enemy minions """

        enemyMinions = []
        for item in pMinionList:
            if item.mPlayerName != self.mPlayerName and item.__class__.__name__ == "Minion" :
                enemyMinions.append(item)
        return enemyMinions

    def hasMinionsInHand(self):
        """ returns True if Minionlist is empty """
        return len(self.mDeck.mMinionList) > 0

    def isDead(self):
        """ returns true is current hp of player is below 1"""
        if self.mCurrentHealthPoints < 1:
            self.mDead = True
            log = self.mPlayerName + " died.\n" 
            self.mGameLogger.mLogString = log


from client.main.deck import Deck
from server.main.gamelogger import GameLogger
