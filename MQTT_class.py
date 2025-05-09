# Author:       Eli Houlton
# Date Updated: 5/7/2025
# Name :        MQTT_Client.py
# Purpose:      Connects to wifi then mqtt server 

from XRPLib import mqtt
import network, ubinascii
import time
import math
from XRPLib.imu import IMU
from XRPLib.rangefinder import Rangefinder
from XRPLib.differential_drive import DifferentialDrive


class Mqtt_Client:
    def __init__(self, wifi, ip):
        #Initialize necessary variables

        self.wifi = wifi
        self.client = None
        self.ip = ip
        self.Eli = None
        self.send_channel = "data"

        self.xrp_imu = IMU.get_default_imu()
        self.drive = DifferentialDrive.get_default_differential_drive()
        self.dist_sensor = Rangefinder.get_default_rangefinder()
        self.encoder_L = self.encoder_R = self.encoder_L_prev = self.encoder_R_prev = 0
        self.wallDist = [0.0] * 7
        self.send_interval = 250 #every .25 seconds
        self.output_data = "empty"
        self.start_time = time.ticks_ms()
        self.t = 0

        self.start()

    def __del__(self):
        self.stop()
        
    def connect_wifi(self, wifi):
        """
        Takes wifi username and password as dictionary and connects pico to that wifi network.
        Requires network and ubinascii libraries

        :param wifi: wifi name
        :type wifi: string
        """

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
        """
        listens to mqtt channel topic   

        """
        #listens to mqtt channel topic
        self.latest_message = msg.decode()
        print(msg.decode())

    def connect_mqtt(self):
        """
        connecting to mqtt for both data collection and robot control (for xbox controller)
        """
        try:
            self.Eli = mqtt.MQTTClient('listener', self.ip, keepalive=1200)
            print('Connected')
            self.Eli.connect()
            self.Eli.set_callback(self.whenCalled)
            self.Eli.subscribe("topic")
        except OSError as e:
            print('MQTT connect Failed'+str(e))
    
    def start(self):
        """
        driver function for establishing pipeline. Run upon initilizing this class.
        """
        self.connect_wifi(self.wifi)
        self.connect_mqtt()

    def send_message(self, message):
        """
        Sends message to MQTT for data collection

        :param message: the data to send to the mqtt formated as csv
        :type  message: string
        """
        try:
            self.Eli.publish(self.send_channel, message) #type: ignore    
        except Exception as e:
            print("Main Loop not excecuted")
            print(e)

    def stop(self):
        """
        What to do on disconnect
        """
        if self.Eli:
            self.Eli.disconnect()
        print("MQTT disconnected")

    def get_median(self, arr):
        """
        Gets median of an input array

        :param arr: array of numbers to take the median of
        :type arr: array
        :return median: the median of the array
        :type median: float
        """
        if not arr:
            raise ValueError("Array cannot be empty")
        sorted_arr = sorted(arr)  # create a sorted copy
        n = len(sorted_arr)
        mid = n // 2
        if n % 2 == 0:
            return (sorted_arr[mid - 1] + sorted_arr[mid]) / 2
        else:
            return sorted_arr[mid]
        
    def get_wall_sensor_input(self):
        """
        Gets new range finder data and run through median filter

        :return dist: the median distance to the wall
        :type median: float
        """
        for i in range(len(self.wallDist) - 1, 0, -1):
            self.wallDist[i] = self.wallDist[i - 1]
        self.wallDist[0] = self.dist_sensor.distance()

        return self.get_median(self.wallDist)

    def pipeLine(self):
        """
        The main function driver of this class. compiles all pipeline data and sends to mqtt server

        """
        imu_data = self.xrp_imu.get_acc_gyro_rates()
        range_f = self.get_wall_sensor_input()
        self.encoder_L = self.drive.get_left_encoder_position()
        self.encoder_R = self.drive.get_right_encoder_position()

        elapsed = time.ticks_diff(time.ticks_ms(), self.start_time)
        t_string = elapsed / 1000
        vel_L = 0.16 * (self.encoder_L - self.encoder_L_prev) / (2 * t_string)
        vel_R = 0.16 * (self.encoder_R - self.encoder_R_prev) / (2 * t_string)

        self.output_data = f"{t_string},{imu_data[0][0]},{imu_data[0][1]},{imu_data[1][2]}," \
                        f"{range_f},{self.encoder_L},{self.encoder_R},{vel_L},{vel_R}"

        if time.ticks_diff(time.ticks_ms(), self.last_send_time) > self.send_interval:
            try:
                self.send_message(self.output_data)
            except Exception as e:
                print("[MQTT Publish Error]", e)
            self.last_send_time = time.ticks_ms()
            self.encoder_L_prev = self.encoder_L
            self.encoder_R_prev = self.encoder_R