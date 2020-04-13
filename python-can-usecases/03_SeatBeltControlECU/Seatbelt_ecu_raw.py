'''
Created on 15-Apr-2020

@author: bk
'''
import can
bus = can.interface.Bus(bustype='socketcan', channel='vcan0', bitrate=250000)
while True:
        message = bus.recv()
        if message.arbitration_id == 0x011  & data==[0,1]:
            print('Activate Seat Belt')
            
        if message.arbitration_id == 0x022  & data==[0,0]:
            print('Release SeatBelt')
            

