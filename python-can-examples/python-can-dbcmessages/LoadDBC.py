'''
Created on 24-Mar-2020

@author: ancit
'''
import cantools
from can.message import Message
db = cantools.db.load_file('/home/bk/git/pythoncan-examples/python-can-examples/resources/motohawk.dbc')
# print the content of the dbc
print(db)

# print a particular message in the dbc
msg = db.get_message_by_name('ExampleMessage')
print(msg)
print(msg.cycle_time)
print(msg.signal_tree)
temperature_signal = msg.signals[2]
print(temperature_signal)
print(temperature_signal.scale)
print(temperature_signal.offset)