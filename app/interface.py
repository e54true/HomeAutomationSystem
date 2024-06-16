from flask import Flask, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from proton.handlers import MessagingHandler
from proton.reactor import Container
import threading

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class SensorData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    temperature = db.Column(db.Float, nullable=True)
    humidity = db.Column(db.Float, nullable=True)
    pm25 = db.Column(db.Float, nullable=True)
    dehumidifier = db.Column(db.Boolean, nullable=True)
    air_purifier = db.Column(db.Boolean, nullable=True)
    air_conditioner = db.Column(db.Boolean, nullable=True)

with app.app_context():
    db.create_all()

class InterfaceNode(MessagingHandler):
    def __init__(self, server_url, address):
        super(InterfaceNode, self).__init__()
        self.server_url = server_url
        self.address = address

    def on_start(self, event):
        conn = event.container.connect(self.server_url)
        event.container.create_receiver(conn, self.address)

    def on_message(self, event):
        data = event.message.body
        print(f"This is interface, receive data or command: {data}")
        with app.app_context():
            current_data = SensorData.query.order_by(SensorData.id.desc()).first()

            if current_data is None:
                current_data = SensorData()

            if 'temperature' in data:
                current_data.temperature = data['temperature']
            if 'humidity' in data:
                current_data.humidity = data['humidity']
            if 'pm25' in data:
                current_data.pm25 = data['pm25']
            if 'dehumidifier' in data:
                current_data.dehumidifier = data['dehumidifier']
            if 'air_purifier' in data:
                current_data.air_purifier = data['air_purifier']
            if 'air_conditioner' in data:
                current_data.air_conditioner = data['air_conditioner']

            db.session.add(current_data)
            db.session.commit()

def start_amqp_container():
    print("Starting AMQP container...")
    container = Container(InterfaceNode("amqp://localhost:5672", "interface_data"))
    container.run()

@app.route('/fetch_data')
def fetch_data():
    data = SensorData.query.order_by(SensorData.id.desc()).first()
    if data:
        return jsonify({
            'temperature': data.temperature,
            'humidity': data.humidity,
            'pm25': data.pm25,
            'dehumidifier': data.dehumidifier,
            'air_purifier': data.air_purifier,
            'air_conditioner': data.air_conditioner
        })
    return jsonify({})

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    threading.Thread(target=start_amqp_container, daemon=True).start()
    app.run(debug=True)
