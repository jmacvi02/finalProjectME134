# MUST RUN THIS AS AN EXE TO ACCESS BLE- INSTALL PYINSTALLER AND RUN
# pyinstaller --onefile xrp_ble_connect.

import asyncio
import pygame
from bleak import BleakClient, BleakScanner

# UUIDs from your PestoLinkAgent (adjust as needed)
UART_SERVICE_UUID = "27df26c5-83f4-4964-bae0-d7b7cb0a1f54"
UART_TX_UUID = "266d9d74-3e10-4fcd-88d2-cb63b5324d0c"  # robot → computer (notifications)
UART_RX_UUID = "452af57e-ad27-422c-88ae-76805ea641a9"  # computer → robot (writes)

ROBOT_NAME = "XRP"  # Replace with your robot name

# Function to handle incoming telemetry (optional, for receiving data)
def notification_handler(sender, data):
    print(f"Telemetry: {data}")

# Function to send joystick data
async def send_joystick_data(client):
    # Initialize Pygame and the joystick
    pygame.init()
    pygame.joystick.init()

    if pygame.joystick.get_count() == 0:
        print("No joystick found!")
        return

    joystick = pygame.joystick.Joystick(0)
    joystick.init()

    try:
        while True:
            # Process events to update the joystick input
            pygame.event.pump()

            # Get joystick axes values (typically -1 to 1)
            x_axis = int((joystick.get_axis(0) + 1) * 127)  # Map from -1:1 to 0:255
            y_axis = int((joystick.get_axis(1) + 1) * 127)  # Map from -1:1 to 0:255
            throttle = int((joystick.get_axis(2) + 1) * 127)  # Map from -1:1 to 0:255
            button = joystick.get_button(0)  # Example: Button 0 state (0 or 1)

            # Build the 20-byte packet to send
            packet = bytearray(20)
            packet[0] = 0x01  # Start byte
            packet[1] = x_axis  # X-axis
            packet[2] = y_axis  # Y-axis
            packet[3] = 127  # Z-axis (neutral)
            packet[4] = throttle  # Throttle
            packet[5] = button  # Button state (0 or 1)
            packet[6] = 0  # Button high byte (could expand if you have more buttons)
            # packet[7..19] remain zeros

            # Send joystick data over Bluetooth to the robot
            print(f"Sending joystick packet: {packet}")
            await client.write_gatt_char(UART_RX_UUID, packet)

            await asyncio.sleep(0.1)  # Delay to avoid spamming the Bluetooth connection

    except KeyboardInterrupt:
        print("Joystick control stopped.")

    finally:
        pygame.quit()

async def main():
    # Scan for Bluetooth devices
    devices = await BleakScanner.discover()
    robot_device = None
    for d in devices:
        if d.name and d.name.startswith(ROBOT_NAME):
            robot_device = d
            break

    if not robot_device:
        print("Robot not found!")
        return

    print(f"Connecting to {robot_device.address}...")
    async with BleakClient(robot_device) as client:
        # Subscribe to notifications (optional, if you want to handle robot telemetry)
        await client.start_notify(UART_TX_UUID, notification_handler)

        # Send joystick data
        await send_joystick_data(client)

        # Stop notifications when done
        await client.stop_notify(UART_TX_UUID)

# Run the main function
asyncio.run(main())
