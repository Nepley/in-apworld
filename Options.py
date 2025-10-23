from dataclasses import dataclass
from Options import Choice, Range, Toggle, PerGameCommonOptions, OptionSet

class Mode(Choice):
	"""
	Which mode you are playing on.
    Practice Mode: You need to unlock the stage in order to progress.
    Normal Mode: The resources are only given at Stage 1.
    Spell Practice: Each Spell Card in Spell Practice are locations.
    Restriction in life, bomb or difficulty for stages 3/4 and 5/6 and character are the only logical gate
	"""
	display_name = "Mode played"
	option_practice = 0
	option_spell_practice = 1
	option_normal = 2
	option_practice_and_spell_practice = 3
	option_normal_and_spell_practice = 4
	default = 0

class StageUnlock(Choice):
	"""
	[Practice] How the stage unlock are grouped in Practice mode and for the Extra Stage if it's apart
    Global: No group
    By Character: Stage group by character
	"""
	display_name = "Stage unlock mode"
	option_global = 0
	option_by_character = 1

class ProgressiveStage(Toggle):
	"""
	[Practice] In Practice mode, determine if stages are unlocked progressively
	"""
	display_name = "Progressive Stage Unlock"
	default = True

class ExcludeLunatic(Toggle):
	"""[Practice/Normal] If the Lunatic difficulty is excluded"""
	display_name = "Exclude Lunatic difficulty"

class NumberLifeMid(Range):
	"""[Practice/Normal] Number of life the randomizer expect you to have before facing Keine, Reimu and Marisa"""
	display_name = "Number of life expected in order to face Keine, Reimu and Marisa"
	range_start = 0
	range_end = 8
	default = 0

class NumberBombsMid(Range):
	"""[Practice/Normal] Number of bombs the randomizer expect you to have before facing Keine, Reimu and Marisa"""
	display_name = "Number of bombs expected in order to face Keine, Reimu and Marisa"
	range_start = 0
	range_end = 8
	default = 0

class DifficultyMid(Choice):
	"""[Practice/Normal] The difficulty expected in order to face Keine, Reimu and Marisa (Starting from Lunatic and got to Easy)"""
	display_name = "Difficulty in order to face Keine, Reimu and Marisa"
	option_lunatic = 0
	option_hard = 1
	option_normal = 2
	option_easy = 3
	default = 0

class NumberLifeEnd(Range):
	"""[Practice/Normal] Number of life the randomizer expect you to have before facing Reisen, Eirin and Kaguya"""
	display_name = "Number of life expected in order to face Reisen, Eirin and Kaguya"
	range_start = 0
	range_end = 8
	default = 0

class NumberBombsEnd(Range):
	"""[Practice/Normal] Number of bombs the randomizer expect you to have before facing Reisen, Eirin and Kaguya"""
	display_name = "Number of bombs expected in order to face Reisen, Eirin and Kaguya"
	range_start = 0
	range_end = 8
	default = 0

class DifficultyEnd(Choice):
	"""[Practice/Normal] The difficulty expected in order to face Reisen, Eirin and Kaguya (Starting from Lunatic and got to Easy)"""
	display_name = "Difficulty in order to face Reisen, Eirin and Kaguya"
	option_lunatic = 0
	option_hard = 1
	option_normal = 2
	option_easy = 3
	default = 0

