import argparse
import os
from simulation_logger import *
import Army
import Navy

		 
def generate_ground_roster(max_value = 40):
	order_of_battle = [0 for i in range(Army.NUM_UNIT_TYPES)]
	roster = []
	muster = Army.Army(*order_of_battle) # make an empty army
	while muster.cost <= max_value: # bombers
		while muster.cost <= max_value: #fighters
			while muster.cost <= max_value: #tanks:
				while muster.cost <= max_value: #artillery
					while muster.cost <= max_value: #infantry
						roster.append(muster)
						order_of_battle[Army.INFANTRY] += 1
						muster = Army.Army(*order_of_battle)
					#Too many infantry. Reset and add arillery
					order_of_battle[Army.INFANTRY] = 0
					order_of_battle[Army.ARTILLERY] += 1
					muster = Army.Army(*order_of_battle)
				#Too many artillery. Reset and add tank
				order_of_battle[Army.INFANTRY] = 0
				order_of_battle[Army.ARTILLERY] = 0
				order_of_battle[Army.TANK] += 1
				muster = Army.Army(*order_of_battle)
			#Too many tank. Reset and add fighter
			order_of_battle[Army.INFANTRY] = 0
			order_of_battle[Army.ARTILLERY] = 0
			order_of_battle[Army.TANK] = 0
			order_of_battle[Army.FIGHTER] += 1
			muster = Army.Army(*order_of_battle)
		#Too many fighter. Reset and add bomber
		order_of_battle[Army.INFANTRY] = 0
		order_of_battle[Army.ARTILLERY] = 0
		order_of_battle[Army.TANK] = 0
		order_of_battle[Army.FIGHTER] = 0
		order_of_battle[Army.BOMBER] += 1
		muster = Army.Army(*order_of_battle)
	return roster

def generate_sea_roster(max_value = 40):
	order_of_battle = [0 for i in range(Navy.NUM_UNIT_TYPES)]
	roster = []
	muster = Navy.Navy(*order_of_battle) # make an empty navy
	while muster.cost < max_value: #Battleships
		while muster.cost < max_value: #Carrier
			while muster.cost < max_value: #Bomber
				while muster.cost < max_value: #Fighter
					while muster.cost < max_value: #Cruiser
						while muster.cost < max_value: #Destroyer
							while muster.cost < max_value: #Submarine
								roster.append(muster)
								order_of_battle[Navy.SUBMARINE] += 1
								muster = Navy.Navy(*order_of_battle)
							#Too many submarine. Reset and add destroyer
							order_of_battle[Navy.SUBMARINE] = 0
							order_of_battle[Navy.DESTROYER] += 1
							muster = Navy.Navy(*order_of_battle)
						#Too many destroyer. Reset and add Cruiser
						order_of_battle[Navy.DESTROYER] = 0
						order_of_battle[Navy.CRUISER] += 1
						muster = Navy.Navy(*order_of_battle)
					#Too many cruiser. Reset and add fighter
					order_of_battle[Navy.CRUISER] = 0
					order_of_battle[Navy.FIGHTER] += 1
					muster = Navy.Navy(*order_of_battle)
				#Too many fighter. Reset and add bomber
				order_of_battle[Navy.FIGHTER] = 0
				order_of_battle[Navy.BOMBER] += 1
				muster = Navy.Navy(*order_of_battle)
			#Too many bomber. Reset and add Carrier
			order_of_battle[Navy.BOMBER] = 0
			order_of_battle[Navy.CARRIER] += 1
			muster = Navy.Navy(*order_of_battle)
		#Too many carrier. Reset and add battleship
		order_of_battle[Navy.CARRIER] = 0
		order_of_battle[Navy.BATTLESHIP] += 1
		muster = Navy.Navy(*order_of_battle)
	return roster

def score_roster(roster, rounds, wounds = 1):
	for army in roster:
		army.score_self(rounds = rounds, wounds_per_round = wounds) #army will simulate combat on offense and defense


#run_simulation only gets a single wound value because different wound values are considered different simulations
@simulation_logger
def run_simulation(round_list, cost_list, wounds, roster_generator):
	super_roster = {}
	for r in round_list:
		super_roster[r] = {}
		for c in cost_list:
			super_roster[r][c] = roster_generator(max_value = c)
			score_roster(super_roster[r][c], rounds=r, wounds = wounds)
	assert super_roster != None
	return super_roster


def write_overview(super_roster, round_list, cost_list, wounds, overview_file, atk_file, def_file, ova_file):
	for mode in ["ova", "atk", "def"]:
		matrix = create_matrix(super_roster, round_list, cost_list, wounds, mode = mode, string_generator = generate_ground_string)
		overview_file.write(matrix + "\n")
	for r in round_list:
		for c in cost_list:
			header_string = "{:<16}{}\n".format("ROUND:{:>2}".format(r), "COST:{:>2}\n".format(c))
			atk_file.write(header_string)
			def_file.write(header_string)
			ova_file.write(header_string)
			atk_file.write(str(sorted(super_roster[r][c], key = lambda x: x.sorting_key(mode = "atk"), reverse = True)[0]))
			def_file.write(str(sorted(super_roster[r][c], key = lambda x: x.sorting_key(mode = "def"), reverse = True)[0]))
			ova_file.write(str(sorted(super_roster[r][c], key = lambda x: x.sorting_key(mode = "ova"), reverse = True)[0]))


