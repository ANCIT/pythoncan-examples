'''
Created on 24-Mar-2020

@author: ancit
'''
import cantools
from can.message import Message
db = cantools.db.load_file('/home/bk/git/pythoncan-examples/python-can-examples/python-can-newdbc-handling/Basic_DBCinExcel.dbc')
# print the content of the dbc
#print(db)

#print a particular message in the dbc
msg = db.get_message_by_name('BrakeMsg')
print(msg)
