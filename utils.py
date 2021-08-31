import json
import time

last_id = None

def get_JID(names_file,ID):
	file = open(names_file, "r")
	file = file.read()
	info = eval(file)
	if(info["type"]=="names"):
		names = info["config"]
		JID = names[ID]
		return(JID)
	else:
		raise Exception('The file does not have a valid format for names')

def get_ID(names_file, JID):
	file = open(names_file, "r")
	file = file.read()
	info = eval(file)
	if(info["type"]=="names"):
		names = info["config"]
		JIDS = {v: k for k, v in names.items()}
		name = JIDS[JID]
		return(name)
	else:
		raise Exception('The file does not have a valid format for names')


def get_neighbors(topology_file, names_file, JID):
	ID = get_ID(names_file, JID)
	file = open(topology_file, "r")
	file = file.read()
	info = eval(file)
	if(info["type"]=="topology"):
		names = info["config"]
		neighbors_IDs = names[ID]
		neighbors_JIDs = [get_JID(names_file,i) for i in neighbors_IDs]
		return(neighbors_JIDs)
	else:
		raise Exception('The file has not a valid format for topology')
	return  

def calculate(message, sender, names_file, topology_file):
	start_time = time.time()
	info = eval(message)
	info["Jumps"] = info["Jumps"] + 1
	nodes = get_neighbors(topology_file, names_file, sender)
	info["List_of_Nodes"] = [info["List_of_Nodes"], nodes]
	info["Distance"] = info["Distance"] - start_time + time.time()
	return (nodes, json.dumps(info))