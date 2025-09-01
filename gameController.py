import pymem
import pymem.exception
from .Tools import getPointerAddress
from .Variables import *
from math import log

class gameController:
	"""Class accessing the game memory"""
	pm = None

	# Player
	addrStage = None
	addrDifficulty = None
	addrCharacter = None

	# Resources
	addrLives = None
	addrBombs = None
	addrPower = None
	addrContinues = None

	# Starting Resources
	addrStartingLives = None
	addrNormalContinueLives = None
	addrStartingBombs = None
	addrStartingPowerPoint = None

	# Stats
	addrMisses = None
	addrScore = None

	# Practice stage access
	addrIllusionEasy = None
	addrIllusionNormal = None
	addrIllusionHard = None
	addrIllusionLunatic = None

	addrMagicEasy = None
	addrMagicNormal = None
	addrMagicHard = None
	addrMagicLunatic = None

	addrDevilEasy = None
	addrDevilNormal = None
	addrDevilHard = None
	addrDevilLunatic = None

	addrNetherEasy = None
	addrNetherNormal = None
	addrNetherHard = None
	addrNetherLunatic = None

	# Extra stage access
	addrIllusionExtra = None
	addrMagicExtra = None
	addrDevilExtra = None
	addrNetherExtra = None

	# Practice stage score
	addrPracticeScore = None

	# Character speed
	addrNormalSpeed = None
	addrFocusSpeed = None
	addrNormalSpeedD = None
	addrFocusSpeedD = None

	# FPS
	addrFpsText = None
	addrFpsUpdate = None

	# Other
	addrControllerHandle = None
	addrInput = None
	addrGameMode = None
	addrMenu = None
	addrMenuCursor = None
	addrIsBossPresent1 = None
	addrIsBossPresent2 = None
	addrKillCondition = None
	addrCharacterLock = None
	addrForceExtra = None
	addrDemoCondition = None
	addrFocusCondition = None
	addrAntiTemperHack = None
	addrCharacterDefaultCursorCondition = None
	addrForceLockSoloCharacter = None

	# Resources Hack
	addrLifeHack1 = None
	addrLifeHack2 = None
	addrBombHack1 = None
	addrBombHack2 = None
	addrPowerHack1 = None
	addrPowerHack2 = None
	addrPowerHack3 = None
	addrPowerHack4 = None

	# Sound
	addrCustomSoundId = None
	addrSoundHack1 = None
	addrSoundHack2 = None

	# Difficulty
	addrMinimumCursorDown = None
	addrMinimumCursorUp = None
	addrDifficultyCondition = None
	addrLastDifficulty = None
	addrDefaultDifficulty1 = None
	addrDefaultDifficulty2 = None
	addrDefaultExtraDifficulty = None
	addrDifficultyCursorDefault = None

	# Time
	addrTime1 = None
	addrTime2 = None

	def __init__(self):
		self.pm = pymem.Pymem(GAME_NAME)

		self.addrStage = self.pm.base_address+ADDR_STAGE
		self.addrDifficulty = self.pm.base_address+ADDR_DIFFICULTY
		self.addrCharacter = self.pm.base_address+ADDR_CHARACTER

		self.addrLives = getPointerAddress(self.pm, self.pm.base_address+ADDR_LIVES[0], ADDR_LIVES[1:])
		self.addrBombs = getPointerAddress(self.pm, self.pm.base_address+ADDR_BOMBS[0], ADDR_BOMBS[1:])
		self.addrPower = getPointerAddress(self.pm, self.pm.base_address+ADDR_POWER[0], ADDR_POWER[1:])
		self.addrContinues = getPointerAddress(self.pm, self.pm.base_address+ADDR_CONTINUE[0], ADDR_CONTINUE[1:])

		self.addrStartingLives = self.pm.base_address+ADDR_STARTING_LIVES
		self.addrNormalContinueLives = self.pm.base_address+ADDR_NORMAL_CONTINUE_LIVES
		self.addrStartingBombs = self.pm.base_address+ADDR_STARTING_BOMBS
		self.addrStartingPowerPoint = self.pm.base_address+ADDR_STARTING_POWER_POINT

		self.addrMisses = self.pm.base_address+ADDR_MISSES
		self.addrScore = getPointerAddress(self.pm, self.pm.base_address+ADDR_SCORE[0], ADDR_SCORE[1:])

		self.addrIllusionEasy = self.pm.base_address+ADDR_ILLUSION_EASY
		self.addrIllusionNormal = self.pm.base_address+ADDR_ILLUSION_NORMAL
		self.addrIllusionHard = self.pm.base_address+ADDR_ILLUSION_HARD
		self.addrIllusionLunatic = self.pm.base_address+ADDR_ILLUSION_LUNATIC

		self.addrMagicEasy = self.pm.base_address+ADDR_MAGIC_EASY
		self.addrMagicNormal = self.pm.base_address+ADDR_MAGIC_NORMAL
		self.addrMagicHard = self.pm.base_address+ADDR_MAGIC_HARD
		self.addrMagicLunatic = self.pm.base_address+ADDR_MAGIC_LUNATIC

		self.addrDevilEasy = self.pm.base_address+ADDR_DEVIL_EASY
		self.addrDevilNormal = self.pm.base_address+ADDR_DEVIL_NORMAL
		self.addrDevilHard = self.pm.base_address+ADDR_DEVIL_HARD
		self.addrDevilLunatic = self.pm.base_address+ADDR_DEVIL_LUNATIC

		self.addrNetherEasy = self.pm.base_address+ADDR_NETHER_EASY
		self.addrNetherNormal = self.pm.base_address+ADDR_NETHER_NORMAL
		self.addrNetherHard = self.pm.base_address+ADDR_NETHER_HARD
		self.addrNetherLunatic = self.pm.base_address+ADDR_NETHER_LUNATIC

		self.addrIllusionExtra = [self.pm.base_address+ADDR_ILLUSION_EXTRA[0], self.pm.base_address+ADDR_ILLUSION_EXTRA[1], self.pm.base_address+ADDR_ILLUSION_EXTRA[2], self.pm.base_address+ADDR_ILLUSION_EXTRA[3]]
		self.addrMagicExtra = [self.pm.base_address+ADDR_MAGIC_EXTRA[0], self.pm.base_address+ADDR_MAGIC_EXTRA[1], self.pm.base_address+ADDR_MAGIC_EXTRA[2], self.pm.base_address+ADDR_MAGIC_EXTRA[3]]
		self.addrDevilExtra = [self.pm.base_address+ADDR_DEVIL_EXTRA[0], self.pm.base_address+ADDR_DEVIL_EXTRA[1], self.pm.base_address+ADDR_DEVIL_EXTRA[2], self.pm.base_address+ADDR_DEVIL_EXTRA[3]]
		self.addrNetherExtra = [self.pm.base_address+ADDR_NETHER_EXTRA[0], self.pm.base_address+ADDR_NETHER_EXTRA[1], self.pm.base_address+ADDR_NETHER_EXTRA[2], self.pm.base_address+ADDR_NETHER_EXTRA[3]]

		self.addrControllerHandle = self.pm.base_address+ADDR_CONTROLLER_HANDLER
		self.addrInput = self.pm.base_address+ADDR_INPUT
		self.addrGameMode = self.pm.base_address+ADDR_GAME_MODE
		self.addrMenu = getPointerAddress(self.pm, self.pm.base_address+ADDR_MENU[0], ADDR_MENU[1:])
		self.addrMenuCursor = getPointerAddress(self.pm, self.pm.base_address+ADDR_MENU_CURSOR[0], ADDR_MENU_CURSOR[1:])
		self.addrIsBossPresent1 = self.pm.base_address+ADDR_IS_BOSS_PRESENT_1
		self.addrIsBossPresent2 = self.pm.base_address+ADDR_IS_BOSS_PRESENT_2
		self.addrDemoCondition = self.pm.base_address+ADDR_DEMO_CONDITION
		self.addrFocusCondition = self.pm.base_address+ADDR_FOCUS_CONDITION
		self.addrAntiTemperHack = self.pm.base_address+ADDR_ANTI_TEMPER_HACK
		self.addrCharacterDefaultCursorCondition = self.pm.base_address+ADDR_CHARACTER_DEFAULT_CURSOR_CONDITION
		self.addrForceLockSoloCharacter = self.pm.base_address+ADDR_FORCE_LOCK_SOLO_CHARACTER

		self.addrKillCondition = self.pm.base_address+ADDR_KILL_CONDITION

		self.addrCharacterLock = [self.pm.base_address+ADDR_DIFFICULTY_LOCK]

		self.addrNormalSpeed = getPointerAddress(self.pm, self.pm.base_address+ADDR_NORMAL_SPEED[0], ADDR_NORMAL_SPEED[1:])
		self.addrFocusSpeed = getPointerAddress(self.pm, self.pm.base_address+ADDR_FOCUS_SPEED[0], ADDR_FOCUS_SPEED[1:])
		self.addrNormalSpeedD = getPointerAddress(self.pm, self.pm.base_address+ADDR_NORMAL_SPEED_D[0], ADDR_NORMAL_SPEED_D[1:])
		self.addrFocusSpeedD = getPointerAddress(self.pm, self.pm.base_address+ADDR_FOCUS_SPEED_D[0], ADDR_FOCUS_SPEED_D[1:])

		self.addrLifeHack1 = self.pm.base_address+ADDR_LIVES_HACK_1
		self.addrLifeHack2 = self.pm.base_address+ADDR_LIVES_HACK_2
		self.addrBombHack1 = self.pm.base_address+ADDR_BOMB_HACK_1
		self.addrBombHack2 = self.pm.base_address+ADDR_BOMB_HACK_2
		self.addrPowerHack1 = self.pm.base_address+ADDR_POWER_HACK_1
		self.addrPowerHack2 = self.pm.base_address+ADDR_POWER_HACK_2
		self.addrPowerHack3 = self.pm.base_address+ADDR_POWER_HACK_3
		self.addrPowerHack4 = self.pm.base_address+ADDR_POWER_HACK_4

		self.addrCustomSoundId = self.pm.base_address+ADDR_CUSTOM_SOUND_ID
		self.addrSoundHack1 = self.pm.base_address+ADDR_SOUND_HACK_1
		self.addrSoundHack2 = self.pm.base_address+ADDR_SOUND_HACK_2

		self.addrFpsText = self.pm.base_address+ADDR_FPS_TEXT
		self.addrFpsUpdate = self.pm.base_address+ADDR_FPS_UPDATE

		self.addrMinimumCursorDown = self.pm.base_address+ADDR_MINIMUM_CURSOR_DOWN
		self.addrMinimumCursorUp = self.pm.base_address+ADDR_MINIMUM_CURSOR_UP
		self.addrDifficultyCondition = self.pm.base_address+ADDR_DIFFICULTY_CONDITION
		self.addrDifficultyCursorDefault = [self.pm.base_address+ADDR_DIFFICULTY_CURSOR_DEFAULT[0], self.pm.base_address+ADDR_DIFFICULTY_CURSOR_DEFAULT[1], self.pm.base_address+ADDR_DIFFICULTY_CURSOR_DEFAULT[2]]

		self.addrPracticeScore = {
			ILLUSION_TEAM:
			{
				EASY:
				[
					self.pm.base_address+ADDR_ILLUSION_EASY_SCORE_1,
					self.pm.base_address+ADDR_ILLUSION_EASY_SCORE_2,
					self.pm.base_address+ADDR_ILLUSION_EASY_SCORE_3,
					self.pm.base_address+ADDR_ILLUSION_EASY_SCORE_4_A,
					self.pm.base_address+ADDR_ILLUSION_EASY_SCORE_4_B,
					self.pm.base_address+ADDR_ILLUSION_EASY_SCORE_5,
					self.pm.base_address+ADDR_ILLUSION_EASY_SCORE_6_A,
					self.pm.base_address+ADDR_ILLUSION_EASY_SCORE_6_B,
				],
				NORMAL:
				[
					self.pm.base_address+ADDR_ILLUSION_NORMAL_SCORE_1,
					self.pm.base_address+ADDR_ILLUSION_NORMAL_SCORE_2,
					self.pm.base_address+ADDR_ILLUSION_NORMAL_SCORE_3,
					self.pm.base_address+ADDR_ILLUSION_NORMAL_SCORE_4_A,
					self.pm.base_address+ADDR_ILLUSION_NORMAL_SCORE_4_B,
					self.pm.base_address+ADDR_ILLUSION_NORMAL_SCORE_5,
					self.pm.base_address+ADDR_ILLUSION_NORMAL_SCORE_6_A,
					self.pm.base_address+ADDR_ILLUSION_NORMAL_SCORE_6_B,
				],
				HARD:
				[
					self.pm.base_address+ADDR_ILLUSION_HARD_SCORE_1,
					self.pm.base_address+ADDR_ILLUSION_HARD_SCORE_2,
					self.pm.base_address+ADDR_ILLUSION_HARD_SCORE_3,
					self.pm.base_address+ADDR_ILLUSION_HARD_SCORE_4_A,
					self.pm.base_address+ADDR_ILLUSION_HARD_SCORE_4_B,
					self.pm.base_address+ADDR_ILLUSION_HARD_SCORE_5,
					self.pm.base_address+ADDR_ILLUSION_HARD_SCORE_6_A,
					self.pm.base_address+ADDR_ILLUSION_HARD_SCORE_6_B,
				],
				LUNATIC:
				[
					self.pm.base_address+ADDR_ILLUSION_LUNATIC_SCORE_1,
					self.pm.base_address+ADDR_ILLUSION_LUNATIC_SCORE_2,
					self.pm.base_address+ADDR_ILLUSION_LUNATIC_SCORE_3,
					self.pm.base_address+ADDR_ILLUSION_LUNATIC_SCORE_4_A,
					self.pm.base_address+ADDR_ILLUSION_LUNATIC_SCORE_4_B,
					self.pm.base_address+ADDR_ILLUSION_LUNATIC_SCORE_5,
					self.pm.base_address+ADDR_ILLUSION_LUNATIC_SCORE_6_A,
					self.pm.base_address+ADDR_ILLUSION_LUNATIC_SCORE_6_B,
				],
			},
			MAGIC_TEAM:
			{
				EASY:
				[
					self.pm.base_address+ADDR_MAGIC_EASY_SCORE_1,
					self.pm.base_address+ADDR_MAGIC_EASY_SCORE_2,
					self.pm.base_address+ADDR_MAGIC_EASY_SCORE_3,
					self.pm.base_address+ADDR_MAGIC_EASY_SCORE_4_A,
					self.pm.base_address+ADDR_MAGIC_EASY_SCORE_4_B,
					self.pm.base_address+ADDR_MAGIC_EASY_SCORE_5,
					self.pm.base_address+ADDR_MAGIC_EASY_SCORE_6_A,
					self.pm.base_address+ADDR_MAGIC_EASY_SCORE_6_B,
				],
				NORMAL:
				[
					self.pm.base_address+ADDR_MAGIC_NORMAL_SCORE_1,
					self.pm.base_address+ADDR_MAGIC_NORMAL_SCORE_2,
					self.pm.base_address+ADDR_MAGIC_NORMAL_SCORE_3,
					self.pm.base_address+ADDR_MAGIC_NORMAL_SCORE_4_A,
					self.pm.base_address+ADDR_MAGIC_NORMAL_SCORE_4_B,
					self.pm.base_address+ADDR_MAGIC_NORMAL_SCORE_5,
					self.pm.base_address+ADDR_MAGIC_NORMAL_SCORE_6_A,
					self.pm.base_address+ADDR_MAGIC_NORMAL_SCORE_6_B,
				],
				HARD:
				[
					self.pm.base_address+ADDR_MAGIC_HARD_SCORE_1,
					self.pm.base_address+ADDR_MAGIC_HARD_SCORE_2,
					self.pm.base_address+ADDR_MAGIC_HARD_SCORE_3,
					self.pm.base_address+ADDR_MAGIC_HARD_SCORE_4_A,
					self.pm.base_address+ADDR_MAGIC_HARD_SCORE_4_B,
					self.pm.base_address+ADDR_MAGIC_HARD_SCORE_5,
					self.pm.base_address+ADDR_MAGIC_HARD_SCORE_6_A,
					self.pm.base_address+ADDR_MAGIC_HARD_SCORE_6_B,
				],
				LUNATIC:
				[
					self.pm.base_address+ADDR_MAGIC_LUNATIC_SCORE_1,
					self.pm.base_address+ADDR_MAGIC_LUNATIC_SCORE_2,
					self.pm.base_address+ADDR_MAGIC_LUNATIC_SCORE_3,
					self.pm.base_address+ADDR_MAGIC_LUNATIC_SCORE_4_A,
					self.pm.base_address+ADDR_MAGIC_LUNATIC_SCORE_4_B,
					self.pm.base_address+ADDR_MAGIC_LUNATIC_SCORE_5,
					self.pm.base_address+ADDR_MAGIC_LUNATIC_SCORE_6_A,
					self.pm.base_address+ADDR_MAGIC_LUNATIC_SCORE_6_B,
				],
			},
			DEVIL_TEAM:
			{
				EASY:
				[
					self.pm.base_address+ADDR_DEVIL_EASY_SCORE_1,
					self.pm.base_address+ADDR_DEVIL_EASY_SCORE_2,
					self.pm.base_address+ADDR_DEVIL_EASY_SCORE_3,
					self.pm.base_address+ADDR_DEVIL_EASY_SCORE_4_A,
					self.pm.base_address+ADDR_DEVIL_EASY_SCORE_4_B,
					self.pm.base_address+ADDR_DEVIL_EASY_SCORE_5,
					self.pm.base_address+ADDR_DEVIL_EASY_SCORE_6_A,
					self.pm.base_address+ADDR_DEVIL_EASY_SCORE_6_B,
				],
				NORMAL:
				[
					self.pm.base_address+ADDR_DEVIL_NORMAL_SCORE_1,
					self.pm.base_address+ADDR_DEVIL_NORMAL_SCORE_2,
					self.pm.base_address+ADDR_DEVIL_NORMAL_SCORE_3,
					self.pm.base_address+ADDR_DEVIL_NORMAL_SCORE_4_A,
					self.pm.base_address+ADDR_DEVIL_NORMAL_SCORE_4_B,
					self.pm.base_address+ADDR_DEVIL_NORMAL_SCORE_5,
					self.pm.base_address+ADDR_DEVIL_NORMAL_SCORE_6_A,
					self.pm.base_address+ADDR_DEVIL_NORMAL_SCORE_6_B,
				],
				HARD:
				[
					self.pm.base_address+ADDR_DEVIL_HARD_SCORE_1,
					self.pm.base_address+ADDR_DEVIL_HARD_SCORE_2,
					self.pm.base_address+ADDR_DEVIL_HARD_SCORE_3,
					self.pm.base_address+ADDR_DEVIL_HARD_SCORE_4_A,
					self.pm.base_address+ADDR_DEVIL_HARD_SCORE_4_B,
					self.pm.base_address+ADDR_DEVIL_HARD_SCORE_5,
					self.pm.base_address+ADDR_DEVIL_HARD_SCORE_6_A,
					self.pm.base_address+ADDR_DEVIL_HARD_SCORE_6_B,
				],
				LUNATIC:
				[
					self.pm.base_address+ADDR_DEVIL_LUNATIC_SCORE_1,
					self.pm.base_address+ADDR_DEVIL_LUNATIC_SCORE_2,
					self.pm.base_address+ADDR_DEVIL_LUNATIC_SCORE_3,
					self.pm.base_address+ADDR_DEVIL_LUNATIC_SCORE_4_A,
					self.pm.base_address+ADDR_DEVIL_LUNATIC_SCORE_4_B,
					self.pm.base_address+ADDR_DEVIL_LUNATIC_SCORE_5,
					self.pm.base_address+ADDR_DEVIL_LUNATIC_SCORE_6_A,
					self.pm.base_address+ADDR_DEVIL_LUNATIC_SCORE_6_B,
				],
			},
			NETHER_TEAM:
			{
				EASY:
				[
					self.pm.base_address+ADDR_NETHER_EASY_SCORE_1,
					self.pm.base_address+ADDR_NETHER_EASY_SCORE_2,
					self.pm.base_address+ADDR_NETHER_EASY_SCORE_3,
					self.pm.base_address+ADDR_NETHER_EASY_SCORE_4_A,
					self.pm.base_address+ADDR_NETHER_EASY_SCORE_4_B,
					self.pm.base_address+ADDR_NETHER_EASY_SCORE_5,
					self.pm.base_address+ADDR_NETHER_EASY_SCORE_6_A,
					self.pm.base_address+ADDR_NETHER_EASY_SCORE_6_B,
				],
				NORMAL:
				[
					self.pm.base_address+ADDR_NETHER_NORMAL_SCORE_1,
					self.pm.base_address+ADDR_NETHER_NORMAL_SCORE_2,
					self.pm.base_address+ADDR_NETHER_NORMAL_SCORE_3,
					self.pm.base_address+ADDR_NETHER_NORMAL_SCORE_4_A,
					self.pm.base_address+ADDR_NETHER_NORMAL_SCORE_4_B,
					self.pm.base_address+ADDR_NETHER_NORMAL_SCORE_5,
					self.pm.base_address+ADDR_NETHER_NORMAL_SCORE_6_A,
					self.pm.base_address+ADDR_NETHER_NORMAL_SCORE_6_B,
				],
				HARD:
				[
					self.pm.base_address+ADDR_NETHER_HARD_SCORE_1,
					self.pm.base_address+ADDR_NETHER_HARD_SCORE_2,
					self.pm.base_address+ADDR_NETHER_HARD_SCORE_3,
					self.pm.base_address+ADDR_NETHER_HARD_SCORE_4_A,
					self.pm.base_address+ADDR_NETHER_HARD_SCORE_4_B,
					self.pm.base_address+ADDR_NETHER_HARD_SCORE_5,
					self.pm.base_address+ADDR_NETHER_HARD_SCORE_6_A,
					self.pm.base_address+ADDR_NETHER_HARD_SCORE_6_B,
				],
				LUNATIC:
				[
					self.pm.base_address+ADDR_NETHER_LUNATIC_SCORE_1,
					self.pm.base_address+ADDR_NETHER_LUNATIC_SCORE_2,
					self.pm.base_address+ADDR_NETHER_LUNATIC_SCORE_3,
					self.pm.base_address+ADDR_NETHER_LUNATIC_SCORE_4_A,
					self.pm.base_address+ADDR_NETHER_LUNATIC_SCORE_4_B,
					self.pm.base_address+ADDR_NETHER_LUNATIC_SCORE_5,
					self.pm.base_address+ADDR_NETHER_LUNATIC_SCORE_6_A,
					self.pm.base_address+ADDR_NETHER_LUNATIC_SCORE_6_B,
				],
			}
		}

	def getStage(self):
		stage = int.from_bytes(self.pm.read_bytes(self.addrStage, 1))
		# If it's 0, then it's the extra stage
		if stage == 0:
			return 9
		else:
			return int(log(stage, 2))+1

	def getDifficulty(self):
		return int.from_bytes(self.pm.read_bytes(self.addrDifficulty, 1))

	def getCharacter(self):
		return int.from_bytes(self.pm.read_bytes(self.addrCharacter, 1))

	def getLives(self):
		self.addrLives = getPointerAddress(self.pm, self.pm.base_address+ADDR_LIVES[0], ADDR_LIVES[1:])
		return int(self.pm.read_float(self.addrLives))

	def getBombs(self):
		self.addrBombs = getPointerAddress(self.pm, self.pm.base_address+ADDR_BOMBS[0], ADDR_BOMBS[1:])
		return int(self.pm.read_float(self.addrBombs))

	def getPower(self):
		self.addrPower = getPointerAddress(self.pm, self.pm.base_address+ADDR_POWER[0], ADDR_POWER[1:])
		return int(self.pm.read_float(self.addrPower))

	def getMisses(self):
		return int.from_bytes(self.pm.read_bytes(self.addrMisses, 1))

	def getScore(self):
		self.addrScore = getPointerAddress(self.pm, self.pm.base_address+ADDR_SCORE[0], ADDR_SCORE[1:])
		return self.pm.read_int(self.addrScore)

	def getContinues(self):
		self.addrContinues = getPointerAddress(self.pm, self.pm.base_address+ADDR_CONTINUE[0], ADDR_CONTINUE[1:])
		return int.from_bytes(self.pm.read_bytes(self.addrContinues, 1))

	def getIllusionEasy(self):
		return int.from_bytes(self.pm.read_bytes(self.addrIllusionEasy, 1))

	def getIllusionNormal(self):
		return int.from_bytes(self.pm.read_bytes(self.addrIllusionNormal, 1))

	def getIllusionHard(self):
		return int.from_bytes(self.pm.read_bytes(self.addrIllusionHard, 1))

	def getIllusionLunatic(self):
		return int.from_bytes(self.pm.read_bytes(self.addrIllusionLunatic, 1))

	def getIllusionExtra(self):
		return [
				int.from_bytes(self.pm.read_bytes(self.addrIllusionExtra[0], 1)),
				int.from_bytes(self.pm.read_bytes(self.addrIllusionExtra[1], 1)),
				int.from_bytes(self.pm.read_bytes(self.addrIllusionExtra[2], 1)),
				int.from_bytes(self.pm.read_bytes(self.addrIllusionExtra[3], 1))
			]

	def getMagicEasy(self):
		return int.from_bytes(self.pm.read_bytes(self.addrMagicEasy, 1))

	def getMagicNormal(self):
		return int.from_bytes(self.pm.read_bytes(self.addrMagicNormal, 1))

	def getMagicHard(self):
		return int.from_bytes(self.pm.read_bytes(self.addrMagicHard, 1))

	def getMagicLunatic(self):
		return int.from_bytes(self.pm.read_bytes(self.addrMagicLunatic, 1))

	def getMagicExtra(self):
		return [
				int.from_bytes(self.pm.read_bytes(self.addrMagicExtra[0], 1)),
				int.from_bytes(self.pm.read_bytes(self.addrMagicExtra[1], 1)),
				int.from_bytes(self.pm.read_bytes(self.addrMagicExtra[2], 1)),
				int.from_bytes(self.pm.read_bytes(self.addrMagicExtra[3], 1))
			]

	def getDevilEasy(self):
		return int.from_bytes(self.pm.read_bytes(self.addrDevilEasy, 1))

	def getDevilNormal(self):
		return int.from_bytes(self.pm.read_bytes(self.addrDevilNormal, 1))

	def getDevilHard(self):
		return int.from_bytes(self.pm.read_bytes(self.addrDevilHard, 1))

	def getDevilLunatic(self):
		return int.from_bytes(self.pm.read_bytes(self.addrDevilLunatic, 1))

	def getDevilExtra(self):
		return [
				int.from_bytes(self.pm.read_bytes(self.addrDevilExtra[0], 1)),
				int.from_bytes(self.pm.read_bytes(self.addrDevilExtra[1], 1)),
				int.from_bytes(self.pm.read_bytes(self.addrDevilExtra[2], 1)),
				int.from_bytes(self.pm.read_bytes(self.addrDevilExtra[3], 1))
			]

	def getNetherEasy(self):
		return int.from_bytes(self.pm.read_bytes(self.addrNetherEasy, 1))

	def getNetherNormal(self):
		return int.from_bytes(self.pm.read_bytes(self.addrNetherNormal, 1))

	def getNetherHard(self):
		return int.from_bytes(self.pm.read_bytes(self.addrNetherHard, 1))

	def getNetherLunatic(self):
		return int.from_bytes(self.pm.read_bytes(self.addrNetherLunatic, 1))

	def getNetherExtra(self):
		return [
				int.from_bytes(self.pm.read_bytes(self.addrNetherExtra[0], 1)),
				int.from_bytes(self.pm.read_bytes(self.addrNetherExtra[1], 1)),
				int.from_bytes(self.pm.read_bytes(self.addrNetherExtra[2], 1)),
				int.from_bytes(self.pm.read_bytes(self.addrNetherExtra[3], 1))
			]

	def getInput(self):
		return int.from_bytes(self.pm.read_bytes(self.addrInput, 1))

	def getGameMode(self):
		try:
			mode = int.from_bytes(self.pm.read_bytes(self.addrGameMode, 1))
		except pymem.exception.MemoryReadError as e:
			mode = -2

		return mode

	def getMenu(self):
		try:
			self.addrMenu = getPointerAddress(self.pm, self.pm.base_address+ADDR_MENU[0], ADDR_MENU[1:])
			menu = int.from_bytes(self.pm.read_bytes(self.addrMenu, 1))
		except pymem.exception.MemoryReadError as e:
			menu = -1

		return menu

	def getMenuCursor(self):
		self.addrMenuCursor = getPointerAddress(self.pm, self.pm.base_address+ADDR_MENU_CURSOR[0], ADDR_MENU_CURSOR[1:])
		return int.from_bytes(self.pm.read_bytes(self.addrMenuCursor, 1))

	def getNormalSpeed(self):
		self.addrNormalSpeed = getPointerAddress(self.pm, self.pm.base_address+ADDR_NORMAL_SPEED[0], ADDR_NORMAL_SPEED[1:])
		return self.pm.read_float(self.addrNormalSpeed)

	def getFocusSpeed(self):
		self.addrFocusSpeed = getPointerAddress(self.pm, self.pm.base_address+ADDR_FOCUS_SPEED[0], ADDR_FOCUS_SPEED[1:])
		return self.pm.read_float(self.addrFocusSpeed)

	def getNormalSpeedD(self):
		self.addrNormalSpeedD = getPointerAddress(self.pm, self.pm.base_address+ADDR_NORMAL_SPEED_D[0], ADDR_NORMAL_SPEED_D[1:])
		return self.pm.read_float(self.addrNormalSpeedD)

	def getFocusSpeedD(self):
		self.addrFocusSpeedD = getPointerAddress(self.pm, self.pm.base_address+ADDR_FOCUS_SPEED_D[0], ADDR_FOCUS_SPEED_D[1:])
		return self.pm.read_float(self.addrFocusSpeedD)

	def getCustomSoundId(self):
		return int.from_bytes(self.pm.read_bytes(self.addrCustomSoundId, 1))

	def getIsBossPresent1(self):
		return int.from_bytes(self.pm.read_bytes(self.addrIsBossPresent1, 1))

	def getIsBossPresent2(self):
		return int.from_bytes(self.pm.read_bytes(self.addrIsBossPresent2, 1))

	def getPracticeStageScore(self, characterId, difficultyId, stageId):
		return int.from_bytes(self.pm.read_bytes(self.addrPracticeScore[characterId][difficultyId][stageId], 4))

	def getMinimumCursorDown(self):
		return int.from_bytes(self.pm.read_bytes(self.addrMinimumCursorDown, 1))

	def getMinimumCursorUp(self):
		return int.from_bytes(self.pm.read_bytes(self.addrMinimumCursorUp, 1))

	def getCharacterDifficulty(self, character, difficulty):
		result = None
		if character == ILLUSION_TEAM:
			if difficulty == EASY:
				result = self.getIllusionEasy()
			elif difficulty == NORMAL:
				result = self.getIllusionNormal()
			elif difficulty == HARD:
				result = self.getIllusionHard()
			elif difficulty == LUNATIC:
				result = self.getIllusionLunatic()
			elif difficulty == EXTRA:
				result = self.getIllusionExtra()
		elif character == MAGIC_TEAM:
			if difficulty == EASY:
				result = self.getMagicEasy()
			elif difficulty == NORMAL:
				result = self.getMagicNormal()
			elif difficulty == HARD:
				result = self.getMagicHard()
			elif difficulty == LUNATIC:
				result = self.getMagicLunatic()
			elif difficulty == EXTRA:
				result = self.getMagicExtra()
		elif character == DEVIL_TEAM:
			if difficulty == EASY:
				result = self.getDevilEasy()
			elif difficulty == NORMAL:
				result = self.getDevilNormal()
			elif difficulty == HARD:
				result = self.getDevilHard()
			elif difficulty == LUNATIC:
				result = self.getDevilLunatic()
			elif difficulty == EXTRA:
				result = self.getDevilExtra()
		elif character == NETHER_TEAM:
			if difficulty == EASY:
				result = self.getNetherEasy()
			elif difficulty == NORMAL:
				result = self.getNetherNormal()
			elif difficulty == HARD:
				result = self.getNetherHard()
			elif difficulty == LUNATIC:
				result = self.getNetherLunatic()
			elif difficulty == EXTRA:
				result = self.getNetherExtra()

		return result

	def getFpsText(self):
		return self.pm.read_bytes(self.addrFpsText, 8)

	def setMenuCursor(self, newCursor):
		self.addrMenuCursor = getPointerAddress(self.pm, self.pm.base_address+ADDR_MENU_CURSOR[0], ADDR_MENU_CURSOR[1:])
		self.pm.write_bytes(self.addrMenuCursor, bytes([newCursor]), 1)

	def setStage(self, newStage):
		self.pm.write_short(self.addrStage, newStage)

	def setDifficulty(self, newDifficulty):
		self.pm.write_short(self.addrDifficulty, newDifficulty)

	def setRank(self, newRank):
		self.pm.write_bytes(self.addrRank, bytes([newRank]), 1)

	def setCharacter(self, newCharacter):
		self.pm.write_short(self.addrCharacter, newCharacter)

	def setLives(self, newLives):
		self.addrLives = getPointerAddress(self.pm, self.pm.base_address+ADDR_LIVES[0], ADDR_LIVES[1:])
		self.pm.write_float(self.addrLives, float(newLives))

	def setBombs(self, newBombs):
		self.addrBombs = getPointerAddress(self.pm, self.pm.base_address+ADDR_BOMBS[0], ADDR_BOMBS[1:])
		self.pm.write_float(self.addrBombs, float(newBombs))

	def setPower(self, newPower):
		self.addrPower = getPointerAddress(self.pm, self.pm.base_address+ADDR_POWER[0], ADDR_POWER[1:])
		self.pm.write_float(self.addrPower, float(newPower))

	def setContinues(self, newContinue):
		self.addrContinues = getPointerAddress(self.pm, self.pm.base_address+ADDR_CONTINUE[0], ADDR_CONTINUE[1:])
		self.pm.write_bytes(self.addrContinues, bytes([newContinue]), 1)

	def setStartingLives(self, newStartingLives):
		self.pm.write_float(self.addrStartingLives, float(newStartingLives))

	def setNormalContinueLives(self, newNormalContinueLives):
		self.pm.write_float(self.addrNormalContinueLives, float(newNormalContinueLives))

	def setStartingBombs(self, newStartingBombs):
		self.pm.write_float(self.addrStartingBombs, float(newStartingBombs))

	def setStartingPowerPoint(self, newStartingPowerPoint):
		self.pm.write_float(self.addrStartingPowerPoint, float(newStartingPowerPoint))

	def setMisses(self, newMisses):
		self.pm.write_bytes(self.addrMisses, bytes([newMisses]), 1)

	def setIllusionEasy(self, newIllusionEasy):
		self.pm.write_int(self.addrIllusionEasy, newIllusionEasy)

	def setIllusionNormal(self, newIllusionNormal):
		self.pm.write_int(self.addrIllusionNormal, newIllusionNormal)

	def setIllusionHard(self, newIllusionHard):
		self.pm.write_int(self.addrIllusionHard, newIllusionHard)

	def setIllusionLunatic(self, newIllusionLunatic):
		self.pm.write_int(self.addrIllusionLunatic, newIllusionLunatic)

	def setIllusionExtra(self, newIllusionExtra):
		self.pm.write_bytes(self.addrIllusionExtra[0], bytes([newIllusionExtra]), 1)
		self.pm.write_bytes(self.addrIllusionExtra[1], bytes([newIllusionExtra]), 1)
		self.pm.write_bytes(self.addrIllusionExtra[2], bytes([newIllusionExtra]), 1)
		self.pm.write_bytes(self.addrIllusionExtra[3], bytes([newIllusionExtra]), 1)

	def setMagicEasy(self, newMagicEasy):
		self.pm.write_int(self.addrMagicEasy, newMagicEasy)

	def setMagicNormal(self, newMagicNormal):
		self.pm.write_int(self.addrMagicNormal, newMagicNormal)

	def setMagicHard(self, newMagicHard):
		self.pm.write_int(self.addrMagicHard, newMagicHard)

	def setMagicLunatic(self, newMagicLunatic):
		self.pm.write_int(self.addrMagicLunatic, newMagicLunatic)

	def setMagicExtra(self, newMagicExtra):
		self.pm.write_bytes(self.addrMagicExtra[0], bytes([newMagicExtra]), 1)
		self.pm.write_bytes(self.addrMagicExtra[1], bytes([newMagicExtra]), 1)
		self.pm.write_bytes(self.addrMagicExtra[2], bytes([newMagicExtra]), 1)
		self.pm.write_bytes(self.addrMagicExtra[3], bytes([newMagicExtra]), 1)

	def setDevilEasy(self, newDevilEasy):
		self.pm.write_int(self.addrDevilEasy, newDevilEasy)

	def setDevilNormal(self, newDevilNormal):
		self.pm.write_int(self.addrDevilNormal, newDevilNormal)

	def setDevilHard(self, newDevilHard):
		self.pm.write_int(self.addrDevilHard, newDevilHard)

	def setDevilLunatic(self, newDevilLunatic):
		self.pm.write_bytes(self.addrDevilLunatic, bytes([newDevilLunatic]), 1)

	def setDevilExtra(self, newDevilExtra):
		self.pm.write_bytes(self.addrDevilExtra[0], bytes([newDevilExtra]), 1)
		self.pm.write_bytes(self.addrDevilExtra[1], bytes([newDevilExtra]), 1)
		self.pm.write_bytes(self.addrDevilExtra[2], bytes([newDevilExtra]), 1)
		self.pm.write_bytes(self.addrDevilExtra[3], bytes([newDevilExtra]), 1)

	def setNetherEasy(self, newNetherEasy):
		self.pm.write_int(self.addrNetherEasy, newNetherEasy)

	def setNetherNormal(self, newNetherNormal):
		self.pm.write_int(self.addrNetherNormal, newNetherNormal)

	def setNetherHard(self, newNetherHard):
		self.pm.write_int(self.addrNetherHard, newNetherHard)

	def setNetherLunatic(self, newNetherLunatic):
		self.pm.write_int(self.addrNetherLunatic, newNetherLunatic)

	def setNetherExtra(self, newNetherExtra):
		self.pm.write_bytes(self.addrNetherExtra[0], bytes([newNetherExtra]), 1)
		self.pm.write_bytes(self.addrNetherExtra[1], bytes([newNetherExtra]), 1)
		self.pm.write_bytes(self.addrNetherExtra[2], bytes([newNetherExtra]), 1)
		self.pm.write_bytes(self.addrNetherExtra[3], bytes([newNetherExtra]), 1)

	def setFpsText(self, newFpsText):
		# If we have less than 8 character, we pad space character
		if len(newFpsText) < 8:
			for char in range(0, (8-len(newFpsText))):
				newFpsText.insert(0, 0x60)
		self.pm.write_bytes(self.addrFpsText, bytes(newFpsText), 8)

	def setCharacterDifficulty(self, character, difficulty, newValue):
		if character == ILLUSION_TEAM:
			if difficulty == EASY:
				self.setIllusionEasy(newValue)
			elif difficulty == NORMAL:
				self.setIllusionNormal(newValue)
			elif difficulty == HARD:
				self.setIllusionHard(newValue)
			elif difficulty == LUNATIC:
				self.setIllusionLunatic(newValue)
			elif difficulty == EXTRA:
				self.setIllusionExtra(newValue)
		elif character == MAGIC_TEAM:
			if difficulty == EASY:
				self.setMagicEasy(newValue)
			elif difficulty == NORMAL:
				self.setMagicNormal(newValue)
			elif difficulty == HARD:
				self.setMagicHard(newValue)
			elif difficulty == LUNATIC:
				self.setMagicLunatic(newValue)
			elif difficulty == EXTRA:
				self.setMagicExtra(newValue)
		elif character == DEVIL_TEAM:
			if difficulty == EASY:
				self.setDevilEasy(newValue)
			elif difficulty == NORMAL:
				self.setDevilNormal(newValue)
			elif difficulty == HARD:
				self.setDevilHard(newValue)
			elif difficulty == LUNATIC:
				self.setDevilLunatic(newValue)
			elif difficulty == EXTRA:
				self.setDevilExtra(newValue)
		elif character == NETHER_TEAM:
			if difficulty == EASY:
				self.setNetherEasy(newValue)
			elif difficulty == NORMAL:
				self.setNetherNormal(newValue)
			elif difficulty == HARD:
				self.setNetherHard(newValue)
			elif difficulty == LUNATIC:
				self.setNetherLunatic(newValue)
			elif difficulty == EXTRA:
				self.setNetherExtra(newValue)

	def setInput(self, newInput):
		self.pm.write_bytes(self.addrInput, bytes([newInput]), 1)

	def setMinimumCursorDown(self, minimumCursorDown):
		self.pm.write_bytes(self.addrMinimumCursorDown, bytes([minimumCursorDown]), 1)

	def setMinimumCursorUp(self, minimumCursorUp):
		self.pm.write_bytes(self.addrMinimumCursorUp, bytes([minimumCursorUp]), 1)

	def setDefaultExtraDifficulty(self, cursor):
		self.pm.write_bytes(self.addrDefaultExtraDifficulty, bytes([cursor]), 1)

	def setNormalSpeed(self, newNormalSpeed):
		self.addrNormalSpeed = getPointerAddress(self.pm, self.pm.base_address+ADDR_NORMAL_SPEED[0], ADDR_NORMAL_SPEED[1:])
		self.pm.write_float(self.addrNormalSpeed, newNormalSpeed)

	def setFocusSpeed(self, newFocusSpeed):
		self.addrFocusSpeed = getPointerAddress(self.pm, self.pm.base_address+ADDR_FOCUS_SPEED[0], ADDR_FOCUS_SPEED[1:])
		self.pm.write_float(self.addrFocusSpeed, newFocusSpeed)

	def setNormalSpeedD(self, newNormalSpeedD):
		self.addrNormalSpeedD = getPointerAddress(self.pm, self.pm.base_address+ADDR_NORMAL_SPEED_D[0], ADDR_NORMAL_SPEED_D[1:])
		self.pm.write_float(self.addrNormalSpeedD, newNormalSpeedD)

	def setFocusSpeedD(self, newFocusSpeedD):
		self.addrFocusSpeedD = getPointerAddress(self.pm, self.pm.base_address+ADDR_FOCUS_SPEED_D[0], ADDR_FOCUS_SPEED_D[1:])
		self.pm.write_float(self.addrFocusSpeedD, newFocusSpeedD)

	def resetBossPresent(self):
		self.pm.write_bytes(self.addrIsBossPresent1, bytes([0]), 1)
		self.pm.write_bytes(self.addrIsBossPresent2, bytes([0]), 1)

	def setPracticeStageScore(self, characterId, difficultyId, stageId, newScore):
		return self.pm.write_int(self.addrPracticeScore[characterId][difficultyId][stageId], newScore)

	def setKill(self, active):
		if active:
			self.pm.write_bytes(self.addrKillCondition, bytes([0x90, 0x90]), 2)
		else:
			self.pm.write_bytes(self.addrKillCondition, bytes([0xEB, 0x44]), 2)

	def setLockToAllDifficulty(self):
		for lock in self.addrCharacterLock:
			self.pm.write_bytes(lock, bytes([0x7F]), 1)

	def setControllerHandler(self, activate):
		if activate:
			self.pm.write_bytes(self.addrControllerHandle, bytes([0x66, 0xA3, 0x28, 0xD5, 0x64, 0x01]), 6)
		else:
			self.pm.write_bytes(self.addrControllerHandle, bytes([0x90, 0x90, 0x90, 0x90, 0x90, 0x90]), 6)

	def initSoundHack(self):
		soundIdHex = "0"+hex(self.addrCustomSoundId)[2:]
		soundId = [int(soundIdHex[i:i+2], 16) for i in range(0, len(soundIdHex), 2)]
		self.pm.write_bytes(self.addrSoundHack1, bytes([0x6A, 0x00,
														0xFF, 0x35, soundId[3], soundId[2], soundId[1], soundId[0],
														0xB9, 0x68, 0x8A, 0x8B, 0x01,
														0xE8, 0x78, 0xE1, 0xC8, 0xFE,
														0xC7, 0x05, soundId[3], soundId[2], soundId[1], soundId[0], 0x30, 0x00, 0x00, 0x00,
														0xE9, 0x43, 0x36, 0xC3, 0xFE]), 33)

		self.pm.write_bytes(self.addrSoundHack2, bytes([0xE9, 0x9C, 0xC9, 0x3C, 0x01,
														0x5D,
														0xC2, 0x08, 0x00]), 9)


	def setCustomSoundId(self, soundId = 0x0D):
		self.pm.write_bytes(self.addrCustomSoundId, bytes([soundId]), 1)

	def initStartingLives(self):
		self.pm.write_bytes(self.addrLifeHack1, bytes([0xC7, 0x40, 0x74, 0x00, 0x00, 0x00, 0x00, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90]), 13)
		self.pm.write_bytes(self.addrLifeHack2, bytes([0xC7, 0x40, 0x74, 0x00, 0x00, 0x00, 0x00, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90]), 13)

	def initStartingBombs(self):
		self.pm.write_bytes(self.addrBombHack1, bytes([0xC7, 0x81, 0x80, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xEB, 0x19]), 12)
		self.pm.write_bytes(self.addrBombHack2, bytes([0xEB, 0xDF, 0x90, 0x90, 0x90, 0x90]), 6)

	def initPowerHack(self):
		self.pm.write_bytes(self.addrPowerHack1, bytes([0x90, 0x90]), 2)
		self.pm.write_bytes(self.addrPowerHack2, bytes([0x90, 0x90]), 2)
		self.pm.write_bytes(self.addrPowerHack3, bytes([0xD9, 0x05, 0xC1, 0xF3, 0x7C, 0x01, 0xD9, 0x98, 0x98, 0x00, 0x00, 0x00, 0x90, 0x90, 0x90, 0x90]), 16)
		self.pm.write_bytes(self.addrPowerHack4, bytes([0xD9, 0x05, 0xC1, 0xF3, 0x7C, 0x01]), 6)

	def initDifficultyHack(self):
		self.pm.write_bytes(self.addrDifficultyCondition, bytes([0xC6, 0x00]), 2)
		self.pm.write_bytes(self.addrDifficultyCursorDefault[0], bytes([0x03]), 1)
		self.pm.write_bytes(self.addrDifficultyCursorDefault[1], bytes([0x03]), 1)
		self.pm.write_bytes(self.addrDifficultyCursorDefault[2], bytes([0x03]), 1)
		self.pm.write_bytes(self.addrCharacterDefaultCursorCondition, bytes([0x90, 0x90, 0x90, 0x90, 0x90, 0x90]), 6)

	def forceLockSoloCharacter(self):
		self.pm.write_bytes(self.addrForceLockSoloCharacter, bytes([0xEB]), 1)

	def initAntiTemperHack(self):
		self.pm.write_bytes(self.addrAntiTemperHack, bytes([0x33, 0xC0, 0xC3]), 3)

	def disableDemo(self):
		self.pm.write_bytes(self.addrDemoCondition, bytes([0xFF, 0xFF, 0xFF, 0x7F]), 4)

	def setFpsUpdate(self, active):
		if active:
			self.pm.write_bytes(self.addrFpsUpdate, bytes([0x68, 0xB8, 0xF3, 0x7C, 0x01]), 5)
		else:
			self.pm.write_bytes(self.addrFpsUpdate, bytes([0x68, 0x58, 0xE6, 0x7C, 0x01]), 5)