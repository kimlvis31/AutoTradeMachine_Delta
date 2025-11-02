import InterProcessesCommunicator

import os

name_MANAGER = "AUXILLARY"

path_PROJECT = os.path.dirname(os.path.realpath(__file__))
path_MANAGER = os.path.join(path_PROJECT + r"\data\m_Auxillary")

class manager_Auxillary:
    def __init__(self, PST):
        self.IPC = InterProcessesCommunicator.IPCommunicator(PST, name_MANAGER, path_MANAGER, ["MAIN", "AUTOTRADER", "BINANCEAPI", "DATAANALYSIS", "DATAMANAGEMENT", "GUI", "SECURITYCONTROL"])
        self.IPC.write_SystemMessage("Initializing AUXILLARY Manager...")
        self.IPC.write_SystemMessage("  Inter-Processes Communicator Initialized!")

        #IPC Files Creation
        f = open(os.path.join(path_MANAGER, 'IPCLog_AUXILLARY.txt'), 'w'); f.close()
        self.IPC.write_SystemMessage("  Inter-Processes Communication Log File Created!: 'IPCLog_AUXILLARY.txt'")
        f = open(os.path.join(path_MANAGER, 'IPCRuntime_AUXILLARY.txt'), 'w'); f.close()
        self.IPC.write_SystemMessage("  Inter-Processes Communication Run Time Data File Created!: 'IPCRuntime_AUXILLARY.txt'")
        
        
    def process(self, IPCB_T0, IPCB_T1, IPCB_T2, IPCB_T3, IPCB_T4, IPCB_T5, IPCB_T6, IPCB_F0, IPCB_F1, IPCB_F2, IPCB_F3, IPCB_F4, IPCB_F5, IPCB_F6):



        #self.IPC.getPRD_IN("AUTOTRADER", "A0")
        #print(self.IPC.get_UpdatedPRDCodes("AUTOTRADER"))
        #self.IPC.write_SystemMessage("HELLO")
        #print(self.IPC.send_FARequest("AUTOTRADER", "01313", ["da", 100, "tqeq"]))

        self.IPC.processMessages(IPCB_T0, IPCB_T1, IPCB_T2, IPCB_T3, IPCB_T4, IPCB_T5, IPCB_T6, IPCB_F0, IPCB_F1, IPCB_F2, IPCB_F3, IPCB_F4, IPCB_F5, IPCB_F6) #Must be placed at the end of the function for appropriate process recording

        return True
