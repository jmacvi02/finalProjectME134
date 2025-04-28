# finalProjectME134
 
Starting mqtt server:
https://www.notion.so/MQTT-3938565fd1b24e7fbdf854a5a0cd6ee7

 
In terminal go to folder with config file (currently in robots folder for this calss) and run:
mosquitto -c mosquitto.conf -v


Use mac’s current IP address to reference: ex. 

192.168.1.235 for 10 Fairmount

mosquitto_sub -t 'test' -h 192.168.86.29 -p 1883

mosquitto_pub -t "test" -h 192.168.1.235 -p 1883 -m "hi there”


-Run main.py on XRP

-Run .exe made from xrp_ble_connect.py. Reference comments at top of this code to get it set up

-Run Data_Collect to use mqtt server to collect data from XRP to be used in ML pipeline


ENSURE ALL HAVE CORRECT MQTT IP ADDRESS and FILEPATHS
