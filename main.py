# Authors:      Darrien, Eli Houlton, Joel MacVicar 
# Date Updated: 5/7/2025
# Name :        main.py
# Purpose:      A driver file to enact one of 3 different control methods developed in this project. 
#               To enact a section, uncomment the corresponding code chunk below

#for xbox control
#from xbox_controlled.xbox_controlled_XRP import TeamWDreamBot
#for classic control
from classicControl.offsetLineFollow import lineFollow
from XRPLib.differential_drive import DifferentialDrive
from XRPLib.board import Board
from MQTT_class import Mqtt_Client
from XRPLib.imu import IMU
from XRPLib.rangefinder import Rangefinder
from remoteMLControl.remoteMLControl import remoteMLControl
import os
import gc

##########################
##### Remote Control #####
##########################
# wifi = {'ssid':"Tufts_Robot",'pass':''}
# # wifi = Fairmount_Wireless = {'ssid':'Verizon_SLD76X','pass':'dice7-gee-prate'}
# # #wifi = {'ssid':'Natalie07','pass':'Blue126Kitchen'}
# IP_add = '10.243.114.200' #Tufts_Secure
# #IP_add = '10.247.137.157' #Tufts Robot
# # IP_add = "192.168.1.235" #home

# wifi = {'ssid':"Tufts_Robot",'pass':''}
# #wifi = Fairmount_Wireless = {'ssid':'Verizon_SLD76X','pass':'dice7-gee-prate'}
# #wifi = {'ssid':'Natalie07','pass':'Blue126Kitchen'}
# #IP_add = '10.243.115.106' #Tufts_Secure
# IP_add = '10.247.137.61' #Tufts Robot
# #IP_add = "192.168.1.235" #home

# bot = TeamWDreamBot(wifi, IP_add)
# bot.start()
# bot.loop() #loops until USER botton pressed
# bot.stop()


###########################
##### Classic Control #####
###########################
# #initializing line following behavior
# lF = lineFollow()
# diffDrive = DifferentialDrive.get_default_differential_drive()
# board = Board.get_default_board()
# # for data collection via mqtt
# wifi = {'ssid':"Tufts_Robot",'pass':''}
# IP_add = '10.243.114.200' #Tufts_Secure

# #while not in the halt state
# while not board.is_button_pressed():
#     lF.transition()
#     lF.execute()

# #halt state
# diffDrive.stop()

#####################################
##### Remote Trained ML Control #####
#####################################

# gc.collect()
# diffDrive = DifferentialDrive.get_default_differential_drive()
# diffDrive.stop()
# board = Board.get_default_board()
# # for data collection via mqtt
# wifi = {'ssid':"Tufts_Robot",'pass':''}
# IP_add = '10.243.114.200' #Tufts_Secure
# pipeLine = Mqtt_Client(wifi, IP_add)
# mLCont = remoteMLControl()


# #while not in the halt state
# while not board.is_button_pressed():
#     #print("controlling")
#     inputs = pipeLine.pipeLine()
#     eff = mLCont.MLPred(inputs)
#     print(f"effL: {eff[0]}, effR: {eff[1]}")
#     diffDrive.set_effort(eff[0], eff[1])

# #halt state
# pipeLine.stop()
# diffDrive.stop()



######################################
##### Classic Trained ML Control #####
######################################

#we need to put the classic model control here

