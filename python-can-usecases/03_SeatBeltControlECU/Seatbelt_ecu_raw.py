'''
Created on 15-Apr-2020

@author: bk
'''
import can
bus = can.interface.Bus(bustype='socketcan', channel='vcan0', bitrate=250000)
while True:
        message = bus.recv()
        data = message.data
        if message.arbitration_id == 0x011 and data == bytearray(b'\x00\x01'):
            print('Activate Seatbelt')
            
        if message.arbitration_id == 0x022 and data==bytearray(b'\x00\x00'):
            print('Release SeatBelt')

