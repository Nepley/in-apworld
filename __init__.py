from typing import List
from .Variables import *

from worlds.AutoWorld import World
from worlds.LauncherComponents import Component, components, launch_subprocess, Type
from .Items import TItem, get_items_by_category, item_table, item_groups
from .Locations import location_table
from .Options import Th08Options
from .Regions import create_regions
from .Rules import set_rules
from .SpellCards import SPELL_CARDS_LIST
from BaseClasses import Item, ItemClassification

def launch_client():
	"""Launch a client instance"""
	from worlds.th08.Client import launch
	launch_subprocess(launch, name="GameClient")

components.append(Component(
	SHORT_NAME+" Client",
	"GameClient",
	func=launch_client,
	component_type=Type.CLIENT
))

class TWorld(World):
	game = DISPLAY_NAME
	options: Th08Options
	options_dataclass = Th08Options

	item_name_groups = item_groups
	item_name_to_id = {name: data.code for name, data in item_table.items()}
	location_name_to_id = {name: id for name, id in location_table.items()}

	def generate_early(self):
		self.spell_cards = []
		self.treasures_locations = []
		self.treasure_final_spell_card = -1
		self.capture_spell_cards_list = []
		self.capture_spell_cards_count = 0
		self.nb_treasure_not_placed = 0
		self.spell_cards_teams = CHARACTERS_LIST

		mode = getattr(self.options, "mode")
		spell_card_difficulties = getattr(self.options, "spell_card_difficulties")
		spell_card_stages = getattr(self.options, "spell_card_stages")
		max_spell_card_count = getattr(self.options, "max_spell_card_count")
		treasure_final_spell_card = getattr(self.options, "treasure_final_spell_card")
		treasure_location = getattr(self.options, "treasure_location")
		capture_spell_cards_stage = getattr(self.options, "capture_spell_cards_stage")
		self.capture_spell_cards_count = getattr(self.options, "capture_spell_cards_count")
		characters = getattr(self.options, "characters")
		spell_cards_teams = getattr(self.options, "spell_cards_teams")
		self.characters_list = []

		goal = getattr(self.options, "goal")

		# Failsafe goal/mode combination
		if goal in SPELL_GOALS and mode not in SPELL_PRACTICE_MODE:
			self.options.goal.value = self.options.goal.option_kaguya
		elif goal in ENDINGS and (mode not in NORMAL_MODE and mode not in PRACTICE_MODE):
			self.options.goal.value = self.options.goal.option_kaguya_treasures

		if mode in SPELL_PRACTICE_MODE:
			self.spell_cards = [spell_id for spell_id in SPELL_CARDS_LIST.keys()]

			# Failsafe
			if not spell_card_difficulties:
				spell_card_difficulties = ["Easy", "Normal", "Hard", "Lunatic", "Extra"]

			if not spell_card_stages:
				spell_card_stages = ["Stage 1", "Stage 2", "Stage 3", "Stage 4A", "Stage 4B", "Stage 5", "Stage 6A", "Stage 6B", "Extra", "Last Word"]

			if goal == CAPTURE_GOAL and not capture_spell_cards_stage:
				capture_spell_cards_stage = ["Stage 1", "Stage 2", "Stage 3", "Stage 4A", "Stage 4B", "Stage 5", "Stage 6A", "Stage 6B", "Extra", "Last Word"]

			if mode not in PRACTICE_MODE and mode not in NORMAL_MODE and goal not in SPELL_GOALS:
				goal = TREASURE_GOAL

			# If we do not have all 4 teams enabled for spell practice, we filter them to get the number needed
			if spell_cards_teams < 4 and characters != SOLO_ONLY:
				self.random.shuffle(self.spell_cards_teams)
				self.spell_cards_teams = self.spell_cards_teams[:spell_cards_teams]

			# We filter out the spell cards that are excluded
			for id, spell in SPELL_CARDS_LIST.items():
				keep = True

				# Check if not excluded by difficulty
				if DIFFICULTY_FROM_ID[spell["difficulty"]] not in spell_card_difficulties:
					keep = False

				# Check if not excluded by stage
				if spell["stage"] not in spell_card_stages:
					keep = False

				if not keep:
					self.spell_cards.remove(id)

			# If we already have 0 spell cards, We force all spell cards from stage 1 to be available
			if len(self.spell_cards) == 0:
				for id, spell in SPELL_CARDS_LIST.items():
					if spell["stage"] == "Stage 1":
						self.spell_cards.append(id)

			if goal == TREASURE_GOAL:
				# We check if the final spell card is valid, if not, we search one backward
				valid = False
				initial_treasure_final_spell_card = -1
				while(not valid and initial_treasure_final_spell_card != treasure_final_spell_card):
					spell_id = str(treasure_final_spell_card)
					if len(spell_id) < 3:
						if len(spell_id) == 1:
							spell_id = "00"+spell_id
						else:
							spell_id = "0"+spell_id

					# Check if not excluded by difficulty or by stage
					if spell_id in self.spell_cards:
						valid = True
						self.treasure_final_spell_card = spell_id
					else:
						if initial_treasure_final_spell_card == -1:
							initial_treasure_final_spell_card = treasure_final_spell_card

						treasure_final_spell_card -= 1
						if treasure_final_spell_card <= 0:
							treasure_final_spell_card = 222

				# if we didn't find any valid spell card, we put it in the final Spell Card of Kaguya (that we force to exist)
				if not valid:
					if "191" not in self.spell_cards:
						self.spell_cards.append("191")
					self.treasure_final_spell_card = "191"

				# We remove the final spell card from the pool to avoid duplicates/problems
				self.spell_cards.remove(self.treasure_final_spell_card)

				# Failsafe
				if treasure_location == TREASURE_ON_KAGUYA and ("Stage 6B" not in spell_card_stages or ("Easy" not in spell_card_difficulties and "Normal" not in spell_card_difficulties and "Hard" not in spell_card_difficulties and "Lunatic" not in spell_card_difficulties)):
					treasure_location = TREASURE_ON_LOCAL

				if treasure_location == TREASURE_ON_LAST_WORD and ("Last Word" not in spell_card_stages or "Extra" not in spell_card_difficulties):
					treasure_location = TREASURE_ON_LOCAL

				# We 'save' 5 spell cards if it's not local or anywhere and we have to remove some spell cards later
				if treasure_location in [TREASURE_ON_KAGUYA, TREASURE_ON_LAST_WORD] and len(self.spell_cards) > max_spell_card_count:
					if treasure_location == TREASURE_ON_KAGUYA:
						spell_list = list(range(184, 191))
						for spell_id in spell_list:
							if str(spell_id) in self.spell_cards:
								self.treasures_locations.append(str(spell_id))
						self.random.shuffle(self.treasures_locations)
						self.treasures_locations = self.treasures_locations[:5]
						for spell_id in self.treasures_locations:
							self.spell_cards.remove(spell_id)
					elif treasure_location == TREASURE_ON_LAST_WORD:
						spell_list = list(range(206, 222))
						for spell_id in spell_list:
							if str(spell_id) in self.spell_cards:
								self.treasures_locations.append(str(spell_id))
						self.random.shuffle(self.treasures_locations)
						self.treasures_locations = self.treasures_locations[:5]

						for spell_id in self.treasures_locations:
							self.spell_cards.remove(spell_id)

					max_spell_card_count -= 5

				# If treasure location is local, we set the treasure to be local_items
				if treasure_location == TREASURE_ON_LOCAL:
					treasures = get_items_by_category("Treasures").keys()
					for treasure in treasures:
						self.options.local_items.value.add(treasure)
			elif goal == CAPTURE_GOAL:
				# We force the accessibility to full
				self.options.accessibility.value = self.options.accessibility.option_full

				# If we're in Capture Spell Cards goal, we add the spell card to the capture list if it's in the selected stages
				for spell_id in self.spell_cards:
					if SPELL_CARDS_LIST[spell_id]["stage"] in capture_spell_cards_stage:
						self.capture_spell_cards_list.append(spell_id)

			# If we still have more spell cards than the maximum allowed, we remove some randomly
			if len(self.spell_cards) > max_spell_card_count:
				self.random.shuffle(self.spell_cards)
				# If we're in Capture Spell Cards goal, we remove first the spell cards that are not needed for the goal
				if goal == CAPTURE_GOAL and len(self.capture_spell_cards_list) < len(self.spell_cards):
					not_needed = [spell for spell in self.spell_cards if spell not in self.capture_spell_cards_list]
					if len(not_needed) >= (len(self.spell_cards) - max_spell_card_count):
						self.spell_cards = [spell for spell in self.spell_cards if spell not in not_needed[:len(self.spell_cards) - max_spell_card_count]]
					else:
						# If we don't have enough "not needed" spell cards, we remove all of them and then remove randomly the remaining needed spell cards
						self.spell_cards = [spell for spell in self.spell_cards if spell not in not_needed]
						self.spell_cards = self.spell_cards[:max_spell_card_count]
				else:
					self.spell_cards = self.spell_cards[:max_spell_card_count]

				# We refill the capture spell cards list with the remaining spell cards
				if goal == CAPTURE_GOAL:
					self.capture_spell_cards_list = []
					for spell_id in self.spell_cards:
						if SPELL_CARDS_LIST[spell_id]["stage"] in capture_spell_cards_stage:
							self.capture_spell_cards_list.append(spell_id)

			# We put back the treasures locations into the spell cards pool
			if self.treasures_locations:
				self.spell_cards += self.treasures_locations

			# If the total spell cards is less than the capture spell cards count, we adjust it
			if goal == CAPTURE_GOAL and len(self.capture_spell_cards_list) < self.capture_spell_cards_count:
				self.capture_spell_cards_count = len(self.capture_spell_cards_list)

			# We sort the spell cards list
			self.spell_cards.sort()

			# We list characters available in spell practice
			if characters == TEAM_ONLY:
				self.characters_list = self.spell_cards_teams
			elif characters == SOLO_ONLY:
				self.characters_list = SOLO_CHARACTERS_LIST
			elif characters == ALL_CHARACTER:
				self.characters_list = self.spell_cards_teams + SOLO_CHARACTERS_LIST

	def fill_slot_data(self) -> dict:
		data = {
			"mode": self.options.mode.value,
			"stage_unlock": self.options.stage_unlock.value,
			"exclude_lunatic": self.options.exclude_lunatic.value,
			"characters": self.options.characters.value,
			"spell_cards_teams": self.spell_cards_teams,
			"number_life_mid": self.options.number_life_mid.value,
			"number_bomb_mid": self.options.number_bomb_mid.value,
			"difficulty_mid": self.options.difficulty_mid.value,
			"number_life_end": self.options.number_life_end.value,
			"number_bomb_end": self.options.number_bomb_end.value,
			"difficulty_end": self.options.difficulty_end.value,
			"extra_stage": self.options.extra_stage.value,
			"number_life_extra": self.options.number_life_extra.value,
			"number_bomb_extra": self.options.number_bomb_extra.value,
			"difficulty_check": self.options.difficulty_check.value,
			"check_multiple_difficulty": self.options.check_multiple_difficulty.value,
			"time_check": self.options.time_check.value,
			"time": self.options.time.value,
			"both_stage_4": self.options.both_stage_4.value,
			"starting_spell_card_count": self.options.starting_spell_card_count.value,
			"spell_card_difficulties": self.options.spell_card_difficulties.value,
			"spell_card_stages": self.options.spell_card_stages.value,
			"max_spell_card_count": self.options.max_spell_card_count.value,
			"goal": self.options.goal.value,
			"ending_required": self.options.ending_required.value,
			"treasure_location": self.options.treasure_location.value,
			"treasure_final_spell_card": self.treasure_final_spell_card,
			"capture_spell_cards_stage": self.options.capture_spell_cards_stage.value,
			"capture_spell_cards_count": int(self.capture_spell_cards_count),
			"death_link": self.options.death_link.value,
			"death_link_trigger": self.options.death_link_trigger.value,
			"death_link_amnesty": self.options.death_link_amnesty.value,
			"ring_link": self.options.ring_link.value,
			"limit_lives": self.options.limit_lives.value,
			"limit_bombs": self.options.limit_bombs.value,
			"capture_spell_cards_list": self.capture_spell_cards_list,
			"nb_treasure_not_placed": self.nb_treasure_not_placed,
		}

		return data

	def create_items(self):
		item_pool: List[TItem] = []
		character_list = []
		progressive_stage_list = []
		stages = []
		spell_cards = []
		extra_stages = []
		treasures = []
		total_locations = len(self.multiworld.get_unfilled_locations(self.player))
		number_placed_item = 0
		mode = getattr(self.options, "mode")
		stage_unlock = getattr(self.options, "stage_unlock")
		progressive_stage = getattr(self.options, "progressive_stage")
		exclude_lunatic = getattr(self.options, "exclude_lunatic")
		characters = getattr(self.options, "characters")
		extra = getattr(self.options, "extra_stage")
		both_stage_4 = getattr(self.options, "both_stage_4")
		time = getattr(self.options, "time")
		starting_spell_card_count = getattr(self.options, "starting_spell_card_count")
		spell_card_difficulties = getattr(self.options, "spell_card_difficulties")
		spell_card_stages = getattr(self.options, "spell_card_stages")
		duplicate_spell_cards = getattr(self.options, "duplicate_spell_cards")
		goal = getattr(self.options, "goal")
		treasure_location = getattr(self.options, "treasure_location")
		traps = getattr(self.options, "traps")
		power_point_trap = getattr(self.options, "power_point_trap")
		bomb_trap = getattr(self.options, "bomb_trap")
		life_trap = getattr(self.options, "life_trap")
		reverse_movement_trap = getattr(self.options, "reverse_movement_trap")
		aya_speed_trap = getattr(self.options, "aya_speed_trap")
		freeze_trap = getattr(self.options, "freeze_trap")
		power_point_drain_trap = getattr(self.options, "power_point_drain_trap")
		reverse_human_youkai_gauge_trap = getattr(self.options, "reverse_human_youkai_gauge_trap")
		extend_time_goal_trap = getattr(self.options, "extend_time_goal_trap")

		# If we're in Normal mode, we force both_stage_4 to be False
		if mode in NORMAL_MODE:
			both_stage_4 = False

		if mode not in PRACTICE_MODE and mode not in NORMAL_MODE and goal not in SPELL_GOALS:
			goal = TREASURE_GOAL
		elif mode not in SPELL_PRACTICE_MODE and goal == TREASURE_GOAL:
			goal = ENDING_FINAL_B

		for name, data in item_table.items():
			quantity = data.max_quantity

			# Categories to be ignored, they will be added in a later stage if necessary.
			if data.category == "Filler":
				continue

			# Will be added later
			if data.category == "Traps":
				continue

			# Will be added manually later
			if data.category == "Endings":
				continue

			# Will be added manually later
			if data.category == "Treasures":
				treasures.append({"name": name, "data": data})
				continue

			# Will be added later
			if data.category in ["[Progressive][Global] Stages", "[Progressive][Character] Stages", "[Progressive][Solo Character] Stages"]:
				progressive_stage_list.append({"name": name, "data": data})
				continue

			# Will be added later
			if data.category in ["Spell Card"]:
				spell_cards.append({"name": name, "data": data})
				continue

			# Will be added later
			if data.category in ["[Not Progressive][Global] Stages", "[Not Progressive][Character] Stages", "[Not Progressive][Solo Character] Stages"]:
				stages.append({"name": name, "data": data})
				continue

			# We do not add Item if we're playing in Spell Card mode only
			if data.category == "Items" and (mode not in PRACTICE_MODE and mode not in NORMAL_MODE):
				continue

			# We do not add Time Point if we're playing in Spell Card mode only
			if data.category == "Time Point" and (mode not in PRACTICE_MODE and mode not in NORMAL_MODE):
				continue

			# Ignored if time is not randomized
			if data.category == "[Time] Items" and (not time or (mode not in PRACTICE_MODE and mode not in NORMAL_MODE)):
				continue

			# We do not add Power Point if we're playing in Spell Card mode only
			if data.category == "Power Point" and (mode not in PRACTICE_MODE and mode not in NORMAL_MODE):
				continue

			# Will be added later
			if data.category == "Characters":
				character_list.append(name)
				continue

			# Will be added later
			if data.category in ["[Global] Extra Stage", "[Character] Extra Stage", "[Solo Character] Extra Stage"]:
				extra_stages.append({"name": name, "data": data})
				continue

			# If Lunatic is excluded, we remove one Lower difficulty
			if data.category == "Items" and name == "Lower Difficulty" and exclude_lunatic:
				quantity -= 1

			item_pool += [self.create_item(name) for _ in range(0, quantity)]

		# Selecting starting character
		if characters in [TEAM_ONLY, ALL_CHARACTER]:
			# If we only have teams, we select one randomly to start with.
			if characters == TEAM_ONLY:
				# If spell practice is on, we take a character that is enabled in it.
				if mode in SPELL_PRACTICE_MODE:
					team = self.random.choice(self.spell_cards_teams)
					starting_character = CHARACTER_TO_ITEM[team][0]
				else:
					starting_character = self.random.choice(character_list)
				self.multiworld.push_precollected(self.create_item(starting_character))
				character_list.remove(starting_character)

			# If we're on Spell Practice only, we don't add characters who don't have check
			for character in character_list:
				if (mode in PRACTICE_MODE or mode in NORMAL_MODE) or ITEM_TO_CHARACTER[character] in self.spell_cards_teams:
					item_pool += [self.create_item(character) for _ in range(0, 1)]

		# Stages
		if mode in PRACTICE_MODE:
			if progressive_stage:
				for stage in progressive_stage_list:
					quantity = stage['data'].max_quantity
					# If there is no extra stage or it's separated, we remove one stage
					if extra != EXTRA_LINEAR and stage['data'].category != "[Progressive][Solo Character] Stages":
						quantity -= 1

					# If there is only one stage 4, we remove one stage
					if not both_stage_4:
						quantity -= 1

					if stage_unlock == STAGE_GLOBAL and stage['data'].category == "[Progressive][Global] Stages":
						item_pool += [self.create_item(stage['name']) for _ in range(0, quantity)]

					if stage_unlock == STAGE_BY_CHARACTER and stage['data'].category == "[Progressive][Character] Stages" and characters in [TEAM_ONLY, ALL_CHARACTER]:
						item_pool += [self.create_item(stage['name']) for _ in range(0, quantity)]

					if stage_unlock == STAGE_BY_CHARACTER and stage['data'].category == "[Progressive][Solo Character] Stages" and characters in [SOLO_ONLY, ALL_CHARACTER]:
						item_pool += [self.create_item(stage['name']) for _ in range(0, quantity)]

				# If we have solo character and we have Extra in linear, we add the Extra unlock for them
				if extra == EXTRA_LINEAR and characters in [SOLO_ONLY, ALL_CHARACTER]:
					item_pool.append(self.create_item("[Solo] Extra Stage"))
			else:
				for stage in stages:
					quantity = stage['data'].max_quantity

					if not both_stage_4 and stage["name"] in ["[Illusion Team] Stage 4A", "[Magic Team] Stage 4B", "[Devil Team] Stage 4B", "[Nether Team] Stage 4A", "[Reimu] Stage 4A", "[Yukari] Stage 4A", "[Marisa] Stage 4B", "[Alice] Stage 4B", "[Sakuya] Stage 4B", "[Remilia] Stage 4B", "[Youmu] Stage 4A", "[Yuyuko] Stage 4A"]:
						continue

					if stage_unlock == STAGE_GLOBAL and stage['data'].category == "[Not Progressive][Global] Stages":
						item_pool += [self.create_item(stage['name']) for _ in range(0, quantity)]

					if stage_unlock == STAGE_BY_CHARACTER and stage['data'].category == "[Not Progressive][Character] Stages" and characters in [TEAM_ONLY, ALL_CHARACTER]:
						item_pool += [self.create_item(stage['name']) for _ in range(0, quantity)]

					if stage_unlock == STAGE_BY_CHARACTER and stage['data'].category == "[Not Progressive][Solo Character] Stages" and characters in [SOLO_ONLY, ALL_CHARACTER]:
						item_pool += [self.create_item(stage['name']) for _ in range(0, quantity)]

				# If Extra is enabled linearly, we change it to apart
				if extra == EXTRA_LINEAR:
					extra = EXTRA_APART

		# Extra
		if extra == EXTRA_APART and (mode in PRACTICE_MODE or mode in NORMAL_MODE):
			for stage in extra_stages:
				quantity = stage['data'].max_quantity

				if stage_unlock == STAGE_GLOBAL and stage['data'].category == "[Global] Extra Stage":
					item_pool += [self.create_item(stage['name']) for _ in range(0, quantity)]

				if stage_unlock == STAGE_BY_CHARACTER and stage['data'].category == "[Character] Extra Stage" and characters in [TEAM_ONLY, ALL_CHARACTER]:
					item_pool += [self.create_item(stage['name']) for _ in range(0, quantity)]

				if stage_unlock == STAGE_BY_CHARACTER and stage['data'].category == "[Solo Character] Extra Stage" and characters in [SOLO_ONLY, ALL_CHARACTER]:
					item_pool += [self.create_item(stage['name']) for _ in range(0, quantity)]

		# Spell Card
		if mode in SPELL_PRACTICE_MODE:
			# Failsafe
			if not spell_card_difficulties:
				spell_card_difficulties = ["Easy", "Normal", "Hard", "Lunatic", "Extra"]

			if not spell_card_stages:
				spell_card_stages = ["Stage 1", "Stage 2", "Stage 3", "Stage 4A", "Stage 4B", "Stage 5", "Stage 6A", "Stage 6B", "Extra", "Last Word"]

			spell_card_items = self.spell_cards

			# If the goal is the treasures, we create the items needed and select the final spell card
			if goal == TREASURE_GOAL:
				# We place the ending on the final spell card
				ending_treasure = self.create_item(ENDING_TREASURE)
				final_spell = SPELL_CARDS_LIST[self.treasure_final_spell_card]
				for character in self.characters_list:
					name = f"[{character}] {self.treasure_final_spell_card} - {final_spell['name']}"
					self.multiworld.get_location(name, self.player).place_locked_item(ending_treasure)
					number_placed_item += 1

				# Failsafe
				if treasure_location == TREASURE_ON_KAGUYA and ("Stage 6B" not in spell_card_stages or ("Easy" not in spell_card_difficulties and "Normal" not in spell_card_difficulties and "Hard" not in spell_card_difficulties and "Lunatic" not in spell_card_difficulties)):
					treasure_location = TREASURE_ON_LOCAL

				if treasure_location == TREASURE_ON_LAST_WORD and ("Last Word" not in spell_card_stages or "Extra" not in spell_card_difficulties):
					treasure_location = TREASURE_ON_LOCAL

				# Placing treasures
				if treasure_location == TREASURE_ON_KAGUYA:
					min_spell = 152
					max_spell = 191
					spell_list = []
					spell_chosen = []
					for i in range(min_spell, max_spell+1):
						spell_id = str(i)
						if spell_id in spell_card_items:
							spell_list.append(str(spell_id))

					# We shuffle the list and take the 5 first result as our spell card
					self.random.shuffle(spell_list)
					for treasure in treasures:
						item = self.create_item(treasure['name'])
						character = self.random.choice(self.characters_list)
						spell = self.random.choice(spell_list)

						nb_try = 0
						while [character, spell] in spell_chosen and nb_try < 100:
							nb_try += 1
							character = self.random.choice(self.characters_list)
							spell = self.random.choice(spell_list)

						# If we didn't manage to place the spell card, we add it to the local item pool
						if nb_try >= 100:
							self.nb_treasure_not_placed += 1
							item_pool += [item for _ in range(0, 1)]
							continue

						spell_detail = SPELL_CARDS_LIST[spell]
						name = f"[{character}] {spell} - {spell_detail['name']}"
						self.multiworld.get_location(name, self.player).place_locked_item(item)
						spell_chosen.append([character, spell])
						number_placed_item += 1
				elif treasure_location == TREASURE_ON_LAST_WORD:
					min_spell = 206
					max_spell = 222
					spell_list = []
					spell_chosen = []
					for i in range(min_spell, max_spell+1):
						spell_id = str(i)
						if spell_id in spell_card_items:
							spell_list.append(str(spell_id))

					# We shuffle the list and take the 5 first result as our spell card
					self.random.shuffle(spell_list)
					for treasure in treasures:
						item = self.create_item(treasure['name'])
						character = self.random.choice(self.characters_list)
						spell = self.random.choice(spell_list)

						nb_try = 0
						while [character, spell] in spell_chosen and nb_try < 100:
							nb_try += 1
							character = self.random.choice(self.characters_list)
							spell = self.random.choice(spell_list)

						# If we didn't manage to place the spell card, we add it to the local item pool
						if nb_try >= 100:
							self.nb_treasure_not_placed += 1
							item_pool += [item for _ in range(0, 1)]
							continue

						spell_detail = SPELL_CARDS_LIST[spell]
						name = f"[{character}] {spell} - {spell_detail['name']}"
						self.multiworld.get_location(name, self.player).place_locked_item(item)
						spell_chosen.append([character, spell])
						number_placed_item += 1
				elif treasure_location == TREASURE_ON_LOCAL or treasure_location == TREASURE_ON_ANYWHERE:
					for treasure in treasures:
						item_pool += [self.create_item(treasure['name']) for _ in range(0, treasure['data'].max_quantity)]

			# We select the starting spellcards
			weighted_spell_card_list = []
			# We give more weight to the first half of the spell cards to have a better chance to get "easier" spell cards at start
			for i in range(0, len(spell_card_items)):
				if i < (len(spell_card_items)/2):
					weight = 5
				else:
					weight = 1
				weighted_spell_card_list.append(weight)

			for i in range(0, starting_spell_card_count):
				if len(spell_card_items) <= 0:
					break
				spell_id = self.random.choices(spell_card_items, weights=weighted_spell_card_list)[0]
				item_name = f"{spell_id} - {SPELL_CARDS_LIST[spell_id]['name']}"
				self.multiworld.push_precollected(self.create_item(item_name))
				weighted_spell_card_list.pop(spell_card_items.index(spell_id))
				spell_card_items.remove(spell_id)

			# We create the remaining spell cards items
			for spell_id in spell_card_items:
				item_name = f"{spell_id} - {SPELL_CARDS_LIST[spell_id]['name']}"
				item_pool += [self.create_item(item_name) for _ in range(0, 1)]

		# Endings
		if mode in PRACTICE_MODE or mode in NORMAL_MODE:
			# Creating and placing Endings
			ending_final_a_illusion = self.create_item("[Illusion Team] Ending - Eirin")
			ending_final_a_magic = self.create_item("[Magic Team] Ending - Eirin")
			ending_final_a_devil = self.create_item("[Devil Team] Ending - Eirin")
			ending_final_a_nether = self.create_item("[Nether Team] Ending - Eirin")
			ending_final_b_illusion = self.create_item("[Illusion Team] Ending - Kaguya")
			ending_final_b_magic = self.create_item("[Magic Team] Ending - Kaguya")
			ending_final_b_devil = self.create_item("[Devil Team] Ending - Kaguya")
			ending_final_b_nether = self.create_item("[Nether Team] Ending - Kaguya")
			ending_extra_illusion = self.create_item("[Illusion Team] Ending - Mokou")
			ending_extra_magic = self.create_item("[Magic Team] Ending - Mokou")
			ending_extra_devil = self.create_item("[Devil Team] Ending - Mokou")
			ending_extra_nether = self.create_item("[Nether Team] Ending - Mokou")
			ending_final_a_reimu = self.create_item("[Reimu] Ending - Eirin")
			ending_final_a_yukari = self.create_item("[Yukari] Ending - Eirin")
			ending_final_a_marisa = self.create_item("[Marisa] Ending - Eirin")
			ending_final_a_alice = self.create_item("[Alice] Ending - Eirin")
			ending_final_a_sakuya = self.create_item("[Sakuya] Ending - Eirin")
			ending_final_a_remilia = self.create_item("[Remilia] Ending - Eirin")
			ending_final_a_youmu = self.create_item("[Youmu] Ending - Eirin")
			ending_final_a_yuyuko = self.create_item("[Yuyuko] Ending - Eirin")
			ending_final_b_reimu = self.create_item("[Reimu] Ending - Kaguya")
			ending_final_b_yukari = self.create_item("[Yukari] Ending - Kaguya")
			ending_final_b_marisa = self.create_item("[Marisa] Ending - Kaguya")
			ending_final_b_alice = self.create_item("[Alice] Ending - Kaguya")
			ending_final_b_sakuya = self.create_item("[Sakuya] Ending - Kaguya")
			ending_final_b_remilia = self.create_item("[Remilia] Ending - Kaguya")
			ending_final_b_youmu = self.create_item("[Youmu] Ending - Kaguya")
			ending_final_b_yuyuko = self.create_item("[Yuyuko] Ending - Kaguya")
			ending_extra_reimu = self.create_item("[Reimu] Ending - Mokou")
			ending_extra_yukari = self.create_item("[Yukari] Ending - Mokou")
			ending_extra_marisa = self.create_item("[Marisa] Ending - Mokou")
			ending_extra_alice = self.create_item("[Alice] Ending - Mokou")
			ending_extra_sakuya = self.create_item("[Sakuya] Ending - Mokou")
			ending_extra_remilia = self.create_item("[Remilia] Ending - Mokou")
			ending_extra_youmu = self.create_item("[Youmu] Ending - Mokou")
			ending_extra_yuyuko = self.create_item("[Yuyuko] Ending - Mokou")

			# If we have the extra stage and the extra boss is a potential goal
			if extra and goal in [ENDING_EXTRA, ENDING_ALL]:
				if characters in [TEAM_ONLY, ALL_CHARACTER]:
					self.multiworld.get_location("[Illusion Team] Stage Extra Clear", self.player).place_locked_item(ending_extra_illusion)
					self.multiworld.get_location("[Magic Team] Stage Extra Clear", self.player).place_locked_item(ending_extra_magic)
					self.multiworld.get_location("[Devil Team] Stage Extra Clear", self.player).place_locked_item(ending_extra_devil)
					self.multiworld.get_location("[Nether Team] Stage Extra Clear", self.player).place_locked_item(ending_extra_nether)
					number_placed_item += 4

				if characters in [SOLO_ONLY, ALL_CHARACTER]:
					self.multiworld.get_location("[Reimu] Stage Extra Clear", self.player).place_locked_item(ending_extra_reimu)
					self.multiworld.get_location("[Yukari] Stage Extra Clear", self.player).place_locked_item(ending_extra_yukari)
					self.multiworld.get_location("[Marisa] Stage Extra Clear", self.player).place_locked_item(ending_extra_marisa)
					self.multiworld.get_location("[Alice] Stage Extra Clear", self.player).place_locked_item(ending_extra_alice)
					self.multiworld.get_location("[Sakuya] Stage Extra Clear", self.player).place_locked_item(ending_extra_sakuya)
					self.multiworld.get_location("[Remilia] Stage Extra Clear", self.player).place_locked_item(ending_extra_remilia)
					self.multiworld.get_location("[Youmu] Stage Extra Clear", self.player).place_locked_item(ending_extra_youmu)
					self.multiworld.get_location("[Yuyuko] Stage Extra Clear", self.player).place_locked_item(ending_extra_yuyuko)
					number_placed_item += 8

			# If Eirin boss is a potential goal
			if goal in [ENDING_FINAL_A, ENDING_ALL]:
				if characters in [TEAM_ONLY, ALL_CHARACTER]:
					self.multiworld.get_location("[Illusion Team] Stage 6A Clear", self.player).place_locked_item(ending_final_a_illusion)
					self.multiworld.get_location("[Magic Team] Stage 6A Clear", self.player).place_locked_item(ending_final_a_magic)
					self.multiworld.get_location("[Devil Team] Stage 6A Clear", self.player).place_locked_item(ending_final_a_devil)
					self.multiworld.get_location("[Nether Team] Stage 6A Clear", self.player).place_locked_item(ending_final_a_nether)
					number_placed_item += 4

				if characters in [SOLO_ONLY, ALL_CHARACTER]:
					self.multiworld.get_location("[Reimu] Stage 6A Clear", self.player).place_locked_item(ending_final_a_reimu)
					self.multiworld.get_location("[Yukari] Stage 6A Clear", self.player).place_locked_item(ending_final_a_yukari)
					self.multiworld.get_location("[Marisa] Stage 6A Clear", self.player).place_locked_item(ending_final_a_marisa)
					self.multiworld.get_location("[Alice] Stage 6A Clear", self.player).place_locked_item(ending_final_a_alice)
					self.multiworld.get_location("[Sakuya] Stage 6A Clear", self.player).place_locked_item(ending_final_a_sakuya)
					self.multiworld.get_location("[Remilia] Stage 6A Clear", self.player).place_locked_item(ending_final_a_remilia)
					self.multiworld.get_location("[Youmu] Stage 6A Clear", self.player).place_locked_item(ending_final_a_youmu)
					self.multiworld.get_location("[Yuyuko] Stage 6A Clear", self.player).place_locked_item(ending_final_a_yuyuko)
					number_placed_item += 8

			# If Kaguya boss is a potential goal
			if (not extra and goal == ENDING_EXTRA) or goal in [ENDING_FINAL_B, ENDING_ALL]:
				if characters in [TEAM_ONLY, ALL_CHARACTER]:
					self.multiworld.get_location("[Illusion Team] Stage 6B Clear", self.player).place_locked_item(ending_final_b_illusion)
					self.multiworld.get_location("[Magic Team] Stage 6B Clear", self.player).place_locked_item(ending_final_b_magic)
					self.multiworld.get_location("[Devil Team] Stage 6B Clear", self.player).place_locked_item(ending_final_b_devil)
					self.multiworld.get_location("[Nether Team] Stage 6B Clear", self.player).place_locked_item(ending_final_b_nether)
					number_placed_item += 4

				if characters in [SOLO_ONLY, ALL_CHARACTER]:
					self.multiworld.get_location("[Reimu] Stage 6B Clear", self.player).place_locked_item(ending_final_b_reimu)
					self.multiworld.get_location("[Yukari] Stage 6B Clear", self.player).place_locked_item(ending_final_b_yukari)
					self.multiworld.get_location("[Marisa] Stage 6B Clear", self.player).place_locked_item(ending_final_b_marisa)
					self.multiworld.get_location("[Alice] Stage 6B Clear", self.player).place_locked_item(ending_final_b_alice)
					self.multiworld.get_location("[Sakuya] Stage 6B Clear", self.player).place_locked_item(ending_final_b_sakuya)
					self.multiworld.get_location("[Remilia] Stage 6B Clear", self.player).place_locked_item(ending_final_b_remilia)
					self.multiworld.get_location("[Youmu] Stage 6B Clear", self.player).place_locked_item(ending_final_b_youmu)
					self.multiworld.get_location("[Yuyuko] Stage 6B Clear", self.player).place_locked_item(ending_final_b_yuyuko)
					number_placed_item += 8

		if mode in SPELL_PRACTICE_MODE and duplicate_spell_cards > 0:
			remaining_locations = total_locations - (len(item_pool) + number_placed_item)

			# If we have duplicate spell cards to add, we count how many of them we need to add
			number_duplicates = int(remaining_locations * duplicate_spell_cards / 100)

			if number_duplicates > 0:
				number_duplicates = min(number_duplicates, len(self.spell_cards))
				duplicateList = self.random.choices(spell_card_items, k=number_duplicates)
				for spell_id in duplicateList:
					item_name = f"{spell_id} - {SPELL_CARDS_LIST[spell_id]['name']}"
					item_pool.append(self.create_item(item_name, ItemClassification.filler))

		if traps > 0:
			remaining_locations = total_locations - (len(item_pool) + number_placed_item)

			# If we have traps, we count how many of them we need to add
			number_traps = int(remaining_locations * traps / 100)

			if number_traps > 0:
				trapList = self.random.choices(["-50% Power Point", "-1 Bomb", "-1 Life", "Reverse Movement", "Aya Speed", "Freeze", "Power Point Drain", "Reverse Human/Youkai Gauge", "Extend Time Goal"], weights=[power_point_trap, bomb_trap, life_trap, reverse_movement_trap, aya_speed_trap, freeze_trap, power_point_drain_trap, reverse_human_youkai_gauge_trap, extend_time_goal_trap], k=number_traps)
				for trap in trapList:
					item_pool.append(self.create_item(trap))

		# Fill any empty locations with filler items.
		while len(item_pool) + number_placed_item < total_locations:
			item_pool.append(self.create_item(self.get_filler_item_name()))

		self.multiworld.itempool += item_pool

	def get_filler_item_name(self) -> str:
		fillers = get_items_by_category("Filler")
		weights = [data.weight for data in fillers.values()]
		return self.random.choices([filler for filler in fillers.keys()], weights, k=1)[0]

	def create_item(self, name: str, classification = "") -> TItem:
		data = item_table[name]
		classification = data.classification if classification == "" else classification
		return TItem(name, classification, data.code, self.player)

	def set_rules(self):
		set_rules(self.multiworld, self.player, self.spell_cards, self.treasure_final_spell_card, self.capture_spell_cards_list, self.capture_spell_cards_count, self.spell_cards_teams)

	def create_regions(self):
		all_spell_cards = self.spell_cards + [self.treasure_final_spell_card] if self.treasure_final_spell_card != -1 else self.spell_cards
		create_regions(self.multiworld, self.player, self.options, all_spell_cards, self.spell_cards_teams)