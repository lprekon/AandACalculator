INFANTRY = 0
ARTILLERY = 1
TANK = 2
FIGHTER = 3
BOMBER = 4


STATS = {}
STATS[INFANTRY] = {"name":"INFANTRY", "attack":1, "defense":2, "cost":3}
STATS[ARTILLERY] = {"name":"ARTILLERY", "attack":2, "defense":2, "cost":4}
STATS[TANK] = {"name":"TANK", "attack":3, "defense":3, "cost":5}
STATS[FIGHTER] = {"name":"FIGHTER", "attack":3, "defense":4, "cost":10}
STATS[BOMBER] = {"name":"BOMBER", "attack":4, "defense":1, "cost":12}

NUM_UNIT_TYPES = len(STATS)

class Army:
	def __init__(self, infantry = 0, artillery = 0, tank = 0, fighter = 0, bomber = 0):
		self.total = [0 for i in range(NUM_UNIT_TYPES)]
		self.total[INFANTRY] = infantry
		self.total[ARTILLERY] = artillery
		self.total[TANK] = tank
		self.total[FIGHTER] = fighter
		self.total[BOMBER] = bomber		

		self.cost = sum((self.total[x] * STATS[x]["cost"] for x in range(NUM_UNIT_TYPES)))

		self.atk_score = 0
		self.def_score = 0
		self.atk_card = []
		self.def_card = []
		self.rounds = 0
		self.wounds_per_round = 0
		
		
	def score_army(self, rounds = 10, wounds_per_round = 1):
		self.rounds = rounds
		self.wounds_per_round = wounds_per_round
		if(self.cost > 0):
			self.atk_card = self.simulate_combat(attack=True)
			self.atk_score = sum(self.atk_card) / self.cost
			self.def_card = self.simulate_combat(attack=False)
			self.def_score = sum(self.def_card) / self.cost

	def simulate_combat(self, attack=True):
		#setup
		self.active = self.total.copy()
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

	def take_wounds(self, attack):
		for w in range(self.wounds_per_round):
				if(not attack and self.active[BOMBER] > 0):
					self.active[BOMBER] -= 1
				elif(self.active[INFANTRY] > 0):
					self.active[INFANTRY] -= 1
				elif (self.active[ARTILLERY] > 0):
					self.active[ARTILLERY] -= 1
				elif (self.active[TANK] > 0):
					self.active[TANK] -= 1
				elif (attack and self.active[FIGHTER] > 0):
					self.active[FIGHTER] -= 1
				elif (not attack and self.active[FIGHTER] > 0):
					self.active[FIGHTER] -= 1
				elif (attack and self.active[BOMBER] > 0):
					self.active[BOMBER] -= 1
				else:
					# if we ever have no more troops left to fight, then the fight is done and we return
					assert(not any(self.active)) # we should have no troops
					return False
		return True

	def calculate_hits(self, attack, power):
		round_hits = [0 for j in range(NUM_UNIT_TYPES)]
		for j in range(NUM_UNIT_TYPES):
			round_hits[j] = self.active[j] * power[j]
		counter = [self.active[INFANTRY], self.active[ARTILLERY]]
		if(attack):
			while counter[INFANTRY] > 0 and counter[ARTILLERY] > 0:
				round_hits[INFANTRY] += 1
				counter[INFANTRY] -= 1
				counter[ARTILLERY] -= 1
		return sum(round_hits)

	def __str__(self):
		val = ""
		for i in range(NUM_UNIT_TYPES):
			val += "{:<15} {}\n".format(STATS[i]["name"], self.total[i])

		val += "COST\t\t" + str(self.cost) + "\n" +\
		 "ATK\t\t" + str(self.atk_score)+ "\n" +\
		 "DEF\t\t" + str(self.def_score) + "\n" +\
		 "RNDS\t\t" + str(self.rounds) + "\n" +\
		 "WNDS\t\t" + str(self.wounds_per_round) + "\n" +\
		 "ATKCARD\t" + str(self.atk_card) + "\n" +\
		 "DEFCARD\t" + str(self.def_card) + "\n"
		
		return val