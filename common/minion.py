import sys
from pick import pick

from common.minionskills import MinionSkills
from common.skill import Skill
from server.main.gamelogger import GameLogger

class Minion:
    """Client class. This class creates a Minion entity."""
    
    def __init__(self):
        """ Constructor of the class CreateMinion . """

        self.mId = int
        self.mGameLogger = GameLogger()
        self.mPlayerName = str
        self.mMinionName = str
        self.mAttackPoints = int
        self.mHealthPoints = int
        self.mCurrentHealthPoints = int 
        self.mAttributePointsLeft = int
        self.mNumberOfSkills = int
        self.mSkills = []
        self.mDead = False

    
    def attack(self, pRing):
        """Looks throug a List and adds them to a new List if enemy
        param: a List Minions and Players
        returns a List of enemies """

        enemies = []
        for item in pRing:
            if item.mPlayerName != self.mPlayerName:
                enemies.append(item)  

        self.findTarget(enemies)

    def findTarget(self, pEnemies):
        """ looks through a list of targets including 
        minions and players and decides who to attack"""

        if len(pEnemies) == 1:
            self.dealDamage(pEnemies[0])
        else:
            if self.areEnemyMinionsInRing(pEnemies):
                enemies = self.removePlayersFromEnemies(pEnemies)
                self.findTarget([enemies[0]])
            else: # attack player
                self.findTarget([pEnemies[0]])
    
    def areEnemyMinionsInRing(self, pEnemies):
        """ looks through Ring and returns true is enemy Minions ar present """

        for item in pEnemies:
            if item.__class__.__name__ == "Minion":
                return True
        return False

    def removePlayersFromEnemies(self, pEnemies):
        """ goes through a list and removes item if class = Player
        returns cleaned list """

        enemies = []
        for item in pEnemies:
            if not item.__class__.__name__ == "Player":
                enemies.append(item)
        return enemies

    def dealDamage(self, pTarget):
        """Deals damage to minion or player"""

        pTarget.mCurrentHealthPoints -= self.mAttackPoints

        if pTarget.__class__.__name__ == "Minion":            
            log= self.mMinionName + " dealt " + str(self.mAttackPoints) + " damage to " + pTarget.mMinionName + "\n"
        
        if pTarget.__class__.__name__ == "Player":
            log= self.mMinionName + " dealt " + str(self.mAttackPoints) + " damage to " + pTarget.mPlayerName + "\n"

        pTarget.mGameLogger.clear()
        pTarget.isDead()
        log += pTarget.mGameLogger.mLogString        
        self.mGameLogger.mLogString = log

    def createMinionDialog(self, pOtherMinionsList):
        """A dialog to create a Minion"""

        self.setUniqueName(pOtherMinionsList)    
        self.setAttackPoints()
        self.setHealthPoints()
        self.mNumberOfSkills = 1
        self.mSkills = self.pickSkill(self.mMinionName)
    
    def setUniqueName(self, pOtherMinionsList):
        """Returns a name for a minion as String if the name was not choosen before"""

        name = self.getInput_setUniqueName("Give your minion a unique name: ")
        isNameUnique = True
        for item in pOtherMinionsList:
            if item.mMinionName == name:
                isNameUnique = False
        if not isNameUnique:
            self.setUniqueName(pOtherMinionsList)
        else:
            self.mMinionName = name


    def setAttackPoints(self):
        """ sets the Attack points of a minion """ 

        if self.mAttributePointsLeft == 1:
            self.mAttackPoints = 0
            self.mAttributePointsLeft -= self.mAttackPoints
            print("Attack points of " + self.mMinionName + " were set to 0.")
        else:
            try:
                attackPoints = self.getInput_setAttackPoints("Set " + self.mMinionName + "s attack value: ")
            except ValueError:
                print("Value has to be of type integer")
                attackPoints = self.mAttributePointsLeft
            if attackPoints >= self.mAttributePointsLeft or attackPoints < 0 :
                print("Invalide Attack value! Choose a value between 0 and " + str(self.mAttributePointsLeft-1))
                self.setAttackPoints()
            else:
                self.mAttackPoints = attackPoints
                self.mAttributePointsLeft -= attackPoints

    
    def setHealthPoints(self):
        """ sets the Health points of a minion """ 

        if self.mAttributePointsLeft == 1:
            self.mHealthPoints = 1
            self.mAttributePointsLeft -= self.mHealthPoints
            print("Health points of " + self.mMinionName + " were set to 1.")
        else:
            try:
                healthPoints = self.getInput_setHealthPoints("Set " + self.mMinionName + "s health value: ")
            except ValueError:
                print("Value has to be of type integer")
                healthPoints = self.mAttributePointsLeft+1
            if healthPoints > self.mAttributePointsLeft or healthPoints <= 0:
                print("Invalide Health value! Choose a positive value higher than 0 and below " + str(self.mAttributePointsLeft))
                self.setHealthPoints()
            else:
                self.mHealthPoints = healthPoints
                self.mAttributePointsLeft -= self.mHealthPoints


    def pickSkill(self, pMinionName):
        """Adds a skill to a minion"""

        pickedSkills = 0
        while pickedSkills < self.mNumberOfSkills:
            title = "Choose a skill for " + pMinionName + ": "
            minionSkills = MinionSkills()
            options = minionSkills.getAllSkillNames()
            skillName, index = pick(options, title)
            print("picked Skill: " + skillName)
            minionSkills.equipSkill(index)
            pickedSkills += 1

        return minionSkills.getAllEquipedSkills()

    def isDead(self):
        """ returns true if hp below 1"""

        if self.mCurrentHealthPoints < 1:
            self.mDead = True
            log = self.mMinionName + " died." 
            self.mGameLogger.mLogString = log
    
    def parseMinion(self, pMinionDict, pPlayername):
        """parses a Minion dictioniary to the Object Minion \n
        param: minion dictionary
        returns a minion instance"""
        self.mId = int(hash(str(pMinionDict)+pPlayername))
        self.mMinionName = pMinionDict["minionName"]
        self.mPlayerName = str(pPlayername)
        self.mAttackPoints = int(pMinionDict["attack"])
        self.mHealthPoints = int(pMinionDict["hp"])
        self.mCurrentHealthPoints = int(pMinionDict["hp"])
        self.mSkills =  MinionSkills().findSkillsByNames(pMinionDict["skills"])
        return self
        
    @staticmethod
    def getEquippedSkillNames(self, pEquipedSkills):
        """Returns a String of all Names of equiped skills. \n 
        parameter: a List of equiped skills"""
        skillNames = []
        for skill in pEquipedSkills:
            skillNames.append(skill.mSkillName)
        return ','.join(skillNames)

    @staticmethod
    def printMinion(pMinion):
        """Prints the stats of a minion and returns it as string"""
        
        log = "\n\t" + str(pMinion.mMinionName + "(" + str(pMinion.mAttackPoints) + "/" + str(pMinion.mHealthPoints) + ") \n\t\tSkills:")
        for skill in pMinion.mSkills:
            log += "\n" + Skill.printSkill(skill)
        return log
            
######## Getter for Inputs. Needed for Mocks ###########

    def getInput_setUniqueName(self, pText):
        return str(input(pText))

    def getInput_setHealthPoints(self, pText):
        return int(input(pText))

    def getInput_setAttackPoints(self, pText):
        return int(input(pText))