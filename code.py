# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import os
import board
import busio
from digitalio import DigitalInOut
import adafruit_connection_manager
import adafruit_minimqtt.adafruit_minimqtt as MQTT

import ipaddress
import wifi
import socketpool
import time
from microcontroller import reset

import usb_hid
from adafruit_hid.mouse import Mouse

# Define callback methods which are called when events occur
# pylint: disable=unused-argument, redefined-outer-name
def connect(mqtt_client, userdata, flags, rc):
    # This function will be called when the mqtt_client is connected
    # successfully to the broker.
    print("Connected to MQTT Broker!")
    print("Flags: {0}\n RC: {1}".format(flags, rc))


def disconnect(mqtt_client, userdata, rc):
    # This method is called when the mqtt_client disconnects
    # from the broker.
    print("Disconnected from MQTT Broker!")


def subscribe(mqtt_client, userdata, topic, granted_qos):
    # This method is called when the mqtt_client subscribes to a new feed.
    print("Subscribed to {0} with QOS level {1}".format(topic, granted_qos))


def unsubscribe(mqtt_client, userdata, topic, pid):
    # This method is called when the mqtt_client unsubscribes from a feed.
    print("Unsubscribed from {0} with PID {1}".format(topic, pid))


def publish(mqtt_client, userdata, topic, pid):
    # This method is called when the mqtt_client publishes data to a feed.
    print("Published to {0} with PID {1}".format(topic, pid))


def message(client, topic, message):
    print("New message on topic {0}: {1}".format(topic, message))


# pool = adafruit_connection_manager.get_radio_socketpool(esp)
# ssl_context = adafruit_connection_manager.get_radio_ssl_context(esp)


def main():
    mouse = Mouse(usb_hid.devices)
    aio_username = os.getenv("aio_username")
    aio_key = os.getenv("aio_key")
    
    ssid = os.getenv("SSID")
    password = os.getenv("PASSWORD")

    wifi.radio.connect(ssid, password)
    pool = socketpool.SocketPool(wifi.radio)

    mqtt_topic_sub = "qctr"
    mqtt_topic_pub = "qctw"
    
    # Set up a MiniMQTT Client
    mqtt_client = MQTT.MQTT(
        broker="broker.emqx.io",
        username="user34542",
        password="psswd",
        socket_pool=pool,
    #     ssl_context=ssl_context,
    )
    # Connect callback handlers to mqtt_client
    mqtt_client.on_connect = connect
    mqtt_client.on_disconnect = disconnect
    mqtt_client.on_subscribe = subscribe
    mqtt_client.on_unsubscribe = unsubscribe
    mqtt_client.on_publish = publish
    mqtt_client.on_message = message

    print("Attempting to connect to %s" % mqtt_client.broker)
    mqtt_client.connect()

    print("Subscribing to %s" % mqtt_topic_sub)
    mqtt_client.subscribe(mqtt_topic_sub)
    
    counter = 1
    while True:
        mqtt_client.loop(2)

        print("Publishing to %s" % mqtt_topic_pub)
        mqtt_client.publish(mqtt_topic_pub, f"{counter}. Hello Broker!")
        counter += 1
        time.sleep(1)
        
        mouse.move(x=3)
        time.sleep(1)
        
        mouse.move(x=-3)

#     print("Unsubscribing from %s" % mqtt_topic)
#     mqtt_client.unsubscribe(mqtt_topic)
# 
#     print("Disconnecting from %s" % mqtt_client.broker)
#     mqtt_client.disconnect()

try:
    main()
except Exception as e:
    print(f"Error: {e}")
    microcontroller.reset()
