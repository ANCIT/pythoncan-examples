'''
Created on 24-Mar-2020

@author: ancit
'''
import cantools
from can.message import Message
db = cantools.db.load_file('/home/bk/git/pythoncan-examples/python-can-examples/resources/motohawk.dbc')

# print a particular message in the dbc
msg = db.get_message_by_name('VehicleMotion')
msg_data = msg.encode({'Velocity':4,'CrashDetected':1,'EngineRunning':1})

import can
bus = can.interface.Bus(bustype='socketcan', channel='vcan0', bitrate=250000)
msg = can.Message(arbitration_id=msg.frame_id,data=msg_data,is_extended_id=False)
try:
    bus.send(msg)
    print("Message sent on {}".format(bus.channel_info))
except can.CanError:
    print("Message NOT sent")




