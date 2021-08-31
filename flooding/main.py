from getpass import getpass
from Client import *

"""
    Main class
"""

if __name__ == '__main__':

    jid = input("Type your jid: ")
    password = getpass("Type your password: ")
    routing = input("Routing type: ")
    
    listening = False
    if routing != "flooding":
        listening = True


    names_file = input("Type the relative url of the file with the names of your network: ")
    topology_file = input("Type the relative url of the file with the topology decription of your network: ")

    try:
        recipient = ''
        message = ''

        if(not listening):
            recipient = input("Write the recipient JID: ") 
            message = input("Write the message: ")

        xmpp = Client(jid, password, recipient, message, routing, listening, names_file, topology_file)
        xmpp.register_plugin('xep_0030') # Service Discovery
        xmpp.register_plugin('xep_0199') # XMPP Ping
        xmpp.register_plugin('xep_0045') # Mulit-User Chat (MUC)
        xmpp.register_plugin('xep_0096') # Jabber Search
        xmpp.register_plugin('xep_0077') ### Band Registration
        xmpp.connect()
        xmpp.process(forever=False)
        
    except KeyboardInterrupt as e:
        print('\nThanks for using the flooding algorithm!\n')