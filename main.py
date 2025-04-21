from xbox_controlled_XRP import TeamWDreamBot

wifi = {'ssid':"Tufts_Robot",'pass':''}
#wifi = Fairmount_Wireless = {'ssid':'Verizon_SLD76X','pass':'dice7-gee-prate'}
#wifi = {'ssid':'Natalie07','pass':'Blue126Kitchen'}
IP_add = '10.243.115.106'

bot = TeamWDreamBot(wifi, IP_add)
bot.start()
bot.loop() #loops until USER botton pressed
bot.stop()