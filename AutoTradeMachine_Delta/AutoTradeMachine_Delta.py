"""
(S)DLT: (System) Determined Loop Time
TRNS: Timer Record Number of Samples
RPT: REPORT
PST: Program Start Time
"""

#ATM Modules
from decimal import ROUND_FLOOR
from multiprocessing import process
from ATM_Delta_Manager_AutoTrader import manager_AutoTrader
from ATM_Delta_Manager_Auxillary import manager_Auxillary
from ATM_Delta_Manager_BinanceAPI import manager_BinanceAPI
from ATM_Delta_Manager_DataAnalysis import manager_DataAnalysis
from ATM_Delta_Manager_DataManagement import manager_DataManagement
from ATM_Delta_Manager_GUI import manager_GUI
from ATM_Delta_Manager_SecurityControl import manager_SecurityControl

#Python Modules
import os
import multiprocessing
import time
import csv
import numpy
import math

path_PROJECT = os.path.dirname(os.path.realpath(__file__))

#PROCESSES ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#Process_P ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def process_P(IPCB_T0, IPCB_T1, IPCB_T2, IPCB_T3, IPCB_T4, IPCB_T5, IPCB_T6, IPCB_F0, IPCB_F1, IPCB_F2, IPCB_F3, IPCB_F4, IPCB_F5, IPCB_F6, processVariables):
    #IPCB Interpretation ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        #IPCB_F0 [AUTOTRADER]
    targetIndex = 1
    while (len(IPCB_F0) > 0):
        line = IPCB_F0.pop(0)
        if (line[0] == "RPT") and (line[1] == "SYS_TIME"): systemManagement[6][targetIndex][0] = int(float(line[2])); systemManagement[6][targetIndex][1] = int(float(line[3])); systemManagement[6][targetIndex][2] = int(float(line[4]))
        elif (line[0] == "RPT") and (line[1] == "SYS_MSG"): addSystemMsg(line[2], str(line[3]), targetIndex)
        elif (line[0] == "RPT") and (line[1] == "SYS_TERMINATED"): addSystemMsg(time.time_ns() - systemManagement[0], "PROCESS TERMINATED: " + str(line[2]), targetIndex)
        elif (line[0] == "DATASHARE"): edit_PRD_IN(targetIndex - 1, line[1:]);
        else: addSystemMsg(time.time_ns() - systemManagement[0], "Unrecognizable Message Detected From IPCB_F0: '" + str(line) + "'")

        #IPCB_F1 [AUXILLARY]
    targetIndex = 2
    while (len(IPCB_F1) > 0):
        line = IPCB_F1.pop(0)
        if (line[0] == "RPT") and (line[1] == "SYS_TIME"): systemManagement[6][targetIndex][0] = int(float(line[2])); systemManagement[6][targetIndex][1] = int(float(line[3])); systemManagement[6][targetIndex][2] = int(float(line[4]))
        elif (line[0] == "RPT") and (line[1] == "SYS_MSG"): addSystemMsg(line[2], str(line[3]), targetIndex)
        elif (line[0] == "RPT") and (line[1] == "SYS_TERMINATED"): addSystemMsg(time.time_ns() - systemManagement[0], "PROCESS TERMINATED: " + str(line[2]), targetIndex)
        elif (line[0] == "DATASHARE"): edit_PRD_IN(targetIndex - 1, line[1:])
        else: addSystemMsg(time.time_ns() - systemManagement[0], "Unrecognizable Message Detected From IPCB_F1: '" + str(line) + "'")

        #IPCB_F2 [BINANCEAPI]
    targetIndex = 3
    while (len(IPCB_F2) > 0):
        line = IPCB_F2.pop(0)
        if (line[0] == "RPT") and (line[1] == "SYS_TIME"): systemManagement[6][targetIndex][0] = int(float(line[2])); systemManagement[6][targetIndex][1] = int(float(line[3])); systemManagement[6][targetIndex][2] = int(float(line[4]))
        elif (line[0] == "RPT") and (line[1] == "SYS_MSG"): addSystemMsg(line[2], str(line[3]), targetIndex)
        elif (line[0] == "RPT") and (line[1] == "SYS_TERMINATED"): addSystemMsg(time.time_ns() - systemManagement[0], "PROCESS TERMINATED: " + str(line[2]), targetIndex)
        elif (line[0] == "DATASHARE"): edit_PRD_IN(targetIndex - 1, line[1:])
        else: addSystemMsg(time.time_ns() - systemManagement[0], "Unrecognizable Message Detected From IPCB_F2: '" + str(line) + "'")

        #IPCB_F3 [DATAANALYSIS]
    targetIndex = 4
    while (len(IPCB_F3) > 0):
        line = IPCB_F3.pop(0)
        if (line[0] == "RPT") and (line[1] == "SYS_TIME"): systemManagement[6][targetIndex][0] = int(float(line[2])); systemManagement[6][targetIndex][1] = int(float(line[3])); systemManagement[6][targetIndex][2] = int(float(line[4]))
        elif (line[0] == "RPT") and (line[1] == "SYS_MSG"): addSystemMsg(line[2], str(line[3]), targetIndex)
        elif (line[0] == "RPT") and (line[1] == "SYS_TERMINATED"): addSystemMsg(time.time_ns() - systemManagement[0], "PROCESS TERMINATED: " + str(line[2]), targetIndex)
        elif (line[0] == "DATASHARE"): edit_PRD_IN(targetIndex - 1, line[1:])
        else: addSystemMsg(time.time_ns() - systemManagement[0], "Unrecognizable Message Detected From IPCB_F3: '" + str(line) + "'")

        #IPCB_F4 [DATAMANAGEMENT]
    targetIndex = 5
    while (len(IPCB_F4) > 0):
        line = IPCB_F4.pop(0)
        if (line[0] == "RPT") and (line[1] == "SYS_TIME"): systemManagement[6][targetIndex][0] = int(float(line[2])); systemManagement[6][targetIndex][1] = int(float(line[3])); systemManagement[6][targetIndex][2] = int(float(line[4]))
        elif (line[0] == "RPT") and (line[1] == "SYS_MSG"): addSystemMsg(line[2], str(line[3]), targetIndex)
        elif (line[0] == "RPT") and (line[1] == "SYS_TERMINATED"): addSystemMsg(time.time_ns() - systemManagement[0], "PROCESS TERMINATED: " + str(line[2]), targetIndex)
        elif (line[0] == "DATASHARE"): edit_PRD_IN(targetIndex - 1, line[1:])
        else: addSystemMsg(time.time_ns() - systemManagement[0], "Unrecognizable Message Detected From IPCB_F4: '" + str(line) + "'")

        #IPCB_F5 [GUI]
    targetIndex = 6
    while (len(IPCB_F5) > 0):
        line = IPCB_F5.pop(0)
        if (line[0] == "RPT") and (line[1] == "SYS_TIME"): systemManagement[6][targetIndex][0] = int(float(line[2])); systemManagement[6][targetIndex][1] = int(float(line[3])); systemManagement[6][targetIndex][2] = int(float(line[4]))
        elif (line[0] == "RPT") and (line[1] == "SYS_MSG"): addSystemMsg(line[2], str(line[3]), targetIndex)
        elif (line[0] == "RPT") and (line[1] == "SYS_TERMINATED"): addSystemMsg(time.time_ns() - systemManagement[0], "PROCESS TERMINATED: " + str(line[2]), targetIndex)
        elif (line[0] == "DATASHARE"): edit_PRD_IN(targetIndex - 1, line[1:])
        else: addSystemMsg(time.time_ns() - systemManagement[0], "Unrecognizable Message Detected From IPCB_F5: '" + str(line) + "'")

        #IPCB_F6 [SECURITYCONTROL]
    targetIndex = 7
    while (len(IPCB_F6) > 0):
        line = IPCB_F6.pop(0)
        if (line[0] == "RPT") and (line[1] == "SYS_TIME"): systemManagement[6][targetIndex][0] = int(float(line[2])); systemManagement[6][targetIndex][1] = int(float(line[3])); systemManagement[6][targetIndex][2] = int(float(line[4]))
        elif (line[0] == "RPT") and (line[1] == "SYS_MSG"): addSystemMsg(line[2], str(line[3]), targetIndex)
        elif (line[0] == "RPT") and (line[1] == "SYS_TERMINATED"): addSystemMsg(time.time_ns() - systemManagement[0], "PROCESS TERMINATED: " + str(line[2]), targetIndex)
        elif (line[0] == "DATASHARE"): edit_PRD_IN(targetIndex - 1, line[1:])
        else: addSystemMsg(time.time_ns() - systemManagement[0], "Unrecognizable Message Detected From IPCB_F6: '" + str(line) + "'")
    #IPCB Interpretation END --------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    
    #Editing PRD_OUT
    if (((time.time_ns() - processVariables["timer_PRDSEND_SYSTIME"]) > (1e9 * processVariables["timerInterval_PRDSEND_SYSTIME"]))):
        processVariables["timer_PRDSEND_SYSTIME"] = time.time_ns()
        edit_PRD_OUT("SYS_TIME_PP", systemManagement[6][0]) #ProcessP Timer Record
        edit_PRD_OUT("SYS_TIME_P0", systemManagement[6][1]) #Process0 Timer Record
        edit_PRD_OUT("SYS_TIME_P1", systemManagement[6][2]) #Process1 Timer Record
        edit_PRD_OUT("SYS_TIME_P2", systemManagement[6][3]) #Process2 Timer Record
        edit_PRD_OUT("SYS_TIME_P3", systemManagement[6][4]) #Process3 Timer Record
        edit_PRD_OUT("SYS_TIME_P4", systemManagement[6][5]) #Process4 Timer Record
        edit_PRD_OUT("SYS_TIME_P5", systemManagement[6][6]) #Process5 Timer Record
        edit_PRD_OUT("SYS_TIME_P6", systemManagement[6][7]) #Process6 Timer Record

    #Announce variation-detected pre-registered data
    for i in range (len(PRD_OUT)):
        if PRD_OUT[i][1] == True: line = ["DATASHARE", PRD_OUT[i][0]] + PRD_OUT[i][2:]; IPCB_T0.append(line); IPCB_T1.append(line); IPCB_T2.append(line); IPCB_T3.append(line); IPCB_T4.append(line); IPCB_T5.append(line); IPCB_T6.append(line)

    #System Message Recording -------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    if (processVariables["setting_RECORD_SYSTEMMESSAGES"] == True):
        if len(systemManagement[5]) > 0:
            f = open(os.path.join(path_MAIN, 'systemMessages.txt'), 'a')
            for i in range (len(systemManagement[5])):
                f.write(systemManagement[5][i] + "\n")
                if (systemManagement[1] == True): print(systemManagement[5][i])
            f.close(); systemManagement[5].clear()
    #System Message Recording END ---------------------------------------------------------------------------------------------------------------------------------------------------------------------
    #Processes Timer Record Logging -------------------------------------------------------------------------------------------------------------------------------------------------------------------
    if (processVariables["setting_RECORD_PROCESSTIMER"] == True):
        f = open(os.path.join(path_MAIN, 'processesTimerRecord.txt'), 'w')
        for i in range (len(systemManagement[6])):
            if i == 0: f.write("PROCESS_P: Average Loop Time [{:.3f} us], Average Processing Time [{:.3f} us], Number of Samples [{:d}] \n".format(systemManagement[6][i][0] / 1000, systemManagement[6][i][1] / 1000, systemManagement[6][i][2]))
            else: f.write("PROCESS{:d}: Average Loop Time [{:.3f} us], Average Processing Time [{:.3f} us], Number of Samples [{:d}] \n".format(i-1, systemManagement[6][i][0] / 1000, systemManagement[6][i][1] / 1000, systemManagement[6][i][2]))
        f.close()
    #Processes Timer Record Logging END ---------------------------------------------------------------------------------------------------------------------------------------------------------------

    return True
