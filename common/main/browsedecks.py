import os
import json
from pick import pick


class BrowseDecks:
    """Lets the user look at all decks """

    def __init__(self, pIsinBrowseMode):
        self.mIsDeckSelected = False
        self.mPath = "./decks/decks/"
        self.mDeck = Deck()
        self.mDeckName = str
        self.mIsinBrowseMode = pIsinBrowseMode
        

    def browseDecks(self):
        """Presents a list of all decks in the directory
        and lets the player select one deck to look at. """

        while not self.mIsDeckSelected:
            
            select, options, index = self.getInput_pickDeck(self.mPath, "Choose a deck")
            print("Chosen deck: "+ select)
        
            with open(self.mPath+options[index]) as f:
                deckDict = json.load(f)
            print(Deck.printDeckDict(deckDict))

            if self.mIsinBrowseMode:
                cont = self.getInput_YesOrNo("Do you want to continue browsing? (y/n)  ")
                if cont == "y":
                    self.browseDecks()
                self.mIsDeckSelected = True
            else:
                done = self.getInput_YesOrNo("Do you want to take this Deck? (y/n)  ")
                if done == "y":
                    self.mDeck = deckDict
                    self.mDeckName = select
                    self.mIsDeckSelected = True
                else:
                    self.browseDecks()

####### Getter for Inputs. Needed for Mocks ##########

    @staticmethod
    def getInput_pickDeck(pPath, pText):
        title = pText
        options = os.listdir(pPath)
        select, index = pick(options, title)
        return select, options, index

    @staticmethod
    def getInput_YesOrNo(pText):
        ans = str(input(pText)).lower()
        return ans


from client.main.deck import Deck
