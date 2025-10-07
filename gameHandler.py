from time import sleep
from .Variables import *
from .gameController import gameController
from .Tools import *
import asyncio

class gameHandler:
	"""Class keeping track of what's unlock for the game and handling interaction with the game."""
	lives = None
	bombs = None
	power = None
	endings = None
	stages = None
	continues = None

	difficulties = None
	characters = None

	gameController = None
	lastSpeeds = []

	bossBeaten = []
	extraBeaten = []

	firstCharacterUnlocked = False

	limitLives = 8
	limitBombs = 8

	def __init__(self):
		self.gameController = gameController()
		self.reset()
		self.initGame()

	#
	# Init Resources
	#

	def giveLives(self):
		self.gameController.setLives(self.lives)

	def giveBombs(self):
		self.gameController.setBombs(self.bombs)

	def givePower(self):
		self.gameController.setPower(self.power)

	def giveContinues(self):
		self.gameController.setContinues(3 - self.continues)

	def setDifficulty(self, excludeEasy = False):
		self.gameController.setDifficulty(self.getLowestDifficulty(excludeEasy))

	def initResources(self, normalMode = False):
		if normalMode:
			self.giveContinues()

	def updateStageList(self, practiceMode = True):
		for characters in CHARACTERS:
			for difficulty in range(4):
				stage = 0x01
				# If we are not in practice mode, we do not update the stage
				if practiceMode and self.characters[characters] and self.difficulties[difficulty]:
					stage = getIntFromBinaryArray(self.stages[characters])

				self.gameController.setCharacterDifficulty(characters, difficulty, stage)

	def updatePracticeScore(self, locations, checked_location):
		scores = {}
		for character in CHARACTERS:
			scores[character] = {}
			for difficulty in range(4):
				scores[character][difficulty] = {}
				for stage in range(8):
					scores[character][difficulty][stage] = [0, 0, 0]

		# We check each locations to see which one has been done
		for id, location_data in locations.items():
			if id in checked_location:
				character = location_data[0]
				stage = location_data[1]
				counter = location_data[2]
				difficulty = location_data[3]

				# If it's not the Extra
				if stage < 8:
					if difficulty >= 0:
						scores[character][difficulty][stage][counter] += 1
					else:
						scores[character][EASY][stage][counter] += 1
						scores[character][NORMAL][stage][counter] += 1
						scores[character][HARD][stage][counter] += 1
						scores[character][LUNATIC][stage][counter] += 1

		# We set the scores depending on the counter
		for character in CHARACTERS:
			for difficulty in range(4):
				for stage in range(8):
					score = 0
					if scores[character][difficulty][stage][0] > 0:
						score += 555555555
					if scores[character][difficulty][stage][1] > 0:
						score += 222222222
					if scores[character][difficulty][stage][1] > 1:
						score += 222222222

					self.gameController.setPracticeStageScore(character, difficulty, stage, score)

	def updateExtraUnlock(self, otherMode = False):
		"""
		Update access to the Extra stage
		"""
		canExtra = self.canExtra()
		if canExtra or otherMode:
			for characters in CHARACTERS:
				if self.characters[characters] and (self.hasExtra[characters] or otherMode):
					self.gameController.setCharacterDifficulty(characters, EXTRA, 0xFF)
				else:
					self.gameController.setCharacterDifficulty(characters, EXTRA, 0x00)
		else:
			for characters in CHARACTERS:
				self.gameController.setCharacterDifficulty(characters, EXTRA, 0x00)

	#
	# Boss
	#

	def isCurrentBossDefeated(self, counter):
		isDefeated = False
		# If it's the extra stage
		if self.gameController.getStage() == 9:
			isDefeated = self.extraBeaten[self.gameController.getCharacter()][counter]
		else:
			isDefeated = self.bossBeaten[self.gameController.getCharacter()][self.gameController.getDifficulty()][self.gameController.getStage()-1][counter]

		return isDefeated

	def setCurrentStageBossBeaten(self, counter, otherDifficulties = False):
		"""
		Set the boss of the current stage with the current character as beaten.
		"""

		if self.gameController.getStage() == 9:
			self.extraBeaten[self.gameController.getCharacter()][counter] = True
		else:
			self.bossBeaten[self.gameController.getCharacter()][self.gameController.getDifficulty()][self.gameController.getStage()-1][counter] = True
			if otherDifficulties:
				if self.difficulties[EASY]:
					self.bossBeaten[self.gameController.getCharacter()][EASY][self.gameController.getStage()-1][counter] = True
				if self.difficulties[NORMAL] and self.gameController.getDifficulty() >= 1:
					self.bossBeaten[self.gameController.getCharacter()][NORMAL][self.gameController.getStage()-1][counter] = True
				if self.difficulties[HARD] and self.gameController.getDifficulty() >= 2:
					self.bossBeaten[self.gameController.getCharacter()][HARD][self.gameController.getStage()-1][counter] = True
				if self.difficulties[LUNATIC] and self.gameController.getDifficulty() >= 3:
					self.bossBeaten[self.gameController.getCharacter()][LUNATIC][self.gameController.getStage()-1][counter] = True

	def setBossBeaten(self, character, stage, counter, difficulty = -1):
		# If we have a valid difficulty
		if difficulty >= 0 and difficulty < 4:
			self.bossBeaten[character][difficulty][stage][counter] = True
		# If it's the Extra Stage
		elif stage == 6:
			self.extraBeaten[character][counter] = True
		# Else, we check all difficulties
		else:
			for diff in range(4):
				self.bossBeaten[character][diff][stage][counter] = True

	def isBossBeaten(self, character, stage, counter, difficulty = -1):
		flags = []
		# If we have a valid difficulty
		if difficulty >= 0 and difficulty < 4:
			flags.append(self.bossBeaten[character][difficulty][stage][counter])
		# If it's the Extra Stage
		elif stage == 8:
			flags.append(self.extraBeaten[character][counter])
		# Else, we check all difficulties
		else:
			for diff in range(4):
				flags.append(self.bossBeaten[character][diff][stage][counter])

		return True if True in flags else False

	#
	# Get Handler Functions
	#

	def getLives(self):
		return min(self.lives, self.limitLives)

	def getBombs(self):
		return min(self.bombs, self.limitBombs)

	def getPower(self):
		return self.power

	def getEndings(self):
		return self.endings

	def getLowestDifficulty(self, excludeEasy = False):
		"""
		Retrieve the lowest difficulty unlocked.
		"""
		difficulty = 3
		if(self.difficulties[EASY] and not excludeEasy):
			difficulty = 0
		elif(self.difficulties[NORMAL] or (self.difficulties[EASY] and excludeEasy)):
			difficulty = 1
		elif(self.difficulties[HARD]):
			difficulty = 2

		return difficulty

	def canExtra(self):
		"""
		If any character can access to the Extra stage.
		"""
		can = False
		for character in CHARACTERS:
			if self.characters[character] and self.hasExtra[character]:
				can = True
				break

		return can

	def getCharactersState(self):
		return self.characters

	#
	# Get Games Functions
	#

	def getGameMode(self):
		return self.gameController.getGameMode()

	def getMenu(self):
		return self.gameController.getMenu()

	def getDifficulty(self):
		return self.gameController.getDifficulty()

	def getMisses(self):
		return self.gameController.getMisses()

	def getCurrentLives(self):
		return self.gameController.getLives()

	def isBossPresent(self):
		# If we are in stage 2 or stage 5, we check differently
		check = False
		if self.gameController.getStage() == 2 or self.gameController.getStage() == 6:
			if self.gameController.getIsBossPresent2() == 1:
				first_boss_present = self.gameController.getIsBossPresent1()
				sleep(0.5)
				second_boss_present = self.gameController.getIsBossPresent1()
				check = first_boss_present == 1 or second_boss_present == 1
		else:
			check = self.gameController.getIsBossPresent1() == 1 or self.gameController.getIsBossPresent2() == 1

		return check

	def getCurrentStage(self):
		return self.gameController.getStage()

	def getCurrentPowerPoint(self):
		return self.gameController.getPower()

	def getCurrentScore(self):
		return self.gameController.getScore()

	def getCurrentContinues(self):
		return self.gameController.getContinues()

	def getCursorPosition(self):
		return self.gameController.getMenuCursor()

	def getCurrentCharacter(self):
		return self.gameController.getCharacter()

	#
	# Set Items Functions
	#

	def addLife(self, addInLevel = True):
		if(self.lives < 8):
			self.lives += 1

		self.gameController.setStartingLives(self.getLives())
		self.gameController.setNormalContinueLives(self.getLives())

		if addInLevel and self.gameController.getGameMode() == IN_GAME:
			self.gameController.setLives(self.gameController.getLives() + 1)

	def addBomb(self, addInLevel = True):
		if(self.bombs < 8):
			self.bombs += 1

		self.gameController.setStartingBombs(self.getBombs())

		if addInLevel and self.gameController.getGameMode() == IN_GAME:
			self.gameController.setBombs(self.gameController.getBombs() + 1)

	def add1Power(self, addInLevel = True):
		if(self.power < 128):
			self.power += 1

		self.gameController.setStartingPowerPoint(self.power)

		if addInLevel and self.gameController.getGameMode() == IN_GAME and self.gameController.getPower() < 128:
			self.gameController.setPower(self.gameController.getPower() + 1)

	def add25Power(self, addInLevel = True):
		if(self.power < 103):
			self.power += 25
		else:
			self.power = 128

		self.gameController.setStartingPowerPoint(self.power)

		if addInLevel and self.gameController.getGameMode() == IN_GAME:
			if self.gameController.getPower() < 103:
				self.gameController.setPower(self.gameController.getPower() + 25)
			else:
				self.gameController.setPower(128)

	def addProgressiveStage(self, extra = False, character = -1, both_stage_4 = True):
		character_list = [character] if character > -1 else CHARACTERS

		for character in character_list:
			no_new_stage = True
			for i in range(len(self.stages[character])):
				if self.stages[character][i] == 0:
					if i not in [3, 4] or both_stage_4 or (i == 3 and character in STAGE_4A_TEAM) or (i == 4 and character in STAGE_4B_TEAM):
						self.stages[character][i] = 1
						no_new_stage = False
						break

			if(no_new_stage and extra):
				self.unlockExtraStage(character)

	def addStage(self, stage, character = -1, both_stage_4 = True):
		character_list = [character] if character > -1 else CHARACTERS

		for character in character_list:
			if self.stages[character][stage] == 0:
				if stage not in [3, 4] or both_stage_4 or (stage == 3 and character in STAGE_4A_TEAM) or (stage == 4 and character in STAGE_4B_TEAM):
					self.stages[character][stage] = 1

	def addContinue(self):
		if(self.continues < 3):
			self.continues += 1

	def addTimePoint(self, value, addInLevel = True):
		self.time_point += value

		self.gameController.setStartingTimePoint(self.time_point)

		if addInLevel and self.gameController.getGameMode() == IN_GAME:
			self.gameController.setTimePoint(self.gameController.getTimePoint() + value)

	def addEnding(self, character, type):
		self.endings[character][type] += 1

	def unlockDifficulty(self, difficulty):
		self.difficulties[difficulty] = True

	def unlockExtraStage(self, character = -1):
		# Unlock for one character/shot type
		if character > -1:
			self.hasExtra[character] = True
		# Unlock for one character
		elif character > -1:
			self.hasExtra[character] = True
		# Unlock for all characters
		else:
			for character in CHARACTERS:
				self.hasExtra[character] = True

	def unlockCharacter(self, character):
		self.characters[character] = True

		# If it was the first character to be unlocked, we set the character to it for the cursor
		if not self.firstCharacterUnlocked:
			self.firstCharacterUnlocked = True

			if self.gameController.getMenu() not in [9, 11, 13]:
				self.gameController.setCharacter(character)

	def unlockTimeGain(self):
		self.gameController.setTimeGain(True)

	def setLivesLimit(self, limit):
		if limit >= 0 and limit <= 8:
			self.limitLives = limit
			self.gameController.setStartingLives(self.getLives())
			self.gameController.setNormalContinueLives(self.getLives())

	def setBombsLimit(self, limit):
		if limit >= 0 and limit <= 8:
			self.limitBombs = limit
			self.gameController.setStartingBombs(self.getBombs())

	#
	# Traps
	#

	def halfPowerPoint(self):
		if(self.gameController.getPower() > 0):
			self.gameController.setPower(self.gameController.getPower() // 2)

	def loseBomb(self):
		if(self.gameController.getBombs() > 0):
			self.gameController.setBombs(self.gameController.getBombs() - 1)

	def loseLife(self):
		if(self.gameController.getLives() > 0):
			self.gameController.setLives(self.gameController.getLives() - 1)

	def powerPointDrain(self):
		if(self.gameController.getPower() > 0):
			self.gameController.setPower(self.gameController.getPower() - 1)

	def reverseControls(self):
		self.gameController.setNormalSpeed(self.gameController.getNormalSpeed()*-1)
		self.gameController.setFocusSpeed(self.gameController.getFocusSpeed()*-1)
		self.gameController.setNormalSpeedD(self.gameController.getNormalSpeedD()*-1)
		self.gameController.setFocusSpeedD(self.gameController.getFocusSpeedD()*-1)

	def ayaSpeed(self):
		self.gameController.setNormalSpeed(self.gameController.getNormalSpeed()*4)
		self.gameController.setFocusSpeed(self.gameController.getFocusSpeed()/4)
		self.gameController.setNormalSpeedD(self.gameController.getNormalSpeedD()*4)
		self.gameController.setFocusSpeedD(self.gameController.getFocusSpeedD()/4)

	def freeze(self):
		self.lastSpeeds = [self.gameController.getNormalSpeed(), self.gameController.getFocusSpeed(), self.gameController.getNormalSpeedD(), self.gameController.getFocusSpeedD()]
		self.gameController.setNormalSpeed(0.0)
		self.gameController.setFocusSpeed(0.0)
		self.gameController.setNormalSpeedD(0.0)
		self.gameController.setFocusSpeedD(0.0)

	def resetSpeed(self):
		self.gameController.setNormalSpeed(self.lastSpeeds[0])
		self.gameController.setFocusSpeed(self.lastSpeeds[1])
		self.gameController.setNormalSpeedD(self.lastSpeeds[2])
		self.gameController.setFocusSpeedD(self.lastSpeeds[3])

	def setHumanYoukaiGauge(self, add):
		self.gameController.setHYGaugeGauge(add)

	def extendTimeGoal(self):
		self.gameController.setTimeGoal(self.gameController.getTimeGoal() + ((self.gameController.getTimeGoal()*25)//100))

	#
	# Other
	#

	def reconnect(self):
		self.gameController = gameController()
		self.initGame()

	def initGame(self):
		self.gameController.initAntiTemperHack()

		self.gameController.initStartingLives()
		self.gameController.initStartingBombs()
		self.gameController.initPowerHack()
		self.gameController.initTimeHack()

		self.gameController.setStartingLives(self.lives)
		self.gameController.setNormalContinueLives(self.lives)
		self.gameController.setStartingBombs(self.bombs)
		self.gameController.setStartingPowerPoint(self.power)
		self.gameController.setStartingTimePoint(self.time_point)

		self.gameController.initSoundHack()
		self.gameController.initDifficultyHack()
		self.gameController.setLockToAllDifficulty()
		self.gameController.disableDemo()
		self.gameController.forceLockSoloCharacter()
		self.gameController.initStageSelectHack()
		self.gameController.setAllClearStats(0xFF)
		self.gameController.setTimeGain(False)

	def reset(self):
		"""
		Method that initialize all the variables to their default values.
		"""
		# Default Value
		self.lives = 0
		self.bombs = 0
		self.power = 0
		self.continues = 0
		self.time_point = 0

		self.stages = {}
		for character in CHARACTERS:
			self.stages[character] = [1, 0, 0, 0, 0, 0, 0, 0]

		self.endings = {}
		for character in CHARACTERS:
			self.endings[character] = {}
			for ending in ENDINGS:
				self.endings[character][ending] = 0

		self.hasExtra = {}
		for character in CHARACTERS:
			self.hasExtra[character] = False

		self.difficulties = {LUNATIC: True, HARD: False, NORMAL: False, EASY: False}

		self.characters = {}
		for character in CHARACTERS:
			self.characters[character] = False

		self.bossBeaten = {}
		for character in CHARACTERS:
			self.bossBeaten[character] = {}
			for difficulty in range(4):
				self.bossBeaten[character][difficulty] = [[False, False, False], [False, False, False], [False, False, False], [False, False, False], [False, False, False], [False, False, False], [False, False], [False, False]]

		self.extraBeaten = {}
		for character in CHARACTERS:
			self.extraBeaten[character] = [False, False]

		self.lastSpeeds = [0, 0, 0, 0]

		self.firstCharacterUnlocked = False

	def playSound(self, soundId):
		self.gameController.setCustomSoundId(soundId)

	async def killPlayer(self):
		self.gameController.setKill(True)
		await asyncio.sleep(0.1)
		self.gameController.setKill(False)

	def giveCurrentPowerPoint(self, power):
		"""
		Give power point to the current stage
		"""
		if self.gameController.getGameMode() == IN_GAME:
			new_power = self.gameController.getPower() + power
			if(new_power > 128):
				new_power = 128
			elif(new_power < 0):
				new_power = 0

			self.gameController.setPower(new_power)

	def resetStageVariables(self):
		"""
		Method to be called when leaving a stage and reset the stage variables.
		"""
		self.gameController.resetBossPresent()

	def updateCursor(self, minValue = -1):
		"""
		Update the minimum cursor position value authorized.
		If -1, it will be the lowest difficulty.
		If -2, it will lock to 1 if the Extra Stage is not unlocked by any character.
		"""
		if minValue == -2:
			minValue = 1 if not self.canExtra() else 0
		else:
			minValue = self.getLowestDifficulty() if minValue == -1 else minValue
		self.gameController.setMinimumCursorDown(minValue)
		self.gameController.setMinimumCursorUp(minValue)

		# If the cursor is "out of bounds", we set it to the minimum value authorized
		if self.gameController.getMenuCursor() < minValue:
			self.gameController.setMenuCursor(minValue)

	async def displayMessage(self, text, color, timer = 2):
		"""
		Display text in game
		"""
		try:
			self.gameController.setFpsUpdate(False)

			if color in [WHITE_TEXT, BLUE_TEXT]:
				text_color = False if WHITE_TEXT else True
				textToDisplay = textToBytes(text, text_color)
				self.gameController.setFpsText(textToDisplay)
				await asyncio.sleep(timer)
			elif color == FLASHING_TEXT:
				currentTimer = timer
				text_color = True
				while currentTimer > 0:
					textToDisplay = textToBytes(text, text_color)
					self.gameController.setFpsText(textToDisplay)
					currentTimer -= 0.5
					text_color = not text_color
					await asyncio.sleep(0.5)

			self.gameController.setFpsUpdate(True)
		except Exception as e:
			pass

	def checkIfCurrentIsPossible(self, isNormalMode = False):
		"""
		Check if the current combinaison is a possible one we what is unlocked
		"""
		possible = True

		# Check difficulty
		if self.getDifficulty() < self.getLowestDifficulty():
			possible = False

		# Check character
		if not self.characters[self.gameController.getCharacter()]:
			possible = False

		# Check stage
		if not isNormalMode and (self.gameController.getStage() < 9 and self.stages[self.gameController.getCharacter()][self.gameController.getStage()-1] == 1) and (self.gameController.getStage() == 9 and self.hasExtra[self.gameController.getCharacter()]):
			possible = False

		return possible