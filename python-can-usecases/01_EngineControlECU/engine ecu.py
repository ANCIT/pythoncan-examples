from __future__ import print_function
import can
import time
import cantools
from pynput import keyboard
import threading

can_bus = can.interface.Bus(bustype='socketcan',channel='vcan0',bitrate=1000000)

def engine_on():
	
    message = can.Message(arbitration_id=0x10, data=[0,0,0,1], is_extended_id=False)
    print("Engine is ON")
    try:
        can_bus.send(message)
        #initialize() # cycle time
        #print(" 0x10 Message sent on {}".format(can_bus.channel_info))
    except can.CanError:
        print("Message NOT sent")

def engine_off():
			# Message ID : 0x10
	message = can.Message(arbitration_id=0x10, data=[0,0,0,0], is_extended_id=False)
	print("Engine is off")
	try:
		can_bus.send(message)
		#print(" 0x10 Message sent on {}".format(can_bus.channel_info))
	except can.CanError:
		print("Message NOT sent")

def apply_break():
	message = can.Message(arbitration_id=0x10, data=[0,0,0,1], is_extended_id=False)
	print("Break Applied")
	try:
		can_bus.send(message)
		#print(" 0x10 Message sent on {}".format(can_bus.channel_info))
	except can.CanError:
		print("Message NOT sent")
		
def apply_accilerate1():
	message = can.Message(arbitration_id=0x10, data=[0,0,10,1], is_extended_id=False)
	print("Accileration : 10")
	try:
		can_bus.send(message)
		#print(" 0x10 Message sent on {}".format(can_bus.channel_info))
	except can.CanError:
		print("Message NOT sent")	

def apply_accilerate2():
	message = can.Message(arbitration_id=0x10, data=[0,0,20,1], is_extended_id=False)
	print("Accileration : 20")
	try:
		can_bus.send(message)
		#print(" 0x10 Message sent on {}".format(can_bus.channel_info))
	except can.CanError:
		print("Message NOT sent")	

def on_Message():
	#Initiating Vehicle Condition to Default
	while True:
		response = can_bus.recv()
		data = response.data
		if response.arbitration_id == 0x020:	
			if response.data == bytearray(b'\n\x00\x00\x00'):
				apply_accilerate1()
			if response.data == bytearray(b'\x14\x00\x00\x00'):
				apply_accilerate2()
	
		if response.arbitration_id == 0x030:
			apply_break()

if __name__ == '__main__':

	engine_off()
	engine_on()
	threading.Thread(on_Message()).start()
	
	#threading.Thread(on_Message()).start()
