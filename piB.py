#!/usr/bin/python


import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt
import time

# set GPIO 0 as LED pin
LED1PIN = 17
LED2PIN = 27
LED3PIN = 22

# setup function for some setup
def setup():
    GPIO.setwarnings(False)
    # set the gpio modes to BCM numbering
    GPIO.setmode(GPIO.BCM)
    # set LEDPIN's mode to output,and initial level to LOW(0V)
    GPIO.setup(LED1PIN, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(LED2PIN, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(LED3PIN, GPIO.OUT, initial=GPIO.LOW)


def on_connect(client, userdata, rc):
    print("Connected with rc: " + str(rc))
    client.subscribe("LightStatus")
    client.subscribe("Status/RaspberryPiA")
    client.subscribe("Status/RaspberryPiC")


def on_message(client, userdata, msg):
    print("Topic: " + msg.topic + "\nMessage: " + str(msg.payload))
    if "LightStatus" in msg.topic:
        if "TurnOn" in msg.payload:
            GPIO.output(LED1PIN, GPIO.HIGH)
        elif "TurnOff" in msg.payload:
            GPIO.output(LED1PIN, GPIO.LOW)
    elif "Status/RaspberryPiA" in msg.topic:
        if "online" in msg.payload:
            GPIO.output(LED2PIN, GPIO.HIGH)
        elif "offline" in msg.payload:
            GPIO.output(LED2PIN, GPIO.LOW)
    elif "Status/RaspberryPiC" in msg.topic:
        if "online" in msg.payload:
            GPIO.output(LED3PIN, GPIO.HIGH)
        elif "offline" in msg.payload:
            GPIO.output(LED3PIN, GPIO.LOW)


# main function
def main():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect("broker.mqttdashboard.com", 1883)
    client.loop_forever()
    pass


# define a destroy function for clean up everything after the script finished
def destroy():
    # turn off LED
    GPIO.output(LED1PIN, GPIO.LOW)
    GPIO.output(LED2PIN, GPIO.LOW)
    GPIO.output(LED3PIN, GPIO.LOW)
    # release resource
    GPIO.cleanup()


#
# if run this script directly ,do:
if __name__ == '__main__':
    setup()
    try:
        main()
    # when 'Ctrl+C' is pressed,child program destroy() will be executed.
    except KeyboardInterrupt:
        destroy()



