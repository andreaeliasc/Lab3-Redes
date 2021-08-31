import getpass
from optparse import OptionParser
import yaml
import networkx as nx
from client import Client
from aioconsole import ainput

def loadConfig():
    lector_topo = open("topology.txt", "r", encoding="utf8")
    lector_names = open("names.txt", "r", encoding="utf8")
    topo_string = lector_topo.read()
    names_string = lector_names.read()
    topo_yaml = yaml.load(topo_string, Loader=yaml.FullLoader)
    names_yaml = yaml.load(names_string, Loader=yaml.FullLoader)
    return topo_yaml, names_yaml

def getNodes(topo, names, user):
    for key, value in names["config"].items():
        if user == value:
            return key, topo["config"][key]

def getGraph(topo, names, user):
    '''Build graph in python a dict'''
    
    graph = {}
    source = None

    for key, value in topo['config'].items():
        graph[key] = {}
        for node in value:
            graph[key][node] = float('inf')
            if names['config'][node] == user:
                source = node
    
    return graph, source


def pruebaGrafo(topo, names):
    G = nx.DiGraph()
    G.add_nodes_from(G.nodes(data=True))
    G.add_edges_from(G.edges(data=True))
    for key, value in names["config"].items():
        G.add_node(key, jid=value)
        
    for key, value in topo["config"].items():
        for i in value:
            G.add_edge(key, i, weight=1)
    
    return G
    
async def main(xmpp: Client):
    corriendo = True
    while corriendo:
        print("""
        Welcome to the chat!

        0. Message
        1. Exit
        """)
        opcion = await ainput("Type an option: ")
        if opcion == '0':
            destinatario = await ainput("Type the recipient's JID:  ")
            activo = True
            while activo:
                mensaje = await ainput("Type your message (type back to get back):  ")
                if (mensaje != 'back') and len(mensaje) > 0:
                    if xmpp.algoritmo == '1':
                        mensaje = "1|" + str(xmpp.jid) + "|" + str(destinatario) + "|" + str(xmpp.graph.number_of_nodes()) + "||" + str(xmpp.nodo) + "|" + str(mensaje)
                        shortest_neighbor_node = xmpp.dvr.shortest_path(destinatario)
                        if shortest_neighbor_node:
                            if shortest_neighbor_node[1] in xmpp.dvr.neighbors:

                                xmpp.send_message(
                                    mto=xmpp.names[shortest_neighbor_node[1]],
                                    mbody=mensaje,
                                    mtype='chat' 
                                )
                            else:
                                pass
                        else:
                            pass
                    else:
                        xmpp.send_message(
                            mto=destinatario,
                            mbody=mensaje,
                            mtype='chat' 
                        )
                elif mensaje == 'back':
                    activo = False
                else:
                    pass
        elif opcion == '1':
            corriendo = False
            xmpp.disconnect()
        else:
            pass


if __name__ == "__main__":

    optp = OptionParser()
    optp.add_option("-j", "--jid", dest="jid",
                    help="JID to use")
    optp.add_option("-p", "--password", dest="password",
                    help="password to use")
    optp.add_option("-a", "--algoritmo", dest="algoritmo",
                    help="algoritmo to use")
    
    opts, args = optp.parse_args()

    topo, names = loadConfig()
    if opts.jid is None:
        opts.jid = input("Type your JID: ")
    if opts.password is None:
        opts.password = getpass.getpass("Type your passowrd: ")
    if opts.algoritmo is None:
        print("""Algorithms Implemented:
        
        1. Distance Vector Routing
        
        """)
        opts.algoritmo = input("Type the number of the algorithm you want to use: ")

    graph_dict, source = getGraph(topo, names, user=opts.jid)

    nodo, nodes = getNodes(topo, names, opts.jid)

    graph = pruebaGrafo(topo, names)

    xmpp = Client(opts.jid, opts.password, opts.algoritmo, nodo, nodes, names["config"], graph, graph_dict, source)
    xmpp.connect() 
    xmpp.loop.run_until_complete(xmpp.connected_event.wait())
    xmpp.loop.create_task(main(xmpp))
    xmpp.process(forever=False)
    