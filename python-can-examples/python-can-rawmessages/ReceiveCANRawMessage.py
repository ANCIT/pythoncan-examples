'''
Created on 24-Mar-2020

@author: ancit
'''
import can
bus = can.interface.Bus(bustype='socketcan', channel='vcan0', bitrate=250000)
while True:
        message = bus.recv()
        print(message)

