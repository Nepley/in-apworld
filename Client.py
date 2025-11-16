from typing import Optional
import asyncio
import colorama
import time
import random
from .gameHandler import *
from .guardRail import *
from .Tools import *
from .Mapping import *
import traceback

from CommonClient import (
	CommonContext,
	ClientCommandProcessor,
	get_base_parser,
	logger,
	server_loop,
	gui_enabled,
)

class TouhouClientProcessor(ClientCommandProcessor):
	def _cmd_multiple_difficulty_check(self, active = None):
		"""Toggle the possibility to check multiple difficulty check by doing the highest difficulty
        :param active: If "on" or "true", enable it. If "off" or "false", disable it."""
		changed = False
		if self.ctx.handler is not None and self.ctx.handler.gameController is not None:
			if active is not None:
				if active.lower() in ["on", "true"]:
					if "DeathLink" not in self.ctx.tags:
						self.ctx.check_multiple_difficulty = True
						changed = True
					logger.info("Multiple difficulty check enabled")
				elif active.lower() in ("off", "false"):
					if "DeathLink" in self.ctx.tags:
						self.ctx.check_multiple_difficulty = False
						changed = True
					logger.info("Multiple difficulty check disabled")
				else:
					logger.error("Invalid argument, use 'on' or 'off'")
			else:
				logger.info(f"Multiple difficulty check is {'enabled' if self.ctx.death_link_is_active else 'disabled'}")
		else:
			logger.error("Multiple difficulty check cannot be changed before connecting to the game and server")

		return changed

	def _cmd_deathlink(self, active = None):
		"""Toggle DeathLink on or off
        :param active: If "on" or "true", enable DeathLink. If "off" or "false", disable DeathLink."""
		changed = False
		if self.ctx.handler is not None and self.ctx.handler.gameController is not None:
			if active is not None:
				if active.lower() in ["on", "true"]:
					if "DeathLink" not in self.ctx.tags:
						self.ctx.tags.add("DeathLink")
						self.ctx.death_link_is_active = True
						changed = True
					logger.info("DeathLink enabled")
				elif active.lower() in ("off", "false"):
					if "DeathLink" in self.ctx.tags:
						self.ctx.tags.remove("DeathLink")
						self.ctx.death_link_is_active = False
						changed = True
					logger.info("DeathLink disabled")
				else:
					logger.error("Invalid argument, use 'on' or 'off'")

				if changed:
					asyncio.create_task(self.ctx.send_msgs([{"cmd": "ConnectUpdate", "tags": self.ctx.tags}]))
			else:
				logger.info(f"DeathLink is {'enabled' if self.ctx.death_link_is_active else 'disabled'}")
		else:
			logger.error("DeathLink cannot be changed before connecting to the game and server")

		return changed

	def _cmd_deathlink_trigger(self, value = None):
		"""Get or Set the trigger for the DeayhLink trigger
        :param value: Possibler values are "life" or "gameover"
		"""
		if self.ctx.handler is not None and self.ctx.handler.gameController is not None:
			if value is not None:
				if value.lower() == "life":
					self.ctx.death_link_trigger = DEATH_LINK_LIFE
					logger.info("DeathLink trigger set to 'Life'")
					return True
				elif value.lower() == "gameover":
					self.ctx.death_link_trigger = DEATH_LINK_GAME_OVER
					logger.info("DeathLink trigger set to 'Game Over'")
					return True
				else:
					logger.error("Invalid argument, use 'life' or 'gameover'")
					return False
			else:
				trigger = "Life" if self.ctx.death_link_trigger == DEATH_LINK_LIFE else "Game Over"
				logger.info(f"Current DeathLink Trigger: {trigger}")
				return True
		else:
			logger.error("DeathLink amnesty cannot be accessed before connecting to the game and server")
			return False

	def _cmd_deathlink_amnesty(self, value = -1):
		"""Get or Set the number of death before sending a DeathLink
        :param value: Set the amnesty to this value, must be between 0 and 10."""
		if self.ctx.handler is not None and self.ctx.handler.gameController is not None:
			if value == -1:
				logger.info(f"Current DeathLink amnesty: {self.ctx.death_link_amnesty}")
				return True
			else:
				try:
					value = int(value)
					if value < 0 or value > 10:
						raise ValueError
					self.ctx.death_link_amnesty = value
					logger.info(f"New DeathLink amnesty: {value}")
					return True
				except ValueError:
					logger.error("Invalid argument, amnesty must be between 0 and 10")
					return False
		else:
			logger.error("DeathLink amnesty cannot be accessed before connecting to the game and server")
			return False

	def _cmd_ringlink(self, active = None):
		"""Toggle RingLink on or off
        :param active: If "on" or "true", enable RingLink. If "off" or "false", disable RingLink."""
		changed = False
		if self.ctx.handler is not None and self.ctx.handler.gameController is not None:
			if active is not None:
				if active.lower() in ("on", "true"):
					if "RingLink" not in self.ctx.tags:
						self.ctx.tags.add("RingLink")
						self.ctx.ring_link_is_active = True
						changed = True
					logger.info("RingLink enabled")
				elif active.lower() in ("off", "false"):
					if "RingLink" in self.ctx.tags:
						self.ctx.tags.remove("RingLink")
						changed = True
						self.ctx.ring_link_is_active = False
					logger.info("RingLink disabled")
				else:
					logger.error("Invalid argument, use 'on' or 'off'")

				if changed:
					asyncio.create_task(self.ctx.send_msgs([{"cmd": "ConnectUpdate", "tags": self.ctx.tags}]))
			else:
				logger.info(f"RingLink is {'enabled' if self.ctx.ring_link_is_active else 'disabled'}")
		else:
			logger.error("RingLink cannot be changed before connecting to the game and server")

		return changed

	def _cmd_limits(self, lives = -1, bombs = -1):
		"""Get or Set the max limits for lives and bombs
        :param lives: New max lives value, must be between 0 and 8.
        :param bombs: New max bombs value, must be between 0 and 8."""
		if self.ctx.handler is not None and self.ctx.handler.gameController is not None:
			if lives == -1 and bombs == -1:
				logger.info(f"Current max lives: {self.ctx.handler.limitLives} / Current max bombs: {self.ctx.handler.limitBombs}")
				return True
			else:
				try:
					lives = int(lives)
					bombs = int(bombs)
					if lives < 0 or lives > 8 or bombs < 0 or bombs > 8:
						raise ValueError
					self.ctx.handler.setLivesLimit(lives)
					self.ctx.handler.setBombsLimit(bombs)
					logger.info(f"New max lives: {lives} / New max bombs: {bombs}")
					return True
				except ValueError:
					logger.error("Invalid argument, limits must be between 0 and 8")
					return False
		else:
			logger.error("Limits cannot be accessed before connecting to the game and server")
			return False

	def _cmd_treasures(self):
		"""Get the number of treasures collected and tell what the final Spell Card is."""
		if self.ctx.handler is not None and self.ctx.handler.gameController is not None:
			if self.ctx.options["goal"] != TREASURE_GOAL:
				logger.error("No Treasure.")
				return False
			logger.info(f"Treasures collected: {self.ctx.handler.treasures}/5")
			logger.info(f"Final Spell Card: {self.ctx.options['treasure_final_spell_card']}")
			if self.ctx.options['nb_treasure_not_placed'] > 0:
				logger.info(f"Note: {self.ctx.options['nb_treasure_not_placed']} treasure(s) were placed 'anywhere'.")
			return True
		else:
			logger.error("Treasures cannot be accessed before connecting to the game and server")
			return False

	def _cmd_captures(self):
		"""Get the number of Spell Cards captured."""
		if self.ctx.handler is not None and self.ctx.handler.gameController is not None:
			if self.ctx.options["goal"] != CAPTURE_GOAL:
				logger.error("No Capture.")
				return False
			logger.info(f"Spell Cards captured: {len(self.ctx.capture_spell_cards_list)}/{self.ctx.options['capture_spell_cards_count']}")
			return True
		else:
			logger.error("Captures cannot be accessed before connecting to the game and server")
			return False

