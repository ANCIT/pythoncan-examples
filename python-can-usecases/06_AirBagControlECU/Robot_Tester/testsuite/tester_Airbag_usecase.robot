*** Settings ***
Resource      ../keywords/curf.robot
Test Setup      Set CAN Bus ${INTERFACE} ${CHANNEL} ${BITRATE} ${DB FILE} 
Test Teardown   End Log Can 
Library    DateTime

*** Variables ***
${DB FILE}              /home/manz/eclipse-workspace/AirbagTestNode_Robot/dbc/airbag_MainBus.dbc
${INTERFACE}            socketcan
${CHANNEL}              vcan0
${BITRATE}              250000
${DEFAULT TIMEOUT}      3
${DEFAULT NODE}         DRIVER


*** Test Cases ***
#Check the reception of a CAN signal 01
#    Check CAN Signal SeatbeltState Equals To 0 TimeOut ${DEFAULT TIMEOUT} Seconds   
Send a Seatbelt Un-lock Signal
    Send Signal SeatbeltState With Value 0
    
Check the reception of Airbag Inactive Status
    Check CAN Signal airbagState Equals To 1 TimeOut ${DEFAULT TIMEOUT} Seconds    

Send a Engine Run Signal
    Send Signal EngineRunning With Value 1
    
Send a Seatbelt Lock Signal
    Send Signal SeatbeltState With Value 1

Check the reception of Airbag Idle Status
    Check CAN Signal airbagState Equals To 0 TimeOut ${DEFAULT TIMEOUT} Seconds 

 # Send a Crash Detected Signal
    # Send Signal EngineRunning With Value 1 
    # Send Signal CrashDetected With Value 1
    
Send a Crash Detected with Engine Run CAN frame
    Send Frame With ID 32 And 000003 As Data
    
Check the reception of Airbag Active Status
    Check CAN Signal airbagState Equals To 2 TimeOut ${DEFAULT TIMEOUT} Seconds 
    
