"""Execute XML Test Cases without a pass verdict"""
from time import sleep
import win32com.client as win32
import configparser

config = configparser.RawConfigParser()
config.read('usecase02_configuration.properties')
configurationPath = config.get('TESTCONFIGURATION', 'configurationpath')
testspec = config.get('TESTCONFIGURATION', 'testspecification')

CANoe = win32.DispatchEx("CANoe.Application")
CANoe.Open(configurationPath)

testSetup = CANoe.Configuration.TestSetup
testSetup.TestEnvironments.Add(testspec)
test_env = testSetup.TestEnvironments.Item('Test Environment')
report = test_env.Report
report = win32.CastTo(test_env, "ITestReport5")
test_env = win32.CastTo(test_env, "ITestEnvironment2")


print(report.FullName)

# Get the XML TestModule (type <TSTestModule>) in the test setup
test_module = test_env.TestModules.Item('Tester')
print(test_module.Path)
report = win32.CastTo(test_module.Report, "ITestReport5")
print(report.FullName)

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