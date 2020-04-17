from __future__ import print_function
import can
import cantools
import threading
from pynput import keyboard

can_bus = can.interface.Bus(bustype='socketcan',channel='vcan0',bitrate=250000)

def _accelerate():
   
    message = can.Message(arbitration_id= 0x20, data=[10,0,0,0], is_extended_id=False)
    print("Engine speed accelerated to 10kmph")
    try:
        can_bus.send(message)
        #print(" 0x20 Message sent on {}".format(can_bus.channel_info))
    except can.CanError:
        print("Message NOT sent")

def _accelerate2():
   
    message = can.Message(arbitration_id= 0x20, data=[20,0,0,0], is_extended_id=False)
    print("Engine speed accelerated to 20kmph")
    try:
        can_bus.send(message)
        #print(" 0x20 Message sent on {}".format(can_bus.channel_info))
    except can.CanError:
        print("Message NOT sent")
 
def _break():
   
    message = can.Message(arbitration_id= 0x30, data=[0,0,0,0], is_extended_id=False)
    print("Engine speed accelerated to 0kmph")
    try:
        can_bus.send(message)
        #print(" 0x30 Message sent on {}".format(can_bus.channel_info))
    except can.CanError:
        print("Message NOT sent")


def on_press(key):
    try:
        if key.char == 'b': 
            _accelerate()
        if key.char == 'c':
            _accelerate2()
        if key.char == 'd':
            _break() 
        if key == keyboard.Key.esc:
            return False
    except AttributeError:
        print(" Unknown Key Event")
        
def on_Key():
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

if __name__ == '__main__':
    #instruction()
    on_Key()
    
            
           