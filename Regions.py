from BaseClasses import MultiWorld, Region
from .Locations import TLocation, location_table
from .Variables import *

def get_regions(difficulty_check, extra, exclude_lunatic):
	regions = {}
	characters = CHARACTERS_LIST
	regions["Menu"] = {"locations": None, "exits": characters}
	if difficulty_check not in DIFFICULTY_CHECK:
		for character in characters:
			regions[character] = {"locations": None, "exits": [f"[{character}] Early", f"[{character}] Mid", f"[{character}] Late"]}
			regions[f"[{character}] Early"] = {"locations": None, "exits": [f"[{character}] Stage 1", f"[{character}] Stage 2"]}
			regions[f"[{character}] Mid"] = {"locations": None, "exits": [f"[{character}] Stage 3", f"[{character}] Stage 4A", f"[{character}] Stage 4B"]}
			regions[f"[{character}] Late"] = {"locations": None, "exits": [f"[{character}] Stage 5", f"[{character}] Stage 6A", f"[{character}] Stage 6B"]}

			level = 0
			for stage in STAGES_LIST:
				level += 1
				if level > 8:
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
			regions[f"[{character}] Mid"] = {"locations": None, "exits": [f"[{character}] Stage 3", f"[{character}] Stage 4A", f"[{character}] Stage 4B"]}
			regions[f"[{character}] Late"] = {"locations": None, "exits": [f"[{character}] Stage 5", f"[{character}] Stage 6A", f"[{character}] Stage 6B"]}

			level = 0
			for stage in STAGES_LIST:
				level += 1
				if level > 8:
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
				regions[f"[{character}] Mid"]["exits"].append(f"[{difficulty}][{character}] Stage 4")
				regions[f"[{character}] Late"]["exits"].append(f"[{difficulty}][{character}] Stage 5")
				if difficulty != "Easy":
					regions[f"[{character}] Late"]["exits"].append(f"[{difficulty}][{character}] Stage 6")

				level = 0
				for stage in STAGES_LIST:
					level += 1
					if level > 8:
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
						regions[f"[{difficulty}][{character}] Stage {level_name}"]["locations"].append(f"[{difficulty}][{character}] {check}")

	return regions

def create_regions(multiworld: MultiWorld, player: int, options):
	difficulty_check = getattr(options, "difficulty_check")
	extra = getattr(options, "extra_stage")
	exclude_lunatic = getattr(options, "exclude_lunatic")

	regions = get_regions(difficulty_check, extra, exclude_lunatic)

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