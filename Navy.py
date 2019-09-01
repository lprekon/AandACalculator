import argparse
import os
import ground_bracket

SUBMARINE = 0
DESTROYER = 1
CRUISER = 2
FIGHTER = 3
CARRIER = 4
BATTLESHIP = 5

NUM_UNIT_TYPES = 6

STATS = {}
STATS[SUBMARINE] = {"name":"SUBMARINE", "attack":2, "defense":1, "cost":6}
STATS[DESTROYER] = {"name":"DESTROYER", "attack":2, "defense":2, "cost":8}
STATS[CRUISER] = {"name":"CRUISER", "attack":3, "defense":3, "cost":12}
STATS[FIGHTER] = {"name":"FIGHTER", "attack":3, "defense":4, "cost":10}
STATS[CARRIER] = {"name":"CARRIER", "attack":1, "defense":2, "cost":14}
STATS[BATTLESHIP] = {"name":"CARRIER", "attack":4, "defense":4, "cost":20}

class Navy(ground_bracket.Army):

	def __init__(self, submarine = 0, destroyer = 0, cruiser = 0, fighter = 0, carrier = 0, battleship = 0):
		self.total = [0 for i in range(NUM_UNIT_TYPES)]
		self.total[SUBMARINE] = submarine
		self.total[DESTROYER] = destroyer
		self.total[CRUISER] = cruiser
		self.total[FIGHTER] = fighter
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
		#setup
		self.active = [0 for i in range(NUM_UNIT_TYPES)]
		self.active[SUBMARINE] = self.total[SUBMARINE]
		self.active[DESTROYER] = self.total[DESTROYER]
		self.active[CRUISER] = self.total[CRUISER]
		self.active[FIGHTER] = self.total[FIGHTER]
		self.active[CARRIER] = self.total[CARRIER]
		self.active[BATTLESHIP] = self.total[BATTLESHIP]
		power = [0 for i in range(NUM_UNIT_TYPES)]
		for i in range(NUM_UNIT_TYPES):
			power[i] = (STATS[i]["attack"] if attack else STATS[i]["defense"])
		expected_hits = [0 for i in range(self.rounds)]
		assert(all((x>=0 for x in expected_hits)))
		
		#run simulation
		for i in range (self.rounds):
			#calculate hits
			round_hits = [0 for j in range(NUM_UNIT_TYPES)]
			for j in range(NUM_UNIT_TYPES):
				round_hits[j] = self.active[j] * power[j]
			counter = [self.active[SUBMARINE], self.active[DESTROYER]]
			if(attack):
				while counter[SUBMARINE] > 0 and counter[DESTROYER] > 0:
					round_hits[SUBMARINE] += 1
					counter[SUBMARINE] -= 1
					counter[DESTROYER] -= 1
			expected_hits[i] = sum(round_hits) / 6.0
			if any((x < 0 for x in expected_hits)):
				print("ERROR: negative expected hits. Dumping...")
				print("total: " + str(self.total))
				print("self.active: " + str(self.active))
				print("power: " + str(power))
				print("expected_hits: " + str(expected_hits))
				print("round: " + str(i))
				print("round_hits: " + str(round_hits))
				assert(False)
			
			#take wounds
			for w in range(self.wounds_per_round):
				if(not attack and self.active[CARRIER] > 0):
					self.active[CARRIER] -= 1
				elif(self.active[SUBMARINE] > 0):
					self.active[SUBMARINE] -= 1
				elif (self.active[DESTROYER] > 0):
					self.active[DESTROYER] -= 1
				elif (self.active[CRUISER] > 0):
					self.active[CRUISER] -= 1
				elif (attack and self.active[FIGHTER] > 0):
					self.active[FIGHTER] -= 1
				elif (not attack and self.active[FIGHTER] > 0):
					self.active[FIGHTER] -= 1
				elif (attack and self.active[CARRIER] > 0):
					self.active[CARRIER] -= 1
				else:
					# if we ever have no more troops left to fight, then the fight is done and we return
					assert(not any(self.active)) # we should have no troops
					return expected_hits
		return expected_hits



def generate_ground_roster(roster, max_value = 40):
	order_of_battle = [0 for i in range(NUM_UNIT_TYPES)]
	muster = Army(*order_of_battle) # make an empty army
	while muster.cost <= max_value: # carriers
		while muster.cost <= max_value: #fighters
			while muster.cost <= max_value: #cruisers:
				while muster.cost <= max_value: #destroyer
					while muster.cost <= max_value: #submarine
						roster.append(muster)
						order_of_battle[SUBMARINE] += 1
						muster = Army(*order_of_battle)
					#Too many submarine. Reset and add arillery
					order_of_battle[SUBMARINE] = 0
					order_of_battle[DESTROYER] += 1
					muster = Army(*order_of_battle)
				#Too many destroyer. Reset and add cruiser
				order_of_battle[SUBMARINE] = 0
				order_of_battle[DESTROYER] = 0
				order_of_battle[CRUISER] += 1
				muster = Army(*order_of_battle)
			#Too many cruiser. Reset and add fighter
			order_of_battle[SUBMARINE] = 0
			order_of_battle[DESTROYER] = 0
			order_of_battle[CRUISER] = 0
			order_of_battle[FIGHTER] += 1
			muster = Army(*order_of_battle)
		#Too many fighter. Reset and add carrier
		order_of_battle[SUBMARINE] = 0
		order_of_battle[DESTROYER] = 0
		order_of_battle[CRUISER] = 0
		order_of_battle[FIGHTER] = 0
		order_of_battle[CARRIER] += 1
		muster = Army(*order_of_battle)
