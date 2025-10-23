import pymem
import pymem.exception
from .Tools import getPointerAddress
from .Variables import *
from math import log
from .SpellCards import SPELL_CARDS_LIST

class gameController:
	"""Class accessing the game memory"""

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

		self.addrIllusionSpellPractice = [self.pm.base_address+ADDR_ILLUSION_SPELL_PRACTICE[0], self.pm.base_address+ADDR_ILLUSION_SPELL_PRACTICE[1], self.pm.base_address+ADDR_ILLUSION_SPELL_PRACTICE[2], self.pm.base_address+ADDR_ILLUSION_SPELL_PRACTICE[3]]
		self.addrMagicSpellPractice = [self.pm.base_address+ADDR_MAGIC_SPELL_PRACTICE[0], self.pm.base_address+ADDR_MAGIC_SPELL_PRACTICE[1], self.pm.base_address+ADDR_MAGIC_SPELL_PRACTICE[2], self.pm.base_address+ADDR_MAGIC_SPELL_PRACTICE[3]]
		self.addrDevilSpellPractice = [self.pm.base_address+ADDR_DEVIL_SPELL_PRACTICE[0], self.pm.base_address+ADDR_DEVIL_SPELL_PRACTICE[1], self.pm.base_address+ADDR_DEVIL_SPELL_PRACTICE[2], self.pm.base_address+ADDR_DEVIL_SPELL_PRACTICE[3]]
		self.addrNetherSpellPractice = [self.pm.base_address+ADDR_NETHER_SPELL_PRACTICE[0], self.pm.base_address+ADDR_NETHER_SPELL_PRACTICE[1], self.pm.base_address+ADDR_NETHER_SPELL_PRACTICE[2], self.pm.base_address+ADDR_NETHER_SPELL_PRACTICE[3]]

		self.addrIllusionEasyClear = self.pm.base_address+ADDR_ILLUSION_EASY_CLEAR
		self.addrIllusionNormalClear = self.pm.base_address+ADDR_ILLUSION_NORMAL_CLEAR
		self.addrIllusionHardClear = self.pm.base_address+ADDR_ILLUSION_HARD_CLEAR
		self.addrIllusionLunaticClear = self.pm.base_address+ADDR_ILLUSION_LUNATIC_CLEAR

		self.addrMagicEasyClear = self.pm.base_address+ADDR_MAGIC_EASY_CLEAR
		self.addrMagicNormalClear = self.pm.base_address+ADDR_MAGIC_NORMAL_CLEAR
		self.addrMagicHardClear = self.pm.base_address+ADDR_MAGIC_HARD_CLEAR
		self.addrMagicLunaticClear = self.pm.base_address+ADDR_MAGIC_LUNATIC_CLEAR

		self.addrDevilEasyClear = self.pm.base_address+ADDR_DEVIL_EASY_CLEAR
		self.addrDevilNormalClear = self.pm.base_address+ADDR_DEVIL_NORMAL_CLEAR
		self.addrDevilHardClear = self.pm.base_address+ADDR_DEVIL_HARD_CLEAR
		self.addrDevilLunaticClear = self.pm.base_address+ADDR_DEVIL_LUNATIC_CLEAR

		self.addrNetherEasyClear = self.pm.base_address+ADDR_NETHER_EASY_CLEAR
		self.addrNetherNormalClear = self.pm.base_address+ADDR_NETHER_NORMAL_CLEAR
		self.addrNetherHardClear = self.pm.base_address+ADDR_NETHER_HARD_CLEAR
		self.addrNetherLunaticClear = self.pm.base_address+ADDR_NETHER_LUNATIC_CLEAR

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
		self.addrHYGaugeHack = self.pm.base_address+ADDR_HY_GAUGE_HACK

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

		self.addrStageSelectStage4Hack1 = self.pm.base_address+ADDR_STAGE_SELECT_STAGE_4_HACK_1
		self.addrStageSelectStage4Hack2 = self.pm.base_address+ADDR_STAGE_SELECT_STAGE_4_HACK_2

		self.addrTimeGainHack = self.pm.base_address+ADDR_TIME_GAIN_HACK
		self.addrTimeHack = self.pm.base_address+ADDR_TIME_HACK
		self.addrStartingTime = self.pm.base_address+ADDR_STARTING_TIME
		self.addrCurrentTime = getPointerAddress(self.pm, self.pm.base_address+ADDR_CURRENT_TIME[0], ADDR_CURRENT_TIME[1:])
		self.addrTimeGoal = getPointerAddress(self.pm, self.pm.base_address+ADDR_TIME_GOAL[0], ADDR_TIME_GOAL[1:])

		self.addrPlayerState = self.pm.base_address+ADDR_PLAYER_STATE
		self.addrStruct = self.pm.base_address+ADDR_STRUCT

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

		self.addrAllCharacterSpellCard = {}
		self.addrSpellCards = {}
		for id, spell in SPELL_CARDS_LIST.items():
			self.addrAllCharacterSpellCard[id] = {"acquired": self.pm.base_address+spell["all_character_addresses"]["acquired"], "challenged": self.pm.base_address+spell["all_character_addresses"]["challenged"]}
			self.addrSpellCards[id] = {}
			for character in CHARACTERS:
				self.addrSpellCards[id][character] = {"acquired": self.pm.base_address+spell["addresses"][character]["acquired"], "challenged": self.pm.base_address+spell["addresses"][character]["challenged"], "unlocked": self.pm.base_address+spell["addresses"][character]["unlocked"]}

		self.addrLastWordConditions = [self.pm.base_address+addr for addr in ADDR_LAST_WORD_CONDITIONS]
		self.addrLastWordUnlock = [self.pm.base_address+addr for addr in ADDR_LAST_WORD_UNLOCK]

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

	def getTimePoint(self):
		self.addrCurrentTime = getPointerAddress(self.pm, self.pm.base_address+ADDR_CURRENT_TIME[0], ADDR_CURRENT_TIME[1:])
		return self.pm.read_int(self.addrCurrentTime)

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

	def getIllusionSpellPractice(self):
		return [
				int.from_bytes(self.pm.read_bytes(self.addrIllusionSpellPractice[0], 1)),
				int.from_bytes(self.pm.read_bytes(self.addrIllusionSpellPractice[1], 1)),
				int.from_bytes(self.pm.read_bytes(self.addrIllusionSpellPractice[2], 1)),
				int.from_bytes(self.pm.read_bytes(self.addrIllusionSpellPractice[3], 1))
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

	def getMagicSpellPractice(self):
		return [
				int.from_bytes(self.pm.read_bytes(self.addrMagicSpellPractice[0], 1)),
				int.from_bytes(self.pm.read_bytes(self.addrMagicSpellPractice[1], 1)),
				int.from_bytes(self.pm.read_bytes(self.addrMagicSpellPractice[2], 1)),
				int.from_bytes(self.pm.read_bytes(self.addrMagicSpellPractice[3], 1))
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

	def getDevilSpellPractice(self):
		return [
				int.from_bytes(self.pm.read_bytes(self.addrDevilSpellPractice[0], 1)),
				int.from_bytes(self.pm.read_bytes(self.addrDevilSpellPractice[1], 1)),
				int.from_bytes(self.pm.read_bytes(self.addrDevilSpellPractice[2], 1)),
				int.from_bytes(self.pm.read_bytes(self.addrDevilSpellPractice[3], 1))
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

	def getNetherSpellPractice(self):
		return [
				int.from_bytes(self.pm.read_bytes(self.addrNetherSpellPractice[0], 1)),
				int.from_bytes(self.pm.read_bytes(self.addrNetherSpellPractice[1], 1)),
				int.from_bytes(self.pm.read_bytes(self.addrNetherSpellPractice[2], 1)),
				int.from_bytes(self.pm.read_bytes(self.addrNetherSpellPractice[3], 1))
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

	def getTimeGoal(self):
		self.addrTimeGoal = getPointerAddress(self.pm, self.pm.base_address+ADDR_TIME_GOAL[0], ADDR_TIME_GOAL[1:])
		return self.pm.read_int(self.addrTimeGoal)

	def getAllCharacterSpellCardAcquired(self, spell_id):
		return int.from_bytes(self.pm.read_bytes(self.addrAllCharacterSpellCard[spell_id]["acquired"], 1))

	def getAllCharacterSpellCardChallenged(self, spell_id):
		return int.from_bytes(self.pm.read_bytes(self.addrAllCharacterSpellCard[spell_id]["challenged"], 1))

	def getSpellCardAcquired(self, spell_id, character):
		return int.from_bytes(self.pm.read_bytes(self.addrSpellCards[spell_id][character]["acquired"], 1))

	def getSpellCardChallenged(self, spell_id, character):
		return int.from_bytes(self.pm.read_bytes(self.addrSpellCards[spell_id][character]["challenged"], 1))

	def getSpellCardUnlocked(self, spell_id, character):
		return int.from_bytes(self.pm.read_bytes(self.addrSpellCards[spell_id][character]["unlocked"], 1))

	def getPlayerState(self):
		return int.from_bytes(self.pm.read_bytes(self.addrPlayerState, 1))

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

	def setTimePoint(self, newTimePoint):
		self.addrCurrentTime = getPointerAddress(self.pm, self.pm.base_address+ADDR_CURRENT_TIME[0], ADDR_CURRENT_TIME[1:])
		self.pm.write_int(self.addrCurrentTime, newTimePoint)

	def setTimeGoal(self, newTimeGoal):
		self.addrTimeGoal = getPointerAddress(self.pm, self.pm.base_address+ADDR_TIME_GOAL[0], ADDR_TIME_GOAL[1:])
		self.pm.write_int(self.addrTimeGoal, newTimeGoal)

	def setStartingLives(self, newStartingLives):
		self.pm.write_float(self.addrStartingLives, float(newStartingLives))

	def setNormalContinueLives(self, newNormalContinueLives):
		self.pm.write_float(self.addrNormalContinueLives, float(newNormalContinueLives))

	def setStartingBombs(self, newStartingBombs):
		self.pm.write_float(self.addrStartingBombs, float(newStartingBombs))

	def setStartingPowerPoint(self, newStartingPowerPoint):
		self.pm.write_float(self.addrStartingPowerPoint, float(newStartingPowerPoint))

	def setStartingTimePoint(self, newStartingTime):
		self.pm.write_int(self.addrStartingTime, newStartingTime)

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

	def setIllusionSpellPractice(self, newIllusionSpellPractice):
		self.pm.write_bytes(self.addrIllusionSpellPractice[0], bytes([newIllusionSpellPractice]), 1)
		self.pm.write_bytes(self.addrIllusionSpellPractice[1], bytes([newIllusionSpellPractice]), 1)
		self.pm.write_bytes(self.addrIllusionSpellPractice[2], bytes([newIllusionSpellPractice]), 1)
		self.pm.write_bytes(self.addrIllusionSpellPractice[3], bytes([newIllusionSpellPractice]), 1)

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

	def setMagicSpellPractice(self, newMagicSpellPractice):
		self.pm.write_bytes(self.addrMagicSpellPractice[0], bytes([newMagicSpellPractice]), 1)
		self.pm.write_bytes(self.addrMagicSpellPractice[1], bytes([newMagicSpellPractice]), 1)
		self.pm.write_bytes(self.addrMagicSpellPractice[2], bytes([newMagicSpellPractice]), 1)
		self.pm.write_bytes(self.addrMagicSpellPractice[3], bytes([newMagicSpellPractice]), 1)

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

	def setDevilSpellPractice(self, newDevilSpellPractice):
		self.pm.write_bytes(self.addrDevilSpellPractice[0], bytes([newDevilSpellPractice]), 1)
		self.pm.write_bytes(self.addrDevilSpellPractice[1], bytes([newDevilSpellPractice]), 1)
		self.pm.write_bytes(self.addrDevilSpellPractice[2], bytes([newDevilSpellPractice]), 1)
		self.pm.write_bytes(self.addrDevilSpellPractice[3], bytes([newDevilSpellPractice]), 1)

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

	def setNetherSpellPractice(self, newNetherSpellPractice):
		self.pm.write_bytes(self.addrNetherSpellPractice[0], bytes([newNetherSpellPractice]), 1)
		self.pm.write_bytes(self.addrNetherSpellPractice[1], bytes([newNetherSpellPractice]), 1)
		self.pm.write_bytes(self.addrNetherSpellPractice[2], bytes([newNetherSpellPractice]), 1)
		self.pm.write_bytes(self.addrNetherSpellPractice[3], bytes([newNetherSpellPractice]), 1)

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

	def setCharacterSpellPractice(self, character, access):
		value = 0x80 if access else 0x00
		if character == ILLUSION_TEAM:
			self.setIllusionSpellPractice(value)
		elif character == MAGIC_TEAM:
			self.setMagicSpellPractice(value)
		elif character == DEVIL_TEAM:
			self.setDevilSpellPractice(value)
		elif character == NETHER_TEAM:
			self.setNetherSpellPractice(value)

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

	def setHYGaugeGauge(self, add):
		if add:
			self.pm.write_bytes(self.addrHYGaugeHack, bytes([0x03]), 1)
		else:
			self.pm.write_bytes(self.addrHYGaugeHack, bytes([0x2B]), 1)

	def setAllCharacterSpellCardAcquired(self, spell_id, value):
		self.pm.write_bytes(self.addrAllCharacterSpellCard[spell_id]["acquired"], bytes([value]), 1)

	def setAllCharacterSpellCardChallenged(self, spell_id, value):
		self.pm.write_bytes(self.addrAllCharacterSpellCard[spell_id]["challenged"], bytes([value]), 1)

	def setSpellCardAcquired(self, spell_id, character, value):
		self.pm.write_bytes(self.addrSpellCards[spell_id][character]["acquired"], bytes([value]), 1)

	def setSpellCardChallenged(self, spell_id, character, value):
		self.pm.write_bytes(self.addrSpellCards[spell_id][character]["challenged"], bytes([value]), 1)

	def setSpellCardUnlock(self, spell_id, character, value):
		self.pm.write_bytes(self.addrSpellCards[spell_id][character]["unlocked"], bytes([value]), 1)

	def resetBossPresent(self):
		self.pm.write_bytes(self.addrIsBossPresent1, bytes([0]), 1)
		self.pm.write_bytes(self.addrIsBossPresent2, bytes([0]), 1)

	def setPracticeStageScore(self, characterId, difficultyId, stageId, newScore):
		return self.pm.write_int(self.addrPracticeScore[characterId][difficultyId][stageId], newScore)

	# 0x01 = off, 0x77 = Final B opened, 0xFF = All Clear
	def setAllClearStats(self, value):
		self.pm.write_bytes(self.addrIllusionEasyClear, bytes([value]), 1)
		self.pm.write_bytes(self.addrIllusionNormalClear, bytes([value]), 1)
		self.pm.write_bytes(self.addrIllusionHardClear, bytes([value]), 1)
		self.pm.write_bytes(self.addrIllusionLunaticClear, bytes([value]), 1)

		self.pm.write_bytes(self.addrMagicEasyClear, bytes([value]), 1)
		self.pm.write_bytes(self.addrMagicNormalClear, bytes([value]), 1)
		self.pm.write_bytes(self.addrMagicHardClear, bytes([value]), 1)
		self.pm.write_bytes(self.addrMagicLunaticClear, bytes([value]), 1)

		self.pm.write_bytes(self.addrDevilEasyClear, bytes([value]), 1)
		self.pm.write_bytes(self.addrDevilNormalClear, bytes([value]), 1)
		self.pm.write_bytes(self.addrDevilHardClear, bytes([value]), 1)
		self.pm.write_bytes(self.addrDevilLunaticClear, bytes([value]), 1)

		self.pm.write_bytes(self.addrNetherEasyClear, bytes([value]), 1)
		self.pm.write_bytes(self.addrNetherNormalClear, bytes([value]), 1)
		self.pm.write_bytes(self.addrNetherHardClear, bytes([value]), 1)
		self.pm.write_bytes(self.addrNetherLunaticClear, bytes([value]), 1)

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
		self.pm.write_bytes(self.addrLifeHack2, bytes([0xC7, 0x41, 0x74, 0x00, 0x00, 0x80, 0x3F,
													   0x8B, 0x4D, 0xFC,
													   0xE8, 0x11, 0x00, 0x00, 0x00,
													   0x8B, 0xE5, 0x5D, 0xC2, 0x04, 0x00]), 21)

	def initStartingBombs(self):
		self.pm.write_bytes(self.addrBombHack1, bytes([0xC7, 0x81, 0x80, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xEB, 0x19]), 12)
		self.pm.write_bytes(self.addrBombHack2, bytes([0x90, 0x90, 0x90, 0x90, 0xEB, 0xDB]), 6)

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

	def initStageSelectHack(self):
		# Hack for stopping the stage 6B unlock from also unlocking both stage 4
		self.pm.write_bytes(self.addrStageSelectStage4Hack1, bytes([0xEB]), 1)
		self.pm.write_bytes(self.addrStageSelectStage4Hack2, bytes([0xEB]), 1)

	def initTimeHack(self):
		self.pm.write_bytes(self.addrTimeHack, bytes([0xC7, 0x40, 0x3C, 0x00, 0x00, 0x00, 0x00, 0x90, 0x90, 0x90]), 10)

	def setTimeGain(self, active):
		if active:
			self.pm.write_bytes(self.addrTimeGainHack, bytes([0x89, 0x51, 0x3C]), 3)
		else:
			self.pm.write_bytes(self.addrTimeGainHack, bytes([0x90, 0x90, 0x90]), 3)

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

	def showSplashScreens(self):
		addr = self.pm.base_address+ADDR_STRUCT
		value = int.from_bytes(self.pm.read_bytes(addr, 4))
		flags = 0b1000000000000001
		new_value = value|flags
		if value != new_value:
			self.pm.write_bytes(addr, new_value.to_bytes(4), 4)

	def setLastWordHack(self):
		for i in range(0, 17):
			self.pm.write_bytes(self.addrLastWordConditions[i], bytes([0xEB]), 1)
			self.pm.write_bytes(self.addrLastWordUnlock[i], bytes([0x00]), 1)