def simulation_logger(sim_step):
	def wrapper(*args, **kwargs):
		print("[*] Executing {}\nargs: {}\nkwargs: {}".format(sim_step.__name__, args, kwargs))
		val = sim_step(*args, **kwargs)
		print("[+] Complete")
		return val
	return wrapper

def return_logger(sim_step):
	def wrapper(*args, **kwargs):
		print("[*] Executing {}\n".format(sim_step.__name__))
		val = sim_step(*args, **kwargs)
		print("[+] Completeed with value: {}\n".format(val) )
		return val
	return wrapper

def string_generator_logger(sim_step):
	def wrapper(unit, width):
		print("[*] calling {} for unit {}".format(sim_step.__name__, unit.total))
		val = sim_step(unit, width)
		print("[*] completed with " + val)
		return val
	return wrapper