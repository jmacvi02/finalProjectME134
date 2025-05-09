# finalProjectME134
OVERVIEW:
To run any of the 3 control methods developed in the project, run main.py after downloading the project onto your XRP. To enact a specific control method, uncomment the corresponding code chunk in main. The start of each section is label, and runs all the way to the label of the next section. 

Below is additional information for using each section. 

SETTING UP MQTT
Starting mqtt server:
https://www.notion.so/MQTT-3938565fd1b24e7fbdf854a5a0cd6ee7
on mac, can run $brew install mosquitto
then edit config file to include
listener 1883
allow_anonymous true
At the bottom.
In terminal go to folder with config file and run:
mosquitto -c mosquitto.conf -v
Use mac’s current IP address to reference: ex. 
mosquitto_sub -t 'test' -h 192.168.86.29 -p 1883
mosquitto_pub -t "test" -h 192.168.1.235 -p 1883 -m "hi there”
Accessing mqtt server from python and micropython is seen in MQTT_client.py and Data_Collect.py


REMOTE CONTROL VIA XBOX CONTROLLER
- Run main.py on XRP
- Run .exe made from xrp_ble_connect.py. Reference comments at top of that python file code to get it set up

CLASSIC CONTROL
- Ensure the Husky lens is mounted on the front,left side of the XRP. The mount must be tall enough to see a line along the top of the inner wall. Connect the Husky lens to via the qwiik port. 
- Train the Husky lens to detect the line along the top wall.
- Place the XRP along one of the walls so the Husky lens is detecting the line.
- Run main.py to begin movement of the XRP
- Press the user button to stop movement. 


ML CONTROL
- Run main.py to initite the ML model.
    - It will take some time for the XRP to begin moving. 
- Press the user button to stop movment
- KNOWN BUG: the XRP does not stop after the user button is pressed

PIPELINE
-Run Data_Collect to use mqtt server to collect data from XRP to be used in ML pipeline


