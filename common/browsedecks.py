import os
import json
from pick import pick
from fsb.client.main.createdeck import CreateDeck

class BrowseDecks:
    """Lets the user look at all decks """

    def __init__(self, pIsinBrowseMode):
        self.mIsDeckSelected = False
        self.mPath = "./fsb/decks/"
        self.mDeck = {}
        self.mDeckName = str
        self.mIsinBrowseMode = pIsinBrowseMode
        self.browseDecks()
        

    def browseDecks(self):
        """Presents a list of all decks in the directory
        and lets the player select one deck to look at. """

        while self.mIsDeckSelected == False:                
            
            title = "Choose a deck"
            options = os.listdir(self.mPath)
            select, index = pick(options, title)
            print("Chosen deck: "+ select)
        
            with open(self.mPath+options[index]) as f:
                deckDict = json.load(f)
            print(CreateDeck.printDeck(deckDict))

            if self.mIsinBrowseMode:
                cont = input("Do you want to continue browsing? (y/n)  ")
                if cont == "y":
                    self.browseDecks()
                self.mIsDeckSelected = True
            else:
                done = input("Do you want to take this Deck? (y/n)  ")
                if done == "y":
                    self.mDeck = deckDict
                    self.mDeckName = select
                    self.mIsDeckSelected = True
                else:
                    self.browseDecks()


        