"""
mqtt.py


"""

import paho.mqtt.client as mqtt
import time
import copy


class MQTT(object):

    def __init__(self, name, network_name, broker):

        # MQTT broker, default broker is locally running
        self.broker = broker
        self.mqtt_port = 1883

        # MQTT client
        self.mqtt_client = mqtt.Client(name)

        # Name of network
        self.network_name = network_name
        self.network_topic = self.network_name + '/'

        # Saves found devices here
        self.found_devices = list()

        # Saves messages from MQTT
        self.messages = list()

    def get_single_message(self, topic):
        """Returns a message from a topic where only 1 message will be posted.
        (For example, finding a device tag as only the tag is getting posted here.)

        :param topic: A topic with 'device_type/device_name/' format
        :return: Tag
        """
        while True:
            messages = self.get_message(topic, seconds=5)
            if messages:
                m = messages[0]
                return m

    def find_messages(self, topic):
        """Retrieves a list of messages from a topic, where different messages will be posted
        (For example, at the network level there are several device types that are posted here)

        :return: A list of messages
        """

        m = set()
        messages = self.get_message(topic, seconds=30)
        if messages:
            for message in messages:
                m.add(message)
        return m

    def get_message(self, topic, seconds=5):
        """Gets messages from a MQTT stream

        :param topic: Topic to subscribe too
        :param seconds: How long to wait for message -> Int
        :return: List of messages from MQTT stream
        """
        self.mqtt_client.connect(self.broker, self.mqtt_port)
        self.mqtt_client.loop_start()
        self.mqtt_client.subscribe(topic)
        self.mqtt_client.on_message = self.on_message
        time.sleep(seconds)
        self.mqtt_client.loop_stop()

        messages = copy.deepcopy(self.messages)
        self.messages = []
        return messages

    def on_message(self, client, userdata, message):
        """Callback function for MQTT
        """

        # Message from device
        device_message = str(message.payload.decode("utf-8"))
        self.messages.append(device_message)
