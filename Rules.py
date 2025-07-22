from BaseClasses import MultiWorld
from .Variables import *
from .Regions import get_regions

def constructStageRule(player, state, nb_stage, mode, difficulty, character_list):
	rule = state.count("Lower Difficulty", player) >= difficulty
	stage_rule = False
	if mode not in NORMAL_MODE:
		if character_list:
			for character in character_list:
				stage_rule = stage_rule or (state.count(f"[{character}] Next Stage", player) >= nb_stage and state.has_any(CHARACTER_TO_ITEM[character], player))
		else:
			stage_rule = state.count("Next Stage", player) >= nb_stage
	else:
		stage_rule = True

	return rule and stage_rule

def makeStageRule(player, nb_stage, mode, difficulty, character_list):
	return lambda state: constructStageRule(player, state, nb_stage, mode, difficulty, character_list)

def makeResourcesRule(player, lives, bombs, difficulties):
	return lambda state: state.count("+1 Life", player) >= lives and state.count("+1 Bomb", player) >= bombs and state.count("Lower Difficulty", player) >= difficulties

def constructExtraRule(player, state, character_list, mode, extra):
	stage_rule = False
	if extra == EXTRA_LINEAR:
		if mode not in NORMAL_MODE:
			if character_list:
				for character in character_list:
					stage_rule = stage_rule or (state.count(f"[{character}] Next Stage", player) >= 6 and state.has_any(CHARACTER_TO_ITEM[character], player))
			else:
				stage_rule = state.count("Next Stage", player) >= 6
		else:
			stage_rule = True
	else:
		if character_list:
			for character in character_list:
				stage_rule = stage_rule or (state.has(f"[{character}] Extra Stage", player) and state.has_any(CHARACTER_TO_ITEM[character], player))
		else:
			stage_rule = state.has("Extra Stage", player)

	return stage_rule

def makeExtraRule(player, character_list, mode, extra):
	return lambda state: constructExtraRule(player, state, character_list, mode, extra)

def makeCharacterRule(player, characters):
	return lambda state: state.has_any(characters, player)

def addDifficultyRule(player, difficulty, rule):
	return lambda state: state.count("Lower Difficulty", player) >= difficulty and rule(state)

def victoryCondition(player, state, normal, extra, type):
	normal_victory = True
	extra_victory = True

	if normal:
		endings = []
		for character in CHARACTERS_LIST:
			endings.append(f"[{character}] {ENDING_FINAL_B_ITEM}")

		if type == ONE_ENDING:
			normal_victory = state.has_any(endings, player)
		elif type == ALL_CHARACTER_ENDING:
			normal_victory = state.has_all(endings, player)

	if extra:
		endings = []
		for character in CHARACTERS_LIST:
			endings.append(f"[{character}] {ENDING_EXTRA_ITEM}")

		if type == ONE_ENDING:
			extra_victory = state.has_any(endings, player)
		elif type == ALL_CHARACTER_ENDING:
			extra_victory = state.has_all(endings, player)

	return normal_victory and extra_victory

