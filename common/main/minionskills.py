from common.main.skill import Skill

class MinionSkills:
    """Client class. This class contains the dialog to create a deck with minions."""
    
    def __init__(self):
        """ Constructor of the class MinionSkills. Creates all current skills"""
        self.mSkillList = []
        self.createSkill("Attack Face", "Minion attacks enemy Nexus if no taunt minion on board")      #ID 0
        self.createSkill("Attack Minion", "Minion attacks enemy Minion with lowest attack value")    #ID 1
        self.createSkill("Taunt", "Minion protects own Nexus by blocking Face attack minions")            #ID 2   

        self.setSkillIds()
        

    def createSkill(self, pName, pDescription):
        """Creates a skill"""

        newSkill = Skill()
        newSkill.mSkillName = str(pName)
        newSkill.mDescription = str(pDescription)
        newSkill.mEquipped = False

        self.mSkillList.append(newSkill)
    
    def equipSkill(self, pIndex):
        """Equips a Skill for a minion"""
        
        self.mSkillList[pIndex].mEquipped = True    

    def findSkillsByNames(self, pSkillNameList):
        """Looks at a List of Skill names and finds the corresponding skill Obj and adds it
        to a List of Skill Objects """

        skillList = []
        for skillname in pSkillNameList:
            for skill in self.mSkillList:
                if skillname == skill.mSkillName:
                    skill.mEquipped = True
                    skillList.append(skill)
        return skillList   

    def setSkillIds(self):
        """iterates through List of Skills and sets ascending Ids"""
        i = 0
        for skill in self.mSkillList:
            skill.mId = i
            i += 1
        
    def getAllSkillNames(self):
        """Returns a list of all skill names"""
        skillNameList = []
        for skill in self.mSkillList:            
            skillNameList.append(skill.mSkillName)
        return skillNameList

    def getAllEquipedSkills(self):
        """returns a list of all equiped skills"""
        equipSkills = []
        for skill in self.mSkillList:
            if skill.mEquipped:
                equipSkills.append(skill)
        return equipSkills
    
    
            