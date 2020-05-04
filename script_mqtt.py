#!/usr/bin/env python3
from influxdb import InfluxDBClient
import paho.mqtt.client as mqtt

# This is the Subscriber

def on_connect(client, userdata, flags, rc):
  print("Connected with result code "+str(rc))
  client.subscribe("+/devices/+/up")
	



def on_message(client, userdata, msg):

  temp = msg.payload.decode().split("temperature\":")[1].split('}')[0]
  devID = msg.payload.decode().split("dev_id\":")[1].split(",")[0].replace("\"","")
  date = msg.payload.decode().split("time\":")[1].split(",")[0].replace("\"","")
  json_body = [
        {
            "measurement": "temperatur",
            "tags": {
                "host": devID,
                "region": "EU"
            },
            "time": date,
            "fields": {
                "int_value": temp
               
            }
        }
    ]
  clientDB.write_points(json_body)
  print(json_body)




IPDOCKER = "172.16.0.150"
client = mqtt.Client()
client.connect("eu.thethings.network",1883,60)
print("lancement du script les informations vont etre envoyé dans la base influxdb suivante : " + IPDOCKER +  "....")
client.username_pw_set("seminaire_lorawan", "ttn-account-v2.mER2Tawa01ffrvohNMNHdxsYWhjfVMhZUW4hruBUdJY")
client.on_connect = on_connect
client.on_message = on_message
clientDB = InfluxDBClient(host=IPDOCKER, port=8086)
clientDB.create_database("temperature")
clientDB.switch_database('temperature')






client.loop_forever()
