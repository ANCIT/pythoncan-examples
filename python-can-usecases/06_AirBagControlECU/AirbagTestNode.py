#Date : Wed Apr 16 2020
#Author : Manzoor A
#Script to Test Airbag ECU Simulation

from __future__ import print_function
import can
import cantools
import threading
from pynput import keyboard

db = cantools.db.load_file('DBC/Basic_DBC.dbc')
can_bus = can.interface.Bus(bustype='socketcan',channel='vcan0',bitrate=250000)
 
VehicleMotionMsg = db.get_message_by_name('VehicleMotion')
SeatbeltSystemMsg = db.get_message_by_name('SeatbeltMsg')
airbagSystemMsg = db.get_message_by_name('AirbagMsg')

def _SeatbeltUnock():
    # Send Seatbelt Unlock Message
    data = SeatbeltSystemMsg.encode({'SeatbeltStatus':0,'SeatbeltLock':0})
    message = can.Message(arbitration_id=SeatbeltSystemMsg.frame_id, data=data, is_extended_id=False)
    try:
        can_bus.send(message)
        print(" Seatbelt Unlocked")
    except can.CanError:
        print("Message NOT sent")
 
def _SeatbeltLock():
    # Send Seatbelt Lock Message
    data = SeatbeltSystemMsg.encode({'SeatbeltStatus':1,'SeatbeltLock':0})
    message = can.Message(arbitration_id=SeatbeltSystemMsg.frame_id, data=data, is_extended_id=False)
    try:
        can_bus.send(message)
        print(" Seatbelt Locked")
    except can.CanError:
        print("Message NOT sent")
         
def _crashDetected():
    # Send Crash Detected Message
    data = VehicleMotionMsg.encode({'Velocity':10,'CrashDetected':1,'EngineRunning':1})
    message = can.Message(arbitration_id=VehicleMotionMsg.frame_id, data=data, is_extended_id=False)
    try:
        can_bus.send(message)
        print(" Crash with Engine ON")
    except can.CanError:
        print("Message NOT sent")
 
def _crashFree():
    # Send Crash Detected Message
    data = VehicleMotionMsg.encode({'Velocity':10,'CrashDetected':0,'EngineRunning':1})
    message = can.Message(arbitration_id=VehicleMotionMsg.frame_id, data=data, is_extended_id=False)
    try:
        can_bus.send(message)
        print(" No Crash with Engine ON")
    except can.CanError:
        print("Message NOT sent")

def _engineOffCrash():
    # Send Engine off and Crash Detected Message
    data = VehicleMotionMsg.encode({'Velocity':0,'CrashDetected':1,'EngineRunning':0})
    message = can.Message(arbitration_id=VehicleMotionMsg.frame_id, data=data, is_extended_id=False)
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
        msgData = db.decode_message(response.arbitration_id, response.data)
        if response.arbitration_id == airbagSystemMsg.frame_id:
            airbagState = (msgData['AirbagStatus'])
            if (airbagState == 'Ready'):
                # Trigger Idle Airbag
                print("\t\t\tAirbag is Ready")
            if (airbagState == 'NotReady'):
                #Trigger Inactive Airbag
                print("\t\t\tAirbag is Not Ready")
            if (airbagState == 'Released'):
                # Trigger Release Airbag
                print("\t\t\tAirbag Released")    
                
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
    