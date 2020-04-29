'''
Created on 24-Mar-2020

@author: ancit
'''
import cantools
from can.message import Message
db = cantools.db.load_file('/home/bk/git/pythoncan-examples/python-can-examples/python-can-newdbc-handling/Basic_DBCinExcel.dbc')

import can
bus = can.interface.Bus(bustype='socketcan', channel='vcan0', bitrate=250000)
while True:
        message = bus.recv()
        print(db.decode_message(message.arbitration_id, message.data))




