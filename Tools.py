from .Variables import *
from .Mapping import CHAR_MAP, ALT_CHAR_MAP
from .Locations import location_table

def textToBytes(text: str, red = False):
	bytes = []
	current_char_map = ALT_CHAR_MAP if red else CHAR_MAP

	for char in text:
		bytes.append(current_char_map[char])

	return bytes

def getLocationMapping(difficulty):
	mapping = {}
	stage_specific_location_id = {"stage_6": [], "extra": []}

	for location, id in location_table.items():
		character_id = 0
		level = -1
		counter = 0
		difficulty_id = -1

		# Check to see what type of location is it in order to skip it or not
		# First pass to see if it's a stage clear or an extra stage location
		valid_location = False
		if "Stage" in location:
			valid_location = True
		else:
			for check in EXTRA_CHECKS:
				if location.endswith(check):
					valid_location = True
					break

		# If it's not, we filter the difficulty
		if not valid_location:
			found = False
			for difficulty_name in DIFFICULTY_LIST:
				if difficulty_name in location:
					found = True
					if difficulty:
						valid_location = True
						break

			# If it's not a difficulty location and we don't want those, it's a valid location
			if not found and not difficulty:
				valid_location = True

		if not valid_location:
			continue

		# Character
		for character in CHARACTERS_LIST:
			if (character in location):
				character_id = CHARACTER_NAME_TO_ID[character]
				break

		# Stage
		if "Stage" in location:
			level_id = location.split(" ")[-2]
			if level_id == "4A":
				level = 3
			elif level_id == "4B":
				level = 4
			elif level_id == "5":
				level = 5
			elif level_id == "6A":
				level = 6
			elif level_id == "6B":
				level = 7
			elif level_id == "Extra":
				level = 8
			else:
				level = int(level_id)-1

			counter = len(STAGES_LIST[level])-1

			# If it's the final stage clear or the extra stage, we add it to the list
			if level == 7:
				stage_specific_location_id["stage_6"].append(id)
			elif level == 8:
				stage_specific_location_id["extra"].append(id)
		else:
			tmp_level = -1
			for stage in STAGES_LIST:
				tmp_level += 1
				tmp_counter = -1
				for check in stage:
					tmp_counter += 1
					if check in location:
						level = tmp_level
						counter = tmp_counter
						break

				if level >= 0:
					break

		# Difficulty
		if difficulty:
			difficulty_counter = -1
			for difficulty_name in DIFFICULTY_LIST:
				difficulty_counter += 1
				if difficulty_name in location:
					difficulty_id = difficulty_counter
					break

		mapping[id] = [character_id, level, counter, difficulty_id]

	return mapping, stage_specific_location_id

def getPointerAddress(pm, base, offsets):
	address = base
	for offset in offsets[:-1]:
		address = pm.read_uint(address)
		address += offset
	return pm.read_uint(address) + offsets[-1]

def getIntFromBinaryArray(binary_array):
	"""Convert a binary array to an integer."""
	result = int(''.join(map(str, binary_array[::-1])), 2)
	return result