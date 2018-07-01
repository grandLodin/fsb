import os
import datetime


class GameLogger:
	"""This Class loggs the game"""

	def __init__(self):
		self.mLogString = ""

	def addString(self, pString):
		"""adds a String to the logstring"""
		self.mLogString += "\n" + pString
		print("\n" + pString)

	def clear(self):
		"""clears the log by setting it to empty string """
		self.mLogString = ""

	def writeLog(self):
		"""opens a text file"""

		now = datetime.datetime.now()
		path = '././gamelogs/'
		timestamp = '{}-{}-{}-{}{}{}'.format(now.year, now.month, now.day, now.hour, now.minute, now.second)
		prefixFilename = str(path + timestamp)
		filename = prefixFilename + ".txt"

		with open(filename, "w") as textfile:
			textfile.write(self.mLogString)

		decksyspath = os.path.abspath(path)
		print("Game log saved in directory \"" + decksyspath + "\" as " + timestamp + ".txt")

	@staticmethod
	def clearConsole():
		os.system('cls' if os.name == 'nt' else 'clear')

	@staticmethod
	def logDamage(pAttacker, pTarget):
		"""
        :param pAttacker: The attacking minion
        :param pTarget: The target of the minion, can be instance of Minion or Player
        :return: void
        """

		name = str()
		if pTarget.__class__.__name__ == 'Minion':
			name = str(pTarget.mMinionName)
		if pTarget.__class__.__name__ == 'Player':
			name = str(pTarget.mPlayerName)

		log = str(pAttacker.mMinionName) + " dealt " + str(pAttacker.mAttackPoints) + \
		    " damage to " + str(name) + "\n"

		pTarget.mGameLogger.clear()
		if pTarget.isDead:
			pTarget.mGameLogger.deathLog(pTarget)
		log += pTarget.mGameLogger.mLogString
		pAttacker.mGameLogger.mLogString = log

	@staticmethod
	def deathLog(pEnitiy):

		log = str()
		if pEnitiy.__class__.__name__ == 'Player':
			log = str(pEnitiy.mPlayerName) + " died."

		if pEnitiy.__class__.__name__ == 'Minion':
			log = str(pEnitiy.mMinionName) + " died."

		pEnitiy.mGameLogger.mLogString = log
