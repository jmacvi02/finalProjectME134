import pygame
import time

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
    
    time.sleep(1)  # Wait for 1 second before updating again

pygame.quit()
