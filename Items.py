from typing import Dict, NamedTuple, Optional
from .Variables import *

from BaseClasses import Item, ItemClassification

class TItem(Item):
	game: str = DISPLAY_NAME

class TItemData(NamedTuple):
	category: str
	code: Optional[int] = None
	classification: ItemClassification = ItemClassification.filler
	max_quantity: int = 1
	weight: int = 1

def get_items_by_category(category: str) -> Dict[str, TItemData]:
	item_dict: Dict[str, TItemData] = {}
	for name, data in item_table.items():
		if data.category == category:
			item_dict.setdefault(name, data)

	return item_dict

item_table: Dict[str, TItemData] = {
	# Items
	"+1 Life":				TItemData("Items", STARTING_ID + 0, ItemClassification.progression_skip_balancing, 8),
	"+1 Bomb":				TItemData("Items", STARTING_ID + 1, ItemClassification.progression_skip_balancing, 8),
	"Lower Difficulty":		TItemData("Items", STARTING_ID + 2, ItemClassification.progression_skip_balancing, 3),
	"+1 Continue":			TItemData("[Normal] Items", STARTING_ID + 3, ItemClassification.useful, 3),
	"+25 Power Point":		TItemData("Power Point", STARTING_ID + 4, ItemClassification.useful, 5),

	# Characters
	"Illusionary Barrier Team":		TItemData("Characters", STARTING_ID + 100, ItemClassification.progression),
	"Aria of Forbidden Magic Team":	TItemData("Characters", STARTING_ID + 101, ItemClassification.progression),
	"Visionary Scarlet Devil Team":	TItemData("Characters", STARTING_ID + 102, ItemClassification.progression),
	"Netherworld Dwellers Team":	TItemData("Characters", STARTING_ID + 103, ItemClassification.progression),

	# Stages
	"Next Stage":					TItemData("[Global] Stages", STARTING_ID + 200, ItemClassification.progression_skip_balancing, 8),
	"[Illusion Team] Next Stage":	TItemData("[Character] Stages", STARTING_ID + 201, ItemClassification.progression_skip_balancing, 8),
	"[Magic Team] Next Stage":		TItemData("[Character] Stages", STARTING_ID + 202, ItemClassification.progression_skip_balancing, 8),
	"[Devil Team] Next Stage":		TItemData("[Character] Stages", STARTING_ID + 203, ItemClassification.progression_skip_balancing, 8),
	"[Nether Team] Next Stage":		TItemData("[Character] Stages", STARTING_ID + 204, ItemClassification.progression_skip_balancing, 8),
	"Extra Stage":					TItemData("[Global] Extra Stage", STARTING_ID + 205, ItemClassification.progression_skip_balancing),
	"[Illusion Team] Extra Stage":	TItemData("[Character] Extra Stage", STARTING_ID + 206, ItemClassification.progression_skip_balancing),
	"[Magic Team] Extra Stage":		TItemData("[Character] Extra Stage", STARTING_ID + 207, ItemClassification.progression_skip_balancing),
	"[Devil Team] Extra Stage":		TItemData("[Character] Extra Stage", STARTING_ID + 208, ItemClassification.progression_skip_balancing),
	"[Nether Team] Extra Stage":	TItemData("[Character] Extra Stage", STARTING_ID + 209, ItemClassification.progression_skip_balancing),

	# Endings
	"[Illusion Team] Ending - Eirin":	TItemData("Endings", STARTING_ID + 300, ItemClassification.progression, 4),
	"[Magic Team] Ending - Eirin":		TItemData("Endings", STARTING_ID + 301, ItemClassification.progression, 4),
	"[Devil Team] Ending - Eirin":		TItemData("Endings", STARTING_ID + 302, ItemClassification.progression, 4),
	"[Nether Team] Ending - Eirin":		TItemData("Endings", STARTING_ID + 303, ItemClassification.progression, 4),
	"[Illusion Team] Ending - Kaguya":	TItemData("Endings", STARTING_ID + 304, ItemClassification.progression, 4),
	"[Magic Team] Ending - Kaguya":		TItemData("Endings", STARTING_ID + 305, ItemClassification.progression, 4),
	"[Devil Team] Ending - Kaguya":		TItemData("Endings", STARTING_ID + 306, ItemClassification.progression, 4),
	"[Nether Team] Ending - Kaguya":	TItemData("Endings", STARTING_ID + 307, ItemClassification.progression, 4),
	"[Illusion Team] Ending - Mokou":	TItemData("Endings", STARTING_ID + 308, ItemClassification.progression, 4),
	"[Magic Team] Ending - Mokou":		TItemData("Endings", STARTING_ID + 309, ItemClassification.progression, 4),
	"[Devil Team] Ending - Mokou":		TItemData("Endings", STARTING_ID + 310, ItemClassification.progression, 4),
	"[Nether Team] Ending - Mokou":		TItemData("Endings", STARTING_ID + 311, ItemClassification.progression, 4),

	# Junk
	"+1 Power Point":	TItemData("Filler", STARTING_ID + 400),

	# Trap
	"-50% Power Point":		TItemData("Traps", STARTING_ID + 500, ItemClassification.trap),
	"-1 Bomb":				TItemData("Traps", STARTING_ID + 501, ItemClassification.trap),
	"-1 Life":				TItemData("Traps", STARTING_ID + 502, ItemClassification.trap),
	"Reverse Movement":		TItemData("Traps", STARTING_ID + 503, ItemClassification.trap),
	"Aya Speed":			TItemData("Traps", STARTING_ID + 504, ItemClassification.trap),
	"Freeze":				TItemData("Traps", STARTING_ID + 505, ItemClassification.trap),
	"Power Point Drain":	TItemData("Traps", STARTING_ID + 506, ItemClassification.trap),
}