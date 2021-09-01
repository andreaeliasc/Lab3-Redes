
import json

"""
	Constants to execute the program
"""

hello = 'HELLO'
echo_send = "ECHO SEND"
echo_response = "ECHO RESPONSE"
message_type= "MESSAGE"
lsp = 'LSP'

"""
	Receives a json-like string and turns it into an object

	Arguments:
		json_string -- json-like string
"""
def json_to_object(jason_string):
    object = json.loads(jason_string)
    return object


"""
	Receives an object and turns it into a json-like string

	Arguments:
		object -- an object
"""
def object_to_json(object):
    json_string = json.dumps(object)
    return json_string

"""
	Receives the ID in the topology and returns the JID on the server

	Arguments:
		names_file -- the filename of the file with the name-node associations
		ID -- The ID in the topology
"""
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

"""
	Receives the JID from the server and returns the ID in the topology

	Arguments:
		names_file -- the filename of the file with the name-node associations
		JID -- The JID in the server
"""
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
		raise Exception('The file has not a valid format for names')


"""
	Returns a list of the neighbors of a given node

	Arguments:
		topology_file -- the filename of the file with the node-node
		JID -- JID -- The JID in the server
"""
def get_neighbors(topology_file, ID):
	file = open(topology_file, "r")
	file = file.read()
	info = eval(file)
	if(info["type"]=="topo"):
		names = info["config"]
		neighbors_IDs = names[ID]
		return(neighbors_IDs)
	else:
		raise Exception('The file has not a valid format for topology')
	return  