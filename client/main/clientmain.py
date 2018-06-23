import os
import sys

class ClientMain():
    """ Class Main for client """

    if __name__=='__main__':
        sys.path.append('././')
    
    from fsb.client.main.createdeck import CreateDeck

    deck = CreateDeck()
    deck.createDeckDialog()
    CreateDeck.saveDeck(deck.createDictionary())
    input("Press the \'any\' key on your keyboard to continue...")

        
