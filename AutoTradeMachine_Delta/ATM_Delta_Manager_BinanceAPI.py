import InterProcessesCommunicator

import ccxt
import os
import time

name_MANAGER = "BINANCEAPI"

path_PROJECT = os.path.dirname(os.path.realpath(__file__))
path_MANAGER = os.path.join(path_PROJECT + r"\data\m_BinanceAPI")

class manager_BinanceAPI:
    def __init__(self, PST):
        #Inter-Processes Communicator Initialization
        self.IPC = InterProcessesCommunicator.IPCommunicator(PST, name_MANAGER, path_MANAGER, ["MAIN", "AUTOTRADER", "AUXILLARY", "DATAANALYSIS", "DATAMANAGEMENT", "GUI", "SECURITYCONTROL"])
        self.IPC.write_SystemMessage("Initializing BINANCE API Manager...")
        self.IPC.write_SystemMessage("  Inter-Processes Communicator Initialized!")

        #IPC Files Creation
        f = open(os.path.join(path_MANAGER, 'IPCLog_BINANCEAPI.txt'), 'w'); f.close()
        self.IPC.write_SystemMessage("  Inter-Processes Communication Log File Created!: 'IPCLog_BINANCEAPI.txt'")
        f = open(os.path.join(path_MANAGER, 'IPCRuntime_BINANCEAPI.txt'), 'w'); f.close()
        self.IPC.write_SystemMessage("  Inter-Processes Communication Run Time Data File Created!: 'IPCRuntime_BINANCEAPI.txt'")

        #Binance Object Creation
        self.binanceObject = ccxt.binance()

        self.IPC.write_SystemMessage("BINANCE API Manager Initialization Complete!")

        self.connectionStatus = False;
        self.connectionLastCheckedTime = time.ctime(time.time());
        self.connectionTimer = 0
        self.connectionCheckInterval = 5

        self.IPC.edit_PRD_OUT("ONLINESTATUS", self.connectionStatus)
        self.IPC.edit_PRD_OUT("LASTCONNECTIONCHECKTIME", self.connectionLastCheckedTime)

    def process(self, IPCB_T0, IPCB_T1, IPCB_T2, IPCB_T3, IPCB_T4, IPCB_T5, IPCB_T6, IPCB_F0, IPCB_F1, IPCB_F2, IPCB_F3, IPCB_F4, IPCB_F5, IPCB_F6):
        #Read FARequests From GUI Manager
        FAR_IN = self.IPC.read_FARequest("GUI")
        while (FAR_IN != "DNF" and FAR_IN != "DAR"): #If FAR Does Exist From GUI Manager
            functionID = FAR_IN.FunctionID
            requestID = FAR_IN.RequestID
            functionParams = FAR_IN.FunctionParameters
            
            if FAR_IN.FunctionID == "CONNECTAPI": 
                FAresult = self.connectAPI("GEAB348IvKhOVcsPQgRbil4Ga7Dy3TZN53UD8nbgQndKNAWU78r1JS16AnR850nu", "ke7Zz9mHfBrTsUUD3iAXCE1ACafBLzOUBAZ056JN4rde1EoEYo8CvXXq4bgbqUOf")
                #FAresult = self.connectAPI(FAR_IN.FunctionParameters[0]["GUIO:BINANCEAPI:APIKEY_INPUTBOX:TEXT"], FAR_IN.FunctionParameters[0]["GUIO:BINANCEAPI:SECRETKEY_INPUTBOX:TEXT"])
                self.IPC.send_FAResult("GUI", requestID, FAresult)
            FAR_IN = self.IPC.read_FARequest("GUI")

        self.checkConnection()

        self.IPC.processMessages(IPCB_T0, IPCB_T1, IPCB_T2, IPCB_T3, IPCB_T4, IPCB_T5, IPCB_T6, IPCB_F0, IPCB_F1, IPCB_F2, IPCB_F3, IPCB_F4, IPCB_F5, IPCB_F6) #Must be placed at the end of the function for appropriate process recording
        return True

    def connectAPI(self, apiKey, secretKey):
        binanceObject = ccxt.binance(config = {'apiKey': apiKey, 'secret': secretKey})
        try:
            balance = binanceObject.fetch_balance()
            #Show Balance Contents
            i = 0
            for key in balance.keys():
                if (type(balance[key]) is dict):
                    print(str(i) + " " + str(key) + ":")
                    j = 0
                    for subKey in balance[key].keys():
                        if subKey == "balances":
                            print("   " + str(j) + " " + str(subKey) + ":")
                            for k in range (len(balance[key][subKey])):
                                print("      " + str(k) + ": " + str(balance[key][subKey][k]))
                        else:
                            print("   " + str(j) + " " + str(subKey) + ": " + str(balance[key][subKey]))
                        j += 1
                else:
                    print(str(i) + " " + str(key) + ": " + str(balance[key]))
                i += 1

            self.binanceObject = binanceObject
            self.connectionStatus = True
            self.IPC.edit_PRD_OUT("ONLINESTATUS", self.connectionStatus)
            self.IPC.write_SystemMessage("CONNECTION SUCCESSFUL")
            return True
        except Exception as e:
            print(e)
            self.IPC.write_SystemMessage("CONNECTION FAILED");
            return False

    def checkConnection(self):
        #Perform Connection Check by Fetching the Account Balance If [1]: Current Connection Status is True, [2]: Connection Timer Has Been Rang
        if ((self.connectionStatus == True) and ((time.time_ns() - self.connectionTimer) > (1e9 * self.connectionCheckInterval))):
            self.connectionTimer = time.time_ns()
            self.IPC.write_SystemMessage("CHECKING CONNECTION...")
            try:
                self.binanceObject.fetch_balance()
                self.connectionLastCheckedTime = time.ctime(time.time())
                self.IPC.edit_PRD_OUT("LASTCONNECTIONCHECKTIME", self.connectionLastCheckedTime)
                self.IPC.write_SystemMessage("Last Connection Check Time: " + self.connectionLastCheckedTime)
                self.IPC.write_SystemMessage("CONNECTION CHECK SUCCESSFUL!!!")
            except:
                self.connectionStatus = False
                self.IPC.edit_PRD_OUT("LASTCONNECTIONCHECKTIME", self.connectionLastCheckedTime)
                self.IPC.edit_PRD_OUT("ONLINESTATUS", self.connectionStatus)
                self.IPC.write_SystemMessage("CONNECTION CHECK FAILED")