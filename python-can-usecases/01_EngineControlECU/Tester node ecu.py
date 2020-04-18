from __future__ import print_function
import can
import cantools
import threading
from pynput import keyboard

can_bus = can.interface.Bus(bustype='socketcan',channel='vcan0',bitrate=250000)

def _accelerate():
   
    message = can.Message(arbitration_id= 0x20, data=[10], is_extended_id=False)
    print("Accelerated to 10kmph")
    try:
        can_bus.send(message)
        #print(" 0x20 Message sent on {}".format(can_bus.channel_info))
    except can.CanError:
        print("Message not sent")

def _accelerate2():
   
    message = can.Message(arbitration_id= 0x20, data=[20], is_extended_id=False)
    print("Accelerated to 20kmph")
    try:
        can_bus.send(message)
        #print(" 0x20 Message sent on {}".format(can_bus.channel_info))
    except can.CanError:
        print("Message NOT sent")
 
def _break():
   
    message = can.Message(arbitration_id= 0x30, data=[0], is_extended_id=False)
    print("Break Applied")
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
        
def on_Message():
    #Initiating Vehicle Condition to Default
    flagAcc1 = True
    flagAcc2 = True
    flagBrk = True
    
    while True:
        response = can_bus.recv()
        data = response.data
        if response.arbitration_id == 0x010:   
            if (response.data == bytearray(b'\n\x01\x00\x00')) and flagAcc1: 
                print("Engine Speed Updated: 10")
                flagAcc1 = False
                flagAcc2 = True
                flagBrk = True
            if (response.data == bytearray(b'\x14\x01\x00\x00')) and flagAcc2:
                print("Engine Speed Updated: 20")
                flagAcc1 = True
                flagAcc2 = False
                flagBrk = True
            if (response.data == bytearray(b'\x00\x01\x00\x00')) and flagBrk:
                print("Engine Speed Updated: 0")
                flagAcc1 = True
                flagAcc2 = True
                flagBrk = False
        
def on_Key():
#     with keyboard.Listener(on_press=on_press) as listener:
#         listener.join()
    keyboard.Listener(on_press=on_press).start()

if __name__ == '__main__':
    #instruction()
    on_Key()
    threading.Thread(on_Message()).start()
    
            
           