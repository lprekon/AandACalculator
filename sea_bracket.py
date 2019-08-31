import argparse
import os

INFANTRY = 0
ARTILLERY = 1
TANK = 2
FIGHTER = 3
BOMBER = 4

NUM_UNIT_TYPES = 5

STATS = {}
STATS[SUBMARINE] = {"name":"SUBMARINE", "attack":2, "defense":1, "cost":6}
STATS[DESTROYER] = {"name":"DESTROYER", "attack":2, "defense":2, "cost":8}
STATS[CRUISER] = {"name":"CRUISER", "attack":3, "defense":3, "cost":12}
STATS[FIGHTER] = {"name":"FIGHTER", "attack":3, "defense":4, "cost":10}
STATS[CARRIER] = {"name":"CARRIER", "attack":1, "defense":2, "cost":14}
STATS[BATTLESHIP] = {"name":"CARRIER", "attack":4, "defense":4, "cost":20}

class Army:
	def __init__(self, infantry = 0, artillery = 0, tank = 0, fighter = 0, bomber = 0):
		self.total = [0 for i in range(NUM_UNIT_TYPES)]
		self.total[INFANTRY] = infantry
		self.total[ARTILLERY] = artillery
		self.total[TANK] = tank
		self.total[FIGHTER] = fighter
		self.total[BOMBER] = bomber		

		self.cost = STATS[INFANTRY]["cost"] * self.total[INFANTRY] + STATS[ARTILLERY]["cost"] * self.total[ARTILLERY] + self.total[TANK] * STATS[TANK]["cost"] + \
		 self.total[FIGHTER] * STATS[FIGHTER]["cost"] + self.total[BOMBER] * STATS[BOMBER]["cost"]
		
		
	def score_army(self, rounds = 10, wounds_per_round = 1):
		self.rounds = rounds
		self.wounds_per_round = wounds_per_round
		if(self.cost > 0):
			self.atk_card = self.calculate_hits(attack=True)
			self.atk_score = sum(self.atk_card) / self.cost
			self.def_card = self.calculate_hits(attack=False)
			self.def_score = sum(self.def_card) / self.cost
		else:
			self.atk_card = []
			self.atk_score = 0
			self.def_card = []
			self.def_score = 0

	def calculate_hits(self, attack=True):
		#setup
		self.active = [0 for i in range(NUM_UNIT_TYPES)]
		self.active[INFANTRY] = self.total[INFANTRY]
		self.active[ARTILLERY] = self.total[ARTILLERY]
		self.active[TANK] = self.total[TANK]
		self.active[FIGHTER] = self.total[FIGHTER]
		self.active[BOMBER] = self.total[BOMBER]
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
			counter = [self.active[INFANTRY], self.active[ARTILLERY]]
			if(attack):
				while counter[INFANTRY] > 0 and counter[ARTILLERY] > 0:
					round_hits[INFANTRY] += 1
					counter[INFANTRY] -= 1
					counter[ARTILLERY] -= 1
			expected_hits[i] = sum(round_hits) / 6.0
			if any((x < 0 for x in expected_hits)):
				print("ERROR: negative expected hits. Dumping...")
				print("total: " + str(self.total))
				print("active: " + str(self.active))
				print("power: " + str(power))
				print("expected_hits: " + str(expected_hits))
				print("round: " + str(i))
				print("round_hits: " + str(round_hits))
				assert(False)
			
			#take wounds
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
					return expected_hits
		return expected_hits

	def __str__(self):
		return "INFANTRY\t" + str(self.total[INFANTRY]) + "\n" +\
		 "ARTILLERY\t" + str(self.total[ARTILLERY]) + "\n" +\
		 "TANK\t\t" + str(self.total[TANK]) + "\n" +\
		 "FIGHTER\t\t" + str(self.total[FIGHTER]) + "\n" +\
		 "BOMBER\t\t" + str(self.total[BOMBER]) + "\n" +\
		 "COST\t\t" + str(self.cost) + "\n" +\
		 "ATK\t\t" + str(self.atk_score)+ "\n" +\
		 "DEF\t\t" + str(self.def_score) + "\n" +\
		 "RNDS\t\t" + str(self.rounds) + "\n" +\
		 "WNDS\t\t" + str(self.wounds_per_round) + "\n" +\
		 "ATKCARD\t" + str(self.atk_card) + "\n" +\
		 "DEFCARD\t" + str(self.def_card) + "\n"


def generate_ground_roster(roster, max_value = 40):
	order_of_battle = [0 for i in range(NUM_UNIT_TYPES)]
	muster = Army(*order_of_battle) # make an empty army
	while muster.cost <= max_value: # bombers
		while muster.cost <= max_value: #fighters
			while muster.cost <= max_value: #tanks:
				while muster.cost <= max_value: #artillery
					while muster.cost <= max_value: #infantry
						roster.append(muster)
						order_of_battle[INFANTRY] += 1
						muster = Army(*order_of_battle)
					#Too many infantry. Reset and add arillery
					order_of_battle[INFANTRY] = 0
					order_of_battle[ARTILLERY] += 1
					muster = Army(*order_of_battle)
				#Too many artillery. Reset and add tank
				order_of_battle[INFANTRY] = 0
				order_of_battle[ARTILLERY] = 0
				order_of_battle[TANK] += 1
				muster = Army(*order_of_battle)
			#Too many tank. Reset and add fighter
			order_of_battle[INFANTRY] = 0
			order_of_battle[ARTILLERY] = 0
			order_of_battle[TANK] = 0
			order_of_battle[FIGHTER] += 1
			muster = Army(*order_of_battle)
		#Too many fighter. Reset and add bomber
		order_of_battle[INFANTRY] = 0
		order_of_battle[ARTILLERY] = 0
		order_of_battle[TANK] = 0
		order_of_battle[FIGHTER] = 0
		order_of_battle[BOMBER] += 1
		muster = Army(*order_of_battle)

