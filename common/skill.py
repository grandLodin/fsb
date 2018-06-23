class Skill:
    """Defines a skill"""

    def __init__(self):
        """Constructor of class Skill"""
        self.mId = int
        self.mSkillName = str
        self.mDescription = str
        self.mEquipped = False
    
    def skill(self):
        """Base method for Skill"""
        pass
    
    @staticmethod
    def printSkill(pSkill):
        """Prints the Skill"""
        log = "\t\t" + pSkill.mSkillName + ", ID: " + str(pSkill.mId) + ", equipped: " + str(pSkill.mEquipped) + "\n\t\t" + pSkill.mDescription
        return log   

