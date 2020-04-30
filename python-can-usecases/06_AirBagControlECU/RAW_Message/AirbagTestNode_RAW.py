#Date : Wed Apr 29 2020
#Author : Manzoor A
#Script to Test Airbag ECU Simulation

import can
import threading
from pynput import keyboard

can_bus = can.interface.Bus(bustype='socketcan',channel='vcan0',bitrate=250000)

seatbeltMsgID = 0x101
airbagMsgID = 0x102
VehicleMotionMsgID = 0x104

def _SeatbeltUnock():
    # Send Seatbelt Unlock Message
    data = [0x00, 0, 0, 0, 0, 0, 0, 0]
    message = can.Message(arbitration_id=seatbeltMsgID, data=data, is_extended_id=False)
    try:
        can_bus.send(message)
        print(" Seatbelt Unlocked")
    except can.CanError:
        print("Message NOT sent")
 
def _SeatbeltLock():
    # Send Seatbelt Lock Message
    data = [0x01, 0, 0, 0, 0, 0, 0, 0]
    message = can.Message(arbitration_id=seatbeltMsgID, data=data, is_extended_id=False)
    try:
        can_bus.send(message)
        print(" Seatbelt Locked")
    except can.CanError:
        print("Message NOT sent")
         
def _crashDetected():
    # Send Crash Detected Message
    data = [0x03, 0, 0x64, 0, 0, 0, 0, 0]
    message = can.Message(arbitration_id=VehicleMotionMsgID, data=data, is_extended_id=False)
    try:
        can_bus.send(message)
        print(" Crash with Engine ON")
    except can.CanError:
        print("Message NOT sent")
 
def _crashFree():
    # Send Crash Detected Message
    data = [0x02, 0, 0x64, 0, 0, 0, 0, 0]
    message = can.Message(arbitration_id=VehicleMotionMsgID, data=data, is_extended_id=False)
    try:
        can_bus.send(message)
        print(" No Crash with Engine ON")
    except can.CanError:
        print("Message NOT sent")

def _engineOffCrash():
    # Send Engine off and Crash Detected Message
    data = [0x01, 0, 0x00, 0, 0, 0, 0, 0]
    message = can.Message(arbitration_id=VehicleMotionMsgID, data=data, is_extended_id=False)
    try:
        can_bus.send(message)
        print(" Crash with Engine Off")
    except can.CanError:
        print("Message NOT sent")
 
def on_press(key):
    try:
        if key.char == 'l': # if key 'l' pressed
            _SeatbeltLock()
        if key.char == 'u': # if key 'u' pressed
            _SeatbeltUnock()
        if key.char == 'c': # if key 'c' pressed
            _crashDetected()
        if key.char == 'o': # if key 'f' pressed
            _engineOffCrash()
        if key.char == 'f': # if key 'c' pressed
            _crashFree()
        if key == keyboard.Key.esc:  # if esc is pressed, terminate
            return False    # Stop listener   
    except AttributeError:
        print(" Unknown Key Event")
#                 
def on_Key():
    # Collect events until on_press return fail
#     with keyboard.Listener(on_press=on_press) as listener:
#         listener.start()
    keyboard.Listener(on_press=on_press).start()
        
        
def on_Message():
    while True:
        response = can_bus.recv()
        if response.arbitration_id == airbagMsgID:
            airbagNotReady = bool(response.data[0] & 1)         #0th Bit of 0th Byte
            airbagReleased = bool(response.data[0] & (1<<1))    #1st Bit of 0th Byte
            
            #   (airbagReleased):    0000 0010
            #             (1<<1):    0000 0010
            #                        0000 0010
                      
            if (airbagReleased):
            #if(response.data[0] == 0x02):
                print("\t\t\tAirbag Released")
                
            elif(airbagNotReady):                        
            #elif(response.data[0] == 0x01):
                print("\t\t\tAirbag is Not Ready")
                
            elif (airbagNotReady is not True):
            #elif(response.data[0] == 0x00):
                print("\t\t\tAirbag is Ready")   
                
def instruction():
    print("Simulation Keys:\n\
            l: Lock Seatbelt\n\
            u: Unock Seatbelt\n\
            c: Crash with Engine On\n\
            o: Crash with Engine Off\n\
            f: Crash free with Engine On\n")
    print("--Test Msg--\t\t--Evaluated Msg--")

if __name__ == '__main__':
    instruction()
    on_Key()
    threading.Thread(on_Message()).start()
    