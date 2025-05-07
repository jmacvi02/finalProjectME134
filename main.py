# Authors:      Eli Houlton and Joel MacVicar 
# Date Updated: 5/7/2025
# Name :        main.py
# Purpose:      A driver file to enact one of 4 different control methods developed in this project. 
#               To enact a section, uncomment the corresponding code chunk below

#from xbox_controlled.xbox_controlled_XRP import TeamWDreamBot
from classicControl.offsetLineFollow import lineFollow
from XRPLib.differential_drive import DifferentialDrive
from XRPLib.board import Board

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
lF = lineFollow()
diffDrive = DifferentialDrive.get_default_differential_drive()
board = Board.get_default_board()

while not board.is_button_pressed():
    lF.transition()
    lF.execute()

diffDrive.stop()

#####################################
##### Remote Trained ML Control #####
#####################################

#we need to put the remote model control here

######################################
##### Classic Trained ML Control #####
######################################

#we need to put the classic model control here

