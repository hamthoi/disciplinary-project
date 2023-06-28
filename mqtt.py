print("MQTT with Adafruit IO")
import time
import random
import sys
from Adafruit_IO import MQTTClient
import requests
import certifi


AIO_USERNAME = "hamthoi"
AIO_KEY = "aio_Elmj68SSjQ7f2lfas1Wr7qbFANwr"

global_equation = "x1+x2+x3"

def init_global_equation():
    global global_equation
    headers = {}
    aio_url = "https://io.adafruit.com/api/v2/hamthoi/feeds/equation"
    x = requests.get(url=aio_url, headers=headers, verify=certifi.where())
    data = x.json()
    global_equation = data["last_value"]    
    print("Get lastest value:", global_equation)

global_equation = "x1+x2+x3"

def modify_value(x1, x2, x3):
    global global_equation
    print("Equation: ", global_equation)
    result = eval(global_equation)
    print(result)
    return result


def connected(client):
    print("Server connected ...")
    client.subscribe("button1")
    client.subscribe("button2")
    client.subscribe("equation")

def subscribe(client , userdata , mid , granted_qos):
    print("Subscribeb!!!")

def disconnected(client):
    print("Disconnected from the server!!!")
    sys.exit (1)

def message(client , feed_id , payload):
    print("Received: " + payload)
    if(feed_id == "equation"):
        global  global_equation
        global_equation = payload
        print(global_equation)

client = MQTTClient(AIO_USERNAME , AIO_KEY)

client.on_connect = connected 
client.on_disconnect = disconnected
client.on_message = message
client.on_subscribe = subscribe

client.connect()
client.loop_background()
init_global_equation()



while True:
    time.sleep(2)
    a1 = random.randint(0,100)
    a2 = random.randint(0,100)
    a3 = random.randint(0,100)
    client.publish("sensor1", a1)
    client.publish("sensor2", a2)
    client.publish("sensor3", a3)
    a4 = modify_value(a1, a2, a3)
    print(a4)
    pass
