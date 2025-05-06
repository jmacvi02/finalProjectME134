import pygame
import time

import paho.mqtt.client as mqtt 
import time

broker_address='10.247.137.123'

Joel = mqtt.Client(client_id="team_w_dream", protocol=mqtt.MQTTv311)

Joel.connect(broker_address, 1883) 

# Initialize Pygame and Joystick
pygame.init()
pygame.joystick.init()

# Check for connected controllers
if pygame.joystick.get_count() > 0:
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    print(f"Using Controller: {joystick.get_name()}")
else:
    print("No controller detected!")
    pygame.quit()
    exit()

# Main loop
running = True
while running:
    pygame.event.pump()  # Process events to get the latest joystick values
    
    axis_0 = joystick.get_axis(0)  # Left joystick Y-axis
    axis_1 = -1*joystick.get_axis(1)  # Right joystick Y-axis
    
    print(f"left/right: {axis_0:.2f}, down/up: {axis_1:.2f}")  # Print values rounded to 2 decimal places
    Joel.publish("topic",str(round(axis_0,2))+","+str(round(axis_1,2))) #LR, UD
    time.sleep(.01)  # Wait for 1 second before updating again

pygame.quit()
Joel.disconnect()