#Process_P END -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        


#Process0 ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def process0(IPCB_T0, IPCB_T1, IPCB_T2, IPCB_T3, IPCB_T4, IPCB_T5, IPCB_T6, IPCB_F0, IPCB_F1, IPCB_F2, IPCB_F3, IPCB_F4, IPCB_F5, IPCB_F6):
    processStatus = True; PST = IPCB_F0.pop(0); SDLT = IPCB_F0.pop(0); record_nSamples = IPCB_F0.pop(0)
    m_AutoTrader = manager_AutoTrader(PST)
    processTimer = [time.perf_counter_ns(), 0, 0] #[0]: Last Loop Start Time, [1]: Current Loop Start Time, [2]: Processing Time
    timerRecord = [[],[]]; timerAvg = [0, 0];
    IPCB_T0.append(["RPT", "SYS_MSG", time.time_ns() - PST, "PROCESS INITIALIZATION COMPLETE!"])
    while (processStatus == True):
        if (time.perf_counter_ns() - processTimer[0]) >= (int(SDLT) * 1000000):
            #Loop END & Record ------------------------------------------------------------------------------------------------------------------------------------------------------------------------
            processTimer[1] = time.perf_counter_ns()
            #Loop Start -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
            while (len(timerRecord[0]) >= int(record_nSamples)): timerRecord[0].pop(1); timerRecord[1].pop(1)
            timerRecord[0].append(processTimer[1] - processTimer[0]); timerRecord[1].append(processTimer[2])
            timerAvg = [numpy.mean(timerRecord[0]), numpy.mean(timerRecord[1])];
            #print("PROCESS0: Average Loop Time [{:.3f} us], Average Processing Time [{:.3f} us], Number of Samples [{:d}]".format(timerAvg[0] / 1000, timerAvg[1] / 1000, len(timerRecord[0])));
            processTimer[2] = time.perf_counter_ns()
            #PROCESS BEGIN ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
            if (m_AutoTrader.process(IPCB_T0, IPCB_T1, IPCB_T2, IPCB_T3, IPCB_T4, IPCB_T5, IPCB_T6, IPCB_F0, IPCB_F1, IPCB_F2, IPCB_F3, IPCB_F4, IPCB_F5, IPCB_F6) == False): processStatus = False; IPCB_T0.append(["RPT", "SYS_TERMINATED", "PROCESS RETURNED 'False'"]) #MAIN PROCESS
            #PROCESS END ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
            IPCB_T0.append(["RPT", "SYS_TIME", str(timerAvg[0]), str(timerAvg[1]), str(len(timerRecord[0]))])
            processTimer[2] = time.perf_counter_ns() - processTimer[2]; processTimer[0] = processTimer[1]
            delay = math.trunc((int(SDLT) - processTimer[2] / 1000000)) / 1000 
            if (delay > 0): time.sleep(delay);
