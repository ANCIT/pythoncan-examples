
# Configuring VCAN [Virtual CAN] in Linux


*   $ sudo modprobe vcan
*   $ sudo ip link add dev vcan0 type vcan
*   $ sudo ip link set up vcan0


## SendCANRawMessage.py
This Python Module would send 1 CAN Message on vcan0


## SendMessagePeriodic.py

This Python Module would send CAN Message on vcan0 in a cyclic mode

*   How to run Periodic Messages
Go to Python Shell and execute exec(open('filepath').read())


## ReceiveCANRawMessage.py

This is a Python Module for receiving all the messages on the Bus

## LoadDBC.py
*	Load the DBC
*	Print the DBC Content
* 	Select a particular message in the DBC
*	Print the Message Content


## SendCANDBCMessage.py
This module is used to Send Message thru DBC Encoding
* Load the DBC
* Get the desired Message [db.get_message_by_name('VehicleMotion')]
* encode the message with data [msg.encode({'Velocity':4,'CrashDetected':1,'EngineRunning':1})]
* send on the can bus


## Receive Message thru CANDUMP using DBC Decoding
candump vcan0 | cantools decode /home/ancit/Documents/malai/python-workspace/python-can-examples/comfort.dbc

## Text based UI for CANDUMP
$ cantools monitor tests/files/dbc/motohawk.dbc

Has options to filter, play, pause, reset whereas candump doesnt have these options

## ReceiveCANDBCMessage.py
This module is used to Receive Message thru DBC Decoding
