# finalProjectME134
 
Starting mqtt server:
https://www.notion.so/MQTT-3938565fd1b24e7fbdf854a5a0cd6ee7

to summarize above

-on mac, can run $brew install mosquitto

- then edit config file to include

listener 1883

allow_anonymous true
 
At the bottom.

In terminal go to folder with config file and run:
mosquitto -c mosquitto.conf -v


Use mac’s current IP address to reference: ex. 

mosquitto_sub -t 'test' -h 192.168.86.29 -p 1883

mosquitto_pub -t "test" -h 192.168.1.235 -p 1883 -m "hi there”

Accessing mqtt server from python and micropython is seen in MQTT_client.py and Data_Collect.py

Once mqtt is installed and running, run these steps to start xbox controller controlling the xrp and collecting data:

-Run main.py on XRP

-Run .exe made from xrp_ble_connect.py. Reference comments at top of that python file code to get it set up

-Run Data_Collect to use mqtt server to collect data from XRP to be used in ML pipeline


ENSURE ALL HAVE CORRECT MQTT IP ADDRESS and FILEPATHS