def create_matrix(super_roster, round_list, cost_list, wounds, mode = "ova", string_generator = lambda x: x.__str__()):
	assert(super_roster != None)
	COLUMN_WIDTH = 20
	column_headers = [("{:^" + str(COLUMN_WIDTH) + "}").format(c) for c in cost_list]
	row_headers = ["{:>2}".format(r) for r in round_list]
	title = "Attackers" if mode == "atk" else "Defenders" if mode == "def" else "Overall"
	matrix = "{:^122}\n".format("Best {} - WOUNDS {:0>2}".format(title, wounds))
	for c in column_headers:
		matrix += c
	matrix += "\n\n"
	for i in range(len(round_list)):
		matrix += row_headers[i]
		for c in cost_list:
			roster = super_roster[round_list[i]][c]
			sorted_roster = sorted(roster, key = lambda x: x.sorting_key(mode), reverse = True)
			best = sorted_roster[0]
			matrix += string_generator(best, COLUMN_WIDTH)
		matrix += "\n\n"
	return matrix

def generate_ground_string(army, column_width):
	return ("{:^" + str(column_width) + "}").format("I{:0>2}A{:0>2}T{:0>2}F{:0>2}B{:0>2}".format(*(army.total)))

def generate_sea_string(navy, column_width):
	return ("{:^" + str(column_width) + "}").format("S{:0>2}D{:0>2}Cr{:0>2}F{:0>2}Bo{:0>2}Ca{:0>2}Ba{:0>2}".format(*navy.total))



def write_report(super_roster, round_list, cost_list, atk_file_prefix = "attack", def_file_prefix = "defend", ova_file_prefix = "overall", entries_per_log=20):
	for r in round_list:
		for c in cost_list:
			attackers_ranked = sorted(super_roster[r][c], key = lambda x: x.sorting_key("atk"), reverse = True)[:entries_per_log]
			defenders_ranked = sorted(super_roster[r][c], key = lambda x: x.sorting_key("def"), reverse = True)[:entries_per_log]
			overall_ranked = sorted(super_roster[r][c], key = lambda x: x.sorting_key("ova"), reverse = True)[:entries_per_log]
			round_cost_info = "Rounds-{:0>2}_Cost-{:0>2}".format(r, c)
			with open("{}_{}.txt".format(atk_file_prefix, round_cost_info), 'w') as atk_file,\
			 open("{}_{}.txt".format(def_file_prefix, round_cost_info), 'w') as def_file, \
			 open("{}_{}.txt".format(ova_file_prefix, round_cost_info), 'w') as ova_file:
				for i in range(len(attackers_ranked)):
					atk_file.write(str(attackers_ranked[i]) + "\n")
					def_file.write(str(defenders_ranked[i]) + "\n")
					ova_file.write(str(overall_ranked[i]) + "\n")
				



def main():
	round_list = [i for i in range(1, 11)]
	cost_list = [i for i in range (5, 45, 5)]
	start_path = os.getcwd()
	for wounds in range (1, 6):
		#Army
		super_roster = run_simulation(round_list=round_list, cost_list=cost_list, wounds=wounds, roster_generator = generate_ground_roster)
		assert super_roster != None
		simulation_directory = "simulation_Army.RND{:0>2}-{:0>2}_COSTS{:0>2}-{:0>2}-{:0>2}_WOUNDS{:0>2}".format(round_list[0], round_list[-1], cost_list[0], cost_list[-1], (cost_list[1] - cost_list[0]), wounds)
		if not os.path.isdir(simulation_directory):
			os.mkdir(simulation_directory)
		os.chdir(simulation_directory)
		log_simulation(super_roster, round_list, cost_list, wounds)
		os.chdir(start_path)

		#Navy
		super_roster = run_simulation(round_list=round_list, cost_list=cost_list, wounds=wounds, roster_generator = generate_ground_roster)
		simulation_directory = "simulation_Navy.RND{:0>2}-{:0>2}_COSTS{:0>2}-{:0>2}-{:0>2}_WOUNDS{:0>2}".format(round_list[0], round_list[-1], cost_list[0], cost_list[-1], (cost_list[1] - cost_list[0]), wounds)
		if not os.path.isdir(simulation_directory):
			os.mkdir(simulation_directory)
		os.chdir(simulation_directory)
		log_simulation(super_roster, round_list, cost_list, wounds)
		os.chdir(start_path)

def log_simulation(super_roster, round_list, cost_list, wounds):
	with open("overview_matrix.txt", 'w') as overview_file, \
		 open("overview_attack.txt", 'w') as atk_file,\
		 open("overview_defense.txt", 'w') as def_file,\
		 open("overview_overall.txt", 'w') as ova_file:
			write_overview(super_roster=super_roster, round_list=round_list, cost_list=cost_list, wounds=wounds, overview_file=overview_file, atk_file=atk_file, def_file=def_file, ova_file=ova_file)

		if not os.path.isdir("detailed_reports"):
			os.mkdir("detailed_reports")
		os.chdir("detailed_reports")
		write_report(super_roster = super_roster, round_list = round_list, cost_list =cost_list)

if __name__ == '__main__':
	main()