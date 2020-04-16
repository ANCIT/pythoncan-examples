#Date : Wed Apr 15 2020
#Author : Manzoor A
#Script to Test Airbag ECU Simulation

from __future__ import print_function
import can
import cantools
import threading
from pynput import keyboard

db = cantools.db.load_file('airbag_MainBus.dbc')
can_bus = can.interface.Bus(bustype='socketcan',channel='vcan0',bitrate=250000)
 
VehicleMotionMsg = db.get_message_by_name('VehicleMotion')
SeatbeltSystemMsg = db.get_message_by_name('SeatbeltSystem')
def _SeatbeltUnock():
    # Send Seatbelt Unlock Message
    data = SeatbeltSystemMsg.encode({'SeatbeltState':0})
    message = can.Message(arbitration_id=SeatbeltSystemMsg.frame_id, data=data, is_extended_id=False)
    try:
        can_bus.send(message)
        print(" Seatbelt Unlocked:\t\t{}".format(data))
    except can.CanError:
        print("Message NOT sent")
 
def _SeatbeltLock():
    # Send Seatbelt Lock Message
    data = SeatbeltSystemMsg.encode({'SeatbeltState':1})
    message = can.Message(arbitration_id=SeatbeltSystemMsg.frame_id, data=data, is_extended_id=False)
    try:
        can_bus.send(message)
        print(" Seatbelt Locked:\t\t{}".format(data))
    except can.CanError:
        print("Message NOT sent")
         
def _crashDetected():
    # Send Crash Detected Message
    data = VehicleMotionMsg.encode({'Velocity':10,'CrashDetected':1,'EngineRunning':1})
    message = can.Message(arbitration_id=VehicleMotionMsg.frame_id, data=data, is_extended_id=False)
    try:
        can_bus.send(message)
        print(" Crash Detected:\t\t{}".format(data))
    except can.CanError:
        print("Message NOT sent")
 
def _crashFree():
    # Send Crash Detected Message
    data = VehicleMotionMsg.encode({'Velocity':10,'CrashDetected':0,'EngineRunning':1})
    message = can.Message(arbitration_id=VehicleMotionMsg.frame_id, data=data, is_extended_id=False)
    try:
        can_bus.send(message)
        print(" Crash Detected:\t\t{}".format(data))
    except can.CanError:
        print("Message NOT sent")
 
def on_press(key):
    print("Key Event Identified")
    try:
        if key.char == 'u': # if key 'u' pressed
            _SeatbeltUnock()
        if key.char == 'c': # if key 'c' pressed
            _crashDetected()
        if key.char == 'f': # if lkey 'c' pressed
            _crashFree()
        if key.char == 'l': # if key 'l' pressed
            _SeatbeltLock()
        if key == keyboard.Key.esc:  # if esc is pressed, terminate
            return False    # Stop listener   
    except AttributeError:
        pass
#                 
def on_Key():
    # Collect events until on_press return fail
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

if __name__ == '__main__':
    on_Key()
