
# Use Case 6 - Airbag System ECU Simulation

## Expectation
To Control the Airbag State according to the seatbelt and Engine running condition

## Functionality
The Airbag will be released only if Seatbelt is worn and Crash detection happened. Otherwise Airbag will be Inactive incase of Seatbelt is not Worn. Rest of the Time airbag will be in idle Condition

## Use Case

## Test Case
Try with Below Message from Terminal to Test
Crash Detected: 	cansend vcan0 032#000001
Crash Not Detected: 	cansend vcan0 032#000000
Seatbelt Unlock: 	cansend vcan0 001#0000
Seatbelt Lock: 		cansend vcan0 001#0100

## Pre-Conditions
### Enable Virtual CAN if on Linux Machine
sudo modprobe vcan
sudo ip link add vcan0 type vcan
sudo ip link set vcan0 up
if need to see the Trace: candump vcan0




