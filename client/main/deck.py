import datetime
from common.minion import Minion

class Deck():
    """Client class. This class contains the dialog to create a deck with minions."""
    
    def __init__(self):
        self.mLog = str
        self.mFilename = str 
        self.mDeckName = str
        self.mCreatorname = str
        self.mMaxAttributePoints = 0
        self.mMinionList = []
        self.mDeckDict = None
    
    def createDeckDialog(self):
        """Navigates through the steps neccessary to create a Deck """

        self.mCreatorname = self.getInput_CreatorName("Enter your name: ")
        self.chooseDeckName()
        self.setMaxAttributePoints()
        self.mFilename = self.autoFilename()
        self.createMinions(self.mMaxAttributePoints)
        Deck.printDeck(self.createDictionary())

    
    
    def autoFilename(self):
        """creates a filename like: 2018-6-22-2396_Leo_10.json"""

        now = datetime.datetime.now()
        timestamp = '{}-{}-{}-{}{}{}'.format(now.year, now.month, now.day, now.hour, now.minute, now.second)
        prefixFilename = str(timestamp+"_"+ self.mCreatorname + "_" + str(self.mMaxAttributePoints))
        return prefixFilename + ".json"
    
    def setMaxAttributePoints(self):
        """A dialog that sets the maximum attribute points to distribute"""
        try:
            maxAttrPoints = self.getInput_setMaxAtributePoints("How many attribute points should your deck have in total? ")
            if maxAttrPoints > 0:
                self.mMaxAttributePoints = maxAttrPoints
            else:
                print("Invalide Value! Must be higher than 0")
                self.setMaxAttributePoints()

        except TypeError:
            print("Invalide Value! Integer expected.")
            self.setMaxAttributePoints()

    
    def createMinions(self, pAttributePointsLeft):
        """Navigates through the creation of a set of minions"""

        if(int(pAttributePointsLeft) > 0):
            print("Attribute points left: " + str(pAttributePointsLeft))
            minion = Minion()
            minion.mAttributePointsLeft = pAttributePointsLeft
            minion.createMinionDialog(self.mMinionList)
            if (minion.mAttackPoints + minion.mHealthPoints) > int(pAttributePointsLeft):
                print ("Not enough attribute points available.")
                self.createMinions(pAttributePointsLeft)               
            else:
                self.mMinionList.append(minion)
                attributePointsLeft = int(pAttributePointsLeft) - (minion.mAttackPoints + minion.mHealthPoints)                
                self.createMinions(attributePointsLeft)

    def chooseDeckName(self):
        """Lets the player choose a Name for the Deck """
        try:
            deckname = self.getInput_chooseDeckName("Choose a Name for your Deck: ")
            self.mDeckName = deckname
        # catch should be not neccessary, but who knows..
        except ValueError:
            print("Invalide Name!")
            self.chooseDeckName()    
    
    def createDictionary(self):
        """Creates a Dictionary containing class variables"""
        dictionary = {}
        dictionary.update({'deckname' : self.mDeckName})
        dictionary.update({'filename' : self.mFilename})
        dictionary.update({'Creatorname' : str(self.mCreatorname)})
        dictionary.update({'maxAttrPoints' : str(self.mMaxAttributePoints)})
        minionListDict = {}
        for minion in self.mMinionList:
            minionDict = {}
            minionDict.update({'minionName' : str(minion.mMinionName)})
            minionDict.update({'attack' : str(minion.mAttackPoints)})
            minionDict.update({'hp' : str(minion.mHealthPoints)})
            skillList = minion.mSkills 
            skillNames = []
            for skill in skillList:
                skillNames.append(skill.mSkillName)          
            minionDict.update({'skills' : skillNames})
            minionListDict.update({minion.mMinionName : minionDict})
        dictionary.update({'minions' : minionListDict})
        self.mDeckDict = dictionary
        return dictionary


    def parseDeck(self, pDeckDict, pPlayerName):
        """parses a deck dictionary to its Class 
        Param: Deck Dictionary
        Returns a Deck"""

        self.mLog = ""
        self.mDeckName = pDeckDict['deckname']
        self.mFilename = pDeckDict['filename']
        self.mCreatorname = pDeckDict['Creatorname']
        self.mMaxAttributePoints = int(pDeckDict['maxAttrPoints'])
        self.mMinionList = Deck.findMinionsInDeck(pDeckDict, pPlayerName)
        self.mDeckDict = pDeckDict
        return self
    
    @staticmethod
    def printDeck(pDeckDict):
        """prints a Deck as string"""

        log = "\n\tCreator of the deck: " + pDeckDict['Creatorname']  
        log += "\n\tDeckname: " + pDeckDict['deckname']
        log += "\n\tAttribute points spent: " + str(pDeckDict['maxAttrPoints'])
        log += "\n\tMinions:"            
        for minion in Deck.findMinionsInDeck(pDeckDict, ""):
            log += Minion.printMinion(minion)
        return log
    
    @staticmethod
    def selectDeck():
        """Method to select a deck
        Returns a dictionary"""

        from common.browsedecks import BrowseDecks

        browseDeck = BrowseDecks(False)
        return browseDeck.mDeck

    @staticmethod
    def findMinionsInDeck(pDeckDict, pPlayerName):
        """iterates through a deck and finds all minions
        Returns a List of Minions"""

        minionDict = pDeckDict['minions']
        minionList = []
        
        for key in minionDict:
            minion = Minion().parseMinion(minionDict[key], str(pPlayerName))
            minionList.append(minion)
        return minionList
  
    @staticmethod
    def saveDeck(pDeckDict):   
        """saves a dictionary as .json"""  
        
        import json
        import os
        path = './decks/'
        pathfilename = path+pDeckDict['filename']  
        with open(pathfilename, 'w') as f:
            json.dump(pDeckDict, f)
        decksyspath = os.path.abspath(path)
        print("Deck saved in directory \"" + decksyspath + "\" as " + pDeckDict['filename'])


####### Getter for Inputs. Needed for Mocks ##########

    def getInput_CreatorName(self, pText):
        return str(input(pText))                        
    
    def getInput_setMaxAtributePoints(self, pText):
        return int(input(pText))

    def getInput_chooseDeckName(self, pText):
        return str(input(pText))