class TouhouContext(CommonContext):
	"""Touhou Game Context"""
	def __init__(self, server_address: Optional[str], password: Optional[str]) -> None:
		super().__init__(server_address, password)
		self.game = DISPLAY_NAME
		self.items_handling = 0b111  # Item from starting inventory, own world and other world
		self.pending_death_link = False
		self.command_processor = TouhouClientProcessor

		self.current_power_point = -1
		self.ring_link_id = None
		self.last_power_point = -1

		self.handler = None # gameHandler
		self.inError = False
		self.msgQueue = []

		# List of items/locations
		self.all_location_ids = None
		self.location_name_to_ap_id = None
		self.location_ap_id_to_name = None
		self.item_name_to_ap_id = None
		self.item_ap_id_to_name = None
		self.previous_location_checked = None
		self.location_mapping = None
		self.stage_specific_location_id = None

		self.is_connected = False
		self.last_death_link = 0
		self.last_ring_link = 0
		self.death_link_is_active = False
		self.ring_link_is_active = False
		self.death_link_amnesty = 0
		self.death_link_trigger = DEATH_LINK_LIFE

		# Spell Card
		self.capture_spell_cards_list = []
		self.victory_sent = False

		# Counter
		self.difficulties = 3
		self.traps = {"power_point_drain": 0, "reverse_control": 0, "aya_speed": 0, "freeze": 0, "bomb": 0, "life": 0, "power_point": 0, "reverse_human_youkai_gauge": 0, "extend_time_goal": 0}
		self.can_trap = True

		self.options = None
		self.check_multiple_difficulty = False
		self.ExtraMenu = False
		self.minimalCursor = 0

	def make_gui(self):
		ui = super().make_gui()
		ui.base_title = f"{DISPLAY_NAME} Client"
		return ui

	async def server_auth(self, password_requested: bool = False):
		if password_requested and not self.password:
			await super().server_auth(password_requested)
		await self.get_username()
		await self.send_connect()

	def on_package(self, cmd: str, args: dict):
		"""
		Manage the package received from the server
		"""
		if cmd == "Connected":
			self.previous_location_checked = args['checked_locations']
			self.all_location_ids = set(args["missing_locations"] + args["checked_locations"])
			self.options = args["slot_data"] # Yaml Options
			self.is_connected = True
			self.check_multiple_difficulty = self.options['check_multiple_difficulty']
			self.location_mapping, self.stage_specific_location_id = getLocationMapping(self.options['difficulty_check'] == DIFFICULTY_CHECK)

			if self.handler is not None:
				self.handler.reset()

			asyncio.create_task(self.send_msgs([{"cmd": "GetDataPackage", "games": [DISPLAY_NAME]}]))

		if cmd == "ReceivedItems":
			asyncio.create_task(self.give_item(args["items"]))

		elif cmd == "DataPackage":
			if not self.all_location_ids:
				# Connected package not received yet, wait for datapackage request after connected package
				return
			self.location_name_to_ap_id = args["data"]["games"][DISPLAY_NAME]["location_name_to_id"]
			self.location_name_to_ap_id = {
				name: loc_id for name, loc_id in
				self.location_name_to_ap_id.items() if loc_id in self.all_location_ids
			}
			self.location_ap_id_to_name = {v: k for k, v in self.location_name_to_ap_id.items()}
			self.item_name_to_ap_id = args["data"]["games"][DISPLAY_NAME]["item_name_to_id"]
			self.item_ap_id_to_name = {v: k for k, v in self.item_name_to_ap_id.items()}
		elif cmd == "Bounced":
			tags = args.get("tags", [])
			# we can skip checking "DeathLink" in ctx.tags, as otherwise we wouldn't have been send this
			if "DeathLink" in tags and self.last_death_link != args["data"]["time"]:
				self.last_death_link = args["data"]["time"]
				self.on_deathlink(args["data"])
			elif "RingLink" in tags and self.ring_link_id != None:
				self.last_ring_link = args["data"]["time"]
				self.on_ringlink(args["data"])

	def client_recieved_initial_server_data(self):
		"""
		This method waits until the client finishes the initial conversation with the server.
		This means:
			- All LocationInfo packages recieved - requested only if patch files dont exist.
			- DataPackage package recieved (id_to_name maps and name_to_id maps are popualted)
			- Connection package recieved (slot number populated)
			- RoomInfo package recieved (seed name populated)
		"""
		return self.is_connected

	async def wait_for_initial_connection_info(self):
		"""
		This method waits until the client finishes the initial conversation with the server.
		See client_recieved_initial_server_data for wait requirements.
		"""
		if self.client_recieved_initial_server_data():
			return

		logger.info("Waiting for connect from server...")
		while not self.client_recieved_initial_server_data():
			await asyncio.sleep(1)

	async def give_item(self, items):
		"""
		Give an item to the player. This method will always give the oldest
		item that the player has recieved from AP, but not in game yet.

		:NetworkItem item: The item to give to the player
		"""

		gotAnyItem = False

		# We wait for the link to be etablished to the game before giving any items
		while self.handler is None or self.handler.gameController is None:
			await asyncio.sleep(0.5)

		for item in items:
			item_id = item.item - STARTING_ID
			match item_id:
				case 0: # Life
					self.handler.addLife()
					gotAnyItem = True
					self.msgQueue.append({"msg": SHORT_ITEM_NAME[item_id], "color": FLASHING_TEXT})
				case 1: # Bomb
					self.handler.addBomb()
					gotAnyItem = True
					self.msgQueue.append({"msg": SHORT_ITEM_NAME[item_id], "color": FLASHING_TEXT})
				case 2: # Lower Difficulty
					self.difficulties -= 1
					self.handler.unlockDifficulty(self.difficulties)
					gotAnyItem = True
					self.msgQueue.append({"msg": SHORT_ITEM_NAME[item_id], "color": FLASHING_TEXT})
				case 3: # Time Gain
					self.handler.unlockTimeGain()
					gotAnyItem = True
					self.msgQueue.append({"msg": SHORT_ITEM_NAME[item_id], "color": FLASHING_TEXT})
				case 4: # 25 Power Point
					self.handler.add25Power()
					gotAnyItem = True
					self.msgQueue.append({"msg": SHORT_ITEM_NAME[item_id], "color": FLASHING_TEXT})
				case 5: # 1000 Time Point
					self.handler.addTimePoint(1000)
					gotAnyItem = True
					self.msgQueue.append({"msg": SHORT_ITEM_NAME[item_id], "color": FLASHING_TEXT})
				case 100: # Illusion Team
					self.handler.unlockCharacter(ILLUSION_TEAM)
					gotAnyItem = True
					self.msgQueue.append({"msg": SHORT_ITEM_NAME[item_id], "color": FLASHING_TEXT})
				case 101: # Magic Team
					self.handler.unlockCharacter(MAGIC_TEAM)
					gotAnyItem = True
					self.msgQueue.append({"msg": SHORT_ITEM_NAME[item_id], "color": FLASHING_TEXT})
				case 102: # Devil Team
					self.handler.unlockCharacter(DEVIL_TEAM)
					gotAnyItem = True
					self.msgQueue.append({"msg": SHORT_ITEM_NAME[item_id], "color": FLASHING_TEXT})
				case 103: # Nether Team
					self.handler.unlockCharacter(NETHER_TEAM)
					gotAnyItem = True
					self.msgQueue.append({"msg": SHORT_ITEM_NAME[item_id], "color": FLASHING_TEXT})
				case 200: # Next Stage
					isExtraStageLinear = self.options['extra_stage'] == EXTRA_LINEAR
					bothStage4 = self.options['both_stage_4']
					self.handler.addProgressiveStage(isExtraStageLinear, -1, bothStage4)
					gotAnyItem = True
					self.msgQueue.append({"msg": SHORT_ITEM_NAME[item_id], "color": FLASHING_TEXT})
				case 201: # [Illusion] Next Stage
					isExtraStageLinear = self.options['extra_stage'] == EXTRA_LINEAR
					bothStage4 = self.options['both_stage_4']
					self.handler.addProgressiveStage(isExtraStageLinear, ILLUSION_TEAM, bothStage4)
					gotAnyItem = True
					self.msgQueue.append({"msg": SHORT_ITEM_NAME[item_id], "color": FLASHING_TEXT})
				case 202: # [Magic] Next Stage
					isExtraStageLinear = self.options['extra_stage'] == EXTRA_LINEAR
					bothStage4 = self.options['both_stage_4']
					self.handler.addProgressiveStage(isExtraStageLinear, MAGIC_TEAM, bothStage4)
					gotAnyItem = True
					self.msgQueue.append({"msg": SHORT_ITEM_NAME[item_id], "color": FLASHING_TEXT})
				case 203: # [Devil] Next Stage
					isExtraStageLinear = self.options['extra_stage'] == EXTRA_LINEAR
					bothStage4 = self.options['both_stage_4']
					self.handler.addProgressiveStage(isExtraStageLinear, DEVIL_TEAM, bothStage4)
					gotAnyItem = True
					self.msgQueue.append({"msg": SHORT_ITEM_NAME[item_id], "color": FLASHING_TEXT})
				case 204: # [Nether] Next Stage
					isExtraStageLinear = self.options['extra_stage'] == EXTRA_LINEAR
					bothStage4 = self.options['both_stage_4']
					self.handler.addProgressiveStage(isExtraStageLinear, NETHER_TEAM, bothStage4)
					gotAnyItem = True
					self.msgQueue.append({"msg": SHORT_ITEM_NAME[item_id], "color": FLASHING_TEXT})
				case 205: # Extra Stage
					isExtraStageApart = self.options['extra_stage'] == EXTRA_APART
					if isExtraStageApart or (self.options['mode'] in PRACTICE_MODE and not self.options['progressive_stage']):
						self.handler.unlockExtraStage()
						gotAnyItem = True
						self.msgQueue.append({"msg": SHORT_ITEM_NAME[item_id], "color": FLASHING_TEXT})
				case 206: # [Illusion] Extra Stage
					isExtraStageApart = self.options['extra_stage'] == EXTRA_APART
					if isExtraStageApart or (self.options['mode'] in PRACTICE_MODE and not self.options['progressive_stage']):
						self.handler.unlockExtraStage(ILLUSION_TEAM)
						gotAnyItem = True
						self.msgQueue.append({"msg": SHORT_ITEM_NAME[item_id], "color": FLASHING_TEXT})
				case 207: # [Magic] Extra Stage
					isExtraStageApart = self.options['extra_stage'] == EXTRA_APART
					if isExtraStageApart or (self.options['mode'] in PRACTICE_MODE and not self.options['progressive_stage']):
						self.handler.unlockExtraStage(MAGIC_TEAM)
						gotAnyItem = True
						self.msgQueue.append({"msg": SHORT_ITEM_NAME[item_id], "color": FLASHING_TEXT})
				case 208: # [Devil] Extra Stage
					isExtraStageApart = self.options['extra_stage'] == EXTRA_APART
					if isExtraStageApart or (self.options['mode'] in PRACTICE_MODE and not self.options['progressive_stage']):
						self.handler.unlockExtraStage(DEVIL_TEAM)
						gotAnyItem = True
						self.msgQueue.append({"msg": SHORT_ITEM_NAME[item_id], "color": FLASHING_TEXT})
				case 209: # [Nether] Extra Stage
					isExtraStageApart = self.options['extra_stage'] == EXTRA_APART
					if isExtraStageApart or (self.options['mode'] in PRACTICE_MODE and not self.options['progressive_stage']):
						self.handler.unlockExtraStage(NETHER_TEAM)
						gotAnyItem = True
						self.msgQueue.append({"msg": SHORT_ITEM_NAME[item_id], "color": FLASHING_TEXT})
				case 2109: # [Solo] Extra Stage
					self.handler.unlockSoloExtraStage()
					gotAnyItem = True
					self.msgQueue.append({"msg": SHORT_ITEM_NAME[item_id], "color": FLASHING_TEXT})
				case 210: # Stage 2
					bothStage4 = self.options['both_stage_4']
					self.handler.addStage(1, -1, bothStage4)
					gotAnyItem = True
					self.msgQueue.append({"msg": SHORT_ITEM_NAME[item_id], "color": FLASHING_TEXT})
				case 211: # Stage 3
					bothStage4 = self.options['both_stage_4']
					self.handler.addStage(2, -1, bothStage4)
					gotAnyItem = True
					self.msgQueue.append({"msg": SHORT_ITEM_NAME[item_id], "color": FLASHING_TEXT})
				case 212: # Stage 4A
					bothStage4 = self.options['both_stage_4']
					self.handler.addStage(3, -1, bothStage4)
					gotAnyItem = True
					self.msgQueue.append({"msg": SHORT_ITEM_NAME[item_id], "color": FLASHING_TEXT})
				case 213: # Stage 4B
					bothStage4 = self.options['both_stage_4']
					self.handler.addStage(4, -1, bothStage4)
					gotAnyItem = True
					self.msgQueue.append({"msg": SHORT_ITEM_NAME[item_id], "color": FLASHING_TEXT})
				case 214: # Stage 5
					bothStage4 = self.options['both_stage_4']
					self.handler.addStage(5, -1, bothStage4)
					gotAnyItem = True
					self.msgQueue.append({"msg": SHORT_ITEM_NAME[item_id], "color": FLASHING_TEXT})
				case 215: # Stage 6A
					bothStage4 = self.options['both_stage_4']
					self.handler.addStage(6, -1, bothStage4)
					gotAnyItem = True
					self.msgQueue.append({"msg": SHORT_ITEM_NAME[item_id], "color": FLASHING_TEXT})
				case 216: # Stage 6B
					bothStage4 = self.options['both_stage_4']
					self.handler.addStage(7, -1, bothStage4)
					gotAnyItem = True
					self.msgQueue.append({"msg": SHORT_ITEM_NAME[item_id], "color": FLASHING_TEXT})
				case 217: # [Illusion Team] Stage 2
					bothStage4 = self.options['both_stage_4']
					self.handler.addStage(1, ILLUSION_TEAM, bothStage4)
					gotAnyItem = True
					self.msgQueue.append({"msg": SHORT_ITEM_NAME[item_id], "color": FLASHING_TEXT})
				case 218: # [Illusion Team] Stage 3
					bothStage4 = self.options['both_stage_4']
					self.handler.addStage(2, ILLUSION_TEAM, bothStage4)
					gotAnyItem = True
					self.msgQueue.append({"msg": SHORT_ITEM_NAME[item_id], "color": FLASHING_TEXT})
				case 219: # [Illusion Team] Stage 4A
					bothStage4 = self.options['both_stage_4']
					self.handler.addStage(3, ILLUSION_TEAM, bothStage4)
					gotAnyItem = True
					self.msgQueue.append({"msg": SHORT_ITEM_NAME[item_id], "color": FLASHING_TEXT})
				case 220: # [Illusion Team] Stage 4B
					bothStage4 = self.options['both_stage_4']
					self.handler.addStage(4, ILLUSION_TEAM, bothStage4)
					gotAnyItem = True
					self.msgQueue.append({"msg": SHORT_ITEM_NAME[item_id], "color": FLASHING_TEXT})
				case 221: # [Illusion Team] Stage 5
					bothStage4 = self.options['both_stage_4']
					self.handler.addStage(5, ILLUSION_TEAM, bothStage4)
					gotAnyItem = True
					self.msgQueue.append({"msg": SHORT_ITEM_NAME[item_id], "color": FLASHING_TEXT})
				case 222: # [Illusion Team] Stage 6A
					bothStage4 = self.options['both_stage_4']
					self.handler.addStage(6, ILLUSION_TEAM, bothStage4)
					gotAnyItem = True
					self.msgQueue.append({"msg": SHORT_ITEM_NAME[item_id], "color": FLASHING_TEXT})
				case 223: # [Illusion Team] Stage 6B
					bothStage4 = self.options['both_stage_4']
					self.handler.addStage(7, ILLUSION_TEAM, bothStage4)
					gotAnyItem = True
					self.msgQueue.append({"msg": SHORT_ITEM_NAME[item_id], "color": FLASHING_TEXT})
				case 224: # [Magic Team] Stage 2
					bothStage4 = self.options['both_stage_4']
					self.handler.addStage(1, MAGIC_TEAM, bothStage4)
					gotAnyItem = True
					self.msgQueue.append({"msg": SHORT_ITEM_NAME[item_id], "color": FLASHING_TEXT})
				case 225: # [Magic Team] Stage 3
					bothStage4 = self.options['both_stage_4']
					self.handler.addStage(2, MAGIC_TEAM, bothStage4)
					gotAnyItem = True
					self.msgQueue.append({"msg": SHORT_ITEM_NAME[item_id], "color": FLASHING_TEXT})
				case 226: # [Magic Team] Stage 4A
					bothStage4 = self.options['both_stage_4']
					self.handler.addStage(3, MAGIC_TEAM, bothStage4)
					gotAnyItem = True
					self.msgQueue.append({"msg": SHORT_ITEM_NAME[item_id], "color": FLASHING_TEXT})
				case 227: # [Magic Team] Stage 4B
					bothStage4 = self.options['both_stage_4']
					self.handler.addStage(4, MAGIC_TEAM, bothStage4)
					gotAnyItem = True
					self.msgQueue.append({"msg": SHORT_ITEM_NAME[item_id], "color": FLASHING_TEXT})
				case 228: # [Magic Team] Stage 5
					bothStage4 = self.options['both_stage_4']
					self.handler.addStage(5, MAGIC_TEAM, bothStage4)
					gotAnyItem = True
					self.msgQueue.append({"msg": SHORT_ITEM_NAME[item_id], "color": FLASHING_TEXT})
				case 229: # [Magic Team] Stage 6A
					bothStage4 = self.options['both_stage_4']
					self.handler.addStage(6, MAGIC_TEAM, bothStage4)
					gotAnyItem = True
					self.msgQueue.append({"msg": SHORT_ITEM_NAME[item_id], "color": FLASHING_TEXT})
				case 230: # [Magic Team] Stage 6B
					bothStage4 = self.options['both_stage_4']
					self.handler.addStage(7, MAGIC_TEAM, bothStage4)
					gotAnyItem = True
					self.msgQueue.append({"msg": SHORT_ITEM_NAME[item_id], "color": FLASHING_TEXT})
				case 231: # [Devil Team] Stage 2
					bothStage4 = self.options['both_stage_4']
					self.handler.addStage(1, DEVIL_TEAM, bothStage4)
					gotAnyItem = True
					self.msgQueue.append({"msg": SHORT_ITEM_NAME[item_id], "color": FLASHING_TEXT})
				case 232: # [Devil Team] Stage 3
					bothStage4 = self.options['both_stage_4']
					self.handler.addStage(2, DEVIL_TEAM, bothStage4)
					gotAnyItem = True
					self.msgQueue.append({"msg": SHORT_ITEM_NAME[item_id], "color": FLASHING_TEXT})
				case 233: # [Devil Team] Stage 4A
					bothStage4 = self.options['both_stage_4']
					self.handler.addStage(3, DEVIL_TEAM, bothStage4)
					gotAnyItem = True
					self.msgQueue.append({"msg": SHORT_ITEM_NAME[item_id], "color": FLASHING_TEXT})
				case 234: # [Devil Team] Stage 4B
					bothStage4 = self.options['both_stage_4']
					self.handler.addStage(4, DEVIL_TEAM, bothStage4)
					gotAnyItem = True
					self.msgQueue.append({"msg": SHORT_ITEM_NAME[item_id], "color": FLASHING_TEXT})
				case 235: # [Devil Team] Stage 5
					bothStage4 = self.options['both_stage_4']
					self.handler.addStage(5, DEVIL_TEAM, bothStage4)
					gotAnyItem = True
					self.msgQueue.append({"msg": SHORT_ITEM_NAME[item_id], "color": FLASHING_TEXT})
				case 236: # [Devil Team] Stage 6A
					bothStage4 = self.options['both_stage_4']
					self.handler.addStage(6, DEVIL_TEAM, bothStage4)
					gotAnyItem = True
					self.msgQueue.append({"msg": SHORT_ITEM_NAME[item_id], "color": FLASHING_TEXT})
				case 237: # [Devil Team] Stage 6B
					bothStage4 = self.options['both_stage_4']
					self.handler.addStage(7, DEVIL_TEAM, bothStage4)
					gotAnyItem = True
					self.msgQueue.append({"msg": SHORT_ITEM_NAME[item_id], "color": FLASHING_TEXT})
				case 238: # [Nether Team] Stage 2
					bothStage4 = self.options['both_stage_4']
					self.handler.addStage(1, NETHER_TEAM, bothStage4)
					gotAnyItem = True
					self.msgQueue.append({"msg": SHORT_ITEM_NAME[item_id], "color": FLASHING_TEXT})
				case 239: # [Nether Team] Stage 3
					bothStage4 = self.options['both_stage_4']
					self.handler.addStage(2, NETHER_TEAM, bothStage4)
					gotAnyItem = True
					self.msgQueue.append({"msg": SHORT_ITEM_NAME[item_id], "color": FLASHING_TEXT})
				case 240: # [Nether Team] Stage 4A
					bothStage4 = self.options['both_stage_4']
					self.handler.addStage(3, NETHER_TEAM, bothStage4)
					gotAnyItem = True
					self.msgQueue.append({"msg": SHORT_ITEM_NAME[item_id], "color": FLASHING_TEXT})
				case 241: # [Nether Team] Stage 4B
					bothStage4 = self.options['both_stage_4']
					self.handler.addStage(4, NETHER_TEAM, bothStage4)
					gotAnyItem = True
					self.msgQueue.append({"msg": SHORT_ITEM_NAME[item_id], "color": FLASHING_TEXT})
				case 242: # [Nether Team] Stage 5
					bothStage4 = self.options['both_stage_4']
					self.handler.addStage(5, NETHER_TEAM, bothStage4)
					gotAnyItem = True
					self.msgQueue.append({"msg": SHORT_ITEM_NAME[item_id], "color": FLASHING_TEXT})
				case 243: # [Nether Team] Stage 6A
					bothStage4 = self.options['both_stage_4']
					self.handler.addStage(6, NETHER_TEAM, bothStage4)
					gotAnyItem = True
					self.msgQueue.append({"msg": SHORT_ITEM_NAME[item_id], "color": FLASHING_TEXT})
				case 244: # [Nether Team] Stage 6B
					bothStage4 = self.options['both_stage_4']
					self.handler.addStage(7, NETHER_TEAM, bothStage4)
					gotAnyItem = True
					self.msgQueue.append({"msg": SHORT_ITEM_NAME[item_id], "color": FLASHING_TEXT})
				case 245: # [Reimu] Next Stage
					isExtraStageLinear = self.options['extra_stage'] == EXTRA_LINEAR
					bothStage4 = self.options['both_stage_4']
					self.handler.addProgressiveStage(isExtraStageLinear, REIMU, bothStage4)
					gotAnyItem = True
					self.msgQueue.append({"msg": SHORT_ITEM_NAME[item_id], "color": FLASHING_TEXT})
				case 246: # [Yukari] Next Stage
					isExtraStageLinear = self.options['extra_stage'] == EXTRA_LINEAR
					bothStage4 = self.options['both_stage_4']
					self.handler.addProgressiveStage(isExtraStageLinear, YUKARI, bothStage4)
					gotAnyItem = True
					self.msgQueue.append({"msg": SHORT_ITEM_NAME[item_id], "color": FLASHING_TEXT})
				case 247: # [Marisa] Next Stage
					isExtraStageLinear = self.options['extra_stage'] == EXTRA_LINEAR
					bothStage4 = self.options['both_stage_4']
					self.handler.addProgressiveStage(isExtraStageLinear, MARISA, bothStage4)
					gotAnyItem = True
					self.msgQueue.append({"msg": SHORT_ITEM_NAME[item_id], "color": FLASHING_TEXT})
				case 248: # [Alice] Next Stage
					isExtraStageLinear = self.options['extra_stage'] == EXTRA_LINEAR
					bothStage4 = self.options['both_stage_4']
					self.handler.addProgressiveStage(isExtraStageLinear, ALICE, bothStage4)
					gotAnyItem = True
					self.msgQueue.append({"msg": SHORT_ITEM_NAME[item_id], "color": FLASHING_TEXT})
				case 249: # [Sakuya] Next Stage
					isExtraStageLinear = self.options['extra_stage'] == EXTRA_LINEAR
					bothStage4 = self.options['both_stage_4']
					self.handler.addProgressiveStage(isExtraStageLinear, SAKUYA, bothStage4)
					gotAnyItem = True
					self.msgQueue.append({"msg": SHORT_ITEM_NAME[item_id], "color": FLASHING_TEXT})
				case 250: # [Remilia] Next Stage
					isExtraStageLinear = self.options['extra_stage'] == EXTRA_LINEAR
					bothStage4 = self.options['both_stage_4']
					self.handler.addProgressiveStage(isExtraStageLinear, REMILIA, bothStage4)
					gotAnyItem = True
					self.msgQueue.append({"msg": SHORT_ITEM_NAME[item_id], "color": FLASHING_TEXT})
				case 251: # [Youmu] Next Stage
					isExtraStageLinear = self.options['extra_stage'] == EXTRA_LINEAR
					bothStage4 = self.options['both_stage_4']
					self.handler.addProgressiveStage(isExtraStageLinear, YOUMU, bothStage4)
					gotAnyItem = True
					self.msgQueue.append({"msg": SHORT_ITEM_NAME[item_id], "color": FLASHING_TEXT})
				case 252: # [Yuyuko] Next Stage
					isExtraStageLinear = self.options['extra_stage'] == EXTRA_LINEAR
					bothStage4 = self.options['both_stage_4']
					self.handler.addProgressiveStage(isExtraStageLinear, YUYUKO, bothStage4)
					gotAnyItem = True
					self.msgQueue.append({"msg": SHORT_ITEM_NAME[item_id], "color": FLASHING_TEXT})
				case 253: # [Reimu] Stage 2
					bothStage4 = self.options['both_stage_4']
					self.handler.addStage(1, REIMU, bothStage4)
					gotAnyItem = True
					self.msgQueue.append({"msg": SHORT_ITEM_NAME[item_id], "color": FLASHING_TEXT})
				case 254: # [Reimu] Stage 3
					bothStage4 = self.options['both_stage_4']
					self.handler.addStage(2, REIMU, bothStage4)
					gotAnyItem = True
					self.msgQueue.append({"msg": SHORT_ITEM_NAME[item_id], "color": FLASHING_TEXT})
				case 255: # [Reimu] Stage 4A
					bothStage4 = self.options['both_stage_4']
					self.handler.addStage(3, REIMU, bothStage4)
					gotAnyItem = True
					self.msgQueue.append({"msg": SHORT_ITEM_NAME[item_id], "color": FLASHING_TEXT})
				case 256: # [Reimu] Stage 4B
					bothStage4 = self.options['both_stage_4']
					self.handler.addStage(4, REIMU, bothStage4)
					gotAnyItem = True
					self.msgQueue.append({"msg": SHORT_ITEM_NAME[item_id], "color": FLASHING_TEXT})
				case 257: # [Reimu] Stage 5
					bothStage4 = self.options['both_stage_4']
					self.handler.addStage(5, REIMU, bothStage4)
					gotAnyItem = True
					self.msgQueue.append({"msg": SHORT_ITEM_NAME[item_id], "color": FLASHING_TEXT})
				case 258: # [Reimu] Stage 6A
					bothStage4 = self.options['both_stage_4']
					self.handler.addStage(6, REIMU, bothStage4)
					gotAnyItem = True
					self.msgQueue.append({"msg": SHORT_ITEM_NAME[item_id], "color": FLASHING_TEXT})
				case 259: # [Reimu] Stage 6B
					bothStage4 = self.options['both_stage_4']
					self.handler.addStage(7, REIMU, bothStage4)
					gotAnyItem = True
					self.msgQueue.append({"msg": SHORT_ITEM_NAME[item_id], "color": FLASHING_TEXT})
				case 260: # [Yukari] Stage 2
					bothStage4 = self.options['both_stage_4']
					self.handler.addStage(1, YUKARI, bothStage4)
					gotAnyItem = True
					self.msgQueue.append({"msg": SHORT_ITEM_NAME[item_id], "color": FLASHING_TEXT})
				case 261: # [Yukari] Stage 3
					bothStage4 = self.options['both_stage_4']
					self.handler.addStage(2, YUKARI, bothStage4)
					gotAnyItem = True
					self.msgQueue.append({"msg": SHORT_ITEM_NAME[item_id], "color": FLASHING_TEXT})
				case 262: # [Yukari] Stage 4A
					bothStage4 = self.options['both_stage_4']
					self.handler.addStage(3, YUKARI, bothStage4)
					gotAnyItem = True
					self.msgQueue.append({"msg": SHORT_ITEM_NAME[item_id], "color": FLASHING_TEXT})
				case 263: # [Yukari] Stage 4B
					bothStage4 = self.options['both_stage_4']
					self.handler.addStage(4, YUKARI, bothStage4)
					gotAnyItem = True
					self.msgQueue.append({"msg": SHORT_ITEM_NAME[item_id], "color": FLASHING_TEXT})
				case 264: # [Yukari] Stage 5
					bothStage4 = self.options['both_stage_4']
					self.handler.addStage(5, YUKARI, bothStage4)
					gotAnyItem = True
					self.msgQueue.append({"msg": SHORT_ITEM_NAME[item_id], "color": FLASHING_TEXT})
				case 265: # [Yukari] Stage 6A
					bothStage4 = self.options['both_stage_4']
					self.handler.addStage(6, YUKARI, bothStage4)
					gotAnyItem = True
					self.msgQueue.append({"msg": SHORT_ITEM_NAME[item_id], "color": FLASHING_TEXT})
				case 266: # [Yukari] Stage 6B
					bothStage4 = self.options['both_stage_4']
					self.handler.addStage(7, YUKARI, bothStage4)
					gotAnyItem = True
					self.msgQueue.append({"msg": SHORT_ITEM_NAME[item_id], "color": FLASHING_TEXT})
				case 267: # [Marisa] Stage 2
					bothStage4 = self.options['both_stage_4']
					self.handler.addStage(1, MARISA, bothStage4)
					gotAnyItem = True
					self.msgQueue.append({"msg": SHORT_ITEM_NAME[item_id], "color": FLASHING_TEXT})
				case 268: # [Marisa] Stage 3
					bothStage4 = self.options['both_stage_4']
					self.handler.addStage(2, MARISA, bothStage4)
					gotAnyItem = True
					self.msgQueue.append({"msg": SHORT_ITEM_NAME[item_id], "color": FLASHING_TEXT})
				case 269: # [Marisa] Stage 4A
					bothStage4 = self.options['both_stage_4']
					self.handler.addStage(3, MARISA, bothStage4)
					gotAnyItem = True
					self.msgQueue.append({"msg": SHORT_ITEM_NAME[item_id], "color": FLASHING_TEXT})
				case 270: # [Marisa] Stage 4B
					bothStage4 = self.options['both_stage_4']
					self.handler.addStage(4, MARISA, bothStage4)
					gotAnyItem = True
					self.msgQueue.append({"msg": SHORT_ITEM_NAME[item_id], "color": FLASHING_TEXT})
				case 271: # [Marisa] Stage 5
					bothStage4 = self.options['both_stage_4']
					self.handler.addStage(5, MARISA, bothStage4)
					gotAnyItem = True
					self.msgQueue.append({"msg": SHORT_ITEM_NAME[item_id], "color": FLASHING_TEXT})
				case 272: # [Marisa] Stage 6A
					bothStage4 = self.options['both_stage_4']
					self.handler.addStage(6, MARISA, bothStage4)
					gotAnyItem = True
					self.msgQueue.append({"msg": SHORT_ITEM_NAME[item_id], "color": FLASHING_TEXT})
				case 273: # [Marisa] Stage 6B
					bothStage4 = self.options['both_stage_4']
					self.handler.addStage(7, MARISA, bothStage4)
					gotAnyItem = True
					self.msgQueue.append({"msg": SHORT_ITEM_NAME[item_id], "color": FLASHING_TEXT})
				case 274: # [Alice] Stage 2
					bothStage4 = self.options['both_stage_4']
					self.handler.addStage(1, ALICE, bothStage4)
					gotAnyItem = True
					self.msgQueue.append({"msg": SHORT_ITEM_NAME[item_id], "color": FLASHING_TEXT})
				case 275: # [Alice] Stage 3
					bothStage4 = self.options['both_stage_4']
					self.handler.addStage(2, ALICE, bothStage4)
					gotAnyItem = True
					self.msgQueue.append({"msg": SHORT_ITEM_NAME[item_id], "color": FLASHING_TEXT})
				case 276: # [Alice] Stage 4A
					bothStage4 = self.options['both_stage_4']
					self.handler.addStage(3, ALICE, bothStage4)
					gotAnyItem = True
					self.msgQueue.append({"msg": SHORT_ITEM_NAME[item_id], "color": FLASHING_TEXT})
				case 278: # [Alice] Stage 4B
					bothStage4 = self.options['both_stage_4']
					self.handler.addStage(4, ALICE, bothStage4)
					gotAnyItem = True
					self.msgQueue.append({"msg": SHORT_ITEM_NAME[item_id], "color": FLASHING_TEXT})
				case 279: # [Alice] Stage 5
					bothStage4 = self.options['both_stage_4']
					self.handler.addStage(5, ALICE, bothStage4)
					gotAnyItem = True
					self.msgQueue.append({"msg": SHORT_ITEM_NAME[item_id], "color": FLASHING_TEXT})
				case 280: # [Alice] Stage 6A
					bothStage4 = self.options['both_stage_4']
					self.handler.addStage(6, ALICE, bothStage4)
					gotAnyItem = True
					self.msgQueue.append({"msg": SHORT_ITEM_NAME[item_id], "color": FLASHING_TEXT})
				case 281: # [Alice] Stage 6B
					bothStage4 = self.options['both_stage_4']
					self.handler.addStage(7, ALICE, bothStage4)
					gotAnyItem = True
					self.msgQueue.append({"msg": SHORT_ITEM_NAME[item_id], "color": FLASHING_TEXT})
				case 282: # [Sakuya] Stage 2
					bothStage4 = self.options['both_stage_4']
					self.handler.addStage(1, SAKUYA, bothStage4)
					gotAnyItem = True
					self.msgQueue.append({"msg": SHORT_ITEM_NAME[item_id], "color": FLASHING_TEXT})
				case 283: # [Sakuya] Stage 3
					bothStage4 = self.options['both_stage_4']
					self.handler.addStage(2, SAKUYA, bothStage4)
					gotAnyItem = True
					self.msgQueue.append({"msg": SHORT_ITEM_NAME[item_id], "color": FLASHING_TEXT})
				case 284: # [Sakuya] Stage 4A
					bothStage4 = self.options['both_stage_4']
					self.handler.addStage(3, SAKUYA, bothStage4)
					gotAnyItem = True
					self.msgQueue.append({"msg": SHORT_ITEM_NAME[item_id], "color": FLASHING_TEXT})
				case 285: # [Sakuya] Stage 4B
					bothStage4 = self.options['both_stage_4']
					self.handler.addStage(4, SAKUYA, bothStage4)
					gotAnyItem = True
					self.msgQueue.append({"msg": SHORT_ITEM_NAME[item_id], "color": FLASHING_TEXT})
				case 286: # [Sakuya] Stage 5
					bothStage4 = self.options['both_stage_4']
					self.handler.addStage(5, SAKUYA, bothStage4)
					gotAnyItem = True
					self.msgQueue.append({"msg": SHORT_ITEM_NAME[item_id], "color": FLASHING_TEXT})
				case 287: # [Sakuya] Stage 6A
					bothStage4 = self.options['both_stage_4']
					self.handler.addStage(6, SAKUYA, bothStage4)
					gotAnyItem = True
					self.msgQueue.append({"msg": SHORT_ITEM_NAME[item_id], "color": FLASHING_TEXT})
				case 288: # [Sakuya] Stage 6B
					bothStage4 = self.options['both_stage_4']
					self.handler.addStage(7, SAKUYA, bothStage4)
					gotAnyItem = True
					self.msgQueue.append({"msg": SHORT_ITEM_NAME[item_id], "color": FLASHING_TEXT})
				case 289: # [Remilia] Stage 2
					bothStage4 = self.options['both_stage_4']
					self.handler.addStage(1, REMILIA, bothStage4)
					gotAnyItem = True
					self.msgQueue.append({"msg": SHORT_ITEM_NAME[item_id], "color": FLASHING_TEXT})
				case 290: # [Remilia] Stage 3
					bothStage4 = self.options['both_stage_4']
					self.handler.addStage(2, REMILIA, bothStage4)
					gotAnyItem = True
					self.msgQueue.append({"msg": SHORT_ITEM_NAME[item_id], "color": FLASHING_TEXT})
				case 291: # [Remilia] Stage 4A
					bothStage4 = self.options['both_stage_4']
					self.handler.addStage(3, REMILIA, bothStage4)
					gotAnyItem = True
					self.msgQueue.append({"msg": SHORT_ITEM_NAME[item_id], "color": FLASHING_TEXT})
				case 292: # [Remilia] Stage 4B
					bothStage4 = self.options['both_stage_4']
					self.handler.addStage(4, REMILIA, bothStage4)
					gotAnyItem = True
					self.msgQueue.append({"msg": SHORT_ITEM_NAME[item_id], "color": FLASHING_TEXT})
				case 293: # [Remilia] Stage 5
					bothStage4 = self.options['both_stage_4']
					self.handler.addStage(5, REMILIA, bothStage4)
					gotAnyItem = True
					self.msgQueue.append({"msg": SHORT_ITEM_NAME[item_id], "color": FLASHING_TEXT})
				case 294: # [Remilia] Stage 6A
					bothStage4 = self.options['both_stage_4']
					self.handler.addStage(6, REMILIA, bothStage4)
					gotAnyItem = True
					self.msgQueue.append({"msg": SHORT_ITEM_NAME[item_id], "color": FLASHING_TEXT})
				case 295: # [Remilia] Stage 6B
					bothStage4 = self.options['both_stage_4']
					self.handler.addStage(7, REMILIA, bothStage4)
					gotAnyItem = True
					self.msgQueue.append({"msg": SHORT_ITEM_NAME[item_id], "color": FLASHING_TEXT})
				case 296: # [Youmu] Stage 2
					bothStage4 = self.options['both_stage_4']
					self.handler.addStage(1, YOUMU, bothStage4)
					gotAnyItem = True
					self.msgQueue.append({"msg": SHORT_ITEM_NAME[item_id], "color": FLASHING_TEXT})
				case 297: # [Youmu] Stage 3
					bothStage4 = self.options['both_stage_4']
					self.handler.addStage(2, YOUMU, bothStage4)
					gotAnyItem = True
					self.msgQueue.append({"msg": SHORT_ITEM_NAME[item_id], "color": FLASHING_TEXT})
				case 298: # [Youmu] Stage 4A
					bothStage4 = self.options['both_stage_4']
					self.handler.addStage(3, YOUMU, bothStage4)
					gotAnyItem = True
					self.msgQueue.append({"msg": SHORT_ITEM_NAME[item_id], "color": FLASHING_TEXT})
				case 299: # [Youmu] Stage 4B
					bothStage4 = self.options['both_stage_4']
					self.handler.addStage(4, YOUMU, bothStage4)
					gotAnyItem = True
					self.msgQueue.append({"msg": SHORT_ITEM_NAME[item_id], "color": FLASHING_TEXT})
				case 2100: # [Youmu] Stage 5
					bothStage4 = self.options['both_stage_4']
					self.handler.addStage(5, YOUMU, bothStage4)
					gotAnyItem = True
					self.msgQueue.append({"msg": SHORT_ITEM_NAME[item_id], "color": FLASHING_TEXT})
				case 2101: # [Youmu] Stage 6A
					bothStage4 = self.options['both_stage_4']
					self.handler.addStage(6, YOUMU, bothStage4)
					gotAnyItem = True
					self.msgQueue.append({"msg": SHORT_ITEM_NAME[item_id], "color": FLASHING_TEXT})
				case 2102: # [Youmu] Stage 6B
					bothStage4 = self.options['both_stage_4']
					self.handler.addStage(7, YOUMU, bothStage4)
					gotAnyItem = True
					self.msgQueue.append({"msg": SHORT_ITEM_NAME[item_id], "color": FLASHING_TEXT})
				case 2103: # [Yuyuko] Stage 2
					bothStage4 = self.options['both_stage_4']
					self.handler.addStage(1, YUYUKO, bothStage4)
					gotAnyItem = True
					self.msgQueue.append({"msg": SHORT_ITEM_NAME[item_id], "color": FLASHING_TEXT})
				case 2104: # [Yuyuko] Stage 3
					bothStage4 = self.options['both_stage_4']
					self.handler.addStage(2, YUYUKO, bothStage4)
					gotAnyItem = True
					self.msgQueue.append({"msg": SHORT_ITEM_NAME[item_id], "color": FLASHING_TEXT})
				case 2105: # [Yuyuko] Stage 4A
					bothStage4 = self.options['both_stage_4']
					self.handler.addStage(3, YUYUKO, bothStage4)
					gotAnyItem = True
					self.msgQueue.append({"msg": SHORT_ITEM_NAME[item_id], "color": FLASHING_TEXT})
				case 2106: # [Yuyuko] Stage 4B
					bothStage4 = self.options['both_stage_4']
					self.handler.addStage(4, YUYUKO, bothStage4)
					gotAnyItem = True
					self.msgQueue.append({"msg": SHORT_ITEM_NAME[item_id], "color": FLASHING_TEXT})
				case 2107: # [Yuyuko] Stage 5
					bothStage4 = self.options['both_stage_4']
					self.handler.addStage(5, YUYUKO, bothStage4)
					gotAnyItem = True
					self.msgQueue.append({"msg": SHORT_ITEM_NAME[item_id], "color": FLASHING_TEXT})
				case 2108: # [Yuyuko] Stage 6A
					bothStage4 = self.options['both_stage_4']
					self.handler.addStage(6, YUYUKO, bothStage4)
					gotAnyItem = True
					self.msgQueue.append({"msg": SHORT_ITEM_NAME[item_id], "color": FLASHING_TEXT})
				case 2109: # [Yuyuko] Stage 6B
					bothStage4 = self.options['both_stage_4']
					self.handler.addStage(7, YUYUKO, bothStage4)
					gotAnyItem = True
					self.msgQueue.append({"msg": SHORT_ITEM_NAME[item_id], "color": FLASHING_TEXT})
				case 300 | 301 | 302 | 303 | 318 | 319 | 320 | 321 | 322 | 323 | 324 | 325: # Ending - Eirin
					values = {300: ILLUSION_TEAM, 301: MAGIC_TEAM, 302: DEVIL_TEAM, 303: NETHER_TEAM, 318: REIMU, 319: YUKARI, 320: MARISA, 321: ALICE, 322: SAKUYA, 323: REMILIA, 324: YOUMU, 325: YUYUKO}
					character = values[item_id]
					self.handler.addEnding(character, ENDING_FINAL_A)
					if self.checkVictory():
						await self.send_msgs([{"cmd": 'StatusUpdate', "status": 30}])
					gotAnyItem = True
					self.msgQueue.append({"msg": SHORT_ITEM_NAME[item_id], "color": FLASHING_TEXT})
				case 304 | 305 | 306 | 307 | 326 | 327 | 328 | 329 | 330 | 331 | 332 | 333: # Ending - Kaguya
					values = {304: ILLUSION_TEAM, 305: MAGIC_TEAM, 306: DEVIL_TEAM, 307: NETHER_TEAM, 326: REIMU, 327: YUKARI, 328: MARISA, 329: ALICE, 330: SAKUYA, 331: REMILIA, 332: YOUMU, 333: YUYUKO}
					character = values[item_id]
					self.handler.addEnding(character, ENDING_FINAL_B)
					if self.checkVictory():
						await self.send_msgs([{"cmd": 'StatusUpdate', "status": 30}])
					gotAnyItem = True
					self.msgQueue.append({"msg": SHORT_ITEM_NAME[item_id], "color": FLASHING_TEXT})
				case 308 | 309 | 310 | 311 | 334 | 335 | 336 | 337 | 338 | 339 | 340 | 341: # Ending - Mokou
					values = {308: ILLUSION_TEAM, 309: MAGIC_TEAM, 310: DEVIL_TEAM, 311: NETHER_TEAM, 334: REIMU, 335: YUKARI, 336: MARISA, 337: ALICE, 338: SAKUYA, 339: REMILIA, 340: YOUMU, 341: YUYUKO}
					character = values[item_id]
					self.handler.addEnding(character, ENDING_EXTRA)
					if self.checkVictory():
						await self.send_msgs([{"cmd": 'StatusUpdate', "status": 30}])
					gotAnyItem = True
					self.msgQueue.append({"msg": SHORT_ITEM_NAME[item_id], "color": FLASHING_TEXT})
				case 312 | 313 | 314 | 315 | 316: # Treasures
					self.handler.addTreasure(self.options['treasure_final_spell_card'])
					gotAnyItem = True
					self.msgQueue.append({"msg": SHORT_ITEM_NAME[item_id], "color": FLASHING_TEXT})
				case 317: # Impossible Request Completed
					if self.options['goal'] == TREASURE_GOAL:
						await self.send_msgs([{"cmd": 'StatusUpdate', "status": 30}])
					gotAnyItem = True
					self.msgQueue.append({"msg": SHORT_ITEM_NAME[item_id], "color": FLASHING_TEXT})
				case 400: # 1 Power Point
					self.handler.add1Power()
					gotAnyItem = True
					self.msgQueue.append({"msg": SHORT_ITEM_NAME[item_id], "color": FLASHING_TEXT})
				case 401: # 10 Time Point
					self.handler.addTimePoint(10)
					gotAnyItem = True
					self.msgQueue.append({"msg": SHORT_ITEM_NAME[item_id], "color": FLASHING_TEXT})
				case 402: # 50 Time Point
					self.handler.addTimePoint(50)
					gotAnyItem = True
					self.msgQueue.append({"msg": SHORT_ITEM_NAME[item_id], "color": FLASHING_TEXT})
				case 500: # -50% Power Point
					self.traps["power_point"] += 1
				case 501: # -1 Bomb
					self.traps["bomb"] += 1
				case 502: # -1 Life
					self.traps["life"] += 1
				case 503: # Reverse Movement
					self.traps["reverse_control"] = 1
				case 504: # Aya Speed
					self.traps["aya_speed"] = 1
				case 505: # Freeze
					self.traps["freeze"] += 1
				case 506: # Power Point Drain
					self.traps["power_point_drain"] = 1
				case 507: # Reverse Human Youkai Gauge
					self.traps["reverse_human_youkai_gauge"] = 1
				case 508: # Extend Time Goal
					self.traps["extend_time_goal"] += 1
				case _:
					if item_id > 6000 and item_id < 7000: # Spell Card
						spell_id = str(item_id)[1:]
						self.handler.unlockSpellCard(spell_id)
						gotAnyItem = True
						self.msgQueue.append({"msg": "SC"+spell_id, "color": FLASHING_TEXT})
					else:
						logger.error(f"Unknown Item: {item}")

		if gotAnyItem:
			self.handler.playSound(0x19)

		# Update the stage list
		self.handler.updateStageList()

	async def update_locations_checked(self):
		"""
		Check if any locations has been checked since last called, if a location has ben checked, we send a message and update our list of checked location
		"""
		new_locations = []

		for id, map in self.location_mapping.items():
			# Check if the boss is beaten and the location is not already checked
			if self.handler.isBossBeaten(*map) and id not in self.previous_location_checked:
				# We add it to the list of checked locations
				new_locations.append(id)

				if self.options['mode'] in NORMAL_MODE:
					# If we are in normal mode, the extra stage is set to linear and the stage 6 has just been cleared. We unlock it if it's not already.
					if self.options['extra_stage'] == EXTRA_LINEAR:
						if not self.handler.canExtra() and id in self.stage_specific_location_id["stage_6"]:
							self.handler.unlockExtraStage()

		# If we have new locations, we send them to the server and add them to the list of checked locations
		if new_locations:
			self.previous_location_checked = self.previous_location_checked + new_locations
			await self.send_msgs([{"cmd": 'LocationChecks', "locations": new_locations}])

	def on_deathlink(self, data):
		"""
		Method that is called when a death link is recieved.
		"""
		self.pending_death_link = True
		return super().on_deathlink(data)

	def on_ringlink(self, data):
		"""
		Method that is called when a ring link is recieved.
		"""
		game_mode = self.handler.getGameMode()
		# If we failed to get the game mode, we cancel the ring link
		if game_mode == -2:
			return

		# We check if we are in a state where we can receive a ring link
		if self.handler.gameController and game_mode == IN_GAME and not self.inError:
			# We check if it was not sent by us
			if data["source"] != self.ring_link_id:
				self.handler.playSound(0x15) if data["amount"] < 5 else self.handler.playSound(0x1F)
				self.handler.giveCurrentPowerPoint(data["amount"])
				self.last_power_point = self.handler.getCurrentPowerPoint()

	async def send_death_link(self):
		"""
		Send a death link to the server if it's active.
		"""
		if self.death_link_is_active:
			await self.send_death()

	def giveResources(self):
		"""
		Give the resources to the player
		"""
		isNormalMode = self.options['mode'] in NORMAL_MODE
		return self.handler.initResources(isNormalMode)

	def updateStageList(self):
		"""
		Update the stage list in practice mode
		"""
		mode = self.options['mode']

		if mode in PRACTICE_MODE or mode in NORMAL_MODE:
			self.handler.updateStageList(mode in PRACTICE_MODE)

		if mode in PRACTICE_MODE:
			self.handler.updatePracticeScore(self.location_mapping, self.previous_location_checked)

		if mode in SPELL_PRACTICE_MODE:
			self.handler.updateSpellPracticeAccess(self.previous_location_checked)

	def setRingLinkTag(self, active):
		if active:
			self.tags.add("RingLink")
			self.ring_link_is_active = True
		else:
			self.tags.remove("RingLink")
			self.ring_link_is_active = False
		asyncio.create_task(self.send_msgs([{"cmd": "ConnectUpdate", "tags": self.tags}]))

	def checkVictory(self):
		"""
		Check if the player has won the game.
		"""
		goal = self.options['goal']
		type = self.options['ending_required']
		extra = self.options['extra_stage']

		normal_a_victory = True
		normal_b_victory = True
		extra_victory = True

		if (goal == ENDING_FINAL_A or goal == ENDING_ALL):
			if type == ONE_ENDING:
				normal_a_victory = False
				for character in CHARACTERS:
					normal_a_victory = normal_a_victory or self.handler.endings[character][ENDING_FINAL_A]
			elif type == ALL_CHARACTER_ENDING:
				for character in CHARACTERS:
					normal_a_victory = normal_a_victory and self.handler.endings[character][ENDING_FINAL_A]

		if (goal == ENDING_FINAL_B or goal == ENDING_ALL) or (extra == NO_EXTRA and goal == ENDING_EXTRA):
			if type == ONE_ENDING:
				normal_b_victory = False
				for character in CHARACTERS:
					normal_b_victory = normal_b_victory or self.handler.endings[character][ENDING_FINAL_B]
			elif type == ALL_CHARACTER_ENDING:
				for character in CHARACTERS:
					normal_b_victory = normal_b_victory and self.handler.endings[character][ENDING_FINAL_B]

		if (goal == ENDING_EXTRA or goal == ENDING_ALL) and extra != NO_EXTRA:
			if type == ONE_ENDING:
				extra_victory = False
				for character in CHARACTERS:
					extra_victory = extra_victory or self.handler.endings[character][ENDING_EXTRA]
			elif type == ALL_CHARACTER_ENDING:
				for character in CHARACTERS:
					extra_victory = extra_victory and self.handler.endings[character][ENDING_EXTRA]

		return normal_a_victory and normal_b_victory and extra_victory

	def checkSpellCardVictory(self):
		if self.options['goal'] != CAPTURE_GOAL:
			return False

		return len(self.capture_spell_cards_list) >= self.options['capture_spell_cards_count']

	async def main_loop(self):
		"""
		Main loop that handles giving resources and updating locations.
		"""
		try:
			# If we're not plyaing in Practice or Normal mode, we leave the loop since it would do nothing
			if self.options['mode'] not in PRACTICE_MODE and self.options['mode'] not in NORMAL_MODE:
				return

			bossPresent = False
			currentMode = -1 # -1: No mode, 0: In Game, 1: In Menu
			currentLives = 0
			bossCounter = -1
			resourcesGiven = False
			noCheck = True #We start by disabling the checks since we don't know where the player would be when connecting the client
			currentScore = 0
			currentContinue = 0
			currentStage = 0
			previous_menu = 0

			while not self.exit_event.is_set() and self.handler.gameController and not self.inError:
				await asyncio.sleep(0.5)
				gameMode = self.handler.getGameMode()
				# If we failed to get the game mode, we skip the loop
				if gameMode == -2:
					continue

				# Mode Check
				if(gameMode == IN_GAME and not noCheck):
					# If we are in spell practice, we do nothing
					if previous_menu == SPELL_CARD_STAGE_SELECT:
						continue

					# A level has started
					if(currentMode != 0):
						currentMode = 0
						bossCounter = -1
						bossPresent = False
						currentScore = 0
						currentContinue = self.handler.getCurrentContinues()
						currentStage = self.handler.getCurrentStage()

						# If the current situation is technically not possible, we lock checks
						if(not self.handler.checkIfCurrentIsPossible((self.options['mode'] in NORMAL_MODE))):
							noCheck = False

					if(not resourcesGiven):
						await asyncio.sleep(0.5)
						# self.giveResources()
						resourcesGiven = True
						currentLives = self.handler.getCurrentLives()

					# We check if the current score is the same or higher than the previous one
					if(currentScore <= self.handler.getCurrentScore() or (self.options['mode'] in NORMAL_MODE and currentContinue <= self.handler.getCurrentContinues())):
						currentScore = self.handler.getCurrentScore()
						currentContinue = self.handler.getCurrentContinues()
					else:
						# If the score is lower, it mean the stage has been restarted, we end the loop and act like we just enter the stage
						currentMode = -1
						resourcesGiven = False
						continue

					# Boss Check
					nbBoss = 3 if self.options['time_check'] and self.handler.getCurrentStage() <= 6 else 2
					if(not bossPresent):
						if(self.handler.isBossPresent() and bossCounter < nbBoss-1):
							bossPresent = True
							bossCounter += 1
					else:
						if bossPresent:
							# If the boss is defeated, we update the locations
							if(not self.handler.isBossPresent()):
								if(not self.handler.isCurrentBossDefeated(bossCounter)):
									self.handler.setCurrentStageBossBeaten(bossCounter, self.check_multiple_difficulty)
									#If the stage is ending, we disable traps and reset the counter
									if bossCounter == nbBoss-1:
										self.can_trap = False
										bossCounter = -1
									await self.update_locations_checked()
								bossPresent = False

					# If we're in practice mode and a boss spawn while there is no more boss in the stage, it's not normal and we stop sending checks
					if (self.options['mode'] in PRACTICE_MODE and bossCounter > nbBoss):
						noCheck = True

					# If the stage has changed and we're in normal mode, we reset some values
					if currentStage != self.handler.getCurrentStage() and self.options['mode'] in NORMAL_MODE:
						currentStage = self.handler.getCurrentStage()
						self.can_trap = True
						bossCounter = -1

					# Death Check
					if(currentLives != self.handler.getCurrentLives()):
						# We update resources after the life has fully been lost
						if(currentLives > self.handler.getCurrentLives()):
							# We give the bombs resources
							self.handler.giveBombs()

						currentLives = self.handler.getCurrentLives()
				elif(gameMode != IN_GAME):
					# We enter in the menu
					if(currentMode != 1):
						self.handler.resetStageVariables()
						currentMode = 1
						resourcesGiven = False
						noCheck = False # We enable the checks once we're in the menu
					menu = self.handler.getMenu()
					if menu > 0 and menu < 20:
						previous_menu = menu
		except Exception as e:
			logger.error(f"Main ERROR:")
			logger.error(traceback.format_exc())
			self.inError = True

	async def menu_loop(self):
		"""
		Loop that handles the characters lock and difficulty lock, depending on the menu.
		Also handle starting item from options
		"""
		try:
			mode = self.options['mode']
			exclude_lunatic = self.options['exclude_lunatic']
			time = self.options['time']
			solo_characters = self.options['characters'] in [SOLO_ONLY, ALL_CHARACTER]

			if exclude_lunatic:
				self.difficulties -= 1
				self.handler.unlockDifficulty(self.difficulties)

			if not time:
				self.handler.unlockTimeGain()

			if solo_characters:
				self.handler.unlockSoloCharacter()

			while not self.exit_event.is_set() and self.handler.gameController and not self.inError:
				await asyncio.sleep(0.1)
				game_mode = self.handler.getGameMode()
				# If we failed to get the game mode, we skip the loop
				if game_mode == -2:
					continue

				try:
					# We force the save to act like he had already show the splash screens
					self.handler.SetSplashScreenToShown()
				except Exception as e:
						pass

				if game_mode != IN_GAME:
					menu = self.handler.getMenu()
					if menu == -1:
						continue

					# We check where we are in the menu in order to determine how we lock/unlock the characters
					if (menu == MAIN_MENU or menu in EXTRA_MENU) or self.handler.getDifficulty() == EXTRA:
						self.ExtraMenu = True
					elif (menu in NORMAL_MENU or menu in PRACTICE_MENU) or self.handler.getDifficulty() < EXTRA:
						self.ExtraMenu = False

					# If solo characters have acces to the Extra Stage
					solo_extra_access = solo_characters and menu == MAIN_MENU and self.handler.canSoloExtra()

					# If we're in the difficulty menu, we put the minimal value to the lowest difficulty
					if menu in [NORMAL_DIFFICULTY_MENU, PRACTICE_DIFFICULTY_MENU]:
						self.minimalCursor = -1
					# If we're in the main menu and we play in practice mode, we lock the access to normal mode
					elif menu == MAIN_MENU and mode not in NORMAL_MODE:
						# 1 If we have access to the extra stage, 2 if we don't
						self.minimalCursor = 1 if self.handler.canExtra() or solo_extra_access else (2 if mode in SPELL_PRACTICE_MODE else 3)
					else:
						self.minimalCursor = 0

					try:
						self.updateStageList()
						self.handler.updateExtraUnlock(not self.ExtraMenu, solo_extra_access, (menu == MAIN_MENU))
						self.handler.updateCursor(self.minimalCursor)

						if self.options['characters'] in [SOLO_ONLY, ALL_CHARACTER]:
							self.handler.forceSpellPracticeAccess(menu == MAIN_MENU)
					except Exception as e:
						pass
		except Exception as e:
			logger.error(f"Menu ERROR: {e}")
			logger.error(traceback.format_exc())
			self.inError = True

	async def trap_loop(self):
		"""
		Loop that handles traps.
		"""

		try:
			PowerPointDrain = False
			ReverseControls = False
			AyaSpeed = False
			Freeze = False
			InLevel = False
			reversedHYGauge = False
			TransitionTimer = 2
			counterTransition = 0
			freezeTimer = 2
			counterFreeze = 0
			currentScore = 0
			currentContinue = 0
			restarted = False
			while not self.exit_event.is_set() and self.handler.gameController and not self.inError:
				await asyncio.sleep(1)
				game_mode = self.handler.getGameMode()
				# If we failed to get the game mode, we skip the loop
				if game_mode == -2:
					continue

				if game_mode == IN_GAME and not restarted:
					# If we enter a level and some time has passed, we activate the traps
					if not InLevel and counterTransition < TransitionTimer:
						counterTransition += 1
					elif not InLevel:
						currentScore = 0
						currentContinue = self.handler.getCurrentContinues()
						InLevel = True
						counterTransition = 0

					# We check if the score is correct in order to know if the stage has been restarted
					if(currentScore <= self.handler.getCurrentScore() or (self.options['mode'] in NORMAL_MODE and currentContinue <= self.handler.getCurrentContinues())):
						currentScore = self.handler.getCurrentScore()
						currentContinue = self.handler.getCurrentContinues()
					else:
						restarted = True
						continue

					if InLevel and self.can_trap:
						# Checks if we need to add a new trap
						if not PowerPointDrain and self.traps['power_point_drain'] > 0:
							PowerPointDrain = True
							self.traps['power_point_drain'] -= 1
							self.msgQueue.append({"msg": SHORT_TRAP_NAME['power_point_drain'], "color": BLUE_TEXT})
							self.handler.playSound(0x1F)
						elif not ReverseControls and self.traps['reverse_control'] > 0:
							ReverseControls = True
							self.traps['reverse_control'] -= 1
							self.msgQueue.append({"msg": SHORT_TRAP_NAME['reverse_control'], "color": BLUE_TEXT})
							self.handler.playSound(0x0D)
							self.handler.reverseControls()
						elif not AyaSpeed and self.traps['aya_speed'] > 0:
							AyaSpeed = True
							self.traps['aya_speed'] -= 1
							self.msgQueue.append({"msg": SHORT_TRAP_NAME['aya_speed'], "color": BLUE_TEXT})
							self.handler.playSound(0x0D)
							self.handler.ayaSpeed()
						elif not Freeze and self.traps['freeze'] > 0:
							Freeze = True
							self.traps['freeze'] -= 1
							self.msgQueue.append({"msg": SHORT_TRAP_NAME['freeze'], "color": BLUE_TEXT})
							self.handler.playSound(0x0D)
							self.handler.freeze()
						elif self.traps['bomb'] > 0:
							self.traps['bomb'] -= 1
							self.msgQueue.append({"msg": SHORT_TRAP_NAME['bomb'], "color": BLUE_TEXT})
							self.handler.playSound(0x0E)
							self.handler.loseBomb()
						elif self.traps['life'] > 0:
							self.traps['life'] -= 1
							self.msgQueue.append({"msg": SHORT_TRAP_NAME['life'], "color": BLUE_TEXT})
							self.handler.playSound(0x04)
							self.handler.loseLife()
						elif self.traps['power_point'] > 0:
							self.traps['power_point'] -= 1
							self.msgQueue.append({"msg": SHORT_TRAP_NAME['power_point'], "color": BLUE_TEXT})
							self.handler.playSound(0x1F)
							self.handler.halfPowerPoint()
						elif not reversedHYGauge and self.traps['reverse_human_youkai_gauge'] > 0:
							self.traps['reverse_human_youkai_gauge'] -= 1
							self.msgQueue.append({"msg": SHORT_TRAP_NAME['reverse_human_youkai_gauge'], "color": BLUE_TEXT})
							self.handler.playSound(0x0D)
							self.handler.setHumanYoukaiGauge(False)
							reversedHYGauge = True
						elif self.traps['extend_time_goal'] > 0:
							self.traps['extend_time_goal'] -= 1
							self.msgQueue.append({"msg": SHORT_TRAP_NAME['extend_time_goal'], "color": BLUE_TEXT})
							self.handler.playSound(0x0D)
							self.handler.extendTimeGoal()

						# Power Point Drain apply each loop until the player dies or the level is exited
						if PowerPointDrain:
							self.handler.powerPointDrain()

						# Freeze apply each loop until the timer is done
						if Freeze:
							if counterFreeze < freezeTimer:
								counterFreeze += 1
							else:
								Freeze = False
								counterFreeze = 0
								self.handler.resetSpeed()
				else:
					if reversedHYGauge:
						self.handler.setHumanYoukaiGauge(True)

					InLevel = False
					PowerPointDrain = False
					ReverseControls = False
					AyaSpeed = False
					Freeze = False
					reversedHYGauge = False
					counterTransition = 0
					counterFreeze = 0
					self.can_trap = True
					restarted = False
					currentScore = 0
		except Exception as e:
			logger.error(f"Trap ERROR: {e}")
			logger.error(traceback.format_exc())
			self.inError = True

	async def death_link_loop(self):
		"""
		Loop that handles death link.
		"""
		try:
			self.pending_death_link = False
			onGoingDeathLink = False
			inLevel = False
			currentMisses = 0
			nb_death = 0
			previous_menu = 0

			while not self.exit_event.is_set() and self.handler.gameController and not self.inError:
				if(self.death_link_is_active):
					await asyncio.sleep(0.5)
				else:
					await asyncio.sleep(2)
					inLevel = False
					continue
				game_mode = self.handler.getGameMode()
				# If we failed to retrieve the game mode, we skip the loop
				if game_mode == -2:
					continue

				if game_mode == IN_GAME:
					# If we enter a level, we set the variables
					if not inLevel:
						inLevel = True
						currentMisses = self.handler.getMisses()
						onGoingDeathLink = False
						self.pending_death_link = False

					# If a death link is sent, we set the flag
					if self.pending_death_link and not onGoingDeathLink:
						onGoingDeathLink = True

					# If we're in Spell Practice, we check if the Player State is 3, if it is, we remove the potential on going death link
					if onGoingDeathLink and previous_menu == SPELL_CARD_STAGE_SELECT and self.handler.getPlayerState() == 3:
						onGoingDeathLink = False
						self.pending_death_link = False

					# If a misses has been added, that mean the player has been killed and we check if it was because of the death link
					# (Receiving a death link is checked by misses as it's more reliable and the player could have deathbomb the death link)
					if currentMisses < self.handler.getMisses():
						# If the player is killed by a death link, we tell the loop it's done
						if onGoingDeathLink:
							onGoingDeathLink = False
							self.pending_death_link = False
						else:
							if self.death_link_trigger == DEATH_LINK_LIFE or (self.death_link_trigger == DEATH_LINK_GAME_OVER and self.handler.getCurrentLives() == 0):
								nb_death += 1
								if nb_death >= self.death_link_amnesty:
									await self.send_death_link()
									nb_death = 0
								else:
									logger.info(f"DeathLink: {nb_death}/{self.death_link_amnesty}")

						currentMisses += 1
					# If no death has occured but a death link is pending, we try to kill the player
					elif self.pending_death_link:
						await self.handler.killPlayer()
				else:
					menu = self.handler.getMenu()
					if menu > 0 and menu < 20:
						previous_menu = menu
					inLevel = False
		except Exception as e:
			logger.error(f"DeathLink ERROR: {e}")
			logger.error(traceback.format_exc())
			self.inError = True

	async def message_loop(self):
		"""
		Loop that handles displaying message
		"""
		try:
			while not self.exit_event.is_set() and self.handler.gameController and not self.inError:
				if self.msgQueue != []:
					msg = self.msgQueue[0]
					self.msgQueue.pop(0)
					task = asyncio.create_task(self.handler.displayMessage(msg['msg'], msg['color']))
					await asyncio.wait([task])
				else:
					await asyncio.sleep(0.1)
		except Exception as e:
			logger.error(f"Message ERROR: {e}")
			logger.error(traceback.format_exc())
			self.inError = True

	async def ring_link_loop(self):
		"""
		Loop that handles Ring Link
		"""
		try:
			self.last_power_point = -1
			self.ring_link_id = random.randint(0, 999999)
			self.timer = 0.5

			while not self.exit_event.is_set() and self.handler.gameController and not self.inError:
				if(self.ring_link_is_active):
					await asyncio.sleep(self.timer)
				else:
					await asyncio.sleep(2)
					self.last_power_point = -1
					continue
				game_mode = self.handler.getGameMode()
				# If we failed to retrieve the game mode, we skip the loop
				if game_mode == -2:
					continue

				if game_mode == IN_GAME:
					# We wait a little before sending ring link
					self.timer = 0.1
					curent_power = self.handler.getCurrentPowerPoint()

					# If last_power_point is -1, that mean it's the first loop, so we just wait a little and then set it
					if self.last_power_point == -1:
						await asyncio.sleep(1)
						self.last_power_point = curent_power
						continue

					# If the power point has changed, we send a ring link
					if self.last_power_point != curent_power:
						diff_power = curent_power-self.last_power_point
						self.last_power_point = curent_power
						asyncio.create_task(self.send_msgs([{"cmd": "Bounce", "tags": ["RingLink"], "data": {"amount": diff_power, "source": self.ring_link_id, "time": time.time()}}]))
				else:
					self.last_power_point = -1
					self.timer = 0.5
		except Exception as e:
			logger.error(f"RingLink ERROR: {e}")
			logger.error(traceback.format_exc())
			self.inError = True

	async def guard_rail_loop(self):
		"""
		Loop that handles the guard rail
		"""
		mode = self.options['mode']
		guard_rail = GuardRail(self.handler.gameController, self.handler, self.options)
		while not self.exit_event.is_set() and self.handler.gameController and not self.inError:
			try:
				await asyncio.sleep(5)
				result = guard_rail.check_memory_addresses()
				if result["error"]:
					logger.error(f"Memory ERROR: {result['message']}")

				if self.handler.getGameMode() != IN_GAME:
					result = guard_rail.check_cursor_state()
					if result["error"]:
						logger.error(f"Cursor State ERROR: {result['message']}")

					result = guard_rail.check_menu_lock()
					if result["error"]:
						logger.error(f"Menu Lock ERROR: {result['message']}")

					if mode in SPELL_PRACTICE_MODE:
						result = guard_rail.check_spell_cards()
						if result["error"]:
							logger.error(f"Spell Card ERROR: {result['message']}")
			except Exception as e:
				logger.error(f"GuardRail ERROR: {e}")
				logger.error(traceback.format_exc())

	async def spell_card_loop(self):
		"""
		Loop that handles spell cards
		"""
		try:
			# If we're not playing in spell practice, we leave the loop since it would do nothing
			if self.options['mode'] not in SPELL_PRACTICE_MODE:
				return

			self.handler.setSpellCardsTeams(self.options['spell_cards_teams'])

			while not self.exit_event.is_set() and self.handler.gameController and not self.inError:
				await asyncio.sleep(1)
				spell_card_acquired = self.handler.getSpellCardAcquired()
				spell_card_acquired_in_game = self.handler.getCurrentSpellCardAcquired()
				new_spell_cards = []
				for id, spell in spell_card_acquired.items():
					for character in CHARACTERS:
						if spell[character] != spell_card_acquired_in_game[id][character]:
							self.handler.setSpellCardAcquired(id, character)
							if spell[character]:
								item_id = STARTING_ID + int("6"+str(character)+id)
								new_spell_cards.append(item_id)

								# If we're in capture goal, we add the spell card to the list if it's not already present and it's valid spell card
								if self.options['goal'] == CAPTURE_GOAL and id not in self.capture_spell_cards_list:
									if id in self.options['capture_spell_cards_list']:
										self.capture_spell_cards_list.append(id)

				if new_spell_cards:
					await self.send_msgs([{"cmd": 'LocationChecks', "locations": new_spell_cards}])

				if self.options['goal'] == CAPTURE_GOAL and self.checkSpellCardVictory() and not self.victory_sent:
					await self.send_msgs([{"cmd": 'StatusUpdate', "status": 30}])
					self.victory_sent = True

		except Exception as e:
			logger.error(f"SpellCard ERROR: {e}")
			logger.error(traceback.format_exc())
			self.inError = True

	async def connect_to_game(self):
		"""
		Connect the client to the game process
		"""
		self.handler = None

		while not self.handler:
			try:
				self.handler = gameHandler()
			except Exception as e:
				await asyncio.sleep(2)

	async def reconnect_to_game(self):
		"""
		Reconnect to client to the game process without resetting everything
		"""
		self.handler.gameController = None

		while not self.handler.gameController:
			try:
				self.handler.reconnect()
			except Exception as e:
				await asyncio.sleep(2)

