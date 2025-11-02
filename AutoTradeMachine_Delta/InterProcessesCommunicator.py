"""
SCRIPT DICTIONARY
    PRD: Pre-Registered Data
    IPCB: Inter-Processes Communication Buffer
    MNF: Manager Not Found
    DNF: Data Not Found
    FAR: Function Activation Request
    BLR: Buffer Limit Reached
    PST: Program Start Time [ns]
"""

import time
import os
from pickle import NONE

#MAIN CLASS -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
class IPCommunicator:
    #MAIN CLASS INITIALIZATION ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def __init__(self, PST, name_MANAGER, path_MANAGER, IPCB_ID, PRD_TIMEOUT = 10000, FAR_BL = 100):
        self.PST = PST
        self.name_MANAGER = name_MANAGER
        self.path_MANAGER = path_MANAGER
        self.IPCB_ID = IPCB_ID

        """
        Pre-registered Data from other managers
            [0]: From IPCB_F0
            [1]: From IPCB_F1
            [2]: From IPCB_F2
            [3]: From IPCB_F3
            [4]: From IPCB_F4
            [5]: From IPCB_F5
            [5]: From IPCB_F6
        """
        self.PRD_OUT = []
        self.PRD_IN = [[],[],[],[],[],[],[]]
        self.PRD_TIMEOUT = PRD_TIMEOUT #Request Timeout Value in milliseconds

        self.updatedPRDCODE = [[],[],[],[],[],[],[]]
        self.systemMessages = []
        #Each list in the FAR_IN list is a collection of request elements
        self.FAR_OUT = [[],[],[],[],[],[],[]]
        self.FAR_IN = [[],[],[],[],[],[],[]]
        self.FAR_BL = FAR_BL

        self.IPCRecords = []

        #[0]: Save IPC History, [1]: Save IPC Real-Time Data
        self.recordControl = [False, True]

    #MAIN CLASS INITIALIZATION END ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    #MAIN CLASS MAIN FUNCTION -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def processMessages(self, IPCB_T0, IPCB_T1, IPCB_T2, IPCB_T3, IPCB_T4, IPCB_T5, IPCB_T6, IPCB_F0, IPCB_F1, IPCB_F2, IPCB_F3, IPCB_F4, IPCB_F5, IPCB_F6):
        #Communicator Data Sorting
        for i in range (len(self.FAR_OUT)):
            attenuator = 0
            for k in range (len(self.FAR_OUT[i])):
                #logIPC(self, "Timeout " + str((time.time_ns() - self.FAR_OUT[i][k - attenuator].timer) / 1000000))
                if (self.FAR_OUT[i][k - attenuator].RequestStatus == "RENOUNCE"): #Remove the request if its status is "RENOUNCE"
                    logIPC(self, "Renounced Request Removed at IPCB_T" + str(i) + ": <" + self.FAR_OUT[i][k - attenuator].RequestID + "> <" + self.FAR_OUT[i][k - attenuator].FunctionID + "> <" + str(self.FAR_OUT[i][k - attenuator].FunctionParameters) + ">" )
                    self.FAR_OUT[i].pop(k - attenuator); attenuator += 1; 
                elif (self.FAR_OUT[i][k - attenuator].RequestStatus == "SENT") and (((time.time_ns() - self.FAR_OUT[i][k - attenuator].timer) / 1000000) > self.PRD_TIMEOUT): #Remove the request if it has been waiting for the result longer than the timeout value
                    logIPC(self, "Timeout Request Removed at IPCB_T" + str(i) + ": <" + self.FAR_OUT[i][k - attenuator].RequestID + "> <" + self.FAR_OUT[i][k - attenuator].FunctionID + "> <" + str(self.FAR_OUT[i][k - attenuator].FunctionParameters) + ">" )
                    self.FAR_OUT[i].pop(k - attenuator); attenuator += 1

        #Read In From IPCBs
        for x in range (7):
            if (x == 0): targetIndex = 0; IPCB_T = IPCB_T0; IPCB_F = IPCB_F0
            elif (x == 1): targetIndex = 1; IPCB_T = IPCB_T1; IPCB_F = IPCB_F1
            elif (x == 2): targetIndex = 2; IPCB_T = IPCB_T2; IPCB_F = IPCB_F2
            elif (x == 3): targetIndex = 3; IPCB_T = IPCB_T3; IPCB_F = IPCB_F3
            elif (x == 4): targetIndex = 4; IPCB_T = IPCB_T4; IPCB_F = IPCB_F4
            elif (x == 5): targetIndex = 5; IPCB_T = IPCB_T5; IPCB_F = IPCB_F5
            elif (x == 6): targetIndex = 6; IPCB_T = IPCB_T6; IPCB_F = IPCB_F6

            while (len(IPCB_F) > 0):
                line = IPCB_F.pop(0);
                logIPC(self, "Reading from IPCB_" + str(x) + ": " + str(line) + "")
                #Data Sharing Read
                if line[0] == "DATASHARE": #[0]: "DATASHARE", [1]: DATACODE, [2:]: DATA
                    if (self.updatedPRDCODE[targetIndex].count(line[1]) == 0): self.updatedPRDCODE[targetIndex].append(line[1])
                    line.insert(2, True); Index = -1; 
                    for i in range (len(self.PRD_IN[targetIndex])):
                        if self.PRD_IN[targetIndex][i][0] == line[1]: Index = i
                    if (Index == -1): self.PRD_IN[targetIndex].append(line[1:]); logIPC(self, "PRD_IN via IPCB_F{:d} Appended: ".format(targetIndex) + "<" + line[1] + "> <" + str(line[2:]) + ">")
                    else: self.PRD_IN[targetIndex][Index] = line[1:]; logIPC(self, "PRD_IN via IPCB_F{:d} Updated: ".format(targetIndex) + "<" + line[1] + "> <" + str(line[2:]) + ">")
                #Function Activation Request Reception
                elif line[0] == "FAREQ": #[0]: "FAREQ", [1]: RequestID, [2]: FunctionID, [3:]: Function Parameters
                    #Successful Request Reception - When there is an available spot in the FAR buffer, append an FAR_IN object with the received data from the message [0]: RequestID, [1]: FunctionID, [2]: FunctionParameters
                    if ((len(self.FAR_IN[targetIndex])) < self.FAR_BL): self.FAR_IN[targetIndex].append(FAR_IN(line[1], line[2], line[3:]))
                    #Request Rejection - When there is no available spot in the FAR buffer, send FAR rejection code "FAREJ"
                    else: 
                        IPCB_T.append(["FAREJ", "BLR", line[1], line[2], line[3:]])
                        logIPC(self, "Rejected FAR From IPCB_F" + str(targetIndex) + " [Buffer Limit Reached]: '" + str(line) + "'")
                #Function Activation Result Reception
                elif line[0] == "FARES": #[0]: "FARES", [1]: RequestID, [2:]: Function Activation Result
                    index = -1
                    for i in range (len(self.FAR_OUT[targetIndex])):
                        if (self.FAR_OUT[targetIndex][i].RequestID == line[1]): index = i; break;
                    if (index == -1):
                        logIPC(self, "FAR Result Received From IPCB_F" + str(targetIndex) + ": <" + line[1] + "> <" + str(line[2:]) + ">")
                    else:
                        self.FAR_OUT[targetIndex][index].Result = list(line[2:])
                        self.FAR_OUT[targetIndex][index].RequestStatus = "RECEIVED"
                        logIPC(self, "FAR Result Received From IPCB_F" + str(targetIndex) + ": <" + line[1] + "> <" + str(line[2:]) + ">")
                #Function Activation Request Rejection Handling
                elif line[0] == "FAREJ": #[0]: "FAREJ", [1]: Rejection Type, [2]: RequestID, [3]: FunctionID, [4:]: Function Parameters
                    requestIndex = -1
                    for i in range (len(self.FAR_OUT[targetIndex])):
                        if (self.FAR_OUT[targetIndex][i].RequestID == line[2]): requestIndex = i; break;
                    if (requestIndex == -1):
                        print(line[1])
                    else:
                        if line[1] == "BLR": #Buffer Limit Reached
                            logIPC(self, "FAR Rejected From IPCB_F" + str(targetIndex) + " due to [" + line[1] + "] Request Will Be Reattempted: <" + line[2] + "> <" + line[3] + "> <" + str(line[4:]) + ">")
                            self.FAR_OUT[targetIndex][requestIndex].RequestStatus = "PENDING"
                        elif line[1] == "IVP": #InValid Parameters
                            logIPC(self, "FAR Rejected From IPCB_F" + str(targetIndex) + " due to [" + line[1] + "] Request Will Be Renounced: <" + line[2] + "> <" + line[3] + "> <" + str(line[4:]) + ">")
                            self.FAR_OUT[targetIndex][requestIndex].RequestStatus = "RENOUNCE"

                else: logIPC(self, "Unrecognizable Message Detected From IPCB_F" + str(targetIndex) + ": '" + str(line) + "'")
                
        #Announce variation-detected pre-registered data
        for i in range (len(self.PRD_OUT)):
            if self.PRD_OUT[i][1] == True:
                line = ["DATASHARE", self.PRD_OUT[i][0]] + self.PRD_OUT[i][2:]; IPCB_T0.append(line); IPCB_T1.append(line); IPCB_T2.append(line); IPCB_T3.append(line); IPCB_T4.append(line); IPCB_T5.append(line); IPCB_T6.append(line)
                logIPC(self, "PRD_OUT Announced: <" + self.PRD_OUT[i][0] + "> <" + str(self.PRD_OUT[i][2:]) + ">"); self.PRD_OUT[i][1] = False
        #Write System Messages
        for i in range (len(self.systemMessages)):
            IPCB_T0.append(["RPT", "SYS_MSG", self.systemMessages[i][0], self.systemMessages[i][1]])
        self.systemMessages.clear()

        #Write Function Activation Messages
        for x in range (7):
            if (x == 0): targetIndex = 0; IPCB_T = IPCB_T0
            elif (x == 1): targetIndex = 1; IPCB_T = IPCB_T1
            elif (x == 2): targetIndex = 2; IPCB_T = IPCB_T2
            elif (x == 3): targetIndex = 3; IPCB_T = IPCB_T3
            elif (x == 4): targetIndex = 4; IPCB_T = IPCB_T4
            elif (x == 5): targetIndex = 5; IPCB_T = IPCB_T5
            elif (x == 6): targetIndex = 6; IPCB_T = IPCB_T6

            #Write Function Activation Requests
            for i in range (len(self.FAR_OUT[targetIndex])):
                if (self.FAR_OUT[targetIndex][i].RequestStatus == "PENDING"):
                    self.FAR_OUT[targetIndex][i].RequestStatus = "SENT"; self.FAR_OUT[targetIndex][i].timer = time.time_ns()
                    if (type(self.FAR_OUT[targetIndex][i].FunctionParameters) == list): IPCB_T.append(["FAREQ", self.FAR_OUT[targetIndex][i].RequestID, self.FAR_OUT[targetIndex][i].FunctionID] + self.FAR_OUT[targetIndex][i].FunctionParameters)
                    else: IPCB_T.append(["FAREQ", self.FAR_OUT[targetIndex][i].RequestID, self.FAR_OUT[targetIndex][i].FunctionID, self.FAR_OUT[targetIndex][i].FunctionParameters])
                    logIPC(self, "FAR Sent via IPCB_T" + str(targetIndex) + " " + "'" + str(["FAREQ", self.FAR_OUT[targetIndex][i].RequestID, self.FAR_OUT[targetIndex][i].FunctionID, self.FAR_OUT[targetIndex][i].FunctionParameters]) + "'")
            
            #Write Function Activation Results
            for i in range (len(self.FAR_IN[targetIndex])):
                if (self.FAR_IN[targetIndex][i].Result is not NONE): #If there exists an result for the corresponding Function Activation Request == The request has been handled by the manager
                    IPCB_T.append(["FARES", self.FAR_IN[targetIndex][i].RequestID, self.FAR_IN[targetIndex][i].Result]) #Append the FAResult to the corresponding IPCB
                    self.FAR_IN[targetIndex].pop(i) #Remove the corresponding FAR as the request has been completed

        #Save IPC Records
        if (self.recordControl[0] == True) and (len(self.IPCRecords) > 0):
            filename = "IPCLog_" + self.name_MANAGER + ".txt"; 
            f = open(os.path.join(self.path_MANAGER, filename), 'a');
            for i in range (len(self.IPCRecords)): f.write(self.IPCRecords[i] + "\n")
            f.write("\n"); f.close(); self.IPCRecords.clear()
        #Save IPC Runtime Data
        if (self.recordControl[1] == True):
            filename = "IPCRuntime_" + self.name_MANAGER + ".txt"; 
            f = open(os.path.join(self.path_MANAGER, filename), 'w');
            f.write("### [PRD_OUT] ### \n")
            if (len(self.PRD_OUT) == 0): f.write("    <N/A>\n")
            else:
                for i in range (len(self.PRD_OUT)): f.write("   " + self.PRD_OUT[i][0] + " : " + str(self.PRD_OUT[i][2:]) + "\n")

            f.write("\n### [PRD_IN] ### \n")
            for i in range (len(self.PRD_IN)):
                f.write("[PRD_IN[" + str(i) + "]] \n")
                if (len(self.PRD_IN[i]) == 0): f.write("    <N/A>\n")
                else: 
                    for k in range (len(self.PRD_IN[i])): f.write("   " + self.PRD_IN[i][k][0] + " : " + str(self.PRD_IN[i][k][2:]) + "\n")
                f.write("\n")

            f.write("\n### [FAR_OUT] ### \n")
            for i in range (len(self.FAR_OUT)):
                f.write("[FAR_OUT[" + str(i) + "]] \n")
                if (len(self.FAR_OUT[i]) == 0): f.write("    <N/A>\n")
                else: 
                    for k in range (len(self.FAR_OUT[i])): f.write("   <" + self.FAR_OUT[i][k].RequestID + "> <" + self.FAR_OUT[i][k].RequestStatus + ">\n")
                f.write("\n")

            f.write("\n### [FAR_IN] ### \n")
            for i in range (len(self.FAR_IN)):
                f.write("[FAR_IN[" + str(i) + "]] \n")
                if (len(self.FAR_IN[i]) == 0): f.write("    <N/A>\n")
                else: 
                    for k in range (len(self.FAR_IN[i])): f.write("   <" + self.FAR_IN[i][k].RequestID + "> <" + self.FAR_IN[i][k].FunctionID + "> <" + str(self.FAR_IN[i][k].FunctionParameters) + ">\n")
                f.write("\n")
                
            f.close();

        #print(self.PRD_IN)
        #print(self.updatedPRDCODE)

        
    #MAIN CLASS MAIN FUNCTION END -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    #MAIN CLASS SUBFUNCTIONS ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    #PRD Control Functions
    def edit_PRD_OUT(self, PRD_CODE, data):
        Index = -1
        for i in range (len(self.PRD_OUT)):
            if self.PRD_OUT[i][0] == PRD_CODE: Index = i
        if Index == -1: 
            if type(data) == list: self.PRD_OUT.append([PRD_CODE, True] + data); logIPC(self, "PRD Appended: <" + PRD_CODE + "> <" + str(data) + ">")
            else: self.PRD_OUT.append([PRD_CODE, True, data]); logIPC(self, "PRD Appended: <" + PRD_CODE + "> <" + str(data) + ">")
        else: 
            if type(data) == list: self.PRD_OUT[Index] = [PRD_CODE, True] + data; logIPC(self, "PRD Edited:<" + PRD_CODE + "> <" + str(data) + ">")
            else: self.PRD_OUT[Index] = ([PRD_CODE, True, data]); logIPC(self, "PRD Edited: <" + PRD_CODE + "> <" + str(data) + ">")
            
    def get_PRD_IN(self, targetManager, PRD_CODE):
        try: managerIndex = self.IPCB_ID.index(targetManager)
        except: return "MNF"
        dataIndex = -1
        for i in range (len(self.PRD_IN[managerIndex])):
            if self.PRD_IN[managerIndex][i][0] == PRD_CODE: dataIndex = i
        if (dataIndex == -1): return "DNF"
        else: return self.PRD_IN[managerIndex][dataIndex][2:]

    def get_UpdatedPRDCodes(self, targetManager):
        try: managerIndex = self.IPCB_ID.index(targetManager)
        except: return "MNF"
        PRD_CODES = list(self.updatedPRDCODE[managerIndex])
        self.updatedPRDCODE[managerIndex].clear()
        return PRD_CODES



    #FA Control Functions
    def send_FARequest(self, targetManager, FunctionID, FunctionParameters):
        try: managerIndex = self.IPCB_ID.index(targetManager)
        except: logIPC(self, "FAR Registration Rejected: Manager '" + targetManager + "' Not Found"); return "MNF"
        RequestID = -1
        for i in range (self.FAR_BL):
            count = 0
            for k in range (len(self.FAR_OUT[managerIndex])):
                if (i == int(self.FAR_OUT[managerIndex][k].RequestID)): count += 1; break;
            if count == 0: RequestID = i; break;
        if (RequestID == -1): logIPC(self, "FAR Registration via IPCB_T" + str(managerIndex) + " Rejected: Buffer Limit Reached [" + targetManager + ", " + FunctionID + ", " + str(FunctionParameters) + "]"); return "BLR"
        else: 
            RequestID = str(RequestID)
            self.FAR_OUT[managerIndex].append(FAR_OUT(RequestID, FunctionID, FunctionParameters))
            logIPC(self, "FAR Registered via IPCB_T" + str(managerIndex) + ": [RID:" + RequestID + "] [" + targetManager + ", " + FunctionID + ", " + str(FunctionParameters) + "]")
            return RequestID

    def read_FARequest(self, targetManager):
        try: managerIndex = self.IPCB_ID.index(targetManager)
        except: logIPC(self, "FAR Read Failed: Manager '" + targetManager + "' Not Found"); return "MNF"
        if (len(self.FAR_IN[managerIndex]) > 0): #If there exists any FARequest from the selected manager,
            for i in range (len(self.FAR_IN[managerIndex])):
                if (self.FAR_IN[managerIndex][i].Read == False): #If the FARequest Has not been read
                    self.FAR_IN[managerIndex][i].Read = True
                    return self.FAR_IN[managerIndex][i] #Return the latest non-read FARequest
            return "DAR" #If all the requests have been read, return the "DAR" keyword (= Data All Read)
        else: return "DNF" #If not, return the "DNF" keyword (= Data Not Found)

    def send_FAResult(self, targetManager, requestID, result):
        try: managerIndex = self.IPCB_ID.index(targetManager)
        except: logIPC(self, "FA Result Registration Failed: Manager '" + targetManager + "' Not Found"); return "MNF"
        resultRegistered = False
        for i in range (len(self.FAR_IN[managerIndex])):
            if (self.FAR_IN[managerIndex][i].RequestID == requestID):
                self.FAR_IN[managerIndex][i].Result = result
                resultRegistered = True; break;
        if (resultRegistered == True): logIPC(self, "FA Result Registration Completed: Manager '" + targetManager + "' Not Found"); #Result Registration Successful
        else: logIPC(self, "FA Result Registration Failed: Request ID '" + requestID + "' Not Found"); #Result Registration Failed - Request ID not found

    def read_FAResult(self, targetManager, requestID):
        try: managerIndex = self.IPCB_ID.index(targetManager)
        except: logIPC(self, "FA Result Read Failed: Manager '" + targetManager + "' Not Found"); return "MNF"
        for i in range (len(self.FAR_OUT[managerIndex])):
            if (self.FAR_OUT[managerIndex][i].RequestID == requestID):
                if (self.FAR_OUT[managerIndex][i].RequestStatus == "RECEIVED"):
                    result = self.FAR_OUT[managerIndex][i].Result
                    self.FAR_OUT[managerIndex].pop(i)
                    logIPC(self, "FA Result Read Complete!");
                    return result
                else:
                    logIPC(self, "FA Result Read Failed: Result For '" + requestID + "' Not Received")
                    return "DNR"
        logIPC(self, "FA Result Read Failed: Request ID '" + requestID + "' Not Found")
        return "DNF"

    #System Message Write
    def write_SystemMessage(self, msg):
        self.systemMessages.append([time.time_ns() - self.PST, msg])
    #MAIN CLASS SUBFUNCTIONS END --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#MAIN CLASS END -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    
