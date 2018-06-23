from pick import pick
from fsb.server.main.arena import Arena
from fsb.server.main.player import Player
from fsb.common.minion import Minion
from fsb.client.main.createdeck import CreateDeck

class Fight:
    """This class handles fighting logic"""

    def __init__(self):

        self.mArean = Arena()
        self.mGameLogger = self.mArean.mGameLogger
        self.mPlayerList = self.mArean.mPlayerList
        self.mNumberOfPlayers = len(self.mPlayerList)
        self.mRound = 1
        self.mNumberOfMinionsInHand = self.getnumberOfMinionsInHands()

        # while not self.doWeHaveAWinner:
        #     if self.getnumberOfMinionsInHands > 0:
        #         self.chooseMinion()
        #         self.calculateDamage()

        while self.mNumberOfMinionsInHand > 0:
            self.chooseMinion()

        endlog = "#############GAME OVER#############"    
        self.mGameLogger.addString(endlog)
        input("press the any key to continue...")

    
    def deployMinion(self, pMinion):
        """Puts a Minion Obj in the Ring"""
        pass

    def chooseMinion(self):
        """every player chooses a Minion to deploy"""
        startlog = "##############Start of Round"+str(self.mRound)+"##############"
        self.mGameLogger.addString(startlog)
        for player in self.mPlayerList:
            print(player.mPlayerName + "s MinionList:\n" + str(player.mDeck.mDeckName) )
            dialog = player.mPlayerName + " select one of your minions"
            options = self.getMinionNamesAsList(player.mDeck.mMinionList)
            if len(options) == 0:
                emptyHandlog = player.mPlayerName +  " has no minions left.\n"
                self.mGameLogger.addString(emptyHandlog)
            else:
                options.append("pass")
                minionName, index = pick(options, dialog)
                if minionName == "pass":
                    passlog = player.mPlayerName + " passed.\n"
                    self.mGameLogger.addString(passlog)
                    pass
                else:
                    minion = player.mDeck.mMinionList[index]
                    log = player.mPlayerName + " has chosen " + minionName + Minion.printMinion(minion)
                    self.mGameLogger.addString(log)
                    self.deployMinion(minion)
                    del player.mDeck.mMinionList[index]
                    input("press the any key...")
        self.mRound += 1
        self.mNumberOfMinionsInHand = self.getnumberOfMinionsInHands()

    def doWeHaveAWinner(self):
        """looks at all players health and returns true 
        if only one player has more than zero health"""
        
        numberOfPlayersAlife = 0
        for player in self.mPlayerList:
            if int(player.mPlayerHealth) > 0:
                numberOfPlayersAlife += 1
        if numberOfPlayersAlife > 1:
            return False
        else:
            self.whoWon()
            return True
    
    def whoWon(self):
        """ Finds the last man standing """
        survivor = []
        for player in self.mPlayerList:
            if player.mPlayerHealth > 0:
                survivor.append(player)
        if len(survivor) == 0:
            log = "Nobody survived this vicious fight. RIP"
        elif len(survivor) == 1:
            log = str(survivor[0].mPlayerName) + " won the fight with " + str(survivor[0].mPlayerHealth) + "HP left."
        else:
            log = "Something went wrong here :/"
        print(log)
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





