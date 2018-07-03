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

    def __str__(self):
        return "\t\t" + self.mSkillName + "\n\t\t\t" + self.mDescription