class ExtraStage(Choice):
	"""
	[Practice/Normal] Determine if the extra stage is included
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
	"""[Practice/Normal] Number of life the randomizer expect you to have before facing Mokou"""
	display_name = "Number of life expected in order to face Mokou"
	range_start = 0
	range_end = 8
	default = 0

class NumberBombsExtra(Range):
	"""[Practice/Normal] Number of bombs the randomizer expect you to have before facing Mokou"""
	display_name = "Number of bombs expected in order to face Mokou"
	range_start = 0
	range_end = 8
	default = 0

class DifficultyCheck(Choice):
	"""
	[Practice/Normal] If checks are separated by difficulty.
    If true_with_lower, the check of the highest difficulty include the check of the lower difficulties that are unlocked
	"""
	display_name = "Difficulty Check"
	option_false = 0
	option_true = 1
	option_true_with_lower = 2

class TimeCheck(Toggle):
	"""
	[Practice/Normal] If having enough Time and finishing (By dying or clearing it) the Last Spell at the end of a stage grant a check
    Only stages where the Time Goal is above 0 are concerned (stage 1 to 5)
	"""
	display_name = "Time Check"

class Time(Toggle):
	"""
	[Practice/Normal] Determine if the abilty to gain Time is randomized.
	"""
	display_name = "Time Randomized"

class BothStage4(Toggle):
	"""
	[Practice] Determine if each team has access to the stage 4A and 4B or only the one they are assigned
	"""
	display_name = "Both Stage 4"
	default = True

class StartingSpellCardCount(Range):
	"""
	[Spell Practice] The number of Spell Card that will be automatically unlocked at the start.
	"""
	display_name = "Starting Spell Card count"
	range_start = 3
	range_end = 10
	default = 5

class MaxSpellCardCount(Range):
	"""
	[Spell Practice] The maximum number of Spell Card that can be unlocked.
	Starting Spell Card is counted in this limit.
	"""
	display_name = "Maximum Spell Card count"
	range_start = 10
	range_end = 222
	default = 222

class SpellCardDifficulties(OptionSet):
	"""
	[Spell Practice] Choose which Spell Card can appear based on their difficulty. It must have at least one difficulty
    Last Word are in the Extra Difficulty.
    If empty, all difficulties will be included.

    Valid Values: ["Easy", "Normal", "Hard", "Lunatic", "Extra"]
	"""
	display_name = "Spell Card Difficulties"
	valid_keys = ["Easy", "Normal", "Hard", "Lunatic", "Extra"]
	default = ["Easy", "Normal", "Hard", "Lunatic", "Extra"]

class SpellCardStages(OptionSet):
	"""
	[Spell Practice] Choose which Spell Card can appear based on their stage. It must have at least one stage.
    If empty, all stages will be included.
    If the combination of Spell Card Difficulties and Spell Card Stages exclude all Spell Cards from the game,
    then all Spell Cards from Stage 1 will be included to avoid having no Spell Cards at all

    Valid Values: ["Stage 1", "Stage 2", "Stage 3", "Stage 4A", "Stage 4B", "Stage 5", "Stage 6A", "Stage 6B", "Extra", "Last Word"]
	"""
	display_name = "Spell Card Stages"
	valid_keys = ["Stage 1", "Stage 2", "Stage 3", "Stage 4A", "Stage 4B", "Stage 5", "Stage 6A", "Stage 6B", "Extra", "Last Word"]
	default = ["Stage 1", "Stage 2", "Stage 3", "Stage 4A", "Stage 4B", "Stage 5", "Stage 6A", "Stage 6B", "Extra", "Last Word"]

class DuplicateSpellCards(Range):
	"""
	[Spell Practice] Percentage of fillers replaced by a duplicate Spell Cards in the item pool. This will allow out of logic checks.
    It is applied before traps.
	"""
	display_name = "Percentage Duplicate Spell Cards"
	range_start = 0
	range_end = 100
	default = 0

class Goal(Choice):
	"""
	Determine the goal.
    Default to Kaguya when the selected goal is invalid or default to Kaguya's Treasure if Spell Card Practice is the only mode.

    [Practice/Normal] Eirin/Kaguya/Mokou: You must beat the selected boss
    [Practice/Normal] All Bosses: You must beat all the bosses (Mokou only when the Extra Stage is active)
    [Spell Practice] Kaguya's Treasures: You must collect the 5 treasures.
	"""
	display_name = "Goal"
	option_eirin = 0
	option_kaguya = 1
	option_mokou = 2
	option_all_bosses = 3
	option_kaguya_treasures = 4
	default = 1

class EndingRequired(Choice):
	"""
	[Practice/Normal] How many time do you need to beat the required boss if it's the selected goal.
	"""
	display_name = "How many time do you need to beat the required boss"
	option_once = 0
	option_all_characters = 1
	default = 0

class TreasureLocation(Choice):
	"""
	[Spell Practice] If the goal is set to Kaguya's Treasure, choose where the treasure are located.
	Default to Local if the selected option is not possible (Ex: Spell Cards excluded)
	Kaguya: They are on Kaguya's Spell Cards
	Last Word: They are on Last Word's Spell Cards
	Local: They are anywhere in the game
	Anywhere: They are anywhere in the multiworld
	"""
	display_name = "Treasure Location"
	option_kaguya = 0
	option_last_word = 1
	option_local = 2
	option_anywhere = 3
	default = 0

class TreasureFinalSpellCard(Range):
	"""
	[Spell Practice] Which Spell Card is set has the victory condition and is unlocked with the 5 treasure
	The value is the ID of the Spell Card.
	If the Spell Card is excluded, it will do -1 to the spell card until it found a valid one.
	Default to the last Spell Card of Kaguya.

	Quick references by stages:
	Stage 1:   1-13
	Stage 2:   14-32
	Stage 3:   33-54
	Stage 4A:  55-77
	Stage 4B:  78-100
	Stage 5:   101-119
	Stage 6A:  120-147
	Stage 6B:  148-191
	Extra:     192-205
	Last Word: 206-222
	"""
	display_name = "Final Spell Card"
	range_start = 1
	range_end = 222
	default = 191

class DeathLink(Toggle):
	"""
	When you die, everyone who enabled death link dies. Of course, the reverse is true too. Can be changed later.
    In Spell Practice, you can only receive Death Links.
	"""
	display_name = "Death Link"

class DeathLinkAmnesty(Range):
	"""
	Number of death before sending a DeathLink. Can be changed later.
	"""
	display_name = "DeathLink Amnesty"
	range_start = 0
	range_end = 10
	default = 0

class RingLink(Toggle):
    """
    Whether your in-level Power Point gain/loss is linked to other players. Can be changed later.
    """
    display_name = "Ring Link"

class LimitLives(Range):
	"""[Practice/Normal] Limit on the maximum number of lives you can have. It only apply on the client, not on the item pool or logic. Can be changed later."""
	display_name = "Lives limit"
	range_start = 0
	range_end = 8
	default = 8

class LimitBombs(Range):
	"""[Practice/Normal] Limit on the maximum number of bombs you can have. It only apply on the client, not on the item pool generation or logic. Can be changed later"""
	display_name = "Bombs limit"
	range_start = 0
	range_end = 8
	default = 8

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

class ReverseHumanYoukaiGaugeTrap(Range):
	"""
	Weight of the reverse human youkai trap.
    This trap make the humain/Youkai gauge gain reversed but not the effect
	"""
	display_name = "Reverse Humain/Youkai gauge trap"
	range_start = 0
	range_end = 100
	default = 15

class ExtendTimeGoalTrap(Range):
	"""
	Weight of the extend time goal trap.
    Add 25% to the time requirement of the current stage
	"""
	display_name = "Extend time goal trap"
	range_start = 0
	range_end = 100
	default = 15

@dataclass
class Th08Options(PerGameCommonOptions):
	mode: Mode
	stage_unlock: StageUnlock
	progressive_stage: ProgressiveStage
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
	time_check: TimeCheck
	time: Time
	both_stage_4: BothStage4
	starting_spell_card_count: StartingSpellCardCount
	spell_card_difficulties: SpellCardDifficulties
	spell_card_stages: SpellCardStages
	max_spell_card_count: MaxSpellCardCount
	duplicate_spell_cards: DuplicateSpellCards
	goal: Goal
	ending_required: EndingRequired
	treasure_location: TreasureLocation
	treasure_final_spell_card: TreasureFinalSpellCard
	death_link: DeathLink
	death_link_amnesty: DeathLinkAmnesty
	ring_link: RingLink
	limit_lives: LimitLives
	limit_bombs: LimitBombs
	traps: Traps
	power_point_trap: PowerPointTrap
	bomb_trap: BombTrap
	life_trap: LifeTrap
	reverse_movement_trap: ReverseMovementTrap
	aya_speed_trap: AyaSpeedTrap
	freeze_trap: FreezeTrap
	power_point_drain_trap: PowerPointDrainTrap
	reverse_human_youkai_gauge_trap: ReverseHumanYoukaiGaugeTrap
	extend_time_goal_trap: ExtendTimeGoalTrap