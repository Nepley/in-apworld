from dataclasses import dataclass
from Options import Choice, Range, Toggle, DeathLink, PerGameCommonOptions

class Mode(Choice):
	"""
	Which mode you are playing on.
    Practice Mode: You need to unlock the stage in order to progress.
    Normal Mode: The resources are only given at Stage 1. Add 3 Continues to the Item Pools
                           Restriction in life, bomb or difficulty for stages 3/4 and 5/6 and character are the only logical gate
	"""
	display_name = "Mode played"
	option_practice = 0
	option_normal = 2
	default = 0

class StageUnlock(Choice):
	"""
	How the stage unlock are grouped in Practice mode and for the Extra Stage if it's apart
    Global: No group
    By Character: Stage group by character
	"""
	display_name = "Stage unlock mode"
	option_global = 0
	option_by_character = 1

class ExcludeLunatic(Toggle):
	"""If the Lunatic difficulty is excluded"""
	display_name = "Exclude Lunatic difficulty"

class NumberLifeMid(Range):
	"""Number of life the randomizer expect you to have before facing Keine, Reimu and Marisa"""
	display_name = "Number of life expected in order to face Keine, Reimu and Marisa"
	range_start = 0
	range_end = 8
	default = 0

class NumberBombsMid(Range):
	"""Number of bombs the randomizer expect you to have before facing Keine, Reimu and Marisa"""
	display_name = "Number of bombs expected in order to face Keine, Reimu and Marisa"
	range_start = 0
	range_end = 8
	default = 0

class DifficultyMid(Choice):
	"""The difficulty expected in order to face Keine, Reimu and Marisa (Starting from Lunatic and got to Easy)"""
	display_name = "Difficulty in order to face Keine, Reimu and Marisa"
	option_lunatic = 0
	option_hard = 1
	option_normal = 2
	option_easy = 3
	default = 0

class NumberLifeEnd(Range):
	"""Number of life the randomizer expect you to have before facing Reisen, Eirin and Kaguya"""
	display_name = "Number of life expected in order to face Reisen, Eirin and Kaguya"
	range_start = 0
	range_end = 8
	default = 0

class NumberBombsEnd(Range):
	"""Number of bombs the randomizer expect you to have before facing Reisen, Eirin and Kaguya"""
	display_name = "Number of bombs expected in order to face Reisen, Eirin and Kaguya"
	range_start = 0
	range_end = 8
	default = 0

class DifficultyEnd(Choice):
	"""The difficulty expected in order to face Reisen, Eirin and Kaguya (Starting from Lunatic and got to Easy)"""
	display_name = "Difficulty in order to face Reisen, Eirin and Kaguya"
	option_lunatic = 0
	option_hard = 1
	option_normal = 2
	option_easy = 3
	default = 0

class ExtraStage(Choice):
	"""
	Determine if the extra stage is included
    Linear: The extra stage is considered as the 7th stage
    Apart: The extra stage has it's own item for it to be unlocked
    This option will follow the rule of how the stage are unlocked in Practice Mode (Global, By Character or By Shot Type)
	"""
	display_name = "Determine if the extra stage is included"
	option_exclude = 0
	option_include_linear = 1
	option_include_apart = 2
	default = 0

class NumberLifeExtra(Range):
	"""Number of life the randomizer expect you to have before facing Mokou"""
	display_name = "Number of life expected in order to face Mokou"
	range_start = 0
	range_end = 8
	default = 0

class NumberBombsExtra(Range):
	"""Number of bombs the randomizer expect you to have before facing Mokou"""
	display_name = "Number of bombs expected in order to face Mokou"
	range_start = 0
	range_end = 8
	default = 0

class DifficultyCheck(Choice):
	"""
	If checks are separated by difficulty.
    If true_with_lower, the check of the highest difficulty include the check of the lower difficulties that are unlocked
	"""
	display_name = "Difficulty Check"
	option_false = 0
	option_true = 1
	option_true_with_lower = 2

class Goal(Choice):
	"""If the Extra Stage is included, determine which boss is the goal."""
	display_name = "Goal"
	option_eirin = 0
	option_kaguya = 1
	option_mokou = 2
	option_all = 3
	default = 1

class EndingRequired(Choice):
	"""
	How many time do you need to beat the required boss.
	"""
	display_name = "How many time do you need to beat the required boss"
	option_once = 0
	option_all_characters = 1
	default = 0

class RingLink(Toggle):
    """
    Whether your in-level Power Point gain/loss is linked to other players
    """
    display_name = "Ring Link"

class Traps(Range):
	"""Percentage of fillers that are traps"""
	display_name = "Percentage of fillers that are traps"
	range_start = 0
	range_end = 100
	default = 0

class PowerPointTrap(Range):
	"""
	Weight of the -50% power point trap.
    This trap reduce the power point by 50%
	"""
	display_name = "-50% power point trap"
	range_start = 0
	range_end = 100
	default = 20

class BombTrap(Range):
	"""
	Weight of the -1 bomb trap.
    This trap remove 1 bomb
	"""
	display_name = "-1 bomb trap"
	range_start = 0
	range_end = 100
	default = 0

class LifeTrap(Range):
	"""
	Weight of the -1 life trap.
    This trap remove 1 life
	"""
	display_name = "-1 life trap"
	range_start = 0
	range_end = 100
	default = 0

class ReverseMovementTrap(Range):
	"""
	Weight of the Reverse Movement trap.
    This trap reverse the movement of the player
	"""
	display_name = "Reverse Movement trap"
	range_start = 0
	range_end = 100
	default = 20

class AyaSpeedTrap(Range):
	"""
	Weight of the Aya speed trap.
    This trap make the speed of the player more extreme (faster normally, slower focus)
	"""
	display_name = "Aya speed trap"
	range_start = 0
	range_end = 100
	default = 20

class FreezeTrap(Range):
	"""
	Weight of the freeze trap.
    This trap freeze the player for a short amount of time
	"""
	display_name = "Freeze trap"
	range_start = 0
	range_end = 100
	default = 5

class PowerPointDrainTrap(Range):
	"""
	Weight of the power point drain trap.
    This trap drain the power point of the player (1 power point per second)
	"""
	display_name = "Power point drain trap"
	range_start = 0
	range_end = 100
	default = 15

@dataclass
class Th08Options(PerGameCommonOptions):
	mode: Mode
	stage_unlock: StageUnlock
	exclude_lunatic: ExcludeLunatic
	number_life_mid: NumberLifeMid
	number_bomb_mid: NumberBombsMid
	difficulty_mid: DifficultyMid
	number_life_end: NumberLifeEnd
	number_bomb_end: NumberBombsEnd
	difficulty_end: DifficultyEnd
	extra_stage: ExtraStage
	number_life_extra: NumberLifeExtra
	number_bomb_extra: NumberBombsExtra
	difficulty_check: DifficultyCheck
	goal: Goal
	ending_required: EndingRequired
	death_link: DeathLink
	ring_link: RingLink
	traps: Traps
	power_point_trap: PowerPointTrap
	bomb_trap: BombTrap
	life_trap: LifeTrap
	reverse_movement_trap: ReverseMovementTrap
	aya_speed_trap: AyaSpeedTrap
	freeze_trap: FreezeTrap
	power_point_drain_trap: PowerPointDrainTrap