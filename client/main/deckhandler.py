import os
import json
import uuid


class DeckHandler:

    def __init__(self, pPath="./decks/decks"):
        self.mPath = pPath

    def list_decks(self, pUser):        

        dict_list = list()
        alldecks_in_dir = os.listdir(self.mPath)
        
        for filename in alldecks_in_dir:
            try:
                with open(os.path.join(self.mPath, filename)) as f:
                    deckDict = json.load(f)
                    if deckDict['creatorname'] == pUser:
                        dict_list.append(deckDict)
            except Exception as e:
                print(filename,  e)
                continue
        return dict_list

    def create_deck(self, pUserId, pDeckDict):
        """ test"""

        deck = pDeckDict
        deck_id = uuid.uuid4()
        deck.update({'creatorname': pUserId})
        deck.update({'id':  deck_id.hex})
        pathfilename = os.path.join(self.mPath, deck_id.hex)
        try:
            with open(pathfilename, 'w+') as f:
                json.dump(deck, f)
                return deck
        except Exception as e:
            return e

    def get_deck(self, pUserId, pDeckId):
        """ returns a dictionary in .json format """

        try:
            with open(os.path.join(self.mPath, pDeckId)) as f:
                deck_dict = json.load(f)
                return deck_dict
        except FileNotFoundError:
            return {}

    def delete_deck(self, pUserId, pDeckId):
        """test"""
        try:
            os.remove(os.path.join(self.mPath, pDeckId))
            return True
        except FileNotFoundError:
            return False
