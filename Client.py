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
	get_base_parser,
	logger,
	server_loop,
	gui_enabled,
)

class TouhouContext(CommonContext):
	"""Touhou Game Context"""
	def __init__(self, server_address: Optional[str], password: Optional[str]) -> None:
		super().__init__(server_address, password)
		self.game = DISPLAY_NAME
		self.items_handling = 0b111  # Item from starting inventory, own world and other world
		self.pending_death_link = False

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

		# Counter
		self.difficulties = 3
		self.traps = {"power_point_drain": 0, "reverse_control": 0, "aya_speed": 0, "freeze": 0, "bomb": 0, "life": 0, "power_point": 0}
		self.can_trap = True

		self.options = None
		self.otherDifficulties = False
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
			self.otherDifficulties = self.options['difficulty_check'] == DIFFICULTY_WITH_LOWER
			self.location_mapping, self.stage_specific_location_id = getLocationMapping(self.options['difficulty_check'] in DIFFICULTY_CHECK)

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
				case 3: # 1 Continue
					self.handler.addContinue()
					gotAnyItem = True
					self.msgQueue.append({"msg": SHORT_ITEM_NAME[item_id], "color": FLASHING_TEXT})
				case 4: # 25 Power Point
					self.handler.add25Power()
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
					if isExtraStageApart or (self.options['mode'] == PRACTICE_MODE and not self.options['progressive_stage']):
						self.handler.unlockExtraStage()
						gotAnyItem = True
						self.msgQueue.append({"msg": SHORT_ITEM_NAME[item_id], "color": FLASHING_TEXT})
				case 206: # [Illusion] Extra Stage
					isExtraStageApart = self.options['extra_stage'] == EXTRA_APART
					if isExtraStageApart or (self.options['mode'] == PRACTICE_MODE and not self.options['progressive_stage']):
						self.handler.unlockExtraStage(ILLUSION_TEAM)
						gotAnyItem = True
						self.msgQueue.append({"msg": SHORT_ITEM_NAME[item_id], "color": FLASHING_TEXT})
				case 207: # [Magic] Extra Stage
					isExtraStageApart = self.options['extra_stage'] == EXTRA_APART
					if isExtraStageApart or (self.options['mode'] == PRACTICE_MODE and not self.options['progressive_stage']):
						self.handler.unlockExtraStage(MAGIC_TEAM)
						gotAnyItem = True
						self.msgQueue.append({"msg": SHORT_ITEM_NAME[item_id], "color": FLASHING_TEXT})
				case 208: # [Devil] Extra Stage
					isExtraStageApart = self.options['extra_stage'] == EXTRA_APART
					if isExtraStageApart or (self.options['mode'] == PRACTICE_MODE and not self.options['progressive_stage']):
						self.handler.unlockExtraStage(DEVIL_TEAM)
						gotAnyItem = True
						self.msgQueue.append({"msg": SHORT_ITEM_NAME[item_id], "color": FLASHING_TEXT})
				case 209: # [Nether] Extra Stage
					isExtraStageApart = self.options['extra_stage'] == EXTRA_APART
					if isExtraStageApart or (self.options['mode'] == PRACTICE_MODE and not self.options['progressive_stage']):
						self.handler.unlockExtraStage(NETHER_TEAM)
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
				case 300 | 301 | 302 | 303: # Ending - Eirin
					character = ILLUSION_TEAM if item_id == 300 else (MAGIC_TEAM if item_id == 301 else (DEVIL_TEAM if item_id == 302 else NETHER_TEAM))
					self.handler.addEnding(character, ENDING_FINAL_A)
					if self.checkVictory():
						await self.send_msgs([{"cmd": 'StatusUpdate', "status": 30}])
					gotAnyItem = True
					self.msgQueue.append({"msg": SHORT_ITEM_NAME[item_id], "color": FLASHING_TEXT})
				case 304 | 305 | 306 | 307: # Ending - Kaguya
					character = ILLUSION_TEAM if item_id == 304 else (MAGIC_TEAM if item_id == 305 else (DEVIL_TEAM if item_id == 306 else NETHER_TEAM))
					self.handler.addEnding(character, ENDING_FINAL_B)
					if self.checkVictory():
						await self.send_msgs([{"cmd": 'StatusUpdate', "status": 30}])
					gotAnyItem = True
					self.msgQueue.append({"msg": SHORT_ITEM_NAME[item_id], "color": FLASHING_TEXT})
				case 308 | 309 | 310 | 311: # Ending - Mokou
					character = ILLUSION_TEAM if item_id == 308 else (MAGIC_TEAM if item_id == 309 else (DEVIL_TEAM if item_id == 310 else NETHER_TEAM))
					self.handler.addEnding(character, ENDING_EXTRA)
					if self.checkVictory():
						await self.send_msgs([{"cmd": 'StatusUpdate', "status": 30}])
					gotAnyItem = True
					self.msgQueue.append({"msg": SHORT_ITEM_NAME[item_id], "color": FLASHING_TEXT})
				case 400: # 1 Power Point
					self.handler.add1Power()
					gotAnyItem = True
					self.msgQueue.append({"msg": SHORT_ITEM_NAME[item_id], "color": FLASHING_TEXT})
				case 500: # -50% Power Point
					self.traps["power_point"] += 1
				case 501: # -1 Bomb
					self.traps["bomb"] += 1
				case 502: # -1 Life
					self.traps["life"] += 1
				case 503: # Reverse Movement
					self.traps["reverse_control"] += 1
				case 504: # Aya Speed
					self.traps["aya_speed"] += 1
				case 505: # Freeze
					self.traps["freeze"] += 1
				case 506: # Power Point Drain
					self.traps["power_point_drain"] += 1
				case _:
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
		if self.options['death_link']:
			await self.send_death()

	def giveResources(self):
		"""
		Give the resources to the player
		"""
		isNormalMode = self.options['mode'] == NORMAL_STATIC_MODE
		return self.handler.initResources(isNormalMode)

	def updateStageList(self):
		"""
		Update the stage list in practice mode
		"""
		mode = self.options['mode']

		self.handler.updateStageList(mode == PRACTICE_MODE)
		self.handler.updatePracticeScore(self.location_mapping, self.previous_location_checked)

	def addRingLinkTag(self):
		self.tags.add("RingLink")
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

	async def main_loop(self):
		"""
		Main loop that handles giving resources and updating locations.
		"""
		try:
			bossPresent = False
			currentMode = -1 # -1: No mode, 0: In Game, 1: In Menu
			currentLives = 0
			bossCounter = -1
			resourcesGiven = False
			noCheck = True #We start by disabling the checks since we don't know where the player would be when connecting the client
			currentScore = 0
			currentContinue = 0
			while not self.exit_event.is_set() and self.handler.gameController and not self.inError:
				await asyncio.sleep(0.5)
				gameMode = self.handler.getGameMode()
				# If we failed to get the game mode, we skip the loop
				if gameMode == -2:
					continue

				# Mode Check
				if(gameMode == IN_GAME and not noCheck):
					# A level has started
					if(currentMode != 0):
						currentMode = 0
						bossCounter = -1
						bossPresent = False
						currentScore = 0
						currentContinue = self.handler.getCurrentContinues()

						# If the current situation is technically not possible, we lock checks
						if(not self.handler.checkIfCurrentIsPossible((self.options['mode'] in NORMAL_MODE))):
							noCheck = False

					if(not resourcesGiven):
						await asyncio.sleep(0.5)
						self.giveResources()
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
					nbBoss = 2
					if(not bossPresent):
						if(self.handler.isBossPresent()):
							bossPresent = True
							bossCounter += 1
					else:
						if bossPresent:
							# If the boss is defeated, we update the locations
							if(not self.handler.isBossPresent()):
								if(not self.handler.isCurrentBossDefeated(bossCounter)):
									#If the stage is ending, we disable traps and reset the counter
									if bossCounter == nbBoss-1:
										self.can_trap = False
										bossCounter = -1
									self.handler.setCurrentStageBossBeaten(bossCounter, self.otherDifficulties)
									await self.update_locations_checked()
								bossPresent = False

					# If we're in practice mode and a boss spawn while there is no more boss in the stage, it's not normal and we stop sending checks
					if (self.options['mode'] == PRACTICE_MODE and bossCounter > nbBoss):
						noCheck = True

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
					self.updateStageList()
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

			if exclude_lunatic:
				self.difficulties -= 1
				self.handler.unlockDifficulty(self.difficulties)

			while not self.exit_event.is_set() and self.handler.gameController and not self.inError:
				await asyncio.sleep(0.1)
				game_mode = self.handler.getGameMode()
				# If we failed to get the game mode, we skip the loop
				if game_mode == -2:
					continue

				if game_mode != IN_GAME:
					menu = self.handler.getMenu()
					if menu == -1:
						continue

					# We check where we are in the menu in order to determine how we lock/unlock the characters
					if (menu == MAIN_MENU or menu in EXTRA_MENU) or self.handler.getDifficulty() == EXTRA:
						self.ExtraMenu = True
					elif (menu in NORMAL_MENU or menu in PRACTICE_MENU) or self.handler.getDifficulty() < EXTRA:
						self.ExtraMenu = False

					# If we're in the difficulty menu, we put the minimal value to the lowest difficulty
					if menu in [NORMAL_DIFFICULTY_MENU, PRACTICE_DIFFICULTY_MENU]:
						self.minimalCursor = -1
					# If we're in the main menu and we play in practice mode, we lock the access to normal mode
					elif menu == MAIN_MENU and mode == PRACTICE_MODE:
						# 1 If we have access to the extra stage, 2 if we don't
						self.minimalCursor = 1 if self.handler.canExtra() else 3
					else:
						self.minimalCursor = 0

					try:
						self.handler.updateExtraUnlock(not self.ExtraMenu)
						self.handler.updateCursor(self.minimalCursor)
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
			NoFocus = False
			ReverseControls = False
			AyaSpeed = False
			Freeze = False
			InLevel = False
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
					if NoFocus:
						self.handler.canFocus(True)

					InLevel = False
					PowerPointDrain = False
					NoFocus = False
					ReverseControls = False
					AyaSpeed = False
					Freeze = False
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

			while not self.exit_event.is_set() and self.handler.gameController and not self.inError:
				await asyncio.sleep(0.5)
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

					# If a misses has been added, that mean the player has been killed and we check if it was because of the death link
					# (Receiving a death link is checked by misses as it's more reliable and the player could have deathbomb the death link)
					if currentMisses < self.handler.getMisses():
						# If the player is killed by a death link, we tell the loop it's done
						if onGoingDeathLink:
							onGoingDeathLink = False
							self.pending_death_link = False
						else:
							await self.send_death_link()

						currentMisses += 1
					# If no death has occured but a death link is pending, we try to kill the player
					elif self.pending_death_link:
						await self.handler.killPlayer()
				else:
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
				await asyncio.sleep(self.timer)
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
		guard_rail = GuardRail(self.handler.gameController, self.handler)
		while not self.exit_event.is_set() and self.handler.gameController and not self.inError:
			try:
				await asyncio.sleep(2)
				result = guard_rail.check_memory_addresses()
				if result["error"]:
					logger.error(f"Memory ERROR: {result['message']}")

				result = guard_rail.check_cursor_state()
				if result["error"]:
					logger.error(f"Cursor State ERROR: {result['message']}")

				result = guard_rail.check_menu_lock()
				if result["error"]:
					logger.error(f"Menu Lock ERROR: {result['message']}")
			except Exception as e:
				logger.error(f"GuardRail ERROR: {e}")
				logger.error(traceback.format_exc())

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

			# We update the locations checked if there was any location that was already checked before the connection
			await ctx.update_locations_checked()
			ctx.updateStageList()

			# Activating Death Link and its loop
			if ctx.options['death_link']:
				await ctx.update_death_link(True)
				asyncio.create_task(ctx.death_link_loop())

			if ctx.options['ring_link']:
				ctx.addRingLinkTag()
				asyncio.create_task(ctx.ring_link_loop())

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