#Process0 END ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#Process1 ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def process1(IPCB_T0, IPCB_T1, IPCB_T2, IPCB_T3, IPCB_T4, IPCB_T5, IPCB_T6, IPCB_F0, IPCB_F1, IPCB_F2, IPCB_F3, IPCB_F4, IPCB_F5, IPCB_F6):
    processStatus = True; PST = IPCB_F0.pop(0); SDLT = IPCB_F0.pop(0); record_nSamples = IPCB_F0.pop(0)
    m_Auxillary = manager_Auxillary(PST)
    processTimer = [time.perf_counter_ns(), 0, 0] #[0]: Last Loop Start Time, [1]: Current Loop Start Time, [2]: Processing Time
    timerRecord = [[],[]]; timerAvg = [0, 0];
    IPCB_T0.append(["RPT", "SYS_MSG", time.time_ns() - PST, "PROCESS INITIALIZATION COMPLETE!"])
    while (processStatus == True):
        if (time.perf_counter_ns() - processTimer[0]) >= (int(SDLT) * 1000000):
            #Loop END & Record ------------------------------------------------------------------------------------------------------------------------------------------------------------------------
            processTimer[1] = time.perf_counter_ns()
            #Loop Start -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
            while (len(timerRecord[0]) >= int(record_nSamples)): timerRecord[0].pop(1); timerRecord[1].pop(1)
            timerRecord[0].append(processTimer[1] - processTimer[0]); timerRecord[1].append(processTimer[2])
            timerAvg = [numpy.mean(timerRecord[0]), numpy.mean(timerRecord[1])];
            #print("PROCESS1: Average Loop Time [{:.3f} us], Average Processing Time [{:.3f} us], Number of Samples [{:d}]".format(timerAvg[0] / 1000, timerAvg[1] / 1000, len(timerRecord[0])));
            processTimer[2] = time.perf_counter_ns()
            #PROCESS BEGIN ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
            if (m_Auxillary.process(IPCB_T0, IPCB_T1, IPCB_T2, IPCB_T3, IPCB_T4, IPCB_T5, IPCB_T6, IPCB_F0, IPCB_F1, IPCB_F2, IPCB_F3, IPCB_F4, IPCB_F5, IPCB_F6) == False): processStatus = False; IPCB_T0.append(["RPT", "SYS_TERMINATED", "PROCESS RETURNED 'False'"]) #MAIN PROCESS
            #PROCESS END ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
            IPCB_T0.append(["RPT", "SYS_TIME", str(timerAvg[0]), str(timerAvg[1]), str(len(timerRecord[0]))])
            processTimer[2] = time.perf_counter_ns() - processTimer[2]; processTimer[0] = processTimer[1]
            delay = math.trunc((int(SDLT) - processTimer[2] / 1000000)) / 1000 
            if (delay > 0): time.sleep(delay);
#Process1 END ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#Process2 ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def process2(IPCB_T0, IPCB_T1, IPCB_T2, IPCB_T3, IPCB_T4, IPCB_T5, IPCB_T6, IPCB_F0, IPCB_F1, IPCB_F2, IPCB_F3, IPCB_F4, IPCB_F5, IPCB_F6):
    processStatus = True; PST = IPCB_F0.pop(0); SDLT = IPCB_F0.pop(0); record_nSamples = IPCB_F0.pop(0)
    m_BinanceAPI = manager_BinanceAPI(PST)
    processTimer = [time.perf_counter_ns(), 0, 0] #[0]: Last Loop Start Time, [1]: Current Loop Start Time, [2]: Processing Time
    timerRecord = [[],[]]; timerAvg = [0, 0];
    IPCB_T0.append(["RPT", "SYS_MSG", time.time_ns() - PST, "PROCESS INITIALIZATION COMPLETE!"])
    while (processStatus == True):
        if (time.perf_counter_ns() - processTimer[0]) >= (int(SDLT) * 1000000):
            #Loop END & Record ------------------------------------------------------------------------------------------------------------------------------------------------------------------------
            processTimer[1] = time.perf_counter_ns()
            #Loop Start -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
            while (len(timerRecord[0]) >= int(record_nSamples)): timerRecord[0].pop(1); timerRecord[1].pop(1)
            timerRecord[0].append(processTimer[1] - processTimer[0]); timerRecord[1].append(processTimer[2])
            timerAvg = [numpy.mean(timerRecord[0]), numpy.mean(timerRecord[1])];
            #print("PROCESS2: Average Loop Time [{:.3f} us], Average Processing Time [{:.3f} us], Number of Samples [{:d}]".format(timerAvg[0] / 1000, timerAvg[1] / 1000, len(timerRecord[0])));
            processTimer[2] = time.perf_counter_ns()
            #PROCESS BEGIN ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
            if (m_BinanceAPI.process(IPCB_T0, IPCB_T1, IPCB_T2, IPCB_T3, IPCB_T4, IPCB_T5, IPCB_T6, IPCB_F0, IPCB_F1, IPCB_F2, IPCB_F3, IPCB_F4, IPCB_F5, IPCB_F6) == False): processStatus = False; IPCB_T0.append(["RPT", "SYS_TERMINATED", "PROCESS RETURNED 'False'"]) #MAIN PROCESS
            #PROCESS END ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
            IPCB_T0.append(["RPT", "SYS_TIME", str(timerAvg[0]), str(timerAvg[1]), str(len(timerRecord[0]))])
            processTimer[2] = time.perf_counter_ns() - processTimer[2]; processTimer[0] = processTimer[1]
            delay = math.trunc((int(SDLT) - processTimer[2] / 1000000)) / 1000 
            if (delay > 0): time.sleep(delay);
