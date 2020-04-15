#Code Generated by TestGenx v.1.0
#ANCIT CONSULTING
#Date : Mon Apr 13 15:54:04 IST 2020
#Author : ANICET

from __future__ import print_function
import can
import time
import cantools
from pynput import keyboard
import threading

can_bus = can.interface.Bus(bustype='socketcan',channel='can0',bitrate=1000000)

def on_Message():
	while True:
		response = can_bus.recv()
		if response.arbitration_id == 0x01:
			# Message ID : 0x02
			message = can.Message(arbitration_id=0x02, data=[2,0,0,0,2,0,0,0], is_extended_id=False)
			try:
				can_bus.send(message)
				print(" 0x02 Message sent on {}".format(can_bus.channel_info))
			except can.CanError:
				print("Message NOT sent")

def on_press(key):
	print("Key Event Identified")
	if key.char == 'a': # handles if key press is a
			# Message ID : 0x03
			message = can.Message(arbitration_id=0x03, data=[3,0,0,0,3,0,0,0], is_extended_id=False)
			try:
				can_bus.send(message)
				print(" 0x03 Message sent on {}".format(can_bus.channel_info))
			except can.CanError:
				print("Message NOT sent")


def on_Key():
	keyboard.Listener(on_press=on_press).start()

def sendMessage():
			# Message ID : 0x01
			message = can.Message(arbitration_id=0x01, data=[1,0,0,0,1,0,0,0], is_extended_id=False)
			try:
				can_bus.send(message)
				print(" 0x01 Message sent on {}".format(can_bus.channel_info))
			except can.CanError:
				print("Message NOT sent")

			# Message ID : 0x04
			message = can.Message(arbitration_id=0x04, data=[4,0,0,0,4,0,0,0], is_extended_id=False)
			try:
				task = can_bus.send_periodic(message,1.0) # cycle time
				print(" 0x04 Message sent on {}".format(can_bus.channel_info))
			except can.CanError:
				print("Message NOT sent")

if __name__ == '__main__':

	sendMessage() # Sending Messages [Periodic / Non Periodic]
	on_Key() # On Key -> Listener Thread
	threading.Thread(on_Message()).start() # 