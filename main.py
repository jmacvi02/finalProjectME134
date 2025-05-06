from xbox_controlled.xbox_controlled_XRP import TeamWDreamBot
from classicControl.offsetLineFollow import lineFollow
from XRPLib.differential_drive import DifferentialDrive
from XRPLib.board import Board

import time

wifi = {'ssid':"Tufts_Robot",'pass':''}
# wifi = Fairmount_Wireless = {'ssid':'Verizon_SLD76X','pass':'dice7-gee-prate'}
# #wifi = {'ssid':'Natalie07','pass':'Blue126Kitchen'}
IP_add = '10.243.114.200' #Tufts_Secure
#IP_add = '10.247.137.157' #Tufts Robot
# IP_add = "192.168.1.235" #home

bot = TeamWDreamBot(wifi, IP_add)
bot.start()
bot.loop() #loops until USER botton pressed
bot.stop()


# lF = lineFollow()
# diffDrive = DifferentialDrive.get_default_differential_drive()
# board = Board.get_default_board()

# while not board.is_button_pressed():
#     lF.transition()
#     lF.execute()
#     time.sleep(0.05)
#     #diffDrive.set_speed(35, 30)
#     # print("in loop")

# diffDrive.stop()


# wifi = {'ssid':"Tufts_Robot",'pass':''}
# #wifi = Fairmount_Wireless = {'ssid':'Verizon_SLD76X','pass':'dice7-gee-prate'}
# #wifi = {'ssid':'Natalie07','pass':'Blue126Kitchen'}
# #IP_add = '10.243.115.106' #Tufts_Secure
# IP_add = '10.247.137.61' #Tufts Robot
# #IP_add = "192.168.1.235" #home

