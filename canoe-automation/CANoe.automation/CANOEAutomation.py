from time import sleep
import win32com.client as win32
import configparser
import time
import pythoncom

testComplete = False

class TestModuleEvents(object):
    def OnReportGenerated(self,Success, SourceFullName, GeneratedFullName):
        print("Report Generated")
        global testComplete
        testComplete = True
   
    def OnStop(self, value):
         global testComplete
         testComplete = True
         print("Test Module Stopped")
     
    def OnStart(self):
        print("Test Module Started")
        global testComplete
        testComplete = False
        
class TestConfigurationEvents(object):
    def OnStart(self):
        print("Measurement Started")
        global testComplete
        testComplete = False
    
    def OnStop(self):
        print("Measurement Stopped")
        global testComplete
        testComplete = False

class CANOEAutomation:
    
    def __init__(self):
        global testComplete
        testComplete = False
        
    def getVerdict(self,argument): 
        switcher = { 
            0: "zero", 
            1: "Passed", 
            2: "Failed",
            3: "None",
            4: "Inconclusive",
            5: "Error in testsystem" 
            } 
  
        # get() method of dictionary data type returns  
        # value of passed argument if it is present  
        # in dictionary otherwise second argument will 
        # be assigned as default value of passed argument 
        return switcher.get(argument, "Not Available") 
        

    def executeTestModule(self, win32, test_module):
        print(test_module)
        seq = test_module.Sequence
        for i in range(1, seq.Count + 1):
            tc = win32.CastTo(seq.Item(i), "ITestCase")
            print(tc)
        
    #
        win32.WithEvents(test_module, TestModuleEvents)
        test_module.Start()
        global testComplete
        while not testComplete:
            pythoncom.PumpWaitingMessages()
            time.sleep(1)
        
        print(self.getVerdict(test_module.Verdict))

    def startCanoe(self):
        #parse the Configuration File to pick the configuration path and tse path
        config = configparser.RawConfigParser()
        config.read('usecase02_configuration.properties')
        configurationPath = config.get('TESTCONFIGURATION', 'configurationpath')
        testspec = config.get('TESTCONFIGURATION', 'testspecification')
        
        CANoe = win32.DispatchEx("CANoe.Application")
        CANoe.Open(configurationPath)

       
        
        testSetup = CANoe.Configuration.TestSetup
        testSetup.TestEnvironments.Add(testspec)
        test_env = testSetup.TestEnvironments.Item(1)
        test_env = win32.CastTo(test_env, "ITestEnvironment2")
        
        CANoe.Measurement.Start()
        sleep(5)  # Sleep because measurement start is not instantaneous
        
        testModules = test_env.TestModules
        for i in range(1, testModules.Count+1):
            test_module = test_env.TestModules.Item(i)
            self.executeTestModule(win32, test_module)
        
        exit()
        
        
        
#         seq = test_module.Sequence
#         for i in range(1, seq.Count+1):
#             # Cast from <ITestSequenceItem> to <ITestCase> to access {.Verdict}
#             # and the {.Enabled} property
#             tc = win32.CastTo(seq.Item(i), "ITestCase")
#             print(tc)
#             if tc.Verdict != 1: # Verdict 1 is pass
#                 tc.Enabled = True
#                 print(f"Enabling Test Case {tc.Ident} with verdict {tc.Verdict}")
#             else:
#                 tc.Enabled = False
#                 print(f"Disabling Test Case {tc.Ident} since it has already passed")
        
if __name__ == '__main__':
    canoeAutomation = CANOEAutomation()
    canoeAutomation.startCanoe()
