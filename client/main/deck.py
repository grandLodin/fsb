import datetime
from builtins import print


# noinspection PyAttributeOutsideInit,
class Deck:
	"""Client class. This class contains the dialog to create a deck with minions."""

	def __init__(self):
		self.mLog = str()
		self.mFilename = str()
		self.mDeckName = str()
		self.mCreatorname = str()
		self.mMaxAttributePoints = int()
		self.mMinionList = list()
		self.mDeckDict = dict()

	def createDeckDialog(self):
		"""Navigates through the steps necessary to create a Deck """

		self.mCreatorname = self.getInput_CreatorName("Enter your name: ")
		self.chooseDeckName()
		self.setMaxAttributePoints()
		self.createMinions(self.mMaxAttributePoints)
		print(str(self))
		self.mDeckDict = self.createDictionary()

	@property
	def autoFilename(self):
		"""creates a filename like: 2018-6-22-2396_Leo_10.json"""

		now = self.timenow()
		timestamp = '{}-{}-{}-{}{}{}'.format(now.year, now.month, now.day, now.hour, now.minute, now.second)
		prefixFilename = str(timestamp + "_" + self.mCreatorname + "_" + str(self.mMaxAttributePoints))
		return prefixFilename + ".json"

	@staticmethod
	def timenow():
		now = datetime.datetime.now()
		return now

	def setMaxAttributePoints(self):
		"""A dialog that sets the maximum attribute points to distribute"""
		try:
			maxAttrPoints = self.getInput_setMaxAttributePoints(
				"How many attribute points should your deck have in total? ")
			if int(maxAttrPoints) > 0:
				self.mMaxAttributePoints = maxAttrPoints
			else:
				print("Invalid Value! Must be higher than 0")
				self.setMaxAttributePoints()
		except ValueError:
			print("Invalid Value! Integer expected.")
			self.setMaxAttributePoints()

	def createMinions(self, pAttributePointsLeft):
		"""Navigates through the creation of a set of minions"""

		attributePointsLeft = pAttributePointsLeft
		while attributePointsLeft > 0:
			minion: Minion = Minion()
			minion, attributePointsLeft = minion.createMinionDialog(self.mMinionList, attributePointsLeft)
			self.mMinionList.append(minion)

	def chooseDeckName(self):
		"""Lets the player choose a Name for the Deck """
		try:
			self.mDeckName: str = self.getInput_chooseDeckName("Choose a Name for your Deck: ")
		# catch should be not necessary, but who knows..
		except ValueError:
			print("Invalid Name!")
			self.chooseDeckName()

	def createDictionary(self):
		"""Creates a Dictionary containing class variables"""
		dictionary: dict = {}
		dictionary.update({'deckname': self.mDeckName})
		dictionary.update({'filename': self.autoFilename})
		dictionary.update({'Creatorname': str(self.mCreatorname)})
		dictionary.update({'maxAttrPoints': str(self.mMaxAttributePoints)})
		minionListDict: dict = {}
		for minion in self.mMinionList:
			minionDict: dict = {}
			minionDict.update({'minionName': str(minion.mMinionName)})
			minionDict.update({'attack': str(minion.mAttackPoints)})
			minionDict.update({'hp': str(minion.mHealthPoints)})
			skillList: list = minion.mSkills
			skillNames: list = []
			for skill in skillList:
				skillNames.append(skill.mSkillName)
			minionDict.update({'skills': skillNames})
			minionListDict.update({minion.mMinionName: minionDict})
		dictionary.update({'minions': minionListDict})
		self.mDeckDict = dictionary
		return dictionary

	def parseDeck(self, pDeckDict, pPlayerName):
		"""parses a deck dictionary to its Class Param: Deck Dictionary Returns a Deck"""

		self.mLog = ""
		self.mDeckName = pDeckDict['deckname']
		self.mFilename = pDeckDict['filename']
		self.mCreatorname = pDeckDict['Creatorname']
		self.mMaxAttributePoints = int(pDeckDict['maxAttrPoints'])
		self.mMinionList = Deck.findMinionsInDeck(pDeckDict, pPlayerName)
		self.mDeckDict = pDeckDict
		return self

	@staticmethod
	def printDeckDict(pDeckDict):
		"""prints a Deck as string"""

		log = "\n\tCreator of the deck: " + pDeckDict['Creatorname']
		log += "\n\tDeckname: " + pDeckDict['deckname']
		log += "\n\tAttribute points spent: " + str(pDeckDict['maxAttrPoints'])
		log += "\n\tMinions:"
		for minion in Deck.findMinionsInDeck(pDeckDict, ""):
			log += str(minion)
		return log

	def __str__(self):
		log = "\n\tCreator of the deck: " + self.mCreatorname
		log += "\n\tDeckname: " + self.mDeckName
		log += "\n\tAttribute points spent: " + str(self.mMaxAttributePoints)
		log += "\n\tMinions:"
		for minion in self.mMinionList:
			log += str(minion)
		return log

	@staticmethod
	def selectDeck():
		"""Method to select a deck Returns a dictionary"""

		from common.main.browsedecks import BrowseDecks
		browseDeck = BrowseDecks(False)
		browseDeck.browseDecks()
		return browseDeck.mDeck

	@staticmethod
	def findMinionsInDeck(pDeckDict, pPlayerName):
		"""iterates through a deck and finds all minions Returns a List of Minions"""

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
		path = './decks/decks/'
		pathfilename = path + pDeckDict['filename']
		with open(pathfilename, 'w') as f:
			json.dump(pDeckDict, f)
		decksyspath = os.path.abspath(path)
		print("Deck saved in directory \"" + decksyspath + "\" as " + pDeckDict['filename'])

####### Getter for Inputs. Needed for Mocks ##########

	@staticmethod
	def getInput_CreatorName(pText) -> str:
		return str(input(pText))

	@staticmethod
	def getInput_setMaxAttributePoints(pText):
		return int(input(pText))

	@staticmethod
	def getInput_chooseDeckName(pText):
		return str(input(pText))


from common.main.minion import Minion