#Process2 END ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#Process3 ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def process3(IPCB_T0, IPCB_T1, IPCB_T2, IPCB_T3, IPCB_T4, IPCB_T5, IPCB_T6, IPCB_F0, IPCB_F1, IPCB_F2, IPCB_F3, IPCB_F4, IPCB_F5, IPCB_F6):
    processStatus = True; PST = IPCB_F0.pop(0); SDLT = IPCB_F0.pop(0); record_nSamples = IPCB_F0.pop(0)
    m_DataAnalysis = manager_DataAnalysis(PST)
    processTimer = [time.perf_counter_ns(), 0, 0] #[0]: Last Loop Start Time, [1]: Current Loop Start Time, [2]: Processing Time
    timerRecord = [[],[]]; timerAvg = [0, 0];
    IPCB_T0.append(["RPT", "SYS_MSG", time.time_ns() - PST, "PROCESS INITIALIZATION COMPLETE!"])
    while (processStatus == True): 
        if (time.perf_counter_ns() - processTimer[0]) >= (int(SDLT) * 1000000):
            #Loop END & Record ------------------------------------------------------------------------------------------------------------------------------------------------------------------------
            processTimer[1] = time.perf_counter_ns()
            #Loop Start -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
            while (len(timerRecord[0]) >= int(record_nSamples)): timerRecord[0].pop(1); timerRecord[1].pop(1)
            timerRecord[0].append(processTimer[1] - processTimer[0]); timerRecord[1].append(processTimer[2])
            timerAvg = [numpy.mean(timerRecord[0]), numpy.mean(timerRecord[1])];
            #print("PROCESS3: Average Loop Time [{:.3f} us], Average Processing Time [{:.3f} us], Number of Samples [{:d}]".format(timerAvg[0] / 1000, timerAvg[1] / 1000, len(timerRecord[0])));
            processTimer[2] = time.perf_counter_ns()
            #PROCESS BEGIN ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
            if (m_DataAnalysis.process(IPCB_T0, IPCB_T1, IPCB_T2, IPCB_T3, IPCB_T4, IPCB_T5, IPCB_T6, IPCB_F0, IPCB_F1, IPCB_F2, IPCB_F3, IPCB_F4, IPCB_F5, IPCB_F6) == False): processStatus = False; IPCB_T0.append(["RPT", "SYS_TERMINATED", "PROCESS RETURNED 'False'"]) #MAIN PROCESS
            #PROCESS END ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
            IPCB_T0.append(["RPT", "SYS_TIME", str(timerAvg[0]), str(timerAvg[1]), str(len(timerRecord[0]))])
            processTimer[2] = time.perf_counter_ns() - processTimer[2]; processTimer[0] = processTimer[1]
            delay = math.trunc((int(SDLT) - processTimer[2] / 1000000)) / 1000 
            if (delay > 0): time.sleep(delay);
#Process3 END ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#Process4 ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def process4(IPCB_T0, IPCB_T1, IPCB_T2, IPCB_T3, IPCB_T4, IPCB_T5, IPCB_T6, IPCB_F0, IPCB_F1, IPCB_F2, IPCB_F3, IPCB_F4, IPCB_F5, IPCB_F6):
    processStatus = True; PST = IPCB_F0.pop(0); SDLT = IPCB_F0.pop(0); record_nSamples = IPCB_F0.pop(0)
    m_DataManagement = manager_DataManagement(PST)
    processTimer = [time.perf_counter_ns(), 0, 0] #[0]: Last Loop Start Time, [1]: Current Loop Start Time, [2]: Processing Time
    timerRecord = [[],[]]; timerAvg = [0, 0];
    IPCB_T0.append(["RPT", "SYS_MSG", time.time_ns() - PST, "PROCESS INITIALIZATION COMPLETE!"])
    while (processStatus == True):
        if (time.perf_counter_ns() - processTimer[0]) >= (int(SDLT) * 1000000):
            #Loop END & Record ------------------------------------------------------------------------------------------------------------------------------------------------------------------------
            processTimer[1] = time.perf_counter_ns()
            #Loop Start -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
            while (len(timerRecord[0]) >= int(record_nSamples)): timerRecord[0].pop(1); timerRecord[1].pop(1)
            timerRecord[0].append(processTimer[1] - processTimer[0]); timerRecord[1].append(processTimer[2])
            timerAvg = [numpy.mean(timerRecord[0]), numpy.mean(timerRecord[1])];
            #print("PROCESS4: Average Loop Time [{:.3f} us], Average Processing Time [{:.3f} us], Number of Samples [{:d}]".format(timerAvg[0] / 1000, timerAvg[1] / 1000, len(timerRecord[0])));
            processTimer[2] = time.perf_counter_ns()
            #PROCESS BEGIN ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
            if (m_DataManagement.process(IPCB_T0, IPCB_T1, IPCB_T2, IPCB_T3, IPCB_T4, IPCB_T5, IPCB_T6, IPCB_F0, IPCB_F1, IPCB_F2, IPCB_F3, IPCB_F4, IPCB_F5, IPCB_F6) == False): processStatus = False; IPCB_T0.append(["RPT", "SYS_TERMINATED", "PROCESS RETURNED 'False'"]) #MAIN PROCESS
            #PROCESS END ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
            IPCB_T0.append(["RPT", "SYS_TIME", str(timerAvg[0]), str(timerAvg[1]), str(len(timerRecord[0]))])
            processTimer[2] = time.perf_counter_ns() - processTimer[2]; processTimer[0] = processTimer[1]
            delay = math.trunc((int(SDLT) - processTimer[2] / 1000000)) / 1000 
            if (delay > 0): time.sleep(delay);
