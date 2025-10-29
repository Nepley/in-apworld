from BaseClasses import MultiWorld
from worlds.generic.Rules import add_rule, set_rule
from .Variables import *
from .Regions import get_regions
from .SpellCards import SPELL_CARDS_LIST

def constructProgressiveStageRule(player, state, nb_stage, mode, difficulty, character_list):
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

def constructStageRule(player, state, stage, mode, difficulty, character_list):
	rule = state.count("Lower Difficulty", player) >= difficulty
	stage_rule = False
	if mode not in NORMAL_MODE:
		if character_list:
			for character in character_list:
				if stage != "Stage 1":
					stage_rule = stage_rule or (state.has(f"[{character}] {stage}", player) and state.has_any(CHARACTER_TO_ITEM[character], player))
				else:
					stage_rule = stage_rule or (state.has_any(CHARACTER_TO_ITEM[character], player))
		else:
			if stage != "Stage 1":
				stage_rule = state.has(f"{stage}", player)
			else:
				stage_rule = True
	else:
		stage_rule = True

	return rule and stage_rule

def makeStageRule(player, nb_stage, mode, difficulty, character_list, progressive_stage):
	if progressive_stage:
		return lambda state: constructProgressiveStageRule(player, state, nb_stage, mode, difficulty, character_list)
	else:
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

def makeSpellCardRule(player, location, spellcard):
	add_rule(location, lambda state: state.has(spellcard, player))

def makeFinalSpellCardRule(player, location):
	add_rule(location, lambda state: state.has("Brilliant Dragon Bullet", player)
		  							and state.has("Buddhist Diamond", player)
									and state.has("Salamander Shield", player)
									and state.has("Life Spring Shield", player)
									and state.has("Jeweled Branch of Hourai", player)
			)

def addDifficultyRule(player, difficulty, rule):
	return lambda state: state.count("Lower Difficulty", player) >= difficulty and rule(state)

def victoryCondition(player, state, normal_a, normal_b, extra, treasure, type):
	normal_a_victory = True
	normal_b_victory = True
	extra_victory = True
	treasure_victory = True

	if normal_a:
		endings = []
		for character in CHARACTERS_LIST:
			endings.append(f"[{character}] {ENDING_FINAL_A_ITEM}")

		if type == ONE_ENDING:
			normal_a_victory = state.has_any(endings, player)
		elif type == ALL_CHARACTER_ENDING:
			normal_a_victory = state.has_all(endings, player)

	if normal_b:
		endings = []
		for character in CHARACTERS_LIST:
			endings.append(f"[{character}] {ENDING_FINAL_B_ITEM}")

		if type == ONE_ENDING:
			normal_b_victory = state.has_any(endings, player)
		elif type == ALL_CHARACTER_ENDING:
			normal_b_victory = state.has_all(endings, player)

	if extra:
		endings = []
		for character in CHARACTERS_LIST:
			endings.append(f"[{character}] {ENDING_EXTRA_ITEM}")

		if type == ONE_ENDING:
			extra_victory = state.has_any(endings, player)
		elif type == ALL_CHARACTER_ENDING:
			extra_victory = state.has_all(endings, player)

	if treasure:
		treasure_victory = state.has(ENDING_TREASURE, player)

	return normal_a_victory and normal_b_victory and extra_victory and treasure_victory

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
	progressive_stage = getattr(multiworld.worlds[player].options, "progressive_stage")
	exclude_lunatic = getattr(multiworld.worlds[player].options, "exclude_lunatic")
	both_stage_4 = getattr(multiworld.worlds[player].options, "both_stage_4")

	# If we're in Normal mode, we force both_stage_4 to be False
	if mode in NORMAL_MODE:
		both_stage_4 = False

	for exit in exits:
		rule = None
		# Rules depend on the name of the target region
		if "Mid" in exit:
			difficulty = difficultyMid if not exclude_lunatic else max(0, difficultyMid-1)
			rule = makeResourcesRule(player, lifeMid, bombsMid, difficulty)
		elif "Late" in exit:
			difficulty = difficultyEnd if not exclude_lunatic else max(0, difficultyEnd-1)
			rule = makeResourcesRule(player, lifeEnd, bombsEnd, difficulty)
		elif "Extra" in exit and "Stage" not in exit and "[SC]" not in exit:
			rule = makeResourcesRule(player, lifeExtra, bombsExtra, 0)
		elif "Stage" in exit and "[SC]" not in exit:
			if "Extra" not in exit:
				if progressive_stage:
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

					if level >= 4 and not both_stage_4:
						level -= 1
				else:
					level = exit.split("] ")[1]

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

				rule = makeStageRule(player, level, mode, difficulty_value, character_value, progressive_stage)
			else:
				# If we don't have global stage unlock, we retrieve the character from the source region
				character_value = []
				if stage_unlock != STAGE_GLOBAL:
					if stage_unlock == STAGE_BY_CHARACTER:
						for character in CHARACTERS_LIST:
							if character in source:
								character_value = [character]
								break

				# If Extra is enabled linearly, we change it to apart
				if extra == EXTRA_LINEAR and mode in PRACTICE_MODE and not progressive_stage:
					extra = EXTRA_APART

				if "Extra" in exit:
					rule = makeExtraRule(player, character_value, mode, extra)

		elif exit in ALL_CHARACTERS_LIST:
			rule = makeCharacterRule(player, CHARACTER_TO_ITEM[exit])

		sourceRegion = multiworld.get_region(source, player)
		targetRegion = multiworld.get_region(exit, player)
		sourceRegion.connect(targetRegion, rule=rule)

