class Entity:
	""" Parent class for Player and Minion"""

	def __init__(self):
		self.mId = int
		self.mGameLogger = GameLogger()
		self.mPlayerName = str()
		self.mHealthPoints = int()
		self.mCurrentHealthPoints = int()
		self.mSkills = list()

	@property
	def isDead(self):
		""" returns true if hp below 1"""

		if self.mCurrentHealthPoints < 1:
			return True
		else:
			return False


from server.main.gamelogger import GameLogger
