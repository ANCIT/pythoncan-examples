from __future__ import print_function
import can
import time
import cantools
from pynput import keyboard
import threading

can_bus = can.interface.Bus(bustype='socketcan',channel='vcan0',bitrate=1000000)

def engine_on():
	
    message = can.Message(arbitration_id=0x10, data=[0,1,0,0], is_extended_id=False)
    try:
        periodicTask.modify_data(message)
        print("Engine is ON")
    except can.CanError:
        print("Message NOT sent")

def apply_break():
	message = can.Message(arbitration_id=0x10, data=[0,1,0,0], is_extended_id=False)
	try:
		#can_bus.send(message)
		periodicTask.modify_data(message)
		print("Break Applied")
		#print(" 0x10 Message sent on {}".format(can_bus.channel_info))
	except can.CanError:
		print("Message NOT sent")
		
def apply_accilerate1():
	message = can.Message(arbitration_id=0x10, data=[10,1,0,0], is_extended_id=False)
	try:
		#can_bus.send(message)
		periodicTask.modify_data(message)
		print("Accileration : 10")
		#print(" 0x10 Message sent on {}".format(can_bus.channel_info))
	except can.CanError:
		print("Message NOT sent")	

def apply_accilerate2():
	message = can.Message(arbitration_id=0x10, data=[20,1,0,0], is_extended_id=False)
	try:
		#can_bus.send(message)
		periodicTask.modify_data(message)
		print("Accileration : 20")
		#print(" 0x10 Message sent on {}".format(can_bus.channel_info))
	except can.CanError:
		print("Message NOT sent")	

def on_Message():
	#Initiating Vehicle Condition to Default
	while True:
		response = can_bus.recv()
		data = response.data
		if response.arbitration_id == 0x020:	
			if response.data == bytearray(b'\n'):
				apply_accilerate1()
			if response.data == bytearray(b'\x14'):
				apply_accilerate2()
	
		if response.arbitration_id == 0x030:
			apply_break()
			
def intiateVehicle():
	message = can.Message(arbitration_id=0x10, data=[0,0,0,0], is_extended_id=False)
	try:
		task = can_bus.send_periodic(message, 1.0)
		print("Vehicle Initiated")
		return task
		#print(" 0x10 Message sent on {}".format(can_bus.channel_info))
	except can.CanError:
		print("Message NOT sent")

if __name__ == '__main__':
	
	periodicTask = intiateVehicle()
	engine_on()
	threading.Thread(on_Message()).start()
	
	#threading.Thread(on_Message()).start()
	
	
	
