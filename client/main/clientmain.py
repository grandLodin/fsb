import os
import sys

class ClientMain():
    """ Class Main for client """

    if __name__=='__main__':
        sys.path.append('././')
    
    from client.main.deck import Deck

    deck: Deck = Deck()
    deck.createDeckDialog()
    Deck.saveDeck(deck.createDictionary())
    input("Press the \'any\' key on your keyboard to continue...")

        