def score_roster(roster, rounds, wounds = 1):
	for army in roster:
		army.score_army(rounds = rounds, wounds_per_round = wounds)

#roster is passed in rather than returned to keep large rosters off the stack (not *certain* how that would work in python, but better safe than sorry)
def run_simulation(roster, rounds, costs, wounds = 1):
	generate_ground_roster(roster, max_value = costs)
	score_roster(roster, rounds=rounds, wounds = wounds)

def write_overview(rounds, costs, wounds, overview_file_prefix = "overview_matrix", atk_file_name = "overview_attack.txt", def_file_name = "overview_defense.txt"):
	column_headers = ["{:^20}".format(c) for c in costs]
	row_headers = ["{:>2}".format(r) for r in rounds]
	attackers_matrix = "  "
	defenders_matrix = "  "
	for c in column_headers:
		attackers_matrix += c
		defenders_matrix += c
	attackers_matrix += "\n\n"
	defenders_matrix += "\n\n"
	atk_file = open(atk_file_name, 'w')
	def_file = open(def_file_name, 'w')
	for r in rounds:
		attackers_matrix += row_headers[r - 1]
		defenders_matrix += row_headers[r - 1]
		for c in costs:
			roster = []
			run_simulation(roster=roster, rounds=r, costs=c, wounds = wounds)
			attackers_ranked = sorted(roster, key = lambda x: x.atk_score, reverse = True)
			defenders_ranked = sorted(roster, key = lambda x: x.def_score, reverse = True)
			best_attacker = attackers_ranked[0]
			best_defender = defenders_ranked[0]
			atk_file.write("ROUND:{:>2}\tCOST:{:>2}\n".format(r, c))
			atk_file.write(str(best_defender) + "\n\n")
			def_file.write("ROUND:{:>2}\tCOST:{:>2}\n".format(r, c))
			def_file.write(str(best_defender) + "\n\n")
			attackers_matrix += "   I{:0>2}A{:0>2}T{:0>2}F{:0>2}B{:0>2}  ".format(*(best_attacker.total))
			defenders_matrix += "   I{:0>2}A{:0>2}T{:0>2}F{:0>2}B{:0>2}  ".format(*(best_defender.total))
		attackers_matrix += "\n\n"
		defenders_matrix += "\n\n"
	atk_file.close()
	def_file.close()
	overview_file_name = "{}.txt".format(overview_file_prefix)
	overview_file = open(overview_file_name, 'w')
	overview_file.write("{:^122}\n".format("Best Attackers - WOUNDS " + str(wounds)))
	overview_file.write("Round{:<55}Cost\n".format(""))
	overview_file.write(attackers_matrix)
	overview_file.write("\n\n")
	overview_file.write("{:^122}\n".format("Best Defenders - WOUNDS " + str(wounds)))
	overview_file.write("Round{:<55}Cost\n".format(""))
	overview_file.write(defenders_matrix)
	overview_file.close()

def write_report(rounds, costs, wounds, atk_file_prefix = "attack", def_file_prefix = "defend", entries_per_log=20):
	for r in rounds:
		for c in costs:
			roster = []
			run_simulation(roster=roster, rounds=r, wounds=wounds, costs=c)
			attackers_ranked = sorted(roster, key = lambda x: x.atk_score, reverse = True)
			defenders_ranked = sorted(roster, key = lambda x: x.def_score, reverse = True)
			with open("{}_Rounds-{:0>2}_Cost-{:0>2}.txt".format(atk_file_prefix, r, c), 'w') as atk_file, open("{}_Rounds-{:0>2}_Cost-{:0>2}.txt".format(def_file_prefix, r, c), 'w') as def_file:
				for i in range(min(entries_per_log, len(roster))):
					atk_file.write(str(attackers_ranked[i]) + "\n")
					def_file.write(str(defenders_ranked[i]) + "\n")



def main():
	rounds = [i for i in range(1, 11)]
	costs = [i for i in range (5, 45, 5)]
	wounds = 2
	#simulation_directory = "overview_RND" +  "{:0>2}".format(str(rounds[0])) + "-" + "{:0>2}".format(str(rounds[-1])) + "_COSTS" + "{:0>2}".format(str(costs[0])) + "-" + "{:0>2}".format(str(costs[-1])) + "-" + "{:0>2}".format(str(costs[1] - costs[0]))
	simulation_directory = "simulation_RND{:0>2}-{:0>2}_COSTS{:0>2}-{:0>2}-{:0>2}_WOUNDS{:0>2}".format(rounds[0], rounds[-1], costs[0], costs[-1], (costs[1] - costs[0]), wounds)
	if not os.path.isdir(simulation_directory):
		os.mkdir(simulation_directory)
	os.chdir(simulation_directory)
	write_overview(rounds, costs, wounds)

	if not os.path.isdir("detailed_reports"):
		os.mkdir("detailed_reports")
	os.chdir("detailed_reports")
	write_report(rounds, costs, wounds)
	

if __name__ == '__main__':
	main()