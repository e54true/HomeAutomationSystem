# Smart Home Dashboard System

## Project Overview
This smart home dashboard system utilizes Apache Qpid to manage communication between sensors, a control center, appliances, and a user interface. It's designed to monitor and control various home conditions such as temperature, humidity, and air quality (PM2.5), and manage smart appliances including dehumidifiers, air purifiers, and air conditioners.

## System Components
- **Sensor**: Detects environmental conditions and sends the data to the control center and interface.
- **Control Center**: Processes the data from the sensor and manages the state of each appliance based on predefined conditions.
- **Appliance**: Executes actions (e.g., turning on or off) as instructed by the control center.
- **Interface**: Provides a web-based user interface to display real-time data and appliance status.

## Installation
- **pip install python-qpid-proton**
- **pip install Flask**

## Start Each Component
- **python broker.py**
- **python sensor.py**
- **python control.py**
- **python appliance.py**
- **python interface.py**

## Access the Dashboard
Open a web browser and go to `http://localhost:5000` to view the dashboard