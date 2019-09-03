import argparse
import os
import ground_bracket

SUBMARINE = 0
DESTROYER = 1
CRUISER = 2
FIGHTER = 3
BOMBER = 4
CARRIER = 5
BATTLESHIP = 6



STATS = {}
STATS[SUBMARINE] = {"name":"SUBMARINE", "attack":2, "defense":1, "cost":6}
STATS[DESTROYER] = {"name":"DESTROYER", "attack":2, "defense":2, "cost":8}
STATS[CRUISER] = {"name":"CRUISER", "attack":3, "defense":3, "cost":12}
STATS[FIGHTER] = {"name":"FIGHTER", "attack":3, "defense":4, "cost":10}
STATS[BOMBER] = {"name":"BOMBER", "attack":4, "defense":1, "cost":12}
STATS[CARRIER] = {"name":"CARRIER", "attack":1, "defense":2, "cost":14}
STATS[BATTLESHIP] = {"name":"BATTLESHIP", "attack":4, "defense":4, "cost":20}

NUM_UNIT_TYPES = len(STATS)

class Navy(ground_bracket.Army):

	#fighters represent fighters from nearby land
	def __init__(self, submarine = 0, destroyer = 0, cruiser = 0, fighter = 0, bomber = 0, carrier = 0, battleship = 0):
		self.total = [0 for i in range(NUM_UNIT_TYPES)]
		self.total[SUBMARINE] = submarine
		self.total[DESTROYER] = destroyer
		self.total[CRUISER] = cruiser
		self.total[FIGHTER] = fighter
		self.total[BOMBER] = bomber
		self.total[CARRIER] = carrier
		self.total[BATTLESHIP] = battleship		

		self.cost = sum((self.total[x] * STATS[x]["cost"] for x in range(NUM_UNIT_TYPES)))
		
		self.atk_score = 0
		self.def_score = 0
		self.atk_card = []
		self.def_card = []
		self.rounds = 0
		self.wounds_per_round = 0

	def simulate_combat(self, attack=True):
		self.wounds_absorbed_by_battleships = 0
		self.active = self.total.copy()
		#If we have more fighters than we could have on defense, reduce fighter count to max possible
		#Invalid counts will have a higher cost, and thus be sorted below valid counts
		if not attack:
			self.active[FIGHTER] = min(self.active[FIGHTER], self.active[CARRIER] * 2)
		power = [STATS[i]["attack"] if attack else STATS[i]["defense"] for i in range(NUM_UNIT_TYPES)]
		expected_hits = [0 for i in range(self.rounds)]
		assert(all((x>=0 for x in expected_hits)))
		
		#run simulation
		for i in range (self.rounds):
			#calculate hits
			expected_hits[i] = self.calculate_hits(power = power, attack = attack) / 6.0
			#take wounds
			if not self.take_wounds(attack):
				return expected_hits # if take_wounds returned false, we're out of the fight
			
		return expected_hits

	def calculate_hits_extra(self, attack, power):
		return 0

	def take_wounds(self, attack):
		for w in range(self.wounds_per_round):
			if self.wounds_absorbed_by_battleships < self.active[BATTLESHIP]:
				self.wounds_absorbed_by_battleships += 1
			else if not attack and self.active[SUBMARINE] > 0:
				self.active[SUBMARINE] -= 1
			else if not attack and self.active[BOMBER] > 0:
				self.active[BOMBER] -= 1
			else if attack and self.active[CARRIER] > 0 and self.active[CARRIER]*2 > self.active[FIGHTER]:
				self.active[CARRIER] -= 1
			else if self.active[SUBMARINE] > 0:
				self.active[SUBMARINE] -= 1
			else if self.active[DESTROYER] > 0:
				self.active[DESTROYER] -= 1
			else if not attack and self.active[CARRIER] > 0 and self.active[CARRIER]*2 > self.active[FIGHTER]:
				self.active[CARRIER] -= 1
			else if self.active[CRUISER] > 0:
				self.active[CRUISER] -=1
			else if self.active[FIGHTER] > 0: #fighter on defense is order just after fighter on attack, so no point checking atk/def
				self.active[FIGHTER] -= 1
			else if attack and self.active[BOMBER] > 0: #checking for atk included for clarity
				self.active[BOMBER] -= 1
			else if self.active[BATTLESHIP] > 0:
				self.active[BATTLESHIP] -= 1
			else:
				return False
		return True
