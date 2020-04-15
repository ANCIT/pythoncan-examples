'''
Created on 15-Apr-2020

@author: bk
'''
import time

import can
from pynput import keyboard

bus = can.interface.Bus(bustype='socketcan', channel='vcan0', bitrate=250000)

def on_press(key):
    if key.char == 'a': # for brake condition
        msg = can.Message(arbitration_id=0x011,data=[0, 1],is_extended_id=False)
        try:
            bus.send(msg)
            print("Message sent on {}".format(bus.channel_info))
        except can.CanError:
            print("Message NOT sent")
    
    if key.char == 'b': # for acceleration
        msg = can.Message(arbitration_id=0x022,data=[0, 0],is_extended_id=False)
        try:
            bus.send(msg)
            print("Message sent on {}".format(bus.channel_info))
        except can.CanError:
            print("Message NOT sent")
 
def get_current_key_input():
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()


msg = can.Message(arbitration_id=0xc0ffee,data=[0, 25, 0, 0, 0, 0, 0, 0],is_extended_id=False)
try:
    task = bus.send_periodic(msg,0.2)
    print("Message sent on {}".format(bus.channel_info))
except can.CanError:
    print("Message NOT sent")

get_current_key_input()