#Code Generated by TestGenx v.1.0
#ANCIT CONSULTING
#Date : Wed Apr 15 00:09:28 IST 2020
#Author : tejas

from __future__ import print_function
import can
import time
import cantools
from pynput import keyboard
import threading

db = cantools.database.load_file('C:/Users/tejas/Documents/CLS.dbc')
can_bus = can.interface.Bus(bustype='socketcan',channel='vcan0',bitrate=1000000)

def on_Message():
	while True:
		response = can_bus.recv()
		if response.arbitration_id == ce:
			# Message : LockingRemoteControlRequest
			example_message = db.get_message_by_name('LockingRemoteControlRequest')
			data = example_message.encode({'LockRequest':0})
			message = can.Message(arbitration_id=example_message.frame_id, data=data, is_extended_id=False)
			try:
				can_bus.send(message)
				print(" LockingRemoteControlRequest Message sent on {}".format(can_bus.channel_info))
			except can.CanError:
				print("Message NOT sent")

def on_press(key):
print("Key Event Identified")
	if key.char == 'a': # handles if key press is a
			# Message : VehicleMotion
			example_message = db.get_message_by_name('VehicleMotion')
			data = example_message.encode({'EngineRunning':1,'CrashDetected':1,'Velocity':10})
			message = can.Message(arbitration_id=example_message.frame_id, data=data, is_extended_id=False)
			try:
				can_bus.send(message)
				print(" VehicleMotion Message sent on {}".format(can_bus.channel_info))
			except can.CanError:
				print("Message NOT sent")


def on_Key():
	keyboard.Listener(on_press=on_press).start()

def sendMessage():
			# Message : CentralLockingSystemState
			example_message = db.get_message_by_name('CentralLockingSystemState')
			data = example_message.encode({'AntiTheftSystemActive':1,'LockState':0})
			message = can.Message(arbitration_id=example_message.frame_id, data=data, is_extended_id=False)
			try:
				can_bus.send(message)
				print(" CentralLockingSystemState Message sent on {}".format(can_bus.channel_info))
			except can.CanError:
				print("Message NOT sent")

if __name__ == '__main__':

	sendMessage()
	on_Key()
	threading.Thread(on_Message()).start()