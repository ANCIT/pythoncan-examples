#ANCIT CONSULTING
#Date : Wed Apr 29
#Author : Manzoor A

from __future__ import print_function
import can
import threading

can_bus = can.interface.Bus(bustype='socketcan',channel='vcan0',bitrate=250000)

seatbeltMsgID = 0x101
airbagMsgID = 0x102
VehicleMotionMsgID = 0x104

def _Airbag_Not_Ready():
	# Send Not Ready Airbag Message
	data = [0x01, 0, 0, 0, 0, 0, 0, 0]
	message = can.Message(arbitration_id=airbagMsgID, data=data, is_extended_id=False)
	try:
		can_bus.send(message)
		print(" Airbag is Not Ready")
	except can.CanError:
		print("Message NOT sent")
				
def _Airbag_Ready():
	# Send Airbag Ready state Message
	data = [0x00, 0, 0, 0, 0, 0, 0, 0]
	message = can.Message(arbitration_id=airbagMsgID, data=data, is_extended_id=False)
	try:
		can_bus.send(message)
		print(" Airbag is Ready")
	except can.CanError:
		print("Message NOT sent")
		
def _Airbag_Release():
	# Send Airbag Release Message
	data = [0x02, 0, 0, 0, 0, 0, 0, 0]
	message = can.Message(arbitration_id=airbagMsgID, data=data, is_extended_id=False)
	try:
		can_bus.send(message)
		print(" Airbag Released")
	except can.CanError:
		print("Message NOT sent")

def on_Message():
	while True:
		response = can_bus.recv()
		if response.arbitration_id == seatbeltMsgID:
			#seatbeltWorn = bool(response.data[0] & 1)  #0th Bit of 0th Byte
			seatbeltWorn = (response.data[0] == 0x01) 
			
			print(" Recieved Seatbelt Message")
			if (seatbeltWorn):
				# Trigger Airbag Ready
				_Airbag_Ready()
			else:
				#Trigger Airbag Not Ready
				_Airbag_Not_Ready()
		
		if response.arbitration_id == VehicleMotionMsgID:
			crashDetected = (bool(response.data[0] & (1)))  #0th Bit of 0th Byte
			engineRunning = (bool(response.data[0] & (1<<1)))  #1st Bit of 0th Byte
			
			print(" Recieved Vehcle Motion Message")
			#if Crash Detected, and Seatbelt is worn 
			if (crashDetected):
				if (seatbeltWorn and engineRunning):
					# Trigger Airbag Release
					_Airbag_Release()
				else:
					#Trigger Airbag Not Ready
					_Airbag_Not_Ready()

if __name__ == '__main__':
	threading.Thread(on_Message()).start()