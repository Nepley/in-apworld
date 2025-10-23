from .Variables import *
from .SpellCards import SPELL_CARDS_LIST
from BaseClasses import Location

class TLocation(Location):
	game: str = SHORT_NAME

location_id_offset = 0
location_table = {}

for character in ALL_CHARACTERS_LIST:
	level = 0
	for stage in STAGES_LIST:
		level += 1
		for check in stage:
			location_table[f"[{character}] {check}"] = STARTING_ID + location_id_offset
			location_id_offset += 1

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
			elif level == 9:
				level_name = "Extra"
			else:
				level_name = level

		location_table[f"[{character}] Stage {level_name} Clear"] = STARTING_ID + location_id_offset
		location_id_offset += 1

for difficulty in DIFFICULTY_LIST:
	for character in ALL_CHARACTERS_LIST:
		level = 0
		for stage in STAGES_LIST:
			level += 1
			if level > 8:
				continue

			for check in stage:
				# We remove the Last Spell location on Easy difficulty
				if "Last Spell" in check and difficulty == "Easy":
					continue

				location_table[f"[{difficulty}][{character}] {check}"] = STARTING_ID + location_id_offset
				location_id_offset += 1

# Spell Cards
for character in ALL_CHARACTERS_LIST:
	for id, spell in SPELL_CARDS_LIST.items():
		# location_id = STARTING_ID + 6000 + character_id + spell_card_id
		location_table[f"[{character}] {id} - {spell['name']}"] = STARTING_ID + int("6"+str(CHARACTER_NAME_TO_ID[character])+id)