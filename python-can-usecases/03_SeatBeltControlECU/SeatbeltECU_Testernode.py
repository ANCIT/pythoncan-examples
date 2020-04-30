'''
Created on 15-Apr-2020

@author: bk
'''

import can
from pynput import keyboard
import threading

bus = can.interface.Bus(bustype='socketcan', channel='vcan0', bitrate=250000)

seatbeltMsgID = 0x101
brakeMsgID = 0x105
accelerationMsgID = 0x106

def on_press(key):
    try:
        if key.char == 'a': # for acceleration
            message = can.Message(arbitration_id=accelerationMsgID,data=[0, 0],is_extended_id=False)
            try:
                bus.send(message)
                print("Message sent: \tVehicle Stopped Moving")
            except can.CanError:
                print("Message NOT sent")
        if key.char == 'b': # for brake condition
            message = can.Message(arbitration_id=brakeMsgID,data=[1, 0],is_extended_id=False)
            try:
                bus.send(message)
                print("Message sent: \tSudden Break Applaid")
            except can.CanError:
                print("Message NOT sent")
    except AttributeError:
        pass
 
def on_Key():
    keyboard.Listener(on_press=on_press).start()

def on_Message():
    while True:
        response = bus.recv()
        msgData = response.data
        if response.arbitration_id == seatbeltMsgID:    # from Seatbelt Message
            seatbeltLock = msgData[0] & (1<<1)          # 1st bit of 0th Byte
            if (seatbeltLock):
                #if Seatbelt is Locked
                print("\tResponse: Seatbelt Locked")
            else:
                #if Seatbelt is Not Locked
                print("\tResponse: Seatbelt Un-locked")

if __name__ == '__main__':
    print("Press keys 'a' or 'b' to Test\n")
    on_Key()
    threading.Thread(on_Message()).start()