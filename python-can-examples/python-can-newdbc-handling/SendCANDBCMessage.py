'''
Created on 24-Mar-2020

@author: ancit
'''
import cantools
from can.message import Message
db = cantools.db.load_file('/home/bk/git/pythoncan-examples/python-can-examples/python-can-newdbc-handling/Basic_DBCinExcel.dbc')

# print a particular message in the dbc
msg = db.get_message_by_name('SeatbeltMsg')
msg_data = msg.encode({'SeatbeltStatus':0})

import can
bus = can.interface.Bus(bustype='socketcan', channel='vcan0', bitrate=250000)
msg = can.Message(arbitration_id=msg.frame_id,data=msg_data,is_extended_id=False)
try:
    bus.send(msg)
    print("Message sent on {}".format(bus.channel_info))
except can.CanError:
    print("Message NOT sent")




