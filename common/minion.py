import sys
from pick import pick

from common.minionskills import MinionSkills
from common.skill import Skill

class Minion:
    """Client class. This class creates a Minion entity."""
    
    def __init__(self):
        """ Constructor of the class CreateMinion . """

        self.mId = int
        self.mPlayer = str
        self.mMinionName = str
        self.mAttackPoints = int
        self.mHealthPoints = int
        self.mAttributePointsLeft = int
        self.mNumberOfSkills = int
        self.mSkills = []
    
    def createMinionDialog(self, pOtherMinionsList):
        """A dialog to create a Minion"""

        self.setUniqueName(pOtherMinionsList)    
        self.setAttackPoints()
        self.setHealthPoints()
        self.mNumberOfSkills = 1
        self.mSkills = self.pickSkill(self.mMinionName)
    
    def setUniqueName(self, pOtherMinionsList):
        """Returns a name for a minion as String if the name was not choosen before"""

        name = str(input("Give your minion a unique name: "))
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
                attackPoints = int(input("Set " + self.mMinionName + "s attack value: "))
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
                healthPoints = int(input("Set " + self.mMinionName + "s health value: "))
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
    
    def parseMinion(self, pMinionDict, pPlayername):
        """parses a Minion dictioniary to the Object Minion \n
        param: minion dictionary
        returns a minion instance"""
        self.mId = int(hash(str(pMinionDict)))
        self.mMinionName = pMinionDict["minionName"]
        self.mPlayer = str(pPlayername)
        self.mAttackPoints = int(pMinionDict["attack"])
        self.mHealthPoints = int(pMinionDict["hp"])
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
            
