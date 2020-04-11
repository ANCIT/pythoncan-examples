##system.kcd

Message Database
Contains 2 Nodes [Motor & Controller]
Contains 2 Messages MotorStatus & MotorControl

## motor.py

Simulated ECU
Sends MotorStatus [Speed & Load Signals] every 1s on the CANBUS
Listens to MotorControl and updates his Speed accordingly


## tester.py

Simulates the MotorControl
Sends different values for Speed so that MotorStatus gets updated

