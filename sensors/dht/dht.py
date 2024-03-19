#!/usr/bin/python
import time
# used lib is: https://github.com/adafruit/Adafruit_CircuitPython_DHT
# lib usage: https://learn.adafruit.com/dht-humidity-sensing-on-raspberry-pi-with-gdocs-logging/python-setup
import adafruit_dht 
import logging
import board
import paho.mqtt.client as mqtt # pip3 install paho-mqtt==1.6.1
import psutil                   # pip3 install psutil

#https://github.com/adafruit/Adafruit_CircuitPython_DHT/issues/27
for proc in psutil.process_iter():
    if proc.name() in ('libgpiod_pulsein', 'libgpiod_pulsei'):
        proc.kill()

SEND_TOHA = True
USE_PRINT = True

# MQTT-Konfiguration
mqttBroker    = '192.168.178.143'
mqttBokerPort =  1883
mqttUser      = 'mqtt-user'
mqttPW        = 'kiokio11MQTT++'
mqttTemp1   = "hygrometer/cellar_1/temperature"   # dht22 Sensor 1 Keller Temperature
mqttTemp2   = "hygrometer/cellar_2/temperature"   # dht22 Sensor 2 Keller Temperature
mqttHum1    = "hygrometer/cellar_1/humidity"
mqttHum2    = "hygrometer/cellar_2/humidity"
errors          = 0

dhtSensor1    = adafruit_dht.DHT22(board.D4 )  # 3.3V
dhtSensor2    = adafruit_dht.DHT22(board.D17) # 5V outside hum/temp
sleep_secs    = 20
use_print     = True

humidity1 = -111
humidity2  = -111
temperature2 = -111
temperature1 = -111

def mqttConnect():
    client = mqtt.Client()
    client.username_pw_set(mqttUser, mqttPW)
    client.connect(mqttBroker, mqttBokerPort)
    return client

def sendData(datapoint, topic, comment=""):
    if USE_PRINT: print("Send data now....")
    try:
        client = mqttConnect()
        if "temperature" in topic:
            if datapoint>-20 and datapoint<50:
                    client.publish(topic, datapoint)
                    if USE_PRINT: print("sending now:", datapoint, "C", comment)
                    client.disconnect()
            else:
              if USE_PRINT: print("Cannot send value limits exceeded:", datapoint, topic, comment)
        elif "humidity" in topic:
            if datapoint>10 and datapoint<95:
                client.publish(topic, datapoint)
                if USE_PRINT: print("sending now:", datapoint, "C", comment)               
                client.disconnect()
            else:
              if USE_PRINT: print("Cannot send value limits exceeded:", datapoint, topic, comment)
    except Exception as e:
        print(e, "probably no wifi currently")

def check_error(in_value, ctrl="hum"):
    if in_value is None or isinstance(in_value, str):
       return True
    if ctrl=="hum":
        if in_value<10 or in_value>100:
            return True
        else:
            return False
    else:
        if in_value<-25 or in_value > 55:
            return True
        else:
            return False

def read(dev):
        temp = -111
        hum  = -111
        try:
                hum, temp  = dev.humidity, dev.temperature
                if use_print:
                        print("PIN "+str(dev)+" :", temp, hum)
        except RuntimeError as error:
                # Errors happen fairly often, DHT's are hard to read, just keep going
                if use_print: print(error.args[0])
                time.sleep(2.0)
        except Exception as error:
                dev.exit()
                raise error
        # except Exception as e:
        #       if use_print:
        #               #dev.exit()
        #               print(e)
        #       error = 1
        return temp, hum, 0

def read2dev(dhtSensor1, dhtSensor2, timeout=sleep_secs):
        time.sleep(sleep_secs)
        temp_in, hum_in, error_in    = read(dhtSensor1)
        temp_out, hum_out, error_out = read(dhtSensor2)
        if check_error(temp_in):
                temp_in = -222
        if check_error(hum_in, ctrl="hum"):
                hum_in = -222
        if check_error(temp_out):
                temp_out = -222
        if check_error(hum_out, ctrl="hum"):
                hum_out = -222
        return temp_in, hum_in, temp_out, hum_out, 0, 0

i = 1
while True:
    temperature2, humidity2, temperature1, humidity1, ci, co = read2dev(dhtSensor1, dhtSensor2)
    sendData(temperature1, mqttTemp1, comment="")
    sendData(temperature2, mqttTemp2, comment="")
    sendData(humidity1, mqttHum1, comment="")
    sendData(humidity2, mqttHum2, comment="")