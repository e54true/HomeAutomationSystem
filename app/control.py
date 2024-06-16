from proton.handlers import MessagingHandler
from proton.reactor import Container
from proton import Message

class Control(MessagingHandler):
    def __init__(self, server_url, sensor_address, appliance_address, interface_address): 
        super(Control, self).__init__()
        self.server_url = server_url
        self.sensor_address = sensor_address
        self.appliance_address = appliance_address
        self.interface_address = interface_address 
        self.sender = None
        self.interface_sender = None 

    def on_start(self, event):
        conn = event.container.connect(self.server_url)
        event.container.create_receiver(conn, self.sensor_address)
        self.sender = event.container.create_sender(conn, self.appliance_address)
        self.interface_sender = event.container.create_sender(conn, self.interface_address) 

    def on_message(self, event):
        data = event.message.body
        print(f"This is control, received data from sensor: {data}")
        self.control_appliances(data)
        self.interface_sender.send(event.message)

    def control_appliances(self, data):
        if data['humidity'] >= 65:
            self.send_command('dehumidifier', 'on')
        elif data['humidity'] < 60:
            self.send_command('dehumidifier', 'off')

        if data['pm25'] > 15:
            self.send_command('air_purifier', 'on')
        elif data['pm25'] < 10:
            self.send_command('air_purifier', 'off')

        if data['temperature'] >= 28:
            self.send_command('air_conditioner', 'on')
        elif data['temperature'] < 26:
            self.send_command('air_conditioner', 'off')

    def send_command(self, appliance, action):
        command = {'appliance': appliance, 'action': action}
        message = Message(body=command)
        self.sender.send(message)
        print(f"This is control, sent command to appliance: {command}")

container = Container(Control("amqp://localhost:5672", "sensor_data", "appliance_commands", "interface_data"))
container.run()