#Process4 END ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#Process5 ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def process5(IPCB_T0, IPCB_T1, IPCB_T2, IPCB_T3, IPCB_T4, IPCB_T5, IPCB_T6, IPCB_F0, IPCB_F1, IPCB_F2, IPCB_F3, IPCB_F4, IPCB_F5, IPCB_F6):
    PST = IPCB_F0.pop(0); SDLT = IPCB_F0.pop(0); record_nSamples = IPCB_F0.pop(0)
    m_GUI = manager_GUI(PST)
    processTimer = [time.perf_counter_ns(), 0, 0] #[0]: Last Loop Start Time, [1]: Current Loop Start Time, [2]: Processing Time
    timerRecord = [[],[]]; timerAvg = [0, 0];
    IPCB_T0.append(["RPT", "SYS_MSG", time.time_ns() - PST, "PROCESS INITIALIZATION COMPLETE!"])
    def m_GUI_mainer0(IPCB_T0, IPCB_T1, IPCB_T2, IPCB_T3, IPCB_T4, IPCB_T5, IPCB_T6, IPCB_F0, IPCB_F1, IPCB_F2, IPCB_F3, IPCB_F4, IPCB_F5, IPCB_F6):
        if (time.perf_counter_ns() - processTimer[0]) >= (int(SDLT) * 1000000):
            #Loop END & Record ------------------------------------------------------------------------------------------------------------------------------------------------------------------------
            processTimer[1] = time.perf_counter_ns()
            #Loop Start -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
            while (len(timerRecord[0]) >= int(record_nSamples)): timerRecord[0].pop(1); timerRecord[1].pop(1)
            timerRecord[0].append(processTimer[1] - processTimer[0]); timerRecord[1].append(processTimer[2])
            timerAvg = [numpy.mean(timerRecord[0]), numpy.mean(timerRecord[1])];
            #print("PROCESS5: Average Loop Time [{:.3f} us], Average Processing Time [{:.3f} us], Number of Samples [{:d}]".format(timerAvg[0] / 1000, timerAvg[1] / 1000, len(timerRecord[0])));
            processTimer[2] = time.perf_counter_ns()
            #PROCESS BEGIN ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
            if (m_GUI.process(IPCB_T0, IPCB_T1, IPCB_T2, IPCB_T3, IPCB_T4, IPCB_T5, IPCB_T6, IPCB_F0, IPCB_F1, IPCB_F2, IPCB_F3, IPCB_F4, IPCB_F5, IPCB_F6) == False): m_GUI.window.destroy(); IPCB_T0.append(["RPT", "SYS_TERMINATED", "PROCESS RETURNED 'False'"]) #MAIN PROCESS
            #PROCESS END ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
            IPCB_T0.append(["RPT", "SYS_TIME", str(timerAvg[0]), str(timerAvg[1]), str(len(timerRecord[0]))])
            processTimer[2] = time.perf_counter_ns() - processTimer[2]; processTimer[0] = processTimer[1]
            delay = math.trunc((int(SDLT) - processTimer[2] / 1000000)) / 1000
            if (delay > 0): time.sleep(delay);
        m_GUI.window.after_idle(m_GUI_mainer0, IPCB_T0, IPCB_T1, IPCB_T2, IPCB_T3, IPCB_T4, IPCB_T5, IPCB_T6, IPCB_F0, IPCB_F1, IPCB_F2, IPCB_F3, IPCB_F4, IPCB_F5, IPCB_F6)


    m_GUI.window.after(100, m_GUI_mainer0, IPCB_T0, IPCB_T1, IPCB_T2, IPCB_T3, IPCB_T4, IPCB_T5, IPCB_T6, IPCB_F0, IPCB_F1, IPCB_F2, IPCB_F3, IPCB_F4, IPCB_F5, IPCB_F6)
    m_GUI.window.mainloop()
#Process5 END ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#Process6 ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def process6(IPCB_T0, IPCB_T1, IPCB_T2, IPCB_T3, IPCB_T4, IPCB_T5, IPCB_T6, IPCB_F0, IPCB_F1, IPCB_F2, IPCB_F3, IPCB_F4, IPCB_F5, IPCB_F6):
    processStatus = True; PST = IPCB_F0.pop(0); SDLT = IPCB_F0.pop(0); record_nSamples = IPCB_F0.pop(0)
    m_SecurityControl = manager_SecurityControl(PST)
    processTimer = [time.perf_counter_ns(), 0, 0] #[0]: Last Loop Start Time, [1]: Current Loop Start Time, [2]: Processing Time
    timerRecord = [[],[]]; timerAvg = [0, 0];
    IPCB_T0.append(["RPT", "SYS_MSG", time.time_ns() - PST, "PROCESS INITIALIZATION COMPLETE!"])
    while (processStatus == True):
        if (time.perf_counter_ns() - processTimer[0]) >= (int(SDLT) * 1000000):
            #Loop END & Record ------------------------------------------------------------------------------------------------------------------------------------------------------------------------
            processTimer[1] = time.perf_counter_ns()
            #Loop Start -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
            while (len(timerRecord[0]) >= int(record_nSamples)): timerRecord[0].pop(1); timerRecord[1].pop(1)
            timerRecord[0].append(processTimer[1] - processTimer[0]); timerRecord[1].append(processTimer[2])
            timerAvg = [numpy.mean(timerRecord[0]), numpy.mean(timerRecord[1])];
            #print("PROCESS6: Average Loop Time [{:.3f} us], Average Processing Time [{:.3f} us], Number of Samples [{:d}]".format(timerAvg[0] / 1000, timerAvg[1] / 1000, len(timerRecord[0])));
            processTimer[2] = time.perf_counter_ns()
            #PROCESS BEGIN ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
            if (m_SecurityControl.process(IPCB_T0, IPCB_T1, IPCB_T2, IPCB_T3, IPCB_T4, IPCB_T5, IPCB_T6, IPCB_F0, IPCB_F1, IPCB_F2, IPCB_F3, IPCB_F4, IPCB_F5, IPCB_F6) == False): processStatus = False; IPCB_T0.append(["RPT", "SYS_TERMINATED", "PROCESS RETURNED 'False'"]) #MAIN PROCESS
            #PROCESS END ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
            IPCB_T0.append(["RPT", "SYS_TIME", str(timerAvg[0]), str(timerAvg[1]), str(len(timerRecord[0]))])
            processTimer[2] = time.perf_counter_ns() - processTimer[2]; processTimer[0] = processTimer[1]
            delay = math.trunc((int(SDLT) - processTimer[2] / 1000000)) / 1000 
            if (delay > 0): time.sleep(delay);
#Process6 END ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------



#AUXILLARY FUNCTIONS ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def readCSV(address):
    returnList = []
    with open(address, newline = '') as csvFile:
        reader = csv.reader(csvFile)
        for row in reader:
            if row: returnList.append(row)
    return returnList

def readTxt(address):
    returnList = []
    with open(address, 'r') as txtFile:
        lines = txtFile.readlines()
        for line in lines:
            if line: returnList.append(line.strip())
    return returnList

