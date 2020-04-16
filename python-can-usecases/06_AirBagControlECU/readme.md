
# Use Case 6 - Airbag System ECU Simulation

## Expectation
To Control the Airbag State according to the seatbelt and Engine running condition

## Functionality
The Airbag will be released only if Seatbelt is worn and Crash detection happened and Engine On. Otherwise Airbag will be Inactive incase of Seatbelt is not Worn or Engine Off. Rest of the Time airbag will be in idle Condition

## Test Case
Press the Below Keys from TestNode window, and Evaluate the Result on ECU Simulation Window

Simulation Keys:

	- l: Lock Seatbelt
	- u: Unock Seatbelt
	- c: Crash with Engine On
	- o: Crash with Engine Off
	- f: Crash free with Engine On

Expected Results:

	- Airbag Inactive    : When Unlock Seatbelt, Crash with Engine Off,
	- Airbag Idle        : Lock Seatbelt
	- Airbag Release     : Lock Seatbelt + Crash with Engine On
	- No Update on Airbag: crash free with Engine On 

## Pre-Conditions
Enable Virtual CAN if on Linux Machine

```bash
sudo modprobe vcan
sudo ip link add vcan0 type vcan
sudo ip link set vcan0 up
if need to see the Trace: candump vcan0
```




