import argparse
import os
from simulation_logger import simulation_logger
import Army

		 
def generate_ground_roster(roster, max_value = 40):
	order_of_battle = [0 for i in range(Army.NUM_UNIT_TYPES)]
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

def score_roster(roster, rounds, wounds = 1):
	for army in roster:
		army.score_army(rounds = rounds, wounds_per_round = wounds)

#roster is passed in rather than returned to keep large rosters off the stack (not *certain* how that would work in python, but better safe than sorry)

def run_simulation(roster, rounds, costs, wounds = 1):
	generate_ground_roster(roster, max_value = costs)
	score_roster(roster, rounds=rounds, wounds = wounds)

@simulation_logger
def write_overview(rounds, costs, wounds, overview_file_prefix = "overview_matrix", atk_file_name = "overview_attack.txt", def_file_name = "overview_defense.txt", overall_file_name = "overview_overall.txt"):
	column_headers = ["{:^20}".format(c) for c in costs]
	row_headers = ["{:>2}".format(r) for r in rounds]
	attackers_matrix = "  "
	defenders_matrix = "  "
	overall_matrix = "  "
	for c in column_headers:
		attackers_matrix += c
		defenders_matrix += c
		overall_matrix += c
	attackers_matrix += "\n\n"
	defenders_matrix += "\n\n"
	overall_matrix += "\n\n"
	with open(atk_file_name, 'w') as atk_file, open(def_file_name, 'w') as def_file, open(overall_file_name, 'w') as ova_file:
		for r in rounds:
			attackers_matrix += row_headers[r - 1]
			defenders_matrix += row_headers[r - 1]
			overall_matrix += row_headers[r - 1]
			for c in costs:
				roster = []
				run_simulation(roster=roster, rounds=r, costs=c, wounds = wounds)
				attackers_ranked = sorted(roster, key = lambda x: x.atk_score, reverse = True)
				defenders_ranked = sorted(roster, key = lambda x: x.def_score, reverse = True)
				overall_ranked = sorted(roster, key = lambda x: x.atk_score + x.def_score, reverse = True)
				best_attacker = attackers_ranked[0]
				best_defender = defenders_ranked[0]
				best_overall = overall_ranked[0]
				atk_file.write("ROUND:{:>2}\tCOST:{:>2}\n".format(r, c))
				atk_file.write(str(best_attacker) + "\n\n")
				def_file.write("ROUND:{:>2}\tCOST:{:>2}\n".format(r, c))
				def_file.write(str(best_defender) + "\n\n")
				ova_file.write("ROUND:{:>2}\tCOST:{:>2}\n".format(r, c))
				ova_file.write(str(best_overall) + "\n\n")
				attackers_matrix += "   I{:0>2}A{:0>2}T{:0>2}F{:0>2}B{:0>2}  ".format(*(best_attacker.total))
				defenders_matrix += "   I{:0>2}A{:0>2}T{:0>2}F{:0>2}B{:0>2}  ".format(*(best_defender.total))
				overall_matrix += "   I{:0>2}A{:0>2}T{:0>2}F{:0>2}B{:0>2}  ".format(*(best_overall.total))
			attackers_matrix += "\n\n"
			defenders_matrix += "\n\n"
			overall_matrix += "\n\n"
		
	overview_file_name = "{}.txt".format(overview_file_prefix)
	overview_file = open(overview_file_name, 'w')
	overview_file.write("{:^122}\n".format("Best Attackers - WOUNDS " + str(wounds)))
	overview_file.write("Round{:<55}Cost\n".format(""))
	overview_file.write(attackers_matrix)
	overview_file.write("\n\n")
	overview_file.write("{:^122}\n".format("Best Defenders - WOUNDS " + str(wounds)))
	overview_file.write("Round{:<55}Cost\n".format(""))
	overview_file.write(defenders_matrix)
	overview_file.write("\n\n")
	overview_file.write("{:^122}\n".format("Best Overall - WOUNDS " + str(wounds)))
	overview_file.write("Round{:<55}Cost\n".format(""))
	overview_file.write(overall_matrix)
	overview_file.close()

def write_report(rounds, costs, wounds, atk_file_prefix = "attack", def_file_prefix = "defend", entries_per_log=20):
	for r in rounds:
		for c in costs:
			roster = []
			run_simulation(roster=roster, rounds=r, wounds=wounds, costs=c)
			attackers_ranked = sorted(roster, key = lambda x: x.atk_score*1000 + sum(x.atk_card), reverse = True)
			defenders_ranked = sorted(roster, key = lambda x: x.def_score*1000 + sum(x.def_card), reverse = True)
			with open("{}_Rounds-{:0>2}_Cost-{:0>2}.txt".format(atk_file_prefix, r, c), 'w') as atk_file, open("{}_Rounds-{:0>2}_Cost-{:0>2}.txt".format(def_file_prefix, r, c), 'w') as def_file:
				for i in range(min(entries_per_log, len(roster))):
					atk_file.write(str(attackers_ranked[i]) + "\n")
					def_file.write(str(defenders_ranked[i]) + "\n")



def main():
	rounds = [i for i in range(1, 11)]
	costs = [i for i in range (5, 45, 5)]
	start_path = os.getcwd()
	for wounds in range (1, 6):
		#simulation_directory = "overview_Army.RND" +  "{:0>2}".format(str(rounds[0])) + "-" + "{:0>2}".format(str(rounds[-1])) + "_COSTS" + "{:0>2}".format(str(costs[0])) + "-" + "{:0>2}".format(str(costs[-1])) + "-" + "{:0>2}".format(str(costs[1] - costs[0]))
		simulation_directory = "simulation_Army.RND{:0>2}-{:0>2}_COSTS{:0>2}-{:0>2}-{:0>2}_WOUNDS{:0>2}".format(rounds[0], rounds[-1], costs[0], costs[-1], (costs[1] - costs[0]), wounds)
		if not os.path.isdir(simulation_directory):
			os.mkdir(simulation_directory)
		os.chdir(simulation_directory)
		write_overview(rounds = rounds, costs = costs, wounds = wounds)

		if not os.path.isdir("detailed_reports"):
			os.mkdir("detailed_reports")
		os.chdir("detailed_reports")
		write_report(rounds, costs, wounds)
		os.chdir(start_path)
	

if __name__ == '__main__':
	main()