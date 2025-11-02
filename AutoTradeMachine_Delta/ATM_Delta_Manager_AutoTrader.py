import InterProcessesCommunicator

import os

name_MANAGER = "AUTOTRADER"

path_PROJECT = os.path.dirname(os.path.realpath(__file__))
path_MANAGER = os.path.join(path_PROJECT + r"\data\m_AutoTrader")

class manager_AutoTrader:
    def __init__(self, PST):
        #Inter-Processes Communicator Initialization
        self.IPC = InterProcessesCommunicator.IPCommunicator(PST, name_MANAGER, path_MANAGER, ["MAIN", "AUXILLARY", "BINANCEAPI", "DATAANALYSIS", "DATAMANAGEMENT", "GUI", "SECURITYCONTROL"])
        self.IPC.write_SystemMessage("Initializing AUTOTRADER Manager...")
        self.IPC.write_SystemMessage("  Inter-Processes Communicator Initialized!")

        #IPC Files Creation
        f = open(os.path.join(path_MANAGER, 'IPCLog_AUTOTRADER.txt'), 'w'); f.close()
        self.IPC.write_SystemMessage("  Inter-Processes Communication Log File Created!: 'IPCLog_AUTOTRADER.txt'")
        f = open(os.path.join(path_MANAGER, 'IPCRuntime_AUTOTRADER.txt'), 'w'); f.close()
        self.IPC.write_SystemMessage("  Inter-Processes Communication Run Time Data File Created!: 'IPCRuntime_AUTOTRADER.txt'")

        
        self.IPC.write_SystemMessage("AUTOTRADER Manager Initialization Complete!")

    def process(self, IPCB_T0, IPCB_T1, IPCB_T2, IPCB_T3, IPCB_T4, IPCB_T5, IPCB_T6, IPCB_F0, IPCB_F1, IPCB_F2, IPCB_F3, IPCB_F4, IPCB_F5, IPCB_F6):





        self.IPC.processMessages(IPCB_T0, IPCB_T1, IPCB_T2, IPCB_T3, IPCB_T4, IPCB_T5, IPCB_T6, IPCB_F0, IPCB_F1, IPCB_F2, IPCB_F3, IPCB_F4, IPCB_F5, IPCB_F6) #Must be placed at the end of the function for appropriate process recording
        return True