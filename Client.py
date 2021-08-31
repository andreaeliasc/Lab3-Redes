import uuid
import json
import slixmpp
from utils import calculate
from slixmpp.exceptions import IqError, IqTimeout

class Client(slixmpp.ClientXMPP):
    def __init__(self, jid, password, recipient, message, routing, listening, names_file, topology_file):
        slixmpp.ClientXMPP.__init__(self, jid, password)

        self.recipient = recipient
        self.listening = listening
        self.msg = message
        self.routing = routing
        self.jid_ = jid
        self.lastid = []
        self.names_file = names_file
        self.topology_file = topology_file

        self.add_event_handler("session_start", self.start)
        self.add_event_handler("message", self.message)
        self.add_event_handler("register", self.register)

    async def start(self, event):
        self.send_presence()
        await self.get_roster()

        if(not self.listening and self.routing=="flooding"):
            msg = {}
            msg["Start"] = self.jid_
            msg["Destiny"] = self.recipient
            msg["Jumps"] = 0
            msg["Distance"] = 0
            msg["List_of_Nodes"] = []
            msg["Message"] = self.msg
            msg["ID"] = str(uuid.uuid4())
            self.lastid.append(msg["ID"])

            receivers, message = calculate(json.dumps(msg), self.jid_, self.names_file, self.topology_file)

            for receiver in receivers:
                print("Message sent to :",receiver)
                self.send_message(mto=receiver, mbody=message, mtype='chat')

    def register(self, iq):
        iq = self.Iq()
        iq['type'] = 'set'
        iq['register']['username'] = self.boundjid.user
        iq['register']['password'] = self.password

        try:
            iq.send()
            print("Authenticated as: ", self.boundjid,"\n")
        except IqError as e:
            print("There was an error, check your credentials ", e,"\n")
            self.disconnect()
        except IqTimeout:
            print("Server took to long to respond")
            self.disconnect()
        except Exception as e:
            print(e)
            self.disconnect()

    def message(self, msg):
        if(self.routing=="flooding"):
            if msg['type'] in ('chat'):
                recipient = str(msg['from']).split('/')[0]
                body = msg['body']
                msg = eval(str(body))
                if(msg["ID"] not in self.lastid):
                    self.lastid.append(msg["ID"])

                    print('\n|',recipient,"says:", msg["Message"],'\nJumps:', msg["Jumps"],', Distance:', msg["Distance"],'|\n')

                    receivers, message = calculate(str(body), self.jid_, self.names_file, self.topology_file)

                    for receiver in receivers:

                        if(receiver!=recipient):
                            print("Message sent to :",receiver)
                            self.send_message(mto=receiver, mbody=message, mtype='chat')