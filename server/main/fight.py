from typing import List
from pick import pick
from server.main.arena import Arena
from server.main.player import Player
from common.main.minion import Minion


class Fight:
	"""This class handles fighting logic"""

	def __init__(self, pArena):

		self.mArena = pArena
		self.mGameLogger = self.mArena.mGameLogger
		self.mPlayerList: List[Player()] = self.mArena.mPlayerList
		self.mNumberOfPlayers = len(self.mPlayerList)
		self.mRound = 1

		while not self.isGameOver():
			self.startRound()
			input("press the any key to continue to the fight...")
			if self.getNumberOfMinionsInHands > 0:
				for player in self.mPlayerList:
					if not player.isDead:
						self.chooseMinion(player)
			self.fight()
			self.endRound()
		self.endGame()

	def startRound(self):
		startlog = "\n############## Start of Round -"+str(self.mRound)+"- ##############\n"
		self.mGameLogger.clearConsole()
		self.mGameLogger.addString(startlog)

	def chooseMinion(self, pPlayer):
		"""every player chooses a Minion to deploy"""

		self.mGameLogger.clearConsole()
		dialog = pPlayer.mPlayerName + " select one of your minions"
		options = Minion.getMinionNamesAsList(pPlayer.mDeck.mMinionList)
		if len(options) == 0:
			emptyHandlog = pPlayer.mPlayerName + " has no minions left.\n"
			self.mGameLogger.addString(emptyHandlog)
		else:
			options.append("pass")
			minionName, index = pick(options, dialog)
			if minionName == "pass":
				passlog = pPlayer.mPlayerName + " passed.\n"
				self.mGameLogger.addString(passlog)
			else:
				minion = pPlayer.mDeck.mMinionList[index]
				print(str(minion))
				deploy = input("Do you want to send " + minion.mMinionName + " in the Ring? (y/n)\n")
				self.mGameLogger.clearConsole()
				if deploy == "y":
					log = pPlayer.mPlayerName + " has chosen " + minionName + str(minion)
					self.mGameLogger.addString(log)
					self.mArena.mRing.append(minion)
					del pPlayer.mDeck.mMinionList[index]
				else:
					self.chooseMinion(pPlayer)
		input("press the any key to continue...")
		self.mGameLogger.clearConsole()

	def fight(self):
		"""all minions fight"""
		for item in self.mArena.mRing:
			if isinstance(item, Minion):
				item.attack(self.mArena.mRing)
				self.mGameLogger.addString(item.mGameLogger.mLogString)

	def clearRingOfDeadBodies(self):
		""" puts dead minions on the graveyard"""

		survivors = []
		for entity in self.mArena.mRing:
			if not entity.isDead:
				survivors.append(entity)
			else:
				self.mArena.mGraveyard.append(entity)
		self.mArena.mRing = survivors

	def endRound(self):
		""" Starts a new Round"""
		self.mGameLogger.addString(str(self))
		self.mRound += 1
		self.clearRingOfDeadBodies()
		input("press the any key to continue...")

	def isGameOver(self):
		"""looks at all players health and returns true
		if only one player has more than zero health"""

		playersAlive = [player for player in self.mPlayerList if not player.isDead]
		if len(playersAlive) > 1:
			if self.mArena.noMinionsInRing and self.mArena.noMinionsInHand:
						self.whoWon(playersAlive)
						return True
			else:
				return False
		elif len(playersAlive) == 1:
			if len(playersAlive[0].findEnemyMinions(self.mArena.mRing)) > 0:
				return False
			else:
				self.whoWon(playersAlive)
				return True
		else: #No Player alive
			self.whoWon(playersAlive)
			return True

	def whoWon(self, pPlayersAlive):
		""" Finds the last man standing """

		if len(pPlayersAlive) == 0:
			log = "Nobody survived this vicious fight. RIP"
		elif len(pPlayersAlive) == 1:
			log = str(pPlayersAlive[0].mPlayerName) + " won the fight with " +\
			      str(pPlayersAlive[0].mCurrentHealthPoints) + " HP left."
		else:
			log = "Draw!"
		self.mGameLogger.addString(log)

	@property
	def getNumberOfMinionsInHands(self) -> int:
		"""
Returns the number of minions in this players hand
		:return: number of minions as int
		"""
		numberOfMinionsInHand = 0
		for player in self.mPlayerList:
			numberOfMinionsInHand += len(player.mDeck.mMinionList)
		return numberOfMinionsInHand

	def endGame(self):
		"""
Just adds GAME OVER to the gamelogger
		"""
		endlog = "#############GAME OVER#############"
		self.mGameLogger.addString(endlog)
		input("press the any key to continue...")

	def __str__(self):
		log = str()
		log += "\t\tEND OF ROUND -" + str(self.mRound) + "-\n\n"
		for player in self.mPlayerList:
			if player.isDead:
				log += "\n\t" + str(player.mPlayerName) + " is dead.\n"
			else:
				log += "\t" + str(player.mPlayerName) + " has " + str(player.mCurrentHealthPoints) + "HP left.\n"
			for minion in self.mArena.mRing:
				if minion.mPlayerName == player.mPlayerName and not isinstance(minion, Player):
					if minion.isDead:
						log += "\t\t" + str(minion.mMinionName) + " died.\n"
					else:
						log += "\t\t" + str(minion.mMinionName) + " A: " + str(minion.mAttackPoints) +\
						" HP: " + str(minion.mHealthPoints) + "/" + str(minion.mCurrentHealthPoints) + "\n"
						for skill in minion.mSkills:
							log += "\t" + str(skill) + "\n"
			log += "\n"
		return log

