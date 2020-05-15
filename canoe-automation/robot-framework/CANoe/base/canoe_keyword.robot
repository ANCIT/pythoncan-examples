*** Settings ***
Library    CANoe.py    WITH NAME    canoe
*** Keywords ***
Open Simulation
    [Arguments]    ${CONFIGURATIONPATH}
    canoe.OPEN SIMULATION  ${CONFIGURATIONPATH}
Load TestSetup
    [Arguments]    ${TESTSPECIFICATION}
    canoe.LOAD TESTSETUP    ${TESTSPECIFICATION}
Start Measurement
    canoe.START MEASUREMENT
Start TestModule
    canoe.START TESTMODULE
Stop Measurement
    canoe.STOP MEASUREMENT
Waiting
    [Arguments]    ${WAIT TIME}
    canoe.WAITING