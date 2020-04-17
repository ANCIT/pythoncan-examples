from __future__ import print_function
import can
import time
import cantools
from pynput import keyboard
import threading

can_bus = can.interface.Bus(bustype='socketcan',channel='vcan0',bitrate=1000000)

def initialize():
			message = can.Message(arbitration_id=0x10, data=[2,2,2,2,2,2,2,2], is_extended_id=False)
			print("Accelerator and Break are initilized")
			try:
				can_bus.send(message)
				print(" 0x10 Message sent on {}".format(can_bus.channel_info))
			except can.CanError:
				print("Message NOT sent")

def engine_on():
	
            message = can.Message(arbitration_id=0x10, data=[1,1,1,1,1,1,1,1], is_extended_id=False)
            print("Engine is ON")
            try:
                can_bus.send(message)
                initialize() # cycle time
                print(" 0x10 Message sent on {}".format(can_bus.channel_info))
            except can.CanError:
                print("Message NOT sent")




def engine_off():
			# Message ID : 0x10
			message = can.Message(arbitration_id=0x10, data=[0,0,0,0,0,0,0,0], is_extended_id=False)
			print("Engine is off"")
			try:
				can_bus.send(message)
				print(" 0x10 Message sent on {}".format(can_bus.channel_info))
			except can.CanError:
				print("Message NOT sent")

if __name__ == '__main__':

	Engine_off()
	Engine_on()
	
	#threading.Thread(on_Message()).start()