def addSystemMsg(generationTime, msg, reporter = 0):
    if reporter == 0: reporterName = "SYSTEM MAIN"
    elif reporter == 1: reporterName = "MANAGER [AUTO TRADER]"
    elif reporter == 2: reporterName = "MANAGER [AUXILLARY]"
    elif reporter == 3: reporterName = "MANAGER [BINANCE API]"
    elif reporter == 4: reporterName = "MANAGER [DATA ANALYSIS]"
    elif reporter == 5: reporterName = "MANAGER [DATA MANAGEMENT]"
    elif reporter == 6: reporterName = "MANAGER [GUI]"
    elif reporter == 7: reporterName = "MANAGER [SECURITY CONTROL]"
    if (generationTime > 1000000000): generationTime = generationTime / 1000000000; line = "[{:.3f}".format(generationTime) + " s] " + reporterName + ": " + msg
    else: generationTime = generationTime / 1000000; line = "[{:.3f}".format(generationTime) + " ms] " + reporterName + ": " + msg
    systemManagement[5].append(line)

def edit_PRD_IN(senderID, data):
    Index = -1
    for i in range (len(PRD_IN[senderID])):
        if PRD_IN[senderID][i][0] == data[0]: Index = i
    if Index == -1: PRD_IN[senderID].append(data);
    else: PRD_IN[senderID][Index] = data;

def edit_PRD_OUT(PRD_CODE, data):
    Index = -1
    for i in range (len(PRD_OUT)):
        if PRD_OUT[i][0] == PRD_CODE: Index = i
    if Index == -1: 
        if type(data) == list: PRD_OUT.append([PRD_CODE, True] + data)
        else: PRD_OUT.append([PRD_CODE, True, data])
    else: 
        if type(data) == list: PRD_OUT[Index] = [PRD_CODE, True] + data
        else: PRD_OUT[Index] = ([PRD_CODE, True, data])
# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------



