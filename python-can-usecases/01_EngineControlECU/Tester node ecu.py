from __future__ import print_function
import can
import time
import cantools
from pynput import keyboard
import threading

can_bus = can.interface.Bus(bustype='socketcan',channel='vcan0',bitrate=1000000)

def on_Message():
	while True:
		response = can_bus.recv()
def on_press(key):
    print("Key Event Identified")
    if key.char == 'b':
        # handles if key press is a to ON the engine
            
	  # Message ID : 0x04 
            message = can.Message(arbitration_id=0x04, data=[20,0,0,0,0,0,0,0], is_extended_id=False)
            print("The engine speed accelerated to 20 kmph")
            try:
                can_bus.send(message)
                print(" 0x04 Message sent on {}".format(can_bus.channel_info))
            except can.CanError:
                print("Message NOT sent")
    
   

    if key.char == 'c': # handles if key press is c to accelerate to 60kmph
			# Message ID : 0x05
	    message = can.Message(arbitration_id=0x05, data=[60,0,0,0,0,0,0,0], is_extended_id=False)
	    print("The engine speed accelerated to 60kmph")
	    try:
		    can_bus.send(message)
		    print(" 0x05 Message sent on {}".format(can_bus.channel_info))
	    except can.CanError:
		    print("Message NOT sent")

    if key.char == 'd': # handles if key press is d to break
			# Message ID : 0x06
	    message = can.Message(arbitration_id=0x06, data=[0,0,0,0,0,0,0,0], is_extended_id=False)
	    print("Break has been applied and engine speed is 0kmph")
	    try:
		    can_bus.send(message)
		    print(" 0x06 Message sent on {}".format(can_bus.channel_info))
	    except can.CanError:
		    print("Message NOT sent")


def on_Key():
	keyboard.Listener(on_press=on_press).start()

def sendMessage():
    
    if __name__ == '__main__':
        
        sendMessage()
        on_Key()
        threading.Thread(on_Message()).start()
