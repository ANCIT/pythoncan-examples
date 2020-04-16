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
		if response.arbitration_id == 0x02:  
			# Message ID : 0x03 to initialize accelerator and break
			message = can.Message(arbitration_id=0x03, data=[2,2,2,2,2,2,2,2], is_extended_id=False)
			print("Accelerator and Break are initilised")
			try:
				can_bus.send(message)
				print(" 0x03 Message sent on {}".format(can_bus.channel_info))
			except can.CanError:
				print("Message NOT sent")

def on_press(key):
    
    print("Key Event Identified")
    if key.char == 'a':
        # handles if key press is a to ON the engine
            
	  # Message ID : 0x02  
            message = can.Message(arbitration_id=0x02, data=[1,1,1,1,1,1,1,1], is_extended_id=False)
            print("Engine is ON")
            try:
                task = can_bus.send_periodic(message,1.0) # cycle time
                print(" 0x02 Message sent on {}".format(can_bus.channel_info))
            except can.CanError:
                print("Message NOT sent")


def on_Key():
	keyboard.Listener(on_press=on_press).start()

def sendMessage():
			# Message ID : 0x10
			message = can.Message(arbitration_id=0x10, data=[0,0,0,0,0,0,0,0], is_extended_id=False)
			try:
				can_bus.send(message)
				print(" 0x10 Message sent on {}".format(can_bus.channel_info))
			except can.CanError:
				print("Message NOT sent")

if __name__ == '__main__':

	sendMessage()
	on_Key()
	threading.Thread(on_Message()).start()
