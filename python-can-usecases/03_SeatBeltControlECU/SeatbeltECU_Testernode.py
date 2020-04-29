'''
Created on 15-Apr-2020

@author: bk
'''

import can
from pynput import keyboard
import threading

seatbeltMsgID = 0x101
ReqSeatbeltMsgID = 0x107

bus = can.interface.Bus(bustype='socketcan', channel='vcan0', bitrate=250000)

def on_press(key):
    try:
        if key.char == 'a': # for brake condition
            msg = can.Message(arbitration_id=ReqSeatbeltMsgID,data=[1, 0],is_extended_id=False)
            try:
                bus.send(msg)
                print("Message sent: \tTrigger Seatbelt Lock")
            except can.CanError:
                print("Message NOT sent")
        
        if key.char == 'b': # for acceleration
            msg = can.Message(arbitration_id=ReqSeatbeltMsgID,data=[0, 0],is_extended_id=False)
            try:
                bus.send(msg)
                print("Message sent: \tTrigger Seatbelt Un-lock")
            except can.CanError:
                print("Message NOT sent")
    except AttributeError:
        pass
 
def on_Key():
#     with keyboard.Listener(on_press=on_press) as listener:
#         listener.join()
    keyboard.Listener(on_press=on_press).start()

def on_Message():
    while True:
        response = bus.recv()
        msgData = response.data
        if response.arbitration_id == seatbeltMsgID:       #from Seatbelt Message
            if (msgData[0] == 0x01):
                #if Seatbelt is Locked
                print("\tResponse: Seatbelt Locked")
            
            if (msgData[0] == 0x00):
                #if Seatbelt is Locked
                print("\tResponse: Seatbelt Un-locked")

if __name__ == '__main__':
    print("Press keys 'a' or 'b' to Test\n")
    on_Key()
    threading.Thread(on_Message()).start()