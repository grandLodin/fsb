from common.main.minion import Minion
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
        for item in pPlayerlist:
            if item.mPlayerName == name:
                print("This Name is not available")
                self.setUniquePlayerName(pPlayerlist)
        self.mPlayerName = name
        log = "Name of Player" + str(playerNumber) + " was set to: " + self.mPlayerName
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
        log += str(self.mDeck)
        self.mGameLogger.addString(log)

    def findEnemyMinions(self, pMinionSet):
        """Looks through a set of Minions and adds them to a List if enemy
        param: a List of Minions
        returns a set of enemy minions """

        return {item for item in pMinionSet if
                        item.mPlayerName != self.mPlayerName
                        and isinstance(item, Minion)}

    @property
    def hasMinionsInHand(self):
        """ returns True if Minionset is empty """
        return len(self.mDeck.mMinionSet) > 0


from client.main.deck import Deck

