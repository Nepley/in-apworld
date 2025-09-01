from .Variables import *
from .gameController import gameController
from .gameHandler import gameHandler
from .Tools import *

class GuardRail:
	def __init__(self, memory_controller: gameController, game_handler: gameHandler):
		self.memory_controller = memory_controller
		self.pm = memory_controller.pm
		self.game_handler = game_handler

	def check_memory_addresses(self):
		result = {"error": False, "message": ""}

		# We check if the the sound hack has been applied correctly
		start_sound_hack_1 = int.from_bytes(self.pm.read_bytes(self.memory_controller.addrSoundHack1, 2))
		start_sound_hack_2 = int.from_bytes(self.pm.read_bytes(self.memory_controller.addrSoundHack2, 2))

		if start_sound_hack_1 != 0x6A00 or start_sound_hack_2 != 0xE99C:
			result["error"] = True
			result["message"] = "Sound Hack not applied correctly."

		if not result["error"]:
			# We check if the starting lives has been set correctly
			starting_lives = self.pm.read_float(self.memory_controller.addrStartingLives)
			if starting_lives != self.game_handler.getLives():
				result["error"] = True
				result["message"] = f"Starting lives not set correctly. Game: {starting_lives}, Expected: {self.game_handler.getLives()}"

		if not result["error"]:
			# We check if the lives after a continue has been set correctly
			lives_after_continue = self.pm.read_float(self.memory_controller.addrNormalContinueLives)
			if lives_after_continue != self.game_handler.getLives():
				result["error"] = True
				result["message"] = f"Lives after continue not set correctly. Game: {lives_after_continue}, Expected: {self.game_handler.getLives()}"

		if not result["error"]:
			# We check if the starting bombs has been set correctly
			starting_bombs = self.pm.read_float(self.memory_controller.addrStartingBombs)
			if starting_bombs != self.game_handler.getBombs():
				result["error"] = True
				result["message"] = f"Starting bombs not set correctly. Game: {starting_bombs}, Expected: {self.game_handler.getBombs()}"

		if not result["error"]:
			# We check if the starting power points has been set correctly
			starting_power_points = self.pm.read_float(self.memory_controller.addrStartingPowerPoint)
			if starting_power_points != self.game_handler.getPower():
				result["error"] = True
				result["message"] = f"Starting power points not set correctly. Game: {starting_power_points}, Expected: {self.game_handler.getPower()}"

		if not result["error"]:
			# We check if stages are unlocked correctly
			stages = self.game_handler.stages
			for character in CHARACTERS:
				handler_stage = getIntFromBinaryArray(stages[character])
				for difficulty in range(4):
					if self.game_handler.characters[character] and difficulty >= self.game_handler.getLowestDifficulty():
						in_game_stage = self.memory_controller.getCharacterDifficulty(character, difficulty)

						if in_game_stage != handler_stage:
							result["error"] = True
							result["message"] = f"Character {character} has incorrect stages ({in_game_stage} != {handler_stage}) for difficulty {difficulty}."

		return result

	def check_cursor_state(self):
		result = {"error": False, "message": ""}

		# If we're in the menu
		if self.game_handler.getGameMode() != IN_GAME:
			menu = self.game_handler.getMenu()
			cursor = self.game_handler.getCursorPosition()
			if menu >= 0 and cursor < 50:
				# If we're in the character select, we check if the cursor is on a character that is unlocked
				if menu in [NORMAL_CHARACTER_MENU, PRACTICE_CHARACTER_MENU, EXTRA_CHARACTER_MENU]:
					characters = self.game_handler.getCharactersState()
					if not characters[cursor]:
						result["error"] = True
						result["message"] = f"Character {cursor} is locked."
				# If we're in the difficulty select, we check if the cursor is on a difficulty that is unlocked
				elif menu in [NORMAL_DIFFICULTY_MENU, PRACTICE_DIFFICULTY_MENU]:
					lowest_difficulty = self.game_handler.getLowestDifficulty()
					if cursor < lowest_difficulty:
						result["error"] = True
						result["message"] = f"Difficulty {cursor} is locked."
				# If we're in the stage select screen, we check if the cursor is on a stage that is unlocked
				elif menu == PRACTICE_STAGE_SELECT_MENU:
					characters = self.game_handler.getCurrentCharacter()
					stages = self.game_handler.stages[characters]
					if stages[cursor] == 0:
						result["error"] = True
						result["message"] = f"Stage {cursor} is locked."

		return result

	def check_menu_lock(self):
		result = {"error": False, "message": ""}

		# If we're in the menu
		if self.game_handler.getGameMode() != IN_GAME:
			menu = self.game_handler.getMenu()
			if menu >= 0:
				# If we're in the difficulty select, we check if the difficulties are locked correctly
				if menu in [NORMAL_DIFFICULTY_MENU, PRACTICE_DIFFICULTY_MENU]:
					lock_down = self.memory_controller.getMinimumCursorDown()
					lock_up = self.memory_controller.getMinimumCursorUp()
					lowest_difficulty = self.game_handler.getLowestDifficulty()
					if lock_down != lowest_difficulty or lock_up != lowest_difficulty:
						result["error"] = True
						result["message"] = f"Difficulty locks are not set correctly."
				# If we're in the character select, we check if the character list is correct
				elif menu in [NORMAL_CHARACTER_MENU, PRACTICE_CHARACTER_MENU, EXTRA_CHARACTER_MENU]:
					for character in CHARACTERS:
						characterExtraAccess = self.memory_controller.getCharacterDifficulty(character, EXTRA)

						if all(x==characterExtraAccess[0] for x in characterExtraAccess):
							characterUnlocked = True if characterExtraAccess[0] == 0xFF else False
							characterLogicallyUnlocked = self.game_handler.characters[character]
							characterHasExtra = self.game_handler.characters[character] and self.game_handler.hasExtra[character]

							if menu == EXTRA_CHARACTER_MENU:
								if characterUnlocked != characterHasExtra:
									result["error"] = True
									result["message"] = f"Character {character} Extra access is not locked or unlocked correctly. Extra Logical state: {characterLogicallyUnlocked}. Current state: {characterUnlocked}."
							else:
								if characterUnlocked != characterLogicallyUnlocked:
									result["error"] = True
									result["message"] = f"Character {character} is not locked or unlocked correctly. Logical state: {characterLogicallyUnlocked}. Current state: {characterUnlocked}."
						else:
							result["error"] = True
							result["message"] = f"Character {character} unlock are not all equals. Easy: {characterExtraAccess[0]}, Normal: {characterExtraAccess[1]}, Hard: {characterExtraAccess[2]}, Lunatic: {characterExtraAccess[3]}"

				# If we're in the main menu, we check if the extra stage and normal mode are locked or unlocked correctly
				elif menu == MAIN_MENU:
					game_mode = self.game_handler.getGameMode()
					can_extra = self.game_handler.canExtra()
					lock_down = self.memory_controller.getMinimumCursorDown()
					lock_up = self.memory_controller.getMinimumCursorUp()
					minimum_cursor = 0 if game_mode == NORMAL_MODE else 1

					if not can_extra and game_mode != NORMAL_MODE:
						minimum_cursor += 2 # +1 When Spell Practice would be unlocked

					if lock_down != minimum_cursor or lock_up != minimum_cursor:
						result["error"] = True
						result["message"] = f"Main menu cursor is not locked correctly. Minimum cursor should be {minimum_cursor}. Current locks are: {lock_down}, {lock_up}."

		return result