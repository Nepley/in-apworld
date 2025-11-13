from BaseClasses import MultiWorld, Region
from .Locations import TLocation, location_table
from .Variables import *
from .SpellCards import SPELL_CARDS_LIST

def get_regions(difficulty_check, extra, exclude_lunatic, both_stage_4, time_check, mode, spell_cards, characters, spell_cards_teams):
	regions = {}
	characters = CHARACTERS_LIST if characters == TEAM_ONLY else (ALL_CHARACTERS_LIST if characters == ALL_CHARACTER else SOLO_CHARACTERS_LIST)
	regions["Menu"] = {"locations": None, "exits": characters}
	for character in characters:
		regions[character] = {"locations": None, "exits": []}

	if mode in PRACTICE_MODE or mode in NORMAL_MODE:
		if difficulty_check == NO_DIFFICULTY_CHECK:
			for character in characters:
				regions[character] = {"locations": None, "exits": [f"[{character}] Early", f"[{character}] Mid", f"[{character}] Late"]}
				regions[f"[{character}] Early"] = {"locations": None, "exits": [f"[{character}] Stage 1", f"[{character}] Stage 2"]}
				regions[f"[{character}] Mid"] = {"locations": None, "exits": [f"[{character}] Stage 3"]}
				regions[f"[{character}] Late"] = {"locations": None, "exits": [f"[{character}] Stage 5", f"[{character}] Stage 6A", f"[{character}] Stage 6B"]}

				if both_stage_4 or character in STAGE_4A_TEAM:
					regions[f"[{character}] Mid"]["exits"].append(f"[{character}] Stage 4A")

				if both_stage_4 or character in STAGE_4B_TEAM:
					regions[f"[{character}] Mid"]["exits"].append(f"[{character}] Stage 4B")

				level = 0
				for stage in STAGES_LIST:
					level += 1
					if level > 8:
						continue

					# If both stage 4 are not active, we skip the corresponding stage 4
					if not both_stage_4 and character not in STAGE_4A_TEAM and level == 4:
						continue

					if not both_stage_4 and character not in STAGE_4B_TEAM and level == 5:
						continue

					if level == 4:
						level_name = "4A"
					elif level == 5:
						level_name = "4B"
					elif level == 6:
						level_name = "5"
					elif level == 7:
						level_name = "6A"
					elif level == 8:
						level_name = "6B"
					else:
						level_name = level

					regions[f"[{character}] Stage {level_name}"] = {"locations": [], "exits": None}
					for check in stage:
						if time_check or "Last Spell" not in check:
							regions[f"[{character}] Stage {level_name}"]["locations"].append(f"[{character}] {check}")
					regions[f"[{character}] Stage {level_name}"]["locations"].append(f"[{character}] Stage {level_name} Clear")

				if extra:
					regions[character]["exits"].append(f"[{character}] Extra")
					regions[f"[{character}] Extra"] = {"locations": [], "exits": [f"[{character}] Stage Extra"]}
					regions[f"[{character}] Stage Extra"] = {"locations": [f"[{character}] Stage Extra Clear"], "exits": None}

					for extra_check in EXTRA_CHECKS:
						regions[f"[{character}] Stage Extra"]["locations"].append(f"[{character}] {extra_check}")
		else:
			for character in characters:
				regions[character] = {"locations": None, "exits": [f"[{character}] Early", f"[{character}] Mid", f"[{character}] Late"]}
				regions[f"[{character}] Early"] = {"locations": None, "exits": [f"[{character}] Stage 1", f"[{character}] Stage 2"]}
				regions[f"[{character}] Mid"] = {"locations": None, "exits": [f"[{character}] Stage 3"]}
				regions[f"[{character}] Late"] = {"locations": None, "exits": [f"[{character}] Stage 5", f"[{character}] Stage 6A", f"[{character}] Stage 6B"]}

				if both_stage_4 or character in STAGE_4A_TEAM:
					regions[f"[{character}] Mid"]["exits"].append(f"[{character}] Stage 4A")

				if both_stage_4 or character in STAGE_4B_TEAM:
					regions[f"[{character}] Mid"]["exits"].append(f"[{character}] Stage 4B")

				level = 0
				for stage in STAGES_LIST:
					level += 1
					if level > 8:
						continue

					# If both stage 4 are not active, we skip the corresponding stage 4
					if not both_stage_4 and character not in STAGE_4A_TEAM and level == 4:
						continue

					if not both_stage_4 and character not in STAGE_4B_TEAM and level == 5:
						continue

					if level == 4:
						level_name = "4A"
					elif level == 5:
						level_name = "4B"
					elif level == 6:
						level_name = "5"
					elif level == 7:
						level_name = "6A"
					elif level == 8:
						level_name = "6B"
					else:
						level_name = level

					regions[f"[{character}] Stage {level_name}"] = {"locations": [f"[{character}] Stage {level_name} Clear"], "exits": None}

				if extra:
					regions[character]["exits"].append(f"[{character}] Extra")
					regions[f"[{character}] Extra"] = {"locations": None, "exits": [f"[{character}] Stage Extra"]}
					regions[f"[{character}] Stage Extra"] = {"locations": [f"[{character}] Stage Extra Clear"], "exits": None}
					for extra in EXTRA_CHECKS:
						regions[f"[{character}] Stage Extra"]["locations"].append(f"[{character}] {extra}")

			for difficulty in DIFFICULTY_LIST:
				if exclude_lunatic and difficulty == "Lunatic":
					continue

				for character in characters:
					regions[f"[{character}] Early"]["exits"].append(f"[{difficulty}][{character}] Stage 1")
					regions[f"[{character}] Early"]["exits"].append(f"[{difficulty}][{character}] Stage 2")
					regions[f"[{character}] Mid"]["exits"].append(f"[{difficulty}][{character}] Stage 3")
					if both_stage_4 or character in STAGE_4A_TEAM:
						regions[f"[{character}] Mid"]["exits"].append(f"[{difficulty}][{character}] Stage 4A")
					if both_stage_4 or character in STAGE_4B_TEAM:
						regions[f"[{character}] Mid"]["exits"].append(f"[{difficulty}][{character}] Stage 4B")
					regions[f"[{character}] Late"]["exits"].append(f"[{difficulty}][{character}] Stage 5")
					regions[f"[{character}] Late"]["exits"].append(f"[{difficulty}][{character}] Stage 6A")
					regions[f"[{character}] Late"]["exits"].append(f"[{difficulty}][{character}] Stage 6B")

					level = 0
					for stage in STAGES_LIST:
						level += 1
						if level > 8:
							continue

						# If both stage 4 are not active, we skip the corresponding stage 4
						if not both_stage_4 and character not in STAGE_4A_TEAM and level == 4:
							continue

						if not both_stage_4 and character not in STAGE_4B_TEAM and level == 5:
							continue

						if level == 4:
							level_name = "4A"
						elif level == 5:
							level_name = "4B"
						elif level == 6:
							level_name = "5"
						elif level == 7:
							level_name = "6A"
						elif level == 8:
							level_name = "6B"
						else:
							level_name = level

						regions[f"[{difficulty}][{character}] Stage {level_name}"] = {"locations": [], "exits": None}
						for check in stage:
							if "Last Spell" in check and difficulty == "Easy":
								continue

							if time_check or "Last Spell" not in check:
								regions[f"[{difficulty}][{character}] Stage {level_name}"]["locations"].append(f"[{difficulty}][{character}] {check}")

	if mode in SPELL_PRACTICE_MODE:
		for character in characters:
			if character in SOLO_CHARACTERS_LIST or character in spell_cards_teams:
				regions[character]["exits"].append(f"[{character}] SpellCard")
				regions[f"[{character}] SpellCard"] = {"locations": [], "exits": [f"[{character}][SC] Stage 1", f"[{character}][SC] Stage 2", f"[{character}][SC] Stage 3", f"[{character}][SC] Stage 4A", f"[{character}][SC] Stage 4B", f"[{character}][SC] Stage 5", f"[{character}][SC] Stage 6A", f"[{character}][SC] Stage 6B", f"[{character}][SC] Extra", f"[{character}][SC] Last Word"]}

				# Init Stages region
				for stage in regions[f"[{character}] SpellCard"]["exits"]:
					regions[stage] = {"locations": [], "exits": None}

				# Filling locations
				for id in spell_cards:
					regions[f"[{character}][SC] "+SPELL_CARDS_LIST[id]["stage"]]["locations"].append(f"[{character}] {id} - {SPELL_CARDS_LIST[id]['name']}")

	return regions

def create_regions(multiworld: MultiWorld, player: int, options, spell_cards: list, spell_cards_teams: list):
	difficulty_check = getattr(options, "difficulty_check")
	extra = getattr(options, "extra_stage")
	exclude_lunatic = getattr(options, "exclude_lunatic")
	both_stage_4 = getattr(options, "both_stage_4")
	mode = getattr(options, "mode")
	time_check = getattr(options, "time_check")
	characters = getattr(options, "characters")

	# If we're in Normal mode, we force both_stage_4 to be False
	if mode in NORMAL_MODE:
		both_stage_4 = False

	regions = get_regions(difficulty_check, extra, exclude_lunatic, both_stage_4, time_check, mode, spell_cards, characters, spell_cards_teams)

	# Set up the regions correctly.
	for name, data in regions.items():
		multiworld.regions.append(create_region(multiworld, player, name, data["locations"]))

def create_region(multiworld: MultiWorld, player: int, name: str, locations: list):
	region = Region(name, player, multiworld)
	if locations:
		for location in locations:
			location = TLocation(player, location, location_table[location], region)
			region.locations.append(location)

	return region