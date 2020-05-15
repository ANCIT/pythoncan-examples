"""Execute XML Test Cases without a pass verdict"""
import sys
from time import sleep
import win32com.client as win32

CANoe = win32.DispatchEx("CANoe.Application")
CANoe.Open("E:/ancit-projects/canoe-autoit/CentralLockingSystem/CentralLockingSystem.cfg")

test_env = CANoe.Configuration.TestSetup.TestEnvironments.Item('Test Environment')
test_env = win32.CastTo(test_env, "ITestEnvironment2")

# Get the XML TestModule (type <TSTestModule>) in the test setup
test_module = test_env.TestModules.Item('Tester')

# {.Sequence} property returns a collection of <TestCases> or <TestGroup>
# or <TestSequenceItem> which is more generic
seq = test_module.Sequence
for i in range(1, seq.Count+1):
    # Cast from <ITestSequenceItem> to <ITestCase> to access {.Verdict}
    # and the {.Enabled} property
    tc = win32.CastTo(seq.Item(i), "ITestCase")
    print(tc)
#     if tc.Verdict != 1: # Verdict 1 is pass
#         tc.Enabled = True
#         print(f"Enabling Test Case {tc.Ident} with verdict {tc.Verdict}")
#     else:
#         tc.Enabled = False
#         print(f"Disabling Test Case {tc.Ident} since it has already passed")


CANoe.Measurement.Start()
sleep(5)   # Sleep because measurement start is not instantaneous
test_module.Start()
sleep(1)