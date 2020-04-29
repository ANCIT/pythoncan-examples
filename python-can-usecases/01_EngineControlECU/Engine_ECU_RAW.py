import can
import threading

can_bus = can.interface.Bus(bustype='socketcan',channel='vcan0',bitrate=250000)

brakeMsgID = 0x105
accelerationMsgID = 0x106
EngineMsgID = 0x104

def apply_break():
	message = can.Message(arbitration_id=EngineMsgID, data=[1,0,0,0], is_extended_id=False)
	try:
		periodicTask.modify_data(message)
		print("Break Applied")
	except can.CanError:
		print("Message not sent")
		
def apply_accelerate(AcclrVal):
	message = can.Message(arbitration_id=EngineMsgID, data=[1,AcclrVal*10,0,0], is_extended_id=False)
	try:
		periodicTask.modify_data(message)
		print("Acceleration : " + str(AcclrVal*10))
	except can.CanError:
		print("Message NOT sent")	

def on_Message():
	#Initiating Vehicle Condition to Default
	while True:
		message = can_bus.recv()
		msgData = message.data
		if message.arbitration_id == accelerationMsgID: 
			acclrValue = msgData[0]
			apply_accelerate(acclrValue)

		if message.arbitration_id == brakeMsgID:
			apply_break()
			
def intiateVehicle():
	message = can.Message(arbitration_id=EngineMsgID, data=[1,5,0,0], is_extended_id=False)
	try:
		task = can_bus.send_periodic(message, 1.0)
		print("Cranking engine & Vehicle Initiated")
		return task
	except can.CanError:
		print("Message NOT sent")

if __name__ == '__main__':
	
	periodicTask = intiateVehicle()
	threading.Thread(on_Message()).start()
	
	
	
