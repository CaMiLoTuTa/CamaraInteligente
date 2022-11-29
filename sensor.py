from machine import Pin
import network
import urequests
import time
import ufirebase as firebase
from umqtt.simple import MQTTClient


# * SENSOR AUDIO
sensor = Pin((2), Pin.IN, Pin.PULL_UP)


# * MQTT Server Parameters
MQTT_CLIENT_ID = ""
MQTT_BROKER = "broker.hivemq.com"
MQTT_USER = ""
MQTT_PASSWORD = ""
topic_sub = 'mensaje/negro'
topic_pub = 'mensaje/negro'


print("Connecting to WiFi", end="")
sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)
sta_if.connect('Q60', 'minumero')
while not sta_if.isconnected():
    print(".", end="")
    time.sleep(0.1)
print(" Connected!")


firebase.setURL("https://ledrgb-cb498-default-rtdb.firebaseio.com")


def sub_cb(topic, msg):
    print('sss')
    if topic == b'diego/boton':
        fun = int(msg.decode())
        print(fun)


print("Connecting to MQTT server... ", end="")
client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER,
                    user=MQTT_USER, password=MQTT_PASSWORD)
client.set_callback(sub_cb)
client.connect()
client.subscribe(topic_sub)
print('Connected to %s MQTT broker, subscribed to %s topic' %
      (MQTT_BROKER, topic_sub))
print("Connected!")


def activarSensorTodas(topic_sub):
    if sensor.value() == 1:
        message = '1'
        client.publish(topic_sub, message)


def activarSensorTel():
    if sensor.value() == 1:
        message = '2'
        client.publish(topic_sub, message)


def activarSensorDis():
    if sensor.value() == 1:
        message = '3'
        client.publish(topic_sub, message)


def activarSensorSms():
    if sensor.value() == 1:
        message = '4'
        client.publish(topic_sub, message)


while True:
    firebase.get("Millos/activar", "activar", bg=0)
    activar = str(firebase.activar)

    valors = sensor.value()
    print(valors)

    if sensor.value() == 0:
        message = '0'
        client.publish(topic_sub, message)

    if activar == '1':
        activarSensorTodas()

    if activar == '2':
        activarSensorTel()

    if activar == '3':
        activarSensorDis()

    if activar == '4':
        activarSensorSms()