#AUXILLARY FUNCTION ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def logIPC(self, msg):
    if (self.recordControl[0] == True):
        loggingTime = time.time_ns() - self.PST
        if (loggingTime > 1000000000): loggingTime = loggingTime / 1000000000; self.IPCRecords.append("[{:.3f}s] ".format(loggingTime) + msg)
        else: loggingTime = loggingTime / 1000000; self.IPCRecords.append("[{:.3f}ms] ".format(loggingTime) + msg)
#AUXILLARY FUNCTION END -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------



#CLASSES --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
class FAR_OUT:
    def __init__(self, RequestID, FunctionID, FunctionParameters):
        self.RequestID = RequestID
        #Request Status - ["PENDING": Request created but not yet sent] ["SENT": Request sent, waiting for response] ["RECEIVED": Result received, waiting to be read] ["RENOUNCE": Request unacceptable, remove the request]
        self.RequestStatus = "PENDING"
        self.FunctionID = FunctionID
        self.FunctionParameters = FunctionParameters
        self.Result = NONE
        self.timer = 0

class FAR_IN:
    def __init__(self, RequestID, FunctionID, FunctionParameters):
        self.RequestID = RequestID
        self.FunctionID = FunctionID
        self.FunctionParameters = FunctionParameters
        self.Result = NONE
        self.Read = False
        self.timer = 0
#CLASSES END ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------