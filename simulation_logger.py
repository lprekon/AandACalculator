def simulation_logger(sim_step):
	def wrapper(*args, **kwargs):
		print("[*] Executing {}\nargs: {}\nkwargs: {}".format(sim_step.__name__, args, kwargs))
		sim_step(*args, **kwargs)