def connect_regions(multiworld: MultiWorld, player: int, source: str, exits: list, rule=None):
	lifeMid = getattr(multiworld.worlds[player].options, "number_life_mid")
	bombsMid = getattr(multiworld.worlds[player].options, "number_bomb_mid")
	difficultyMid = getattr(multiworld.worlds[player].options, "difficulty_mid")
	lifeEnd = getattr(multiworld.worlds[player].options, "number_life_end")
	bombsEnd = getattr(multiworld.worlds[player].options, "number_bomb_end")
	difficultyEnd = getattr(multiworld.worlds[player].options, "difficulty_end")
	lifeExtra = getattr(multiworld.worlds[player].options, "number_life_extra")
	bombsExtra = getattr(multiworld.worlds[player].options, "number_bomb_extra")
	mode = getattr(multiworld.worlds[player].options, "mode")
	extra = getattr(multiworld.worlds[player].options, "extra_stage")
	difficulty_check = getattr(multiworld.worlds[player].options, "difficulty_check")
	stage_unlock = getattr(multiworld.worlds[player].options, "stage_unlock")
	exclude_lunatic = getattr(multiworld.worlds[player].options, "exclude_lunatic")

	for exit in exits:
		rule = None
		# Rules depend on the name of the target region
		if "Mid" in exit:
			difficulty = difficultyMid if not exclude_lunatic else max(0, difficultyMid-1)
			rule = makeResourcesRule(player, lifeMid, bombsMid, difficulty)
		elif "Late" in exit:
			difficulty = difficultyEnd if not exclude_lunatic else max(0, difficultyEnd-1)
			rule = makeResourcesRule(player, lifeEnd, bombsEnd, difficulty)
		elif "Extra" in exit and "Stage" not in exit:
			rule = makeResourcesRule(player, lifeExtra, bombsExtra, 0)
		elif "Stage" in exit:
			if "Extra" not in exit:
				if "4A" in exit:
					level = 3
				elif "4B" in exit:
					level = 4
				elif "5" in exit:
					level = 5
				elif "6A" in exit:
					level = 6
				elif "6B" in exit:
					level = 7
				else:
					level = int(exit[-1])-1

				difficulty_value = 0
				if difficulty_check in DIFFICULTY_CHECK:
					lower_difficulty = 4
					for difficulty in DIFFICULTY_LIST:
						lower_difficulty -= 1
						if difficulty in exit:
							difficulty_value = lower_difficulty
							break

					if exclude_lunatic:
						difficulty_value -= 1

				# If we don't have global stage unlock, we retrieve the character from the source region
				character_value = []
				if stage_unlock != STAGE_GLOBAL:
					if stage_unlock == STAGE_BY_CHARACTER:
						for character in CHARACTERS_LIST:
							if character in source:
								character_value = [character]
								break

				rule = makeStageRule(player, level, mode, difficulty_value, character_value)
			else:
				# If we don't have global stage unlock, we retrieve the character from the source region
				character_value = []
				if stage_unlock != STAGE_GLOBAL:
					if stage_unlock == STAGE_BY_CHARACTER:
						for character in CHARACTERS_LIST:
							if character in source:
								character_value = [character]
								break

				if "Extra" in exit:
					rule = makeExtraRule(player, character_value, mode, extra)

		elif exit in ALL_CHARACTERS_LIST:
			rule = makeCharacterRule(player, CHARACTER_TO_ITEM[exit])

		sourceRegion = multiworld.get_region(source, player)
		targetRegion = multiworld.get_region(exit, player)
		sourceRegion.connect(targetRegion, rule=rule)

def set_rules(multiworld: MultiWorld, player: int):
	difficulty_check = getattr(multiworld.worlds[player].options, "difficulty_check")
	extra = getattr(multiworld.worlds[player].options, "extra_stage")
	endingRequired = getattr(multiworld.worlds[player].options, "ending_required")
	goal = getattr(multiworld.worlds[player].options, "goal")
	exclude_lunatic = getattr(multiworld.worlds[player].options, "exclude_lunatic")

	# Regions
	regions = get_regions(difficulty_check, extra, exclude_lunatic)

	for name, data in regions.items():
		if data["exits"]:
			connect_regions(multiworld, player, name, data["exits"])

	# Endings

	# Check if the Extra stage is enabled if the goal is set to the Extra stage.
	if extra == NO_EXTRA and goal == ENDING_EXTRA:
		goal = ENDING_FINAL_B_ITEM

	# Win condition.
	multiworld.completion_condition[player] = lambda state: victoryCondition(player, state, (goal in [ENDING_FINAL_B, ENDING_ALL]), (goal in [ENDING_EXTRA, ENDING_ALL] and extra != NO_EXTRA), endingRequired)