#MAIN ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    multiprocessing.freeze_support()

    programStartTime = time.time_ns()
    #Inter-Processes Communication Buffer Initialization
    """
    interProcComBuffer[0]  : From m_MAIN to m_AutoTrader
    interProcComBuffer[1]  : From m_MAIN to m_Auxillary
    interProcComBuffer[2]  : From m_MAIN to m_BinanceAPI
    interProcComBuffer[3]  : From m_MAIN to m_DataAnalysis
    interProcComBuffer[4]  : From m_MAIN to m_DataManagement
    interProcComBuffer[5]  : From m_MAIN to m_GUI
    interProcComBuffer[6]  : From m_MAIN to m_SecurityControl

    interProcComBuffer[7]  : From m_AutoTrader to m_MAIN
    interProcComBuffer[8]  : From m_AutoTrader to m_Auxillary
    interProcComBuffer[9]  : From m_AutoTrader to m_BinanceAPI
    interProcComBuffer[10] : From m_AutoTrader to m_DataAnalysis
    interProcComBuffer[11] : From m_AutoTrader to m_DataManagement
    interProcComBuffer[12] : From m_AutoTrader to m_GUI
    interProcComBuffer[13] : From m_AutoTrader to m_SecurityControl

    interProcComBuffer[14] : From m_Auxillary to m_MAIN
    interProcComBuffer[15] : From m_Auxillary to m_AutoTrader
    interProcComBuffer[16] : From m_Auxillary to m_BinanceAPI
    interProcComBuffer[17] : From m_Auxillary to m_DataAnalysis
    interProcComBuffer[18] : From m_Auxillary to m_DataManagement
    interProcComBuffer[19] : From m_Auxillary to m_GUI
    interProcComBuffer[20] : From m_Auxillary to m_SecurityControl

    interProcComBuffer[21] : From m_BinanceAPI to m_MAIN
    interProcComBuffer[22] : From m_BinanceAPI to m_AutoTrader
    interProcComBuffer[23] : From m_BinanceAPI to m_Auxillary
    interProcComBuffer[24] : From m_BinanceAPI to m_DataAnalysis
    interProcComBuffer[25] : From m_BinanceAPI to m_DataManagement
    interProcComBuffer[26] : From m_BinanceAPI to m_GUI
    interProcComBuffer[27] : From m_BinanceAPI to m_SecurityControl

    interProcComBuffer[28] : From m_DataAnalysis to m_MAIN
    interProcComBuffer[29] : From m_DataAnalysis to m_AutoTrader
    interProcComBuffer[30] : From m_DataAnalysis to m_Auxillary
    interProcComBuffer[31] : From m_DataAnalysis to m_BinanceAPI
    interProcComBuffer[32] : From m_DataAnalysis to m_DataManagement
    interProcComBuffer[33] : From m_DataAnalysis to m_GUI
    interProcComBuffer[34] : From m_DataAnalysis to m_SecurityControl

    interProcComBuffer[35] : From m_DataManagement to m_MAIN
    interProcComBuffer[36] : From m_DataManagement to m_AutoTrader
    interProcComBuffer[37] : From m_DataManagement to m_Auxillary
    interProcComBuffer[38] : From m_DataManagement to m_BinanceAPI
    interProcComBuffer[39] : From m_DataManagement to m_DataAnalysis
    interProcComBuffer[40] : From m_DataManagement to m_GUI
    interProcComBuffer[41] : From m_DataManagement to m_SecurityControl

    interProcComBuffer[42] : From m_GUI to m_MAIN
    interProcComBuffer[43] : From m_GUI to m_AutoTrader
    interProcComBuffer[44] : From m_GUI to m_Auxillary
    interProcComBuffer[45] : From m_GUI to m_BinanceAPI
    interProcComBuffer[46] : From m_GUI to m_DataAnalysis
    interProcComBuffer[47] : From m_GUI to m_DataManagement
    interProcComBuffer[48] : From m_GUI to m_SecurityControl

    interProcComBuffer[49] : From m_SecurityControl to m_MAIN
    interProcComBuffer[50] : From m_SecurityControl to m_AutoTrader
    interProcComBuffer[51] : From m_SecurityControl to m_Auxillary
    interProcComBuffer[52] : From m_SecurityControl to m_BinanceAPI
    interProcComBuffer[53] : From m_SecurityControl to m_DataAnalysis
    interProcComBuffer[54] : From m_SecurityControl to m_DataManagement
    interProcComBuffer[55] : From m_SecurityControl to m_GUI
    """
    IPCB = []
    mp_manager = multiprocessing.Manager()
    for i in range (56): IPCB.append(mp_manager.list());
    """
    [0]: Program Start Time
    [1]: Console Mode On
    [2]: Process Status
    [3]: Process System Defined Loop Times
    [4]: Process Timer Recorder Defined Number of Samples
    [5]: System Messages
    [6]: Process Timer Records [Average Loop Time, Average Processing Time, Number of Time Records]
    """
    systemManagement = []
    systemManagement.append(programStartTime)
    systemManagement.append(True)
    systemManagement.append([False, False, False, False, False, False, False, False])
    systemManagement.append([10, 10, 10, 10, 10, 10, 10, 10])
    systemManagement.append([1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000])
    systemManagement.append([])
    systemManagement.append([[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0]])

    """
    PRD_IN[0]: AUTOTRADER
    PRD_IN[1]: AUXILLARY
    PRD_IN[2]: BINANCEAPI
    PRD_IN[3]: DATAANALYSIS
    PRD_IN[4]: DATAMANAGEMENT
    PRD_IN[5]: GUI
    PRD_IN[6]: SECURITYCONTROL
    """
    PRD_IN = [[],[],[],[],[],[],[]]
    PRD_OUT = []
    
    addSystemMsg(time.time_ns() - systemManagement[0], "PROGRAM STARTED [" + time.ctime(time.time()) + "]")
    #Processes Spawning
    processes = []
    processes.append(multiprocessing.Process(name = "MANAGER_AUTOTRADER",      target = process0, args = (IPCB[7], IPCB[8], IPCB[9], IPCB[10], IPCB[11], IPCB[12], IPCB[13], IPCB[0], IPCB[15], IPCB[22], IPCB[29], IPCB[36], IPCB[43], IPCB[50])))
    processes.append(multiprocessing.Process(name = "MANAGER_AUXILLARY",       target = process1, args = (IPCB[14], IPCB[15], IPCB[16], IPCB[17], IPCB[18], IPCB[19], IPCB[20], IPCB[1], IPCB[8], IPCB[23], IPCB[30], IPCB[37], IPCB[44], IPCB[51])))
    processes.append(multiprocessing.Process(name = "MANAGER_BINANCEAPI",      target = process2, args = (IPCB[21], IPCB[22], IPCB[23], IPCB[24], IPCB[25], IPCB[26], IPCB[27], IPCB[2], IPCB[9], IPCB[16], IPCB[31], IPCB[38], IPCB[45], IPCB[52])))
    processes.append(multiprocessing.Process(name = "MANAGER_DATAANALYSIS",    target = process3, args = (IPCB[28], IPCB[29], IPCB[30], IPCB[31], IPCB[32], IPCB[33], IPCB[34], IPCB[3], IPCB[10], IPCB[17], IPCB[24], IPCB[39], IPCB[46], IPCB[53])))
    processes.append(multiprocessing.Process(name = "MANAGER_DATAMANAGEMENT",  target = process4, args = (IPCB[35], IPCB[36], IPCB[37], IPCB[38], IPCB[39], IPCB[40], IPCB[41], IPCB[4], IPCB[11], IPCB[18], IPCB[25], IPCB[32], IPCB[47], IPCB[54])))
    processes.append(multiprocessing.Process(name = "MANAGER_GUI",             target = process5, args = (IPCB[42], IPCB[43], IPCB[44], IPCB[45], IPCB[46], IPCB[47], IPCB[48], IPCB[5], IPCB[12], IPCB[19], IPCB[26], IPCB[33], IPCB[40], IPCB[55])))
    processes.append(multiprocessing.Process(name = "MANAGER_SECURITYCONTROL", target = process6, args = (IPCB[49], IPCB[50], IPCB[51], IPCB[52], IPCB[53], IPCB[54], IPCB[55], IPCB[6], IPCB[13], IPCB[20], IPCB[27], IPCB[34], IPCB[41], IPCB[48])))

    #Program Management Data Initialization
    path_MAIN = os.path.join(path_PROJECT + r"\data\m_MAIN")
    if os.path.isfile(os.path.join(path_MAIN, 'initializationSettings.txt')):
        addSystemMsg(time.time_ns() - systemManagement[0], "INITIALIZATION SETTINGS FILE FOUND, FILE DEFINED SETTINGS WILL BE USED")
        initSettingsFile = readTxt(os.path.join(path_MAIN, 'initializationSettings.txt'))
        for i in range (len(initSettingsFile)):
            words = initSettingsFile[i].split(" ")
            if words[0] == "PROCESS_P_DLT": systemManagement[3][0] = words[1];
            elif words[0] == "PROCESS_0_DLT": systemManagement[3][1] = words[1];
            elif words[0] == "PROCESS_1_DLT": systemManagement[3][2] = words[1];
            elif words[0] == "PROCESS_2_DLT": systemManagement[3][3] = words[1];
            elif words[0] == "PROCESS_3_DLT": systemManagement[3][4] = words[1];
            elif words[0] == "PROCESS_4_DLT": systemManagement[3][5] = words[1];
            elif words[0] == "PROCESS_5_DLT": systemManagement[3][6] = words[1];
            elif words[0] == "PROCESS_6_DLT": systemManagement[3][7] = words[1];
            elif words[0] == "PROCESS_P_TRNS": systemManagement[4][0] = words[1];
            elif words[0] == "PROCESS_0_TRNS": systemManagement[4][1] = words[1];
            elif words[0] == "PROCESS_1_TRNS": systemManagement[4][2] = words[1];
            elif words[0] == "PROCESS_2_TRNS": systemManagement[4][3] = words[1];
            elif words[0] == "PROCESS_3_TRNS": systemManagement[4][4] = words[1];
            elif words[0] == "PROCESS_4_TRNS": systemManagement[4][5] = words[1];
            elif words[0] == "PROCESS_5_TRNS": systemManagement[4][6] = words[1];
            elif words[0] == "PROCESS_6_TRNS": systemManagement[4][7] = words[1];
            else: addSystemMsg(time.time_ns() - systemManagement[0], "UNRECOGNIZABLE SETTING DETECTED: " + str(initSettingsFile[i]) + "AT LINE NUMBER " + str(i))
        addSystemMsg(time.time_ns() - systemManagement[0], "INITIALIZATION SETTINGS IMPORT COMPLETED!!")
    else: 
        addSystemMsg(time.time_ns() - systemManagement[0], "THERE EXISTS NO INITIALIZATION SETTINGS FILE, DEFAULT SETTINGS WILL BE USED - File Not Found: 'initializationSettings.txt'")
    
    processVariables = dict()
    
    processVariables["setting_RECORD_PROCESSTIMER"] = True
    processVariables["setting_RECORD_SYSTEMMESSAGES"] = True

    processVariables["timer_PRDSEND_SYSTIME"] = 0
    processVariables["timerInterval_PRDSEND_SYSTIME"] = 1

        #Program Record Files Creation
    f = open(os.path.join(path_MAIN, 'systemMessages.txt'), 'w'); f.close()
    addSystemMsg(time.time_ns() - systemManagement[0], "System Message Record File Created: 'systemMessages.txt'")
    f = open(os.path.join(path_MAIN, 'processesTimerRecord.txt'), 'w'); f.close()
    addSystemMsg(time.time_ns() - systemManagement[0], "Processes Timer Record File Created: 'processesTimerRecord.txt'")

        #Program Initialization Data Record
    addSystemMsg(time.time_ns() - systemManagement[0], "PROCESS_P DLT SET TO " + str(systemManagement[3][0]))
    addSystemMsg(time.time_ns() - systemManagement[0], "PROCESS_0 DLT SET TO " + str(systemManagement[3][1]))
    addSystemMsg(time.time_ns() - systemManagement[0], "PROCESS_1 DLT SET TO " + str(systemManagement[3][2]))
    addSystemMsg(time.time_ns() - systemManagement[0], "PROCESS_2 DLT SET TO " + str(systemManagement[3][3]))
    addSystemMsg(time.time_ns() - systemManagement[0], "PROCESS_3 DLT SET TO " + str(systemManagement[3][4]))
    addSystemMsg(time.time_ns() - systemManagement[0], "PROCESS_4 DLT SET TO " + str(systemManagement[3][5]))
    addSystemMsg(time.time_ns() - systemManagement[0], "PROCESS_5 DLT SET TO " + str(systemManagement[3][6]))
    addSystemMsg(time.time_ns() - systemManagement[0], "PROCESS_6 DLT SET TO " + str(systemManagement[3][7]))
    addSystemMsg(time.time_ns() - systemManagement[0], "PROCESS_P TRNS SET TO " + str(systemManagement[4][0]))
    addSystemMsg(time.time_ns() - systemManagement[0], "PROCESS_0 TRNS SET TO " + str(systemManagement[4][1]))
    addSystemMsg(time.time_ns() - systemManagement[0], "PROCESS_1 TRNS SET TO " + str(systemManagement[4][2]))
    addSystemMsg(time.time_ns() - systemManagement[0], "PROCESS_2 TRNS SET TO " + str(systemManagement[4][3]))
    addSystemMsg(time.time_ns() - systemManagement[0], "PROCESS_3 TRNS SET TO " + str(systemManagement[4][4]))
    addSystemMsg(time.time_ns() - systemManagement[0], "PROCESS_4 TRNS SET TO " + str(systemManagement[4][5]))
    addSystemMsg(time.time_ns() - systemManagement[0], "PROCESS_5 TRNS SET TO " + str(systemManagement[4][6]))
    addSystemMsg(time.time_ns() - systemManagement[0], "PROCESS_6 TRNS SET TO " + str(systemManagement[4][7]))

        #Process Initialization Data Pass
    IPCB[0].append(systemManagement[0]); IPCB[0].append(systemManagement[3][1]); IPCB[0].append(systemManagement[4][1]);
    IPCB[1].append(systemManagement[0]); IPCB[1].append(systemManagement[3][2]); IPCB[1].append(systemManagement[4][2]);
    IPCB[2].append(systemManagement[0]); IPCB[2].append(systemManagement[3][3]); IPCB[2].append(systemManagement[4][3]);
    IPCB[3].append(systemManagement[0]); IPCB[3].append(systemManagement[3][4]); IPCB[3].append(systemManagement[4][4]);
    IPCB[4].append(systemManagement[0]); IPCB[4].append(systemManagement[3][5]); IPCB[4].append(systemManagement[4][5]);
    IPCB[5].append(systemManagement[0]); IPCB[5].append(systemManagement[3][6]); IPCB[5].append(systemManagement[4][6]);
    IPCB[6].append(systemManagement[0]); IPCB[6].append(systemManagement[3][7]); IPCB[6].append(systemManagement[4][7]);

    #Processes Start
    for i in range (len(processes)):
        processes[i].start()

    #MAIN PROCESS CONTROL ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    mainP_processStatus = True; systemManagement[2][0] = True
    mainP_SDLT = systemManagement[3][0]; mainP_record_nSamples = systemManagement[4][0]
    mainP_processTimer = [time.perf_counter_ns(), 0, 0] #[0]: Last Loop Start Time, [1]: Current Loop Start Time, [2]: Processing Time
    mainP_timerRecord = [[],[]]; mainP_timerAvg = [0, 0];

    while (mainP_processStatus == True):
        if (time.perf_counter_ns() - mainP_processTimer[0]) >= (int(mainP_SDLT) * 1000000):
            #Loop END & Record ------------------------------------------------------------------------------------------------------------------------------------------------------------------------
            mainP_processTimer[1] = time.perf_counter_ns()
            #Loop Start -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
            while (len(mainP_timerRecord[0]) >= int(mainP_record_nSamples)): mainP_timerRecord[0].pop(1); mainP_timerRecord[1].pop(1)
            mainP_timerRecord[0].append(mainP_processTimer[1] - mainP_processTimer[0]); mainP_timerRecord[1].append(mainP_processTimer[2])
            mainP_timerAvg = [numpy.mean(mainP_timerRecord[0]), numpy.mean(mainP_timerRecord[1])];
            #print("PROCESS_P: Average Loop Time [{:.3f} us], Average Processing Time [{:.3f} us], Number of Samples [{:d}]".format(mainP_timerAvg[0] / 1000, mainP_timerAvg[1] / 1000, len(mainP_timerRecord[0])));
            mainP_processTimer[2] = time.perf_counter_ns()
            #PROCESS BEGIN ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
            if (process_P(IPCB[0], IPCB[1], IPCB[2], IPCB[3], IPCB[4], IPCB[5], IPCB[6], IPCB[7], IPCB[14], IPCB[21], IPCB[28], IPCB[35], IPCB[42], IPCB[49], processVariables) == False): #MAIN PROCES
                mainP_processStatus = False; systemManagement[2][0] = False; addSystemMsg(time.time_ns() - systemManagement[0], "MAIN PROCESS TERMINATED, PROGRAM TERMINATION SEQUENCE BEGIN")
                #PROGRAM TERMINATION SEQUENCE ---------------------------------------------------------------------------------------------------------------------------------------------------------
                







                    #Print and Record All the Remaining System Messages
                f = open(os.path.join(path_MAIN, 'systemMessages.txt'), 'a')
                for i in range (len(systemManagement[5])):
                    f.write(systemManagement[5][i] + "\n")
                    if (systemManagement[1] == True): print(systemManagement[5][i])
                f.close();
                #PROGRAM TERMINATION SEQUENCE END -----------------------------------------------------------------------------------------------------------------------------------------------------
            #PROCESS END ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
            systemManagement[6][0][0] = mainP_timerAvg[0]; systemManagement[6][0][1] = mainP_timerAvg[1]; systemManagement[6][0][2] = len(mainP_timerRecord[0])
            mainP_processTimer[2] = time.perf_counter_ns() - mainP_processTimer[2]; mainP_processTimer[0] = mainP_processTimer[1]
            delay = math.trunc((int(mainP_SDLT) - mainP_processTimer[2] / 1000000)) / 1000 
            if (delay > 0): time.sleep(delay);
    #MAIN PROCESS CONTROL END --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    #Wait For Processes Termination
    for i in range (len(processes)):
        processes[i].join()

# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------