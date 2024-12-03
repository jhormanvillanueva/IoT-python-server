#Suscribe to mqtt broker and publish messages to a topic
#This is a simple example of how to use the paho-mqtt library to subscribe to a topic and publish messages to a topic


#import paho.mqtt.client as mqtt
import time

from flask import Flask

app = Flask(__name__)


@app.route('/')
def index():
    return 'Hello World!'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
