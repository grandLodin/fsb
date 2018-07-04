from typing import List
from pick import pick


class Fight:
	"""This class handles fighting logic"""

	def __init__(self, pArena):

		self.mArena: Arena() = pArena
		self.mGameLogger = self.mArena.mGameLogger
		self.mPlayerList: List[Player()] = self.mArena.mPlayerList
		self.mNumberOfPlayers = len(self.mPlayerList)
		self.mRound = 1

		while not self.isGameOver():
			self.startRound()
			self.deployMinion()
			self.fight()
			self.endRound()
		self.endGame()

	def startRound(self):
		""" Just a Screen that shows some stuff. No logic in here."""
		self.mGameLogger.clearConsole()
		startLog = "\n############## Start of Round -" + str(self.mRound) + "- ##############\n"
		self.mGameLogger.addString(startLog)

	def deployMinion(self):
		"""
		Lets the players deploy a minion, if still minions in hands
		:return: None
		"""
		if self.getNumberOfMinionsInHands > 0:
			for player in self.mPlayerList:
				if not player.isDead:
					input("press the any key to continue...")
					self.chooseMinion(player)

	def chooseMinion(self, pPlayer):
		"""every player chooses a Minion to deploy"""

		self.mGameLogger.clearConsole()
		dialog = pPlayer.mPlayerName + " select one of your minions"
		options = Minion.getMinionNamesAsList(pPlayer.mDeck.mMinionSet)
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
				minion = list(pPlayer.mDeck.mMinionSet)[index]
				print(str(minion))
				deploy = self.getInput_chooseMinion("Do you want to send " + minion.mMinionName + " in the Ring? (y/n)\n")
				self.mGameLogger.clearConsole()
				if deploy == "y":
					log = pPlayer.mPlayerName + " has chosen " + minionName + str(minion)
					self.mGameLogger.addString(log)
					self.mArena.mRing.add(minion)
					pPlayer.mDeck.mMinionSet.remove(minion)
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
		survivors = {entity for entity in self.mArena.mRing if not entity.isDead}
		self.mArena.mGraveyard.update(self.mArena.mRing.difference(survivors))
		self.mArena.mRing = survivors

	def endRound(self):
		""" Starts a new Round"""
		self.mGameLogger.addString(str(self))
		self.mRound += 1
		self.clearRingOfDeadBodies()
		input("press the any key to continue...")

	def isGameOver(self) -> bool:
		"""looks at all players health and returns true
		if only one player has more than zero health"""

		playersAlive = [player for player in self.mPlayerList if not player.isDead]
		if len(playersAlive) > 1:  # More than one player alive but no minions left to play and on board.
			if self.mArena.noMinionsInRing and self.mArena.noMinionsInHand:
						self.whoWon(playersAlive)
						return True
			else:  # More than one player alive but still minions left to play or on board.
				return False
		elif len(playersAlive) == 1:  # All enemy players dead, but still enemy minions on board.
			if len(playersAlive[0].findEnemyMinions(self.mArena.mRing)) > 0:
				return False
			else:  # All enemy players dead and no enemy minions on board.
				self.whoWon(playersAlive)
				return True
		else:  # No Player alive.
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
		Returns the number of minions in all players hands
		:return: number of minions as int
		"""
		numberOfMinionsInHand = 0
		for player in self.mPlayerList:
			numberOfMinionsInHand += len(player.mDeck.mMinionSet)
		return numberOfMinionsInHand

	def endGame(self):
		"""
		Just adds GAME OVER SCREEN  to the gamelogger
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

####### Getter for Inputs. Needed for Mocks ##########

	@staticmethod
	def getInput_chooseMinion(pText):
		return input(pText).lower()


from server.main.arena import Arena
from server.main.player import Player
from common.main.minion import Minion
