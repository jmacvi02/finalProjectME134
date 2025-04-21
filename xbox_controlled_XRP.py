import math
from XRPLib.defaults import *
import time
from machine import Timer
from XRPLib import mqtt
import network, ubinascii
from XRPLib.imu import IMU
from huskylensPythonLibrary import HuskyLensLibrary

class TeamWDreamBot:
    def __init__(self, wifi, ip):
        self.xrp_imu = IMU.get_default_imu()
        self.wifi = wifi
        self.client = None
        self.timer = Timer()
        self.ip = ip
        self.L_motor = EncodedMotor.get_default_encoded_motor(index=1)
        self.R_motor = EncodedMotor.get_default_encoded_motor(index=2)
        self.drive = DifferentialDrive(self.L_motor,self.R_motor) # type: ignore
        self.latest_message = "0,0"
        self.send_interval = 10
        self.Eli = None
        self.output_data = "empty"
        self.start_time = time.time_ns()/1000000

        # # Initialize HuskyLens on I2C and differential drive system
        # self.husky = HuskyLensLibrary("I2C")
        # # Ensure HuskyLens is in line tracking mode
        # while not self.husky.line_tracking_mode():
        #     self.husky.line_tracking_mode()

    def connect_wifi(self, wifi):
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
            self.latest_message = msg.decode()

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
    
    def print_Imu(self):
        return self.xrp_imu.get_acc_gyro_rates()

    def send_data(self, data):
        self.Eli.publish("data", data) #type:ignore
    
    def start(self):
        board.led_on()
        time.sleep(.25)
        board.led_off()
        self.connect_wifi(self.wifi)
        self.connect_mqtt()

        self.timer.init(period=self.send_interval, mode=Timer.PERIODIC,callback=lambda t: self.send_data(self.output_data))
        print("[System] Timer started")
        board.led.on()

    def loop(self):
        try:
            while not board.is_button_pressed():
                self.Eli.check_msg() #type:ignore
                absX, absY = map(float, self.latest_message.split(","))
                mag, angle = self.joyToMagAng(absX, absY)
                eff_l, eff_r = self.mapToEffort(mag, angle)
                self.drive.set_effort(eff_l , eff_r)
                imu_data = self.print_Imu()
                # state = self.husky.command_request_arrows()
                # print("state: "+str(state)) # type: ignore
                # if len(state) > 0: # type: ignore
                #     state_vector = state[0]
                #     # x1 and x2 are the left and right points of the arrow
                #     sx1 = state_vector[0]  # x1
                #     sx2 = state_vector[2]  # x2
                # else:
                #     print("Camera Not detecting line")
                #     sx1 = "NA"
                #     sx2 = "NA"

                t = (time.time_ns()/1000000) - self.start_time
                self.output_data = str(t)+","+str(eff_l)+","+str(eff_r)#+","+str(imu_data[0][0])+","+str(imu_data[0][1])+","+str(imu_data[1][2])#+","+str(sx1)+","+str(sx2)
                time.sleep(.01)
                print(self.output_data)
        except Exception as e:
            print("Main Loop not excecuted")
            print(e)

    def stop(self):
        self.timer.deinit()
        if self.Eli:
            self.Eli.disconnect()
        print("[System] Timer and MQTT disconnected")
        board.led_off()
        self.drive.set_effort(0,0)