async def game_watcher(ctx: TouhouContext):
	"""
	Client loop, watching the game process.
	Start the different loops once connected that will handle the game.
	It will also attempt to reconnect if the connection to the game is lost.

	:TouhouContext ctx: The client context instance.
	"""

	await ctx.wait_for_initial_connection_info()

	while not ctx.exit_event.is_set():
		if not ctx.server:
			# client disconnected from server
			await ctx.wait_for_initial_connection_info()

		# First connection
		if ctx.handler is None and not ctx.inError:
			logger.info(f"Waiting for connection to {SHORT_NAME}...")
			asyncio.create_task(ctx.connect_to_game())
			while(ctx.handler is None and not ctx.exit_event.is_set()):
				await asyncio.sleep(1)

		# Connection following an error
		if ctx.inError:
			logger.info(f"Connection lost. Waiting for connection to {SHORT_NAME}...")
			asyncio.create_task(ctx.reconnect_to_game())
			await asyncio.sleep(1)
			while(ctx.handler.gameController is None and not ctx.exit_event.is_set()):
				await asyncio.sleep(1)

		if ctx.handler and ctx.handler.gameController:
			ctx.inError = False
			logger.info(f"{SHORT_NAME} process found. Starting loop...")

			# We start all the diffrent loops
			asyncio.create_task(ctx.main_loop())
			asyncio.create_task(ctx.menu_loop())
			asyncio.create_task(ctx.trap_loop())
			asyncio.create_task(ctx.message_loop())
			asyncio.create_task(ctx.guard_rail_loop())
			asyncio.create_task(ctx.death_link_loop())
			asyncio.create_task(ctx.ring_link_loop())
			asyncio.create_task(ctx.spell_card_loop())

			# We update the locations checked if there was any location that was already checked before the connection
			await ctx.update_locations_checked()
			ctx.updateStageList()

			# Activating Death Link / Ring Link if needed
			if ctx.options['death_link']:
				await ctx.update_death_link(True)
				ctx.death_link_is_active = True

			if ctx.options['death_link_amnesty']:
				ctx.death_link_amnesty = ctx.options['death_link_amnesty']

			if ctx.options['death_link_trigger']:
				ctx.death_link_trigger = ctx.options['death_link_trigger']

			if ctx.options['ring_link']:
				ctx.setRingLinkTag(True)

			# We set the limits for lives and bombs
			ctx.handler.setLivesLimit(ctx.options['limit_lives'])
			ctx.handler.setBombsLimit(ctx.options['limit_bombs'])

			# Infinite loop while there is no error. If there is an error, we exit this loop in order to restart the connection
			while not ctx.exit_event.is_set() and not ctx.inError:
				await asyncio.sleep(1)

def launch():
	"""
	Launch a client instance (wrapper / args parser)
	"""
	async def main(args):
		"""
		Launch a client instance (threaded)
		"""
		ctx = TouhouContext(args.connect, args.password)
		ctx.server_task = asyncio.create_task(server_loop(ctx))
		if gui_enabled:
			ctx.run_gui()
		ctx.run_cli()
		watcher = asyncio.create_task(
			game_watcher(ctx),
			name="GameProgressionWatcher"
		)
		await ctx.exit_event.wait()
		await watcher
		await ctx.shutdown()

	parser = get_base_parser(description=SHORT_NAME+" Client")
	args, _ = parser.parse_known_args()

	colorama.init()
	asyncio.run(main(args))
	colorama.deinit()