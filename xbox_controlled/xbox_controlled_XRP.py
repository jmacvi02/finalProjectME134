# Author:       Eli Houlton
# Date Updated: 5/7/2025
# Name :        xbox_controlled_XRP.py
# Purpose:      Implementation of a class to control an XRP via an xbox controller using bluetooth.

import math
from XRPLibMotor3Opt.defaults import *
import time
from machine import Timer
from XRPLib import mqtt
import network, ubinascii
from XRPLib.imu import IMU
from pestolink import PestoLinkAgent
from MQTT_class import Mqtt_Client

class TeamWDreamBot:
    def __init__(self, wifi, ip):
        #Initialize necessary variables
        # blink led to let user know main is running:
        board.led_on()
        time.sleep(.2)
        board.led_off()
        ble_name = "XRP"
        self.pestolink = PestoLinkAgent(ble_name)
        self.xrp_imu = IMU.get_default_imu()
        self.drive = DifferentialDrive.get_default_differential_drive()
        self.latest_message = "0,0"
        self.encoder_L = self.encoder_R = 0
        self.send_interval = 250 #every .25 seconds
        self.output_data = "empty"
        self.start_time = time.ticks_ms()
        self.dist_sensor = Rangefinder(20, 21)

        self.mqtt_client = Mqtt_Client(wifi, ip)
        self.start()


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

    def joyToMagAng(self, absX, absY):
        #Used to convert xbox input into efforts to send the motors

        centX = 0 #offset val ELI PUT THE X VALUE AT CENTER HERE
        centY = 0 #offset val ELI PUT THE Y VALUE AT  CENTER HERE

        relX = absX - centX
        relY = absY - centY

        mag = math.sqrt(relX**2 + relY**2)
        #quadrant 1
        if relX >= 0 and relY >= 0:
            angle = -1*((math.pi/2) - math.atan2(relY, relX))
        #quad 2
        elif relX <= 0 and relY >= 0:
            angle = (math.pi/2) - math.atan2(relY, abs(relX))
        #quad 3
        elif relX <= 0 and relY <= 0:
            angle = (math.pi)/2 + math.atan2(abs(relY), abs(relX))
        #quad 4
        elif relX >= 0 and relY <= 0:
            angle = - (math.pi)/2 - math.atan2(abs(relY), relX)
        else:
            angle = 0
            mag = 0
            print("err no quadrant picked")

        if mag < .1:
            mag = 0
        
        return mag, angle

    def mapToEffort(self, mag, angle):
        #Used to convert xbox input into efforts to send the motors

        maxMAG = 1 #ELI PUT WHATEVER THE MAGNITUDE IS WHEN JOY STICK IS ALL THE WAY EXTENDED HERE

        magFactor = 1 / maxMAG
        effortMag = mag * magFactor

        if abs(angle) <= (3*math.pi) / 4:
            turnFactor = 0.8 / ((3* math.pi) / 4)
            effortAngle = angle * turnFactor
            effortL = effortMag - effortAngle
            effortR = effortMag + effortAngle  

        elif abs(angle) > (3*math.pi) / 4:
            turnFactor = (0.5/ (math.pi))
            effortAngle = (math.pi - angle) * turnFactor
            effortL = (-effortMag  + effortAngle)/2
            effortR = (-effortMag  - effortAngle)/2

        if effortMag < .2:
            effortL = 0
            effortR = 0


        return effortL, effortR
    
    def get_wall_sensor_input(self):
        ranges = []
        for i in range(7):
            ranges.append(self.dist_sensor.distance())
        return self.get_median(ranges)

    def get_median(self, arr):
        # Function created with help from chatgpt
        if not arr:
            raise ValueError("Array cannot be empty")
        arr.sort()  # Sort the array
        n = len(arr)
        mid = n // 2  # Find the middle index
        if n % 2 == 0:
            return (arr[mid - 1] + arr[mid]) / 2  # Average of two middle values for even length
        else:
            return arr[mid]  # Middle value for odd length
        
    def print_Imu(self):
        return self.xrp_imu.get_acc_gyro_rates()
    
    def start(self):
        board.led.on()
        print("waiting for BLE connect - run xrp_ble_connect.exe")
        while not self.pestolink.is_connected():  # Check if a BLE connection is established
            board.led.off()
            time.sleep(.25)
            board.led.on()
            time.sleep(.25)
        print("BLE connected")
        print("[System] Timer started")
        board.led.on()

    def loop(self):
        # loops until user button is pressed, converts xbox controller input to commands, and sends data over mqtt
        try:
            t=0
            vel_L = vel_R = 0
            encoder_L_prev = encoder_R_prev = 0
            while not board.is_button_pressed():
                eff_l = eff_r = "NA"
                if self.pestolink.is_connected():  # Check if a BLE connection is established
                    absX = self.pestolink.get_axis(0)
                    absY = -1 * self.pestolink.get_axis(1)
                    mag, angle = self.joyToMagAng(absX, absY)
                    eff_l, eff_r = self.mapToEffort(mag, angle)
                    self.drive.set_effort(eff_l , eff_r)
                    
                else: #default behavior when no BLE connection is open
                    print("BLE not connected")
                    drivetrain.arcade(0, 0)

                imu_data = self.print_Imu()
                range_f = self.get_wall_sensor_input()
                self.encoder_L = self.drive.get_left_encoder_position()
                self.encoder_R = self.drive.get_right_encoder_position()

                elapsed = time.ticks_diff(time.ticks_ms(), self.start_time)
                t_string = elapsed/1000
                vel_L = (self.encoder_L - encoder_L_prev)/t_string
                vel_R = (self.encoder_R - encoder_R_prev)/t_string

                self.output_data = str(t_string)+","+str(eff_l)+","+str(eff_r)+","\
                    +str(imu_data[0][0])+","+str(imu_data[0][1])+","+str(imu_data[1][2])\
                        +","+str(range_f)+","+str(self.encoder_L)+","+str(self.encoder_R)\
                        +","+str(vel_L)+","+str(vel_R)

                if time.ticks_diff(time.ticks_ms(), t) > self.send_interval:
                    try:
                        self.mqtt_client.send_message(self.output_data)
                    except Exception as e:
                        print("[MQTT Publish Error]", e)
                    t = time.ticks_ms()
                encoder_L_prev = self.encoder_L
                encoder_R_prev = self.encoder_R
                time.sleep(0.05)
                
        except Exception as e:
            print("Main Loop not excecuted")
            print(e)

    def stop(self):
        board.led_off()
        self.drive.set_effort(0,0)