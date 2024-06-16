import random
from proton import Message
from proton.handlers import MessagingHandler
from proton.reactor import Container

class Sensor(MessagingHandler):
    def __init__(self, server_url, control_address, interface_address):
        super(Sensor, self).__init__()
        self.server_url = server_url
        self.control_address = control_address
        self.interface_address = interface_address
        self.current_data = {
            'temperature': random.randint(24, 30),
            'humidity': random.randint(50, 70),
            'pm25': random.randint(5, 20)
        }

    def on_start(self, event):
        conn = event.container.connect(self.server_url)
        self.control_sender = event.container.create_sender(conn, self.control_address) 
        self.interface_sender = event.container.create_sender(conn, self.interface_address)
        self.schedule_next_send(event)

    def generate_new_value(self, old_value):
        return old_value + random.choice([-1, 1])

    def send_data(self, event):
        self.current_data['temperature'] = self.generate_new_value(self.current_data['temperature'])
        self.current_data['humidity'] = self.generate_new_value(self.current_data['humidity'])
        self.current_data['pm25'] = self.generate_new_value(self.current_data['pm25'])

        message = Message(body=self.current_data)
        self.control_sender.send(message)
        self.interface_sender.send(message)
        print(f"This is sensor, sent data to control and interface: {message.body}")
        self.schedule_next_send(event)

    def schedule_next_send(self, event):
        event.reactor.schedule(5, self)

    def on_timer_task(self, event):
        self.send_data(event)

container = Container(Sensor("amqp://localhost:5672", "sensor_data", "interface_data"))
container.run()
