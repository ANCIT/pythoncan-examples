import can
import cantools
import threading

bus = can.interface.Bus(bustype='socketcan', channel='vcan0', bitrate=250000)
db = cantools.db.load_file('Basic_DBC.dbc')

brakeMsg = db.get_message_by_name('BrakeMsg')
accelerationMsg = db.get_message_by_name('AccelarationMsg')
EngineMsg = db.get_message_by_name('VehicleMotion')

def apply_break():
	data = EngineMsg.encode({'Velocity':0,'CrashDetected':0,'EngineRunning':1})
	message = can.Message(arbitration_id=EngineMsg.frame_id, data=data, is_extended_id=False)
	try:
		periodicTask.modify_data(message)
		print("Break Applied")
	except can.CanError:
		print("Message not sent")
		
def apply_accelerate(AcclVal):
	data = EngineMsg.encode({'Velocity': (AcclVal*10),'CrashDetected':0,'EngineRunning':1})
	message = can.Message(arbitration_id=EngineMsg.frame_id, data=data, is_extended_id=False)
	try:
		periodicTask.modify_data(message)
		print("Acceleration : " + str(AcclVal*10))
	except can.CanError:
		print("Message NOT sent")	

def on_Message():
	while True:
		message = bus.recv()
		msgData = db.decode_message(message.arbitration_id, message.data)
		if message.arbitration_id == accelerationMsg.frame_id:
			acclrValue = (msgData['Acceleration'])
			apply_accelerate(acclrValue)

		if message.arbitration_id == brakeMsg.frame_id:
			apply_break()
			
def intiateVehicle():
	data = EngineMsg.encode({'Velocity':5,'CrashDetected':0,'EngineRunning':1})
	message = can.Message(arbitration_id=EngineMsg.frame_id, data=data, is_extended_id=False)
	try:
		task = bus.send_periodic(message, 1.0)
		print("Cranking engine & Vehicle Initiated")
		return task
	except can.CanError:
		print("Message NOT sent")

if __name__ == '__main__':
	periodicTask = intiateVehicle()
	threading.Thread(on_Message()).start()
	
	
	
