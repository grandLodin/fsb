import os
import json
import uuid
from client.main.deck import Deck


class DeckHandler:

    def __init__(self, pPath = "./decks/decks"):
        self.mPath = pPath

    def list_decks(self, pUser):        

        dictList = list()
        alldecks_in_dir  = os.listdir(self.mPath)
        
        for filename in alldecks_in_dir:
            try:
                with open(os.path.join(self.mPath, filename)) as f:
                    deckDict = json.load(f)
                    if deckDict['creatorname'] == pUser:
                        dictList.append(deckDict)
            except Exception as e:
                print(filename,  e)
                continue
        return dictList

    def create_deck(self, pUserId, pDeckDict):
        """ test"""

        deck = pDeckDict
        deckId = uuid.uuid4()
        deck.update({'creatorname': pUserId})
        deck.update({'id':  deckId.hex})
        pathfilename = os.path.join(self.mPath, deckId.hex)
        try:
            with open(pathfilename, 'w+') as f:
                json.dump(deck, f)
                return deck
        except Exception as e:
            return e
 

    def delete_deck(self, pUserId, pDeckId):
        """test"""
        try:
            os.remove(os.path.join(self.mPath, pDeckId))
            return True
        except FileNotFoundError:
            return False