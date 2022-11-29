
import network
import time
import urequests
from machine import Pin, ADC, PWM, RTC
import ufirebase as firebase
from time import localtime
import ntptime
from umqtt.simple import MQTTClient


# ~ CONEXIÓN WIFI
print("Connecting to WiFi", end="")
sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)
sta_if.connect('PETRA', 'PETRA2021')
while not sta_if.isconnected():
    print(".", end="")
    time.sleep(0.1)
print(" Connected!")

# * MQTT Server Parameters
MQTT_CLIENT_ID = ""
MQTT_BROKER = "broker.hivemq.com"
MQTT_USER = ""
MQTT_PASSWORD = ""
topic_sub = 'mensaje/negro'
topic_pub = 'mensaje/negro'


def sub_cb(topic, msg):
    # print(f"llego el topic: {topic} con el valor {msg}")
    if topic == 'mensaje/negro':
        fun = msg.decode()
    fun = msg.decode()
    print(fun)

    if fun == '0':
        pass

    if fun == '1':
        mensajeTodos()
        print('Mensaje enviado')

    if fun == '2':
        mensajeTel()
        print('Mensaje enviado')

    if fun == '3':
        mensajeDis()
        print('Mensaje enviado')

    if fun == '4':
        mensajeSms()
        print('Mensaje enviado')


# ~ URLS PARA NOTIFICACIONES
url = "https://maker.ifttt.com/trigger/notamb/with/key/inSrLr4nyMQ8ShQ0noTQEo4Hy2fO1f4ZYMVvxUEUW13"
urlDis = "https://maker.ifttt.com/trigger/ambnot/with/key/inSrLr4nyMQ8ShQ0noTQEo4Hy2fO1f4ZYMVvxUEUW13?"
urlSMS = "https://maker.ifttt.com/trigger/sms/with/key/inSrLr4nyMQ8ShQ0noTQEo4Hy2fO1f4ZYMVvxUEUW13?"
urlTel = "https://maker.ifttt.com/trigger/telegram_not/with/key/inSrLr4nyMQ8ShQ0noTQEo4Hy2fO1f4ZYMVvxUEUW13?"


# ~ SUBE LOS DATOS A IFTTT

msg1 = 'HEY'

def mensajeTodos():
    respuestaTel = urequests.get(
        urlTel+"&value1="+str(msg1) + "&value2="+str(fecha)+"&value3="+str(hora))
    respuestaTel.close()
    respuestaDis = urequests.get(
        urlDis+"&value1="+str(msg1) + "&value2="+str(fecha)+"&value3="+str(hora))
    respuestaDis.close()
    respuestaSMS = urequests.get(
        urlSMS+"&value1="+str(msg1) + "&value2="+str(fecha)+"&value3="+str(hora))
    respuestaSMS.close()


def mensajeTel():
    respuestaTel = urequests.get(
        urlTel+"&value1="+str(msg1) + "&value2="+str(fecha)+"&value3="+str(hora))
    respuestaTel.close()


def mensajeDis():
    respuestaDis = urequests.get(
        urlDis+"&value1="+str(msg1) + "&value2="+str(fecha)+"&value3="+str(hora))
    respuestaDis.close()


def mensajeSms():
    respuestaSMS = urequests.get(
        urlSMS+"&value1="+str(msg1) + "&value2="+str(fecha)+"&value3="+str(hora))
    respuestaSMS.close()


print("Connecting to MQTT server... ", end="")
client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER,
                    user=MQTT_USER, password=MQTT_PASSWORD)
client.set_callback(sub_cb)
client.connect()
client.subscribe(topic_sub)
print('Connected to %s MQTT broker, subscribed to %s topic' %
      (MQTT_BROKER, topic_sub))
print("Connected!")

while True:
    ntptime.settime()
    rtc = RTC()
    hora = f'{((localtime()[3])+19):02d}:{localtime()[4]:02d}:{localtime()[5]:02d}'
    fecha = f'{localtime()[0]:02d}/{localtime()[1]:02d}/{localtime()[2]:02d}'
    fechaYHora = fecha + ' ' + hora

    print('Esperando')
    client.wait_msg()