def set_rules(multiworld: MultiWorld, player: int, spell_cards: list, treasure_final_spell_card: str):
	difficulty_check = getattr(multiworld.worlds[player].options, "difficulty_check")
	extra = getattr(multiworld.worlds[player].options, "extra_stage")
	endingRequired = getattr(multiworld.worlds[player].options, "ending_required")
	goal = getattr(multiworld.worlds[player].options, "goal")
	exclude_lunatic = getattr(multiworld.worlds[player].options, "exclude_lunatic")
	both_stage_4 = getattr(multiworld.worlds[player].options, "both_stage_4")
	mode = getattr(multiworld.worlds[player].options, "mode")
	time_check = getattr(multiworld.worlds[player].options, "time_check")
	time = getattr(multiworld.worlds[player].options, "time")

	# If we're in Normal mode, we force both_stage_4 to be False
	if mode in NORMAL_MODE:
		both_stage_4 = False

	if mode not in PRACTICE_MODE and mode not in NORMAL_MODE and goal != TREASURE_GOAL:
		goal = TREASURE_GOAL
	elif mode not in SPELL_PRACTICE_MODE and goal == TREASURE_GOAL:
		goal = ENDING_FINAL_B

	# Regions
	all_spell_cards = spell_cards + [treasure_final_spell_card] if treasure_final_spell_card != -1 else []
	regions = get_regions(difficulty_check, extra, exclude_lunatic, both_stage_4, time_check, mode, all_spell_cards)

	for name, data in regions.items():
		if data["exits"]:
			connect_regions(multiworld, player, name, data["exits"])

		# Last Spell locations
		if time and data["locations"] and "SpellCard" not in name:
			for location_name in data["locations"]:
				if "Last Spell" in location_name:
					location = multiworld.get_location(location_name, player)
					add_rule(location, lambda state: state.has("Time Gain", player))

		# SpellCards
		if "[SC]" in name and data['locations']:
			for location_name in data["locations"]:
				location = multiworld.get_location(location_name, player)
				item = location_name.split("] ")[1]
				spell_id = item.split(" - ")[0]

				if goal == TREASURE_GOAL and treasure_final_spell_card == spell_id:
					makeFinalSpellCardRule(player, location)
				else:
					makeSpellCardRule(player, location, item)

	# Endings

	# Failsafe
	if goal in [ENDING_FINAL_A, ENDING_FINAL_B, ENDING_EXTRA, ENDING_ALL]:
		# If we're not playing in normal or practice mode, that mean we are in spell card mode, and set the corresponding goal
		if mode in PRACTICE_MODE or mode in NORMAL_MODE:
			# Check if the Extra stage is enabled if the goal is set to the Extra stage.
			if extra == NO_EXTRA and goal == ENDING_EXTRA:
				goal = ENDING_FINAL_B
		else:
			goal = TREASURE_GOAL
	elif goal in [TREASURE_GOAL]:
		if mode not in SPELL_PRACTICE_MODE:
			goal = ENDING_FINAL_B

	# Win condition.
	multiworld.completion_condition[player] = lambda state: victoryCondition(player, state,
																			(goal in [ENDING_FINAL_A, ENDING_ALL] and (mode in PRACTICE_MODE or mode in NORMAL_MODE)),
																			(goal in [ENDING_FINAL_B, ENDING_ALL] and (mode in PRACTICE_MODE or mode in NORMAL_MODE)),
																			(goal in [ENDING_EXTRA, ENDING_ALL] and extra != NO_EXTRA and (mode in PRACTICE_MODE or mode in NORMAL_MODE)),
																			(goal in [TREASURE_GOAL] and mode in SPELL_PRACTICE_MODE),
																			endingRequired
																		)