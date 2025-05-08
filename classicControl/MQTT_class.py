# Author:       Eli Houlton
# Date Updated: 5/7/2025
# Name :        MQTT_Client.py
# Purpose:      Connects to wifi then mqtt server 

from XRPLib import mqtt
import network, ubinascii

class Mqtt_Client:
    def __init__(self, wifi, ip):
        #Initialize necessary variables

        self.wifi = wifi
        self.client = None
        self.ip = ip
        self.Eli = None
        self.send_channel = "data"

        self.start()

    def __del__(self):
        self.stop()
        
    def connect_wifi(self, wifi):
        # Takes wifi username and password as dictionary and connects pico to that wifi network.
        # Requires network and ubinascii libraries
        station = network.WLAN(network.STA_IF)
        station.active(True)
        mac = ubinascii.hexlify(network.WLAN().config('mac'),':').decode()
        print("MAC " + mac)
        
        station.connect(wifi['ssid'],wifi['pass'])
        while not station.isconnected():
            time.sleep(1)
        print('Connection successful')
        print(station.ifconfig())

    def whenCalled(self, topic, msg):
            #listens to mqtt channel topic
            self.latest_message = msg.decode()
            print(msg.decode())

    def connect_mqtt(self):
        try:
            self.Eli = mqtt.MQTTClient('listener', self.ip, keepalive=1200)
            print('Connected')
            self.Eli.connect()
            self.Eli.set_callback(self.whenCalled)
            self.Eli.subscribe("topic")
        except OSError as e:
            print('MQTT connect Failed'+str(e))
    
    def start(self):
        board.led_on()
        time.sleep(.25)
        board.led_off()
        self.connect_wifi(self.wifi)
        self.connect_mqtt()
        board.led.on()


    def send_message(self, message):
        try
            self.Eli.publish(self.send_channel, self.output_data) #type: ignore    
        except Exception as e:
            print("Main Loop not excecuted")
            print(e)

    def stop(self):
        # What to do on disconnect
        if self.Eli:
            self.Eli.disconnect()
        print("MQTT disconnected")
        board.led_off()
        self.drive.set_effort(0,0)
        
