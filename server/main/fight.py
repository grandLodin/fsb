from typing import List
from pick import pick
from server.main.arena import Arena
from server.main.player import Player
from common.main.minion import Minion


class Fight:
	"""This class handles fighting logic"""

	def __init__(self):

		# TODO LPO: Fight should be in arena and not vice versa
		self.mArena = Arena()
		self.mGameLogger = self.mArena.mGameLogger
		self.mPlayerList: List[Player()] = self.mArena.mPlayerList
		self.mNumberOfPlayers = len(self.mPlayerList)
		self.mRound = 1
		self.mNumberOfMinionsInHand = self.getNumberOfMinionsInHands

		while not self.isGameOver():
			self.startRound()
			input("press the any key to continue to the fight...")
			if self.mNumberOfMinionsInHand > 0:
				for player in self.mPlayerList:
					if not player.isDead:
						self.chooseMinion(player)
			self.fight()
			self.clearRingOfDeadBodies()
			self.endRound()
		self.endGame()

	def fight(self):
		"""all minions fight"""
		for item in self.mArena.mRing:
			if item.__class__.__name__ == "Minion":
				item.attack(self.mArena.mRing)
				self.mGameLogger.addString(item.mGameLogger.mLogString)

	def endRound(self):
		""" Starts a new Round"""
		self.mRound += 1
		self.mNumberOfMinionsInHand = self.getNumberOfMinionsInHands
		input("press the any key to continue...")

	def startRound(self):
		startlog = "############## Start of Round -"+str(self.mRound)+"- ##############"
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
				print(Minion.printMinion(minion))
				deploy = input("Do you want to send " + minion.mMinionName + " in the Ring? (y/n)\n")
				self.mGameLogger.clearConsole()
				if deploy == "y":
					log = pPlayer.mPlayerName + " has chosen " + minionName + Minion.printMinion(minion)
					self.mGameLogger.addString(log)
					self.mArena.mRing.append(minion)
					del pPlayer.mDeck.mMinionList[index]
				else:
					self.chooseMinion(pPlayer)
		input("press the any key to continue...")
		self.mGameLogger.clearConsole()

	# TODO LPO move to Arena class
	def clearRingOfDeadBodies(self):
		""" puts dead minions on the graveyard"""

		survivors = []
		for entity in self.mArena.mRing:
			if not entity.isDead:
				survivors.append(entity)
			else:
				self.mArena.mGraveyard.append(entity)
		self.mArena.mRing = survivors

	# TODO LPO move to Arena class
	def isGameOver(self):
		"""looks at all players health and returns true
		if only one player has more than zero health"""

		playersAlive = []
		for player in self.mPlayerList:
			if not player.isDead:
				playersAlive.append(player)
		if len(playersAlive) > 1:
			if self.mArena.noMinionsInRing():
				noMinionsLeftToPlay = True
				for player in playersAlive:
					if player.hasMinionsInHand():
						noMinionsLeftToPlay = False
					if noMinionsLeftToPlay:
						self.whoWon(playersAlive)
						return True
			else:
				return False

			return False
		if len(playersAlive) == 1:
			if len(playersAlive[0].findEnemyMinions(self.mArena.mRing)) > 0:
				return False
			else:
				self.whoWon(playersAlive)
				return True
		else: #No Player alive
			self.whoWon(playersAlive)
			return True

	# TODO LPO move to arena Class
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

	# TODO LPO move func to Arena
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






