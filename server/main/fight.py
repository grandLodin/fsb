from pick import pick
from server.main.arena import Arena
from server.main.player import Player
from common.minion import Minion


class Fight:
    """This class handles fighting logic"""

    def __init__(self):

        self.mArena = Arena()
        self.mGameLogger = self.mArena.mGameLogger
        self.mPlayerList = self.mArena.mPlayerList
        self.mNumberOfPlayers = len(self.mPlayerList)
        self.mRound = 1
        self.mNumberOfMinionsInHand = self.getnumberOfMinionsInHands()

        while not self.isGameOver():
            self.startRound()
            if self.mNumberOfMinionsInHand > 0:
                for player in self.mPlayerList:
                    if not player.mDead:
                        self.chooseMinion(player)
            self.fight()
            self.clearRingOfDeadBodies()
            self.endRound()
        self.endGame()


    def fight(self):
        """all minions fight"""
        for item in self.mArena.mRing:
            if item.__class__.__name__ == "Minion":
                item.attack(self.mArena.mRing)
                self.mGameLogger.addString(item.mGameLogger.mLogString)

    def endRound(self):
        """ Starts a new Round"""                
        self.mRound += 1
        self.mNumberOfMinionsInHand = self.getnumberOfMinionsInHands()
        input("press the any key to continue...")

    def startRound(self):
        startlog = "##############Start of Round -"+str(self.mRound)+"- ##############"
        self.mGameLogger.addString(startlog)        



    def chooseMinion(self, pPlayer):
        """every player chooses a Minion to deploy"""       
        
        #print(pPlayer.mPlayerName + "s MinionList:\n" + str(pPlayer.mDeck.mDeckName) )
        dialog = pPlayer.mPlayerName + " select one of your minions"
        options = self.getMinionNamesAsList(pPlayer.mDeck.mMinionList)
        if len(options) == 0:
            emptyHandlog = pPlayer.mPlayerName +  " has no minions left.\n"
            self.mGameLogger.addString(emptyHandlog)
        else:
            options.append("pass")
            minionName, index = pick(options, dialog)
            if minionName == "pass":
                passlog = pPlayer.mPlayerName + " passed.\n"
                self.mGameLogger.addString(passlog)
            else:
                minion = pPlayer.mDeck.mMinionList[index]
                print(Minion.printMinion(minion))
                deploy = input("Do you want to send " + minion.mMinionName + " in the Ring? (y/n)\n")
                if deploy == "y":                            
                    log = pPlayer.mPlayerName + " has chosen " + minionName + Minion.printMinion(minion)
                    self.mGameLogger.addString(log)
                    self.mArena.mRing.append(minion)
                    del pPlayer.mDeck.mMinionList[index]                    
                else:
                    self.chooseMinion(pPlayer)
        input("press the any key to continue...")
        
    
    def clearRingOfDeadBodies(self):
        """ puts dead minions on the graveyard"""

        for i, entity in enumerate(self.mArena.mRing):
            if entity.mDead:
                del self.mArena.mRing[i]
                self.mArena.mGraveyard.append(entity)
    

    def isGameOver(self):
        """looks at all players health and returns true 
        if only one player has more than zero health"""
        
        playersAlive = []
        for player in self.mPlayerList:
            if not player.mDead:
                playersAlive.append(player)
        if len(playersAlive) > 1:
            if self.mArena.noMinionsInRing():
                noMinionsLeftToPlay = True
                for player in playersAlive:
                    if player.hasMinionsInHand():
                        noMinionsLeftToPlay = False
                return noMinionsLeftToPlay
            else:
                return False

            return False
        if len(playersAlive) == 1:
            if len(playersAlive[0].findEnemyMinions(self.mArena.mRing)) > 0:
                return False
            else:                    
                self.whoWon(playersAlive)
                return True
        else: #no Player alive            
            self.whoWon(playersAlive)
            return True
    
    def whoWon(self, pPlayersAlive):
        """ Finds the last man standing """

        if len(pPlayersAlive) == 0:
            log = "Nobody survived this vicious fight. RIP"
        elif len(pPlayersAlive) == 1:
            log = str(pPlayersAlive[0].mPlayerName) + " won the fight with " + str(pPlayersAlive[0].mPlayerHealth) + "HP left."
        else:
            log = "Something went wrong here :/"
        self.mGameLogger.addString(log)
        
    def getnumberOfMinionsInHands(self):
        """looks into all player hands and counts the minions"""
        numberOfMinionsInHand = 0
        for player in self.mPlayerList:
            numberOfMinionsInHand += len(player.mDeck.mMinionList)
        return numberOfMinionsInHand

    def getMinionNamesAsList(self, pMinionList):
        """MinionList -> MinionNameList"""
        names = []
        for minion in pMinionList:
            names.append(minion.mMinionName)
        return names
    
    def endGame(self):
        endlog = "#############GAME OVER#############"    
        self.mGameLogger.addString(endlog)
        input("press the any key to continue...")





