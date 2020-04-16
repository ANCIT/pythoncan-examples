#ANCIT CONSULTING
#Date : Wed Apr 16
#Author : Manzoor A

from __future__ import print_function
import can
import cantools
import threading
db = cantools.db.load_file('/home/bk/git/pythoncan-examples/python-can-usecases/06_AirBagControlECU/airbag_MainBus.dbc')
can_bus = can.interface.Bus(bustype='socketcan',channel='vcan0',bitrate=250000)

VehicleMotionMsg = db.get_message_by_name('VehicleMotion')
SeatbeltSystemMsg = db.get_message_by_name('SeatbeltSystem')
airbagSystemMsg = db.get_message_by_name('AirbagSystem')

def _inactiveAirbag():
	# Send In-activate Airbag Message
	msgData = {'airbagState':1,'AirbagCondition':0}
	data = airbagSystemMsg.encode(msgData)
	message = can.Message(arbitration_id=airbagSystemMsg.frame_id, data=data, is_extended_id=False)
	try:
		can_bus.send(message)
		print(" AirbagSystem Inactive:\t\t{}".format(msgData))
	except can.CanError:
		print("Message NOT sent")
				
def _idleAirbag():
	# Send Idle Airbag state Message
	msgData = {'airbagState':0,'AirbagCondition':0}
	data = airbagSystemMsg.encode(msgData)
	message = can.Message(arbitration_id=airbagSystemMsg.frame_id, data=data, is_extended_id=False)
	try:
		can_bus.send(message)
		print(" Airbag in Idle Condition:\t{}".format(msgData))
	except can.CanError:
		print("Message NOT sent")
		
def _releaseAirbag():
	# Send Airbag Release Message
	msgData = {'airbagState':2,'AirbagCondition':0}
	data = airbagSystemMsg.encode(msgData)
	message = can.Message(arbitration_id=airbagSystemMsg.frame_id, data=data, is_extended_id=False)
	try:
		can_bus.send(message)
		print(" Airbag Released:\t\t{}".format(msgData))
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
			seatbeltState = (msgData['SeatbeltState'])
			print(" Recieved Seatbelt Message:\t{}".format(msgData))
			#if Seatbelt is not Worn
			if (seatbeltState == 0):
				#Trigger Inactive Airbag
				_inactiveAirbag()
			else:
				# Trigger Idle Airbag
				_idleAirbag()
		
		if response.arbitration_id == VehicleMotionMsg.frame_id:
			crashDetected = (msgData['CrashDetected'])
			engineRunning = (msgData['EngineRunning'])
			print(" Recieved Vehcle Message:\t{}".format(msgData))
			#if Crash Detected, and Seatbelt is worn 
			if (crashDetected==1):
				if (seatbeltState == 1 and engineRunning==1):
					# Trigger Airbag Release
					_releaseAirbag()
				else:
					#Trigger Inactive Airbag
					_inactiveAirbag()

if __name__ == '__main__':
	threading.Thread(on_Message()).start()