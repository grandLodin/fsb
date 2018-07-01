from typing import List
from pick import pick

from server.main.entity import Entity


class Minion(Entity):
	"""Client class. This class creates a Minion entity."""

	def __init__(self):
		""" Constructor of the class CreateMinion . """

		super().__init__()
		self.mMinionName = str()
		self.mAttackPoints = int()
		self.mNumberOfSkills = int()

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
			else:  # attack player
				self.findTarget([pEnemies[0]])

	# TODO LPO: make it more general isSubclassInRing(subclass, pEnemies)
	@staticmethod
	def areEnemyMinionsInRing(pEnemies):
		""" looks through Ring and returns true is enemy Minions ar present """

		for item in pEnemies:
			if isinstance(item, Minion):
				return True
		return False

	# TODO LPO: make it more general removeSubclassFromEnemies(subclass, pEnemies)
	@staticmethod
	def removePlayersFromEnemies(pEnemies):
		""" goes through a list and removes item if class = Player
        returns cleaned list """

		enemies = []
		for item in pEnemies:
			if not isinstance(item, Player):
				enemies.append(item)
		return enemies

	def dealDamage(self, pTarget):
		"""Deals damage to minion or player"""

		pTarget.mCurrentHealthPoints -= self.mAttackPoints
		GameLogger.logDamage(self, pTarget)

	def createMinionDialog(self, pOtherMinionsList, pAttributePointsLeft):
		"""A dialog to create a Minion"""

		self.setUniqueName(pOtherMinionsList)
		afterAttack = self.setAttackPoints(pAttributePointsLeft)
		afterHealth = self.setHealthPoints(afterAttack)
		self.mNumberOfSkills = 1
		self.mSkills = self.pickSkill(self.mMinionName)
		attributePointsLeft = afterHealth
		return self, attributePointsLeft

	def setUniqueName(self, pOtherMinionsList):
		"""Returns a name for a minion as String if the name was not choosen before"""

		name = self.getInput_setUniqueName("Give your minion a unique name: ")
		isNameUnique = True
		for item in pOtherMinionsList:
			if item.mMinionName == name:
				isNameUnique = False
		if not isNameUnique:
			print("The name \"" + str(name) + "\" has already been chosen.")
			self.setUniqueName(pOtherMinionsList)
		else:
			self.mMinionName = name

	def setAttackPoints(self, pAttributePoints) -> int:
		""" sets the Attack points of a minion """

		attributePointsLeft = int(pAttributePoints)
		if attributePointsLeft == 1:
			self.mAttackPoints = 0
			print("Attack points of " + str(self.mMinionName) + " were set to 0.")
			return 1
		else:
			print("Attribute points left: " + str(attributePointsLeft))
			try:
				attackPoints = self.getInput_setAttackPoints("Set " + str(self.mMinionName) + "s attack value: ")
			except ValueError:
				print("Value has to be of type integer")
				attackPoints = attributePointsLeft
			if attackPoints >= attributePointsLeft or attackPoints < 0:
				print("Invalid attack value! Choose a value between 0 and " + str(attributePointsLeft - 1))
				return self.setAttackPoints(pAttributePoints)
			else:
				self.mAttackPoints = attackPoints
				attributePointsLeft -= attackPoints
				return attributePointsLeft

	def setHealthPoints(self, pAttributePoints) -> int:
		"""
		Sets the Health points of this instance of a minion
		:param pAttributePoints: available attribute points
		:return: attribute points left after substraction of health points
		"""

		attributePointsLeft = int(pAttributePoints)
		if attributePointsLeft == 1:
			self.mHealthPoints = 1
			attributePointsLeft -= self.mHealthPoints
			print("Health points of " + str(self.mMinionName) + " were set to 1.")
			return 0
		else:
			print("Attribute points left: " + str(attributePointsLeft))
			try:
				healthPoints = self.getInput_setHealthPoints("Set " + str(self.mMinionName) + "s health value: ")
			except ValueError:
				print("Value has to be of type integer")
				healthPoints = attributePointsLeft + 1
			if healthPoints > attributePointsLeft or healthPoints <= 0:
				print("Invalid health value! Choose a positive value higher than 0 and below " + str(
					attributePointsLeft))
				return self.setHealthPoints(pAttributePoints)
			else:
				self.mHealthPoints = healthPoints
				attributePointsLeft -= self.mHealthPoints
				return attributePointsLeft

	def pickSkill(self, pMinionName):
		"""Adds a skill to a minion"""

		pickedSkills = 0
		minionSkills = MinionSkills()
		while pickedSkills < int(self.mNumberOfSkills):
			title = "Choose a skill for " + pMinionName + ": "
			options = minionSkills.getAllSkillNames()
			skillName, index = pick(options, title)
			print("picked Skill: " + skillName)
			minionSkills.equipSkill(index)
			pickedSkills += 1

		return minionSkills.getAllEquippedSkills()

	def parseMinion(self, pMinionDict, pPlayername):
		"""parses a Minion dictioniary to the Object Minion \n
        param: minion dictionary
        returns a minion instance"""

		self.mId = int(hash(str(pMinionDict) + pPlayername))
		self.mMinionName = pMinionDict["minionName"]
		self.mPlayerName = str(pPlayername)
		self.mAttackPoints = int(pMinionDict["attack"])
		self.mHealthPoints = int(pMinionDict["hp"])
		self.mCurrentHealthPoints = int(pMinionDict["hp"])
		self.mSkills = MinionSkills().findSkillsByNames(pMinionDict["skills"])
		return self


	@staticmethod
	def getEquippedSkillNames(pEquipedSkills):
		"""Returns a String of all Names of equiped skills. \n
        parameter: a List of equiped skills"""
		skillNames = []
		for skill in pEquipedSkills:
			skillNames.append(skill.mSkillName)
		return ','.join(skillNames)

	@staticmethod
	def getMinionNamesAsList(pMinionList: List) -> List[str]:
		"""
		Converts a list of Minion objects  into a list of names of the minions
		:param pMinionList:
		:return: List of names
		"""
		names: List[str] =[]
		for minion in pMinionList:
			names.append(minion.mMinionName)
		return names

	# TODO LPO: convert to __str__
	@staticmethod
	def printMinion(pMinion):
		"""Prints the stats of a minion and returns it as string"""

		log = "\n\t" + str(pMinion.mMinionName + "(" + str(pMinion.mAttackPoints) + "/" + str(
			pMinion.mHealthPoints) + ") \n\t\tSkills:")
		for skill in pMinion.mSkills:
			log += "\n" + Skill.printSkill(skill)
		return log

# ============== Getter for Inputs. Needed for Mocks ================

	@staticmethod
	def getInput_setUniqueName(pText):
		return str(input(pText))

	@staticmethod
	def getInput_setHealthPoints(pText):
		return int(input(pText))

	@staticmethod
	def getInput_setAttackPoints(pText):
		return int(input(pText))


from common.main.minionskills import MinionSkills
from common.main.skill import Skill
from server.main.gamelogger import GameLogger
from server.main.player import Player
