#ANCIT CONSULTING
#Date : Wed Apr 16
#Author : Manzoor A

from __future__ import print_function
import can
import cantools
import threading
db = cantools.db.load_file('/home/bk/git/pythoncan-examples/python-can-usecases/06_AirBagControlECU/DBC/Basic_DBCinExcel.dbc')
can_bus = can.interface.Bus(bustype='socketcan',channel='vcan0',bitrate=250000)

VehicleMotionMsg = db.get_message_by_name('VehicleMotion')
SeatbeltSystemMsg = db.get_message_by_name('SeatbeltMsg')
airbagSystemMsg = db.get_message_by_name('AirbagMsg')

def _Airbag_Not_Ready():
	# Send In-activate Airbag Message
	msgData = {'AirbagStatus':1,'AirbagCondition':0 }
	data = airbagSystemMsg.encode(msgData)
	message = can.Message(arbitration_id=airbagSystemMsg.frame_id, data=data, is_extended_id=False)
	try:
		can_bus.send(message)
		print(" Airbag is Not Ready")
	except can.CanError:
		print("Message NOT sent")
				
def _Airbag_Ready():
	# Send Idle Airbag state Message
	msgData = {'AirbagStatus':0,'AirbagCondition':0}
	data = airbagSystemMsg.encode(msgData)
	message = can.Message(arbitration_id=airbagSystemMsg.frame_id, data=data, is_extended_id=False)
	try:
		can_bus.send(message)
		print(" Airbag is Ready")
	except can.CanError:
		print("Message NOT sent")
		
def _Airbag_Release():
	# Send Airbag Release Message
	msgData = {'AirbagStatus':2,'AirbagCondition':0}
	data = airbagSystemMsg.encode(msgData)
	message = can.Message(arbitration_id=airbagSystemMsg.frame_id, data=data, is_extended_id=False)
	try:
		can_bus.send(message)
		print(" Airbag Released")
	except can.CanError:
		print("Message NOT sent")

def on_Message():
	#Initiating Vehicle Condition to Default
	seatbeltState = 0
	crashDetected = 0
	while True:
		response = can_bus.recv()
		msgData = db.decode_message(response.arbitration_id, response.data)
		if response.arbitration_id == SeatbeltSystemMsg.frame_id:
			seatbeltState = (msgData['SeatbeltStatus'])
			print(" Recieved Seatbelt Message")
			#if Seatbelt is not Worn
			if (seatbeltState == 1):
				#Trigger Inactive Airbag
				_Airbag_Not_Ready()()
			else:
				# Trigger Idle Airbag
				_Airbag_Ready()()
		
		if response.arbitration_id == VehicleMotionMsg.frame_id:
			crashDetected = (msgData['CrashDetected'])
			engineRunning = (msgData['EngineRunning'])
			print(" Recieved Vehcle Message:\t{}".format(msgData))
			#if Crash Detected, and Seatbelt is worn 
			if (crashDetected==1):
				if (seatbeltState == 0 and engineRunning==1):
					# Trigger Airbag Release
					_Airbag_Release()
				else:
					#Trigger Inactive Airbag
					_Airbag_Not_Ready()()

if __name__ == '__main__':
	threading.Thread(on_Message()).start()