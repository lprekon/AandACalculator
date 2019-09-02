def simulation_logger(sim_step):
	def wrapper(*args, **kwargs):
		print("[*] Executing {}\nargs: {}\nkwargs: {}".format(sim_step.__name__, args, kwargs))
		val = sim_step(*args, **kwargs)
		print("[+] Complete")
		return val
	return wrapper
