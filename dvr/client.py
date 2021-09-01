from distanceVectorRouting import DistanceVectorRouting
import asyncio
from datetime import datetime
import slixmpp
import networkx as nx
import ast

class Client(slixmpp.ClientXMPP):
    def __init__(self, jid, password, algoritmo, nodo, nodes, names, graph, graph_dict, source):
        super().__init__(jid, password)
        self.received = set()
        self.algoritmo = algoritmo
        self.names = names
        self.graph = graph
        self.dvr = DistanceVectorRouting(graph, graph_dict, source, names)
        self.nodo = nodo
        self.nodes = nodes
        self.schedule(name="echo", callback=self.echo_message, seconds=5, repeat=True)
        self.schedule(name="update", callback=self.update_message, seconds=10, repeat=True)
        
        self.connected_event = asyncio.Event()
        self.presences_received = asyncio.Event()

        self.add_event_handler('session_start', self.start)
        self.add_event_handler('message', self.message)
    
        self.register_plugin('xep_0030') # Service Discovery
        self.register_plugin('xep_0045') # Multi-User Chat
        self.register_plugin('xep_0199') # Ping

    async def start(self, event):
        self.send_presence() 
        await self.get_roster()
        self.connected_event.set()

    async def message(self, msg):
        if msg['type'] in ('normal', 'chat'):
            await self.reply_message(msg['body'])

    async def reply_message(self, msg):
        message = msg.split('|')
        if message[0] == '1':
            if self.algoritmo == '1':
                if message[2] == self.jid:
                    print("Incoming message >> " +  message[6])
                else:
                    shortest_neighbor_node = self.dvr.shortest_path(message[2])
                    if shortest_neighbor_node:
                        if shortest_neighbor_node[1] in self.dvr.neighbors:
                            # We send the message
                            StrMessage = "|".join(message)
                            self.send_message(
                                mto=message[2],
                                mbody=StrMessage,
                                mtype='chat' 
                            )
                        else:
                            pass
                    else:
                        pass
        elif message[0] == '2':
            if self.algoritmo == '1':
                esquemaRecibido = message[6]

                divido = esquemaRecibido.split('-')
                nodos = ast.literal_eval(divido[0])
                aristas = ast.literal_eval(divido[1])
                self.graph.add_nodes_from(nodos)
                self.graph.add_weighted_edges_from(aristas)

                self.dvr.update_graph(nx.to_dict_of_dicts(self.graph))

                dataneighbors = self.graph.nodes().data()
                dataedges = self.graph.edges.data('weight')
                StrNodes = str(dataneighbors) + "-" + str(dataedges)

                for i in self.dvr.neighbors:
                    update_msg = "2|" + str(self.jid) + "|" + str(self.names[i]) + "|" + str(self.graph.number_of_nodes()) + "||" + str(self.nodo) + "|" + StrNodes
                    self.send_message(
                            mto=self.dvr.names['config'][i],
                            mbody=update_msg,
                            mtype='chat'
                        )
        elif message[0] == '3':
            if message[6] == '':
                now = datetime.now()
                timestamp = datetime.timestamp(now)
                mensaje = msg + str(timestamp)
                self.send_message(
                            mto=message[1],
                            mbody=mensaje,
                            mtype='chat' 
                        )
            else:
                difference = float(message[6]) - float(message[4])
                self.graph[self.nodo][message[5]]['weight'] = difference
        else:
            pass

    def echo_message(self):
        for i in self.nodes:
            now = datetime.now()
            timestamp = datetime.timestamp(now)
            mensaje = "3|" + str(self.jid) + "|" + str(self.names[i]) + "||"+ str(timestamp) +"|" + str(i) + "|"
            self.send_message(
                        mto=self.names[i],
                        mbody=mensaje,
                        mtype='chat' 
                    )

    def update_message(self):
        if self.algoritmo == '1':
            dataneighbors = self.graph.nodes().data()
            dataedges = self.graph.edges.data('weight')
            StrNodes = str(dataneighbors) + "-" + str(dataedges)
            for i in self.dvr.neighbors:
                update_msg = "2|" + str(self.jid) + "|" + str(self.names[i]) + "|" + str(self.graph.number_of_nodes()) + "||" + str(self.nodo) + "|" + StrNodes
                self.send_message(
                        mto=self.dvr.names[i],
                        mbody=update_msg,
                        mtype='chat'
                    )