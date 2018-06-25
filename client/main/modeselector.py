from pick import pick

class ModeSelector:
    """Lets the player choose between modes  """

    def __init__(self):
        self.mLoop: bool = True
        self.selectMode()

    def selectMode(self):
        """Lets the player choose between modes."""

        dialog: str = "Do you want to play, create a new deck, browse your decks or exit"
        options: list = ["Play", "Create a Deck", "Browse Decks", "Exit"]
        choice, index = pick(options, dialog)

        if index == 0:
            print("You choose: " + choice)
            from server.main.servermain import ServerMain
            ServerMain()
            self.mLoop = True

        if index == 1:
            print("You choose: " + choice)
            from client.main.clientmain import ClientMain
            ClientMain()
            self.mLoop = True        

        if index == 2:
            print("You choose: " + choice)
            from common.browsedecks import BrowseDecks
            BrowseDecks(True)
            self.mLoop = True

        if index == 3:
            print("You choose: " + choice)
            self.mLoop = False   
    