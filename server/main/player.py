from server.main.entity import Entity


class Player(Entity):
    """Class for Entity Player"""

    def __init__(self):

        super().__init__()
        self.mDeck = Deck()

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
        self.mHealthPoints = pNexusHealth
        self.mCurrentHealthPoints = self.mHealthPoints

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



from client.main.deck import Deck
