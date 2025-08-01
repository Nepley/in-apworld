from typing import List
from .Variables import *

from worlds.AutoWorld import World
from worlds.LauncherComponents import Component, components, launch_subprocess, Type
from .Items import TItem, get_items_by_category, item_table
from .Locations import location_table
from .Options import Th08Options
from .Regions import create_regions
from .Rules import set_rules

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

	item_name_to_id = {name: data.code for name, data in item_table.items()}
	location_name_to_id = {name: id for name, id in location_table.items()}

	def fill_slot_data(self) -> dict:
		return {option_name: getattr(self.options, option_name).value for option_name in self.options_dataclass.__dataclass_fields__.keys()}

	def create_items(self):
		item_pool: List[TItem] = []
		character_list = []
		stages = []
		extra_stages = []
		total_locations = len(self.multiworld.get_unfilled_locations(self.player))
		number_placed_item = 0
		mode = getattr(self.options, "mode")
		stage_unlock = getattr(self.options, "stage_unlock")
		exclude_lunatic = getattr(self.options, "exclude_lunatic")
		extra = getattr(self.options, "extra_stage")
		goal = getattr(self.options, "goal")
		traps = getattr(self.options, "traps")
		power_point_trap = getattr(self.options, "power_point_trap")
		bomb_trap = getattr(self.options, "bomb_trap")
		life_trap = getattr(self.options, "life_trap")
		reverse_movement_trap = getattr(self.options, "reverse_movement_trap")
		aya_speed_trap = getattr(self.options, "aya_speed_trap")
		freeze_trap = getattr(self.options, "freeze_trap")
		power_point_drain_trap = getattr(self.options, "power_point_drain_trap")

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

			# Will be added later
			if data.category in ["[Global] Stages", "[Character] Stages"]:
				stages.append({"name": name, "data": data})
				continue

			# Ignored if it's not normal mode
			if data.category == "[Normal] Items" and mode == PRACTICE_MODE:
				continue

			# Will be added later
			if data.category == "Characters":
				character_list.append(name)
				continue

			# Will be added later
			if data.category in ["[Global] Extra Stage", "[Character] Extra Stage"]:
				extra_stages.append({"name": name, "data": data})
				continue

			# If Lunatic is excluded, we remove one Lower difficulty
			if data.category == "Items" and name == "Lower Difficulty" and exclude_lunatic:
				quantity -= 1

			item_pool += [self.create_item(name) for _ in range(0, quantity)]

		# Stages
		if mode == PRACTICE_MODE:
			for stage in stages:
				quantity = stage['data'].max_quantity
				# If there is no extra stage or it's separated, we remove one stage
				if extra != EXTRA_LINEAR:
					quantity -= 1

				if stage_unlock == STAGE_GLOBAL and stage['data'].category == "[Global] Stages":
					item_pool += [self.create_item(stage['name']) for _ in range(0, quantity)]

				if stage_unlock == STAGE_BY_CHARACTER and stage['data'].category == "[Character] Stages":
					item_pool += [self.create_item(stage['name']) for _ in range(0, quantity)]

		# Extra
		if extra == EXTRA_APART:
			for stage in extra_stages:
				quantity = stage['data'].max_quantity

				if stage_unlock == STAGE_GLOBAL and stage['data'].category == "[Global] Extra Stage":
					item_pool += [self.create_item(stage['name']) for _ in range(0, quantity)]

				if stage_unlock == STAGE_BY_CHARACTER and stage['data'].category == "[Character] Extra Stage":
					item_pool += [self.create_item(stage['name']) for _ in range(0, quantity)]

		# Selecting starting character
		chosen = self.random.choice(character_list)
		self.multiworld.push_precollected(self.create_item(chosen))
		character_list.remove(chosen)
		for character in character_list:
			item_pool += [self.create_item(character) for _ in range(0, 1)]

		# Creating and placing Endings
		ending_final_b_illusion = self.create_item("[Illusion Team] Ending - Kaguya")
		ending_final_b_magic = self.create_item("[Magic Team] Ending - Kaguya")
		ending_final_b_devil = self.create_item("[Devil Team] Ending - Kaguya")
		ending_final_b_nether = self.create_item("[Nether Team] Ending - Kaguya")
		ending_extra_illusion = self.create_item("[Illusion Team] Ending - Mokou")
		ending_extra_magic = self.create_item("[Magic Team] Ending - Mokou")
		ending_extra_devil = self.create_item("[Devil Team] Ending - Mokou")
		ending_extra_nether = self.create_item("[Nether Team] Ending - Mokou")

		# If we have the extra stage and the extra boss is a potential goal
		if extra and goal not in [ENDING_FINAL_B]:
				self.multiworld.get_location("[Illusion Team] Stage Extra Clear", self.player).place_locked_item(ending_extra_illusion)
				self.multiworld.get_location("[Magic Team] Stage Extra Clear", self.player).place_locked_item(ending_extra_magic)
				self.multiworld.get_location("[Devil Team] Stage Extra Clear", self.player).place_locked_item(ending_extra_devil)
				self.multiworld.get_location("[Nether Team] Stage Extra Clear", self.player).place_locked_item(ending_extra_nether)
				number_placed_item += 4

		# If the final boss is a potential goal
		if (not extra and goal == ENDING_EXTRA) or goal in [ENDING_FINAL_B, ENDING_ALL]:
				self.multiworld.get_location("[Illusion Team] Stage 6B Clear", self.player).place_locked_item(ending_final_b_illusion)
				self.multiworld.get_location("[Magic Team] Stage 6B Clear", self.player).place_locked_item(ending_final_b_magic)
				self.multiworld.get_location("[Devil Team] Stage 6B Clear", self.player).place_locked_item(ending_final_b_devil)
				self.multiworld.get_location("[Nether Team] Stage 6B Clear", self.player).place_locked_item(ending_final_b_nether)
				number_placed_item += 4

		if traps > 0:
			remaining_locations = total_locations - (len(item_pool) + number_placed_item)

			# If we have traps, we count how many of them we need to add
			number_traps = int(remaining_locations * traps / 100)

			if number_traps > 0:
				trapList = self.random.choices(["-50% Power Point", "-1 Bomb", "-1 Life", "Reverse Movement", "Aya Speed", "Freeze", "Power Point Drain"], weights=[power_point_trap, bomb_trap, life_trap, reverse_movement_trap, aya_speed_trap, freeze_trap, power_point_drain_trap], k=number_traps)
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

	def create_item(self, name: str) -> TItem:
		data = item_table[name]
		return TItem(name, data.classification, data.code, self.player)

	def set_rules(self):
		set_rules(self.multiworld, self.player)

	def create_regions(self):
		create_regions(self.multiworld, self.player, self.options)