from proton.handlers import MessagingHandler
from proton.reactor import Container
from proton import Message

class Appliance(MessagingHandler):
    def __init__(self, server_url, address, interface_address): 
        super(Appliance, self).__init__()
        self.server_url = server_url
        self.address = address
        self.interface_address = interface_address  
        self.appliances = {
            "dehumidifier": False,
            "air_purifier": False,
            "air_conditioner": False
        }

    def on_start(self, event):
        conn = event.container.connect(self.server_url)
        event.container.create_receiver(conn, self.address)
        self.interface_sender = event.container.create_sender(conn, self.interface_address) 

    def on_message(self, event):
        command = event.message.body
        appliance = command['appliance']
        action = command['action']
        self.control_appliance(appliance, action)

    def control_appliance(self, appliance, action):
        if action == "on":
            self.appliances[appliance] = True
            #print(f"{appliance.capitalize()} turned on.")
        elif action == "off":
            self.appliances[appliance] = False
            #print(f"{appliance.capitalize()} turned off.")

        status_message = Message(body={appliance: self.appliances[appliance]})
        self.interface_sender.send(status_message)
        print(f"This is appliance, sent status to interface: {status_message.body}")


container = Container(Appliance("amqp://localhost:5672", "appliance_commands", "interface_data"))
container.run()
