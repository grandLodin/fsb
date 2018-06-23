import os
import json

from client.main.createdeck import CreateDeck
from common.browsedecks import BrowseDecks
from common.minion import Minion
from server.main.gamelogger import GameLogger

class Player():
    """Class for Entity Player"""

    def __init__(self):
        self.mGameLogger = GameLogger()
        self.mName = str 
        self.mDeck = {}

        self.mPlayerHealth = int
        self.mCurrentHealthPoints = int
        self.mDead = False


    def setUniquePlayerName(self, pPlayerlist):
        """Checks if Player Name has already been choosen"""

        playerNumber =len(pPlayerlist)+1
        name = str(input("Player" + str(playerNumber) + " choose your Name:\n"))
        isNameUnique = True
        for item in pPlayerlist:
            if item.mName == name:
                isNameUnique = False
        if not isNameUnique:
            print("This Name is not available")
            self.setUniquePlayerName(pPlayerlist)
        else:
            self.mName = name            
            log = "Name of Player"+str(playerNumber)+" was set to: " + self.mName
            self.mGameLogger.addString(log)
        
    def setInitialPlayerHealth(self, pNexusHealth):
        """ """
        self.mPlayerHealth = pNexusHealth
        self.mCurrentHealthPoints = self.mPlayerHealth
    
    def setDeck(self):
        """set the mDeck member for Class Player"""

        deckDict = CreateDeck.selectDeck()
        deck = CreateDeck().parseDeck(deckDict)

        log = "\t" + self.mName + " selected the deck: " + deckDict['filename']
        log += CreateDeck.printDeck(deckDict)
        self.mGameLogger.addString(log)
        self.mDeck = deck

    def isDead(self):
        """ returns true is current hp of player is below 1"""
        if self.mCurrentHealthPoints < 1:
            return True
