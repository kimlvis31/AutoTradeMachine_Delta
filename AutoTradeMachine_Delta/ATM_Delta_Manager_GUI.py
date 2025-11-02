from pickle import NONE

import InterProcessesCommunicator
import GUIObjects_Alpha

import tkinter
import os
import time

from shapely.geometry import Point, Polygon

name_MANAGER = "GUI"

path_PROJECT = os.path.dirname(os.path.realpath(__file__))
path_MANAGER = os.path.join(path_PROJECT + r"\data\m_GUI")
path_IMAGES = os.path.join(path_MANAGER + r"\imgs")
path_CTGO = os.path.join(path_IMAGES + r"\CTGO")

#mouseStatusFlag: [0]: CursorMovedFlag, [1]: LeftButtonClickedFlag, [2]: RightButtonClickedFlag, [3]: WheelButtonClickedFlag, [4]: LeftButtonReleasedFlag, [5]: RightButtonReleasedFlag, [6]: WheelButtonReleasedFlag, [7]: WheelMovedUpFlag, [8]: WheelMovedDownFlag
mouseStatusFlag = 0b00000000000
#mouseStatus: [0]: MousePositionX, [1]: MousePositionY, [2]: LeftButtonStatus, [3]: WheelButtonStatus, [4]: RightButtonStatus
mouseStatus = [0, 0, "DEFAULT", "DEFAULT", "DEFAULT"]
MOUSE_CURSORMOVED     = 0b00000000001
MOUSE_LEFTCLICKED     = 0b00000000010
MOUSE_RIGHTCLICKED    = 0b00000000100
MOUSE_WHEELCLICKED    = 0b00000001000
MOUSE_LEFTRELEASED    = 0b00000010000
MOUSE_RIGHTRELEASED   = 0b00000100000
MOUSE_WHEELRELEASED   = 0b00001000000
MOUSE_WHEELMOVEDUP    = 0b00010000000
MOUSE_WHEELMOVEDDOWN  = 0b00100000000
MOUSE_WHEELMOVEDLEFT  = 0b01000000000
MOUSE_WHEELMOVEDRIGHT = 0b10000000000
MOUSE_XPOS = 0
MOUSE_YPOS = 1
MOUSE_LEFTBUTTON = 2
MOUSE_WHEELBUTTON = 3
MOUSE_RIGHTBUTTON = 4
#keyStat : [keyEventFlag(0), lastClickedKeyCode(1), lastClickedKey(2), shiftClicked(3)]
keyStat = [0, 0, '', 0]

#MAIN CLASS ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
class manager_GUI:
    def __init__(self, PST):
        #Inter-Processes Communicator Initialization
        self.IPC = InterProcessesCommunicator.IPCommunicator(PST, name_MANAGER, path_MANAGER, ["MAIN", "AUTOTRADER", "AUXILLARY", "BINANCEAPI", "DATAANALYSIS", "DATAMANAGEMENT", "GUI"])
        self.IPC.write_SystemMessage("Initializing GRAPHICAL USER INTERFACE Manager...")
        self.IPC.write_SystemMessage("  Inter-Processes Communicator Initialized!")
        
        #IPC Files Creation
        f = open(os.path.join(path_MANAGER, 'IPCLog_GUI.txt'), 'w'); f.close()
        self.IPC.write_SystemMessage("  Inter-Processes Communication Log File Created!: 'IPCLog_GUI.txt'")
        f = open(os.path.join(path_MANAGER, 'IPCRuntime_GUI.txt'), 'w'); f.close()
        self.IPC.write_SystemMessage("  Inter-Processes Communication Run Time Data File Created!: 'IPCRuntime_GUI.txt'")

        #Tkinter Initialization
        self.window = tkinter.Tk()
        self.canvas = tkinter.Canvas(self.window, width = 2560, height = 1440, bg = "gray10", bd = 0, highlightthickness = 0)
        self.text = tkinter.Text(self.window)
        self.window.title("ATM_DELTA") #Window Title
        self.window.geometry("2560x1440") #Window size setting, 2560x1440
        self.window.resizable(False,False) #Disable window resizing
        self.window.attributes("-fullscreen", True) #Set the window to start as fullscreen mode
        self.window.bind("<F11>", lambda event: self.window.attributes("-fullscreen", not self.window.attributes("-fullscreen"))) #Enables F11 Key to go to and escape from fullScreen]
        
        #Manager Canvas and Window Control
        self.canvasLabels_manager = []; self.devMode = False
        self.frameLimiterTimer = time.perf_counter_ns()
        self.definedFPS = 100

        #Input Devices Key Binding
        bindKeys(self.window); self.IPC.write_SystemMessage("  Key Binding Complete!")

        #GUI Control Variables Initialization
        self.currentPage = ""
        self.lastSelectedGUIO = -1
        self.lastSelectedHitBoxList = []
        self.searchGUIO = True
        self.GUIOs = dict()

        #Reading CTGO File
        self.IPC.write_SystemMessage("  Reading CTGO File")
        CTGOFileData = []
        with open(os.path.join(path_CTGO + r"\CTGO_A.bin"), 'r') as file:
            lines = file.readlines()
            for line in lines:
                if not(line == "\n"): CTGOFileData.append(line.strip())
            file.close()
        CTGOFileData = textInConfinementToArray(CTGOFileData, "<", ">")
        self.IPC.write_SystemMessage("  CTGO File Read Complete!")

        #GUIOList Files Read and GUIOs Initialization
        filesList = [f for f in os.listdir(path_MANAGER) if os.path.isfile(os.path.join(path_MANAGER, f))]
        GUIOObjectFiles = []
        for file in filesList:
            if file.split("_")[0] == "GUIOList" and file.split(".")[1] == "bin": GUIOObjectFiles.append(file); self.IPC.write_SystemMessage("  GUIO File Found: '{:s}'".format(file))

        if (len(GUIOObjectFiles) == 0): self.IPC.write_SystemMessage("  Cannot Find Any Graphical User Inferface Object File, No GUI Object Initialized")
        else:
            for file in GUIOObjectFiles:
                self.IPC.write_SystemMessage("  Reading GUIO File Contents: {:s}".format(file))
                GUIOListLines = []
                with open(os.path.join(path_MANAGER, file), 'r') as GUIOFile:
                    lines = GUIOFile.readlines()
                    for line in lines:
                        if not(line == "\n") and not(line.lstrip()[0] == "#"): GUIOListLines.append(line.strip())
                    GUIOFile.close()
                
                GUIOFileData = textInConfinementToArray(GUIOListLines, "<", ">")
                if (GUIOFileData == NONE): self.IPC.write_SystemMessage("  No Content Found: {:s}".format(file))
                else:
                    pageLoadCommands = []; GUIObjects = []
                    for contentIndex in range (len(GUIOFileData)):
                        if (len(GUIOFileData) == 0): self.IPC.write_SystemMessage("  Content Number {:d} Is Empty: {:s}".format(contentIndex, file))
                        else:
                            if (GUIOFileData[contentIndex][0] == "PAGELOADCOMMANDS"): pageLoadCommands = GUIOFileData[contentIndex][1:]
                            elif (GUIOFileData[contentIndex][0] == "BUTTON_TYPE_A"): GUIObjects.append(GUIObjects_Alpha.button_typeA(GUIOFileData[contentIndex][1:], CTGOFileData)); self.IPC.write_SystemMessage("    Object Content {:d} Initializated: 'BUTTON_TYPE_A'".format(contentIndex))
                            elif (GUIOFileData[contentIndex][0] == "SWITCH_TYPE_A"): GUIObjects.append(GUIObjects_Alpha.switch_typeA(GUIOFileData[contentIndex][1:], CTGOFileData)); self.IPC.write_SystemMessage("    Object Content {:d} Initializated: 'SWITCH_TYPE_A'".format(contentIndex))
                            elif (GUIOFileData[contentIndex][0] == "SLIDER_TYPE_A"): GUIObjects.append(GUIObjects_Alpha.slider_typeA(GUIOFileData[contentIndex][1:], CTGOFileData)); self.IPC.write_SystemMessage("    Object Content {:d} Initializated: 'SLIDER_TYPE_A'".format(contentIndex))
                            elif (GUIOFileData[contentIndex][0] == "TEXTINPUTBOX_TYPE_A"): GUIObjects.append(GUIObjects_Alpha.textInputBox_typeA(GUIOFileData[contentIndex][1:], CTGOFileData)); self.IPC.write_SystemMessage("    Object Content {:d} Initializated: 'TEXTINPUTBOX_TYPE_A'".format(contentIndex))
                            elif (GUIOFileData[contentIndex][0] == "TEXTBOX_TYPE_A"): GUIObjects.append(GUIObjects_Alpha.textBox_typeA(GUIOFileData[contentIndex][1:], CTGOFileData)); self.IPC.write_SystemMessage("    Object Content {:d} Initializated: 'TEXTBOX_TYPE_A'".format(contentIndex))
                            elif (GUIOFileData[contentIndex][0] == "LISTBOX_TYPE_A"): GUIObjects.append(GUIObjects_Alpha.listBox_typeA(GUIOFileData[contentIndex][1:], CTGOFileData)); self.IPC.write_SystemMessage("    Object Content {:d} Initializated: 'LISTBOX_TYPE_A'".format(contentIndex))
                            elif (GUIOFileData[contentIndex][0] == "PASSIVEGRAPHICS_TYPE_A"): GUIObjects.append(GUIObjects_Alpha.passiveGraphics_typeA(GUIOFileData[contentIndex][1:], CTGOFileData)); self.IPC.write_SystemMessage("    Object Content {:d} Initializated: 'PASSIVEGRAPHICS_TYPE_A'".format(contentIndex))
                            elif (GUIOFileData[contentIndex][0] == "BINARYINDICATOR_TYPE_A"): GUIObjects.append(GUIObjects_Alpha.binaryIndicator_typeA(GUIOFileData[contentIndex][1:], CTGOFileData)); self.IPC.write_SystemMessage("    Object Content {:d} Initializated: 'BINARYINDICATOR_TYPE_A'".format(contentIndex))
                            else: self.IPC.write_SystemMessage("    Object Content {:d} Initialization Failed: Content Unacceptable - Content Type Unrecognizable".format(i))
                    self.GUIOs[file[9:-4]] = [pageLoadCommands, GUIObjects]
                    self.IPC.write_SystemMessage("  GUIO File Read Complete!: {:s}".format(file))
        
        #Object Graphical Intrusion Analysis
        for page in self.GUIOs:
            for i in range (len(self.GUIOs[page][1])):
                for k in range (len(self.GUIOs[page][1])):
                    coordsI = [(self.GUIOs[page][1][i].data["COORD_X"], self.GUIOs[page][1][i].data["COORD_Y"]),
                               (self.GUIOs[page][1][i].data["COORD_X"] + self.GUIOs[page][1][i].data["WIDTH"], self.GUIOs[page][1][i].data["COORD_Y"]),
                               (self.GUIOs[page][1][i].data["COORD_X"] + self.GUIOs[page][1][i].data["WIDTH"], self.GUIOs[page][1][i].data["COORD_Y"] + self.GUIOs[page][1][i].data["HEIGHT"]),
                               (self.GUIOs[page][1][i].data["COORD_X"], self.GUIOs[page][1][i].data["COORD_Y"] + self.GUIOs[page][1][i].data["HEIGHT"])]
                    coordsK = [(self.GUIOs[page][1][k].data["COORD_X"], self.GUIOs[page][1][k].data["COORD_Y"]),
                               (self.GUIOs[page][1][k].data["COORD_X"] + self.GUIOs[page][1][k].data["WIDTH"], self.GUIOs[page][1][k].data["COORD_Y"]),
                               (self.GUIOs[page][1][k].data["COORD_X"] + self.GUIOs[page][1][k].data["WIDTH"], self.GUIOs[page][1][k].data["COORD_Y"] + self.GUIOs[page][1][k].data["HEIGHT"]),
                               (self.GUIOs[page][1][k].data["COORD_X"], self.GUIOs[page][1][k].data["COORD_Y"] + self.GUIOs[page][1][k].data["HEIGHT"])]
                    if (i != k) and (self.GUIOs[page][1][i].data["LAYER"] < self.GUIOs[page][1][k].data["LAYER"]) and (isPolygonInPolygon(coordsI, coordsK)): self.GUIOs[page][1][i].gIntrusions.append(k);
                    
        loadPage(self, "DASHBOARD")
        setDevMode(self, False)
        self.IPC.write_SystemMessage("GRAPHICAL USER INTERFACE Manager Initialization Complete!")

    def process(self, IPCB_T0, IPCB_T1, IPCB_T2, IPCB_T3, IPCB_T4, IPCB_T5, IPCB_T6, IPCB_F0, IPCB_F1, IPCB_F2, IPCB_F3, IPCB_F4, IPCB_F5, IPCB_F6):
        global mouseStatusFlag;
        results = []
        
        #GUIO Object Control
        if (mouseStatusFlag != 0):
            if (mouseStatusFlag & MOUSE_CURSORMOVED): #MOUSE MOVED
                results += selectPriorityGUIO(self)
                results.append([self.GUIOs[self.currentPage][1][self.lastSelectedGUIO], self.GUIOs[self.currentPage][1][self.lastSelectedGUIO].processData(userInput = ("M:MOVED", self.lastSelectedHitBoxList, (mouseStatus[MOUSE_XPOS], mouseStatus[MOUSE_YPOS])))])
            if (self.lastSelectedGUIO != -1):
                if (mouseStatusFlag & MOUSE_LEFTCLICKED):     results.append([self.GUIOs[self.currentPage][1][self.lastSelectedGUIO], self.GUIOs[self.currentPage][1][self.lastSelectedGUIO].processData(userInput = ("M:CLICKED_L",   self.lastSelectedHitBoxList, (mouseStatus[MOUSE_XPOS], mouseStatus[MOUSE_YPOS])))])
                if (mouseStatusFlag & MOUSE_RIGHTCLICKED):    results.append([self.GUIOs[self.currentPage][1][self.lastSelectedGUIO], self.GUIOs[self.currentPage][1][self.lastSelectedGUIO].processData(userInput = ("M:CLICKED_R",   self.lastSelectedHitBoxList, (mouseStatus[MOUSE_XPOS], mouseStatus[MOUSE_YPOS])))])
                if (mouseStatusFlag & MOUSE_WHEELCLICKED):    results.append([self.GUIOs[self.currentPage][1][self.lastSelectedGUIO], self.GUIOs[self.currentPage][1][self.lastSelectedGUIO].processData(userInput = ("M:CLICKED_W",   self.lastSelectedHitBoxList, (mouseStatus[MOUSE_XPOS], mouseStatus[MOUSE_YPOS])))])
                if (mouseStatusFlag & MOUSE_LEFTRELEASED):    results.append([self.GUIOs[self.currentPage][1][self.lastSelectedGUIO], self.GUIOs[self.currentPage][1][self.lastSelectedGUIO].processData(userInput = ("M:RELEASED_L",  self.lastSelectedHitBoxList, (mouseStatus[MOUSE_XPOS], mouseStatus[MOUSE_YPOS])))])
                if (mouseStatusFlag & MOUSE_RIGHTRELEASED):   results.append([self.GUIOs[self.currentPage][1][self.lastSelectedGUIO], self.GUIOs[self.currentPage][1][self.lastSelectedGUIO].processData(userInput = ("M:RELEASED_R",  self.lastSelectedHitBoxList, (mouseStatus[MOUSE_XPOS], mouseStatus[MOUSE_YPOS])))])
                if (mouseStatusFlag & MOUSE_WHEELRELEASED):   results.append([self.GUIOs[self.currentPage][1][self.lastSelectedGUIO], self.GUIOs[self.currentPage][1][self.lastSelectedGUIO].processData(userInput = ("M:RELEASED_W",  self.lastSelectedHitBoxList, (mouseStatus[MOUSE_XPOS], mouseStatus[MOUSE_YPOS])))])
                if (mouseStatusFlag & MOUSE_WHEELMOVEDUP):    results.append([self.GUIOs[self.currentPage][1][self.lastSelectedGUIO], self.GUIOs[self.currentPage][1][self.lastSelectedGUIO].processData(userInput = ("M:WHEEL_UP",    self.lastSelectedHitBoxList, (mouseStatus[MOUSE_XPOS], mouseStatus[MOUSE_YPOS])))])
                if (mouseStatusFlag & MOUSE_WHEELMOVEDDOWN):  results.append([self.GUIOs[self.currentPage][1][self.lastSelectedGUIO], self.GUIOs[self.currentPage][1][self.lastSelectedGUIO].processData(userInput = ("M:WHEEL_DOWN",  self.lastSelectedHitBoxList, (mouseStatus[MOUSE_XPOS], mouseStatus[MOUSE_YPOS])))])
                if (mouseStatusFlag & MOUSE_WHEELMOVEDLEFT):  results.append([self.GUIOs[self.currentPage][1][self.lastSelectedGUIO], self.GUIOs[self.currentPage][1][self.lastSelectedGUIO].processData(userInput = ("M:WHEEL_LEFT",  self.lastSelectedHitBoxList, (mouseStatus[MOUSE_XPOS], mouseStatus[MOUSE_YPOS])))])
                if (mouseStatusFlag & MOUSE_WHEELMOVEDRIGHT): results.append([self.GUIOs[self.currentPage][1][self.lastSelectedGUIO], self.GUIOs[self.currentPage][1][self.lastSelectedGUIO].processData(userInput = ("M:WHEEL_RIGHT", self.lastSelectedHitBoxList, (mouseStatus[MOUSE_XPOS], mouseStatus[MOUSE_YPOS])))])

        #GUIO Processing and Result Handling
        for i in range (len(self.GUIOs[self.currentPage][1])): 
            results.append([self.GUIOs[self.currentPage][1][i], self.GUIOs[self.currentPage][1][i].processData(data = dataSearch(self, self.GUIOs[self.currentPage][1][i].requestData()))]) #Processing and Result Handling
            if (self.GUIOs[self.currentPage][1][i].data["FAR"] != NONE): #Function Activation Result Receival
                FAresult = self.IPC.read_FAResult(self.GUIOs[self.currentPage][1][i].data["FAR"][0], self.GUIOs[self.currentPage][1][i].data["FAR"][1]) #Search for the result from the IPC Module
                if (FAresult != "DNR"):
                    if (FAresult != "DNF"): self.GUIOs[self.currentPage][1][i].data["FARESULT"] = FAresult
                    self.GUIOs[self.currentPage][1][i].data["FAR"] = NONE #Reset the object's FAR Data

        #Interpret Results
        resultsInterpreter(self, results)

        #Draw GUI Objects
        if ((time.perf_counter_ns() - self.frameLimiterTimer) > (1 / self.definedFPS * 1e9)):
            drawGUIObjects(self)
            self.frameLimiterTimer = time.perf_counter_ns()


        #Mouse and Keyboard Status Flag Initialization
        keyStat[0] = 0  #Reset - Keyboard Event Flag
        mouseStatusFlag = 0b000000000

        self.IPC.processMessages(IPCB_T0, IPCB_T1, IPCB_T2, IPCB_T3, IPCB_T4, IPCB_T5, IPCB_T6, IPCB_F0, IPCB_F1, IPCB_F2, IPCB_F3, IPCB_F4, IPCB_F5, IPCB_F6) #Must be placed at the end of the function for appropriate process recording
        return True
#MAIN CLASS END -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#AUXIALLRY FUNCTIONS ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def dataSearch(self, dataNames):
    def search(dataName):
        words = dataName.split(":")
        if (words[0] == "MANAGER"): #"MANAGER":MANAGERDATANAME
            if (words[1] == "DEVMODE"): return self.devMode;
            elif (words[1] == "MOUSESTATUS"): return mouseStatus;
            elif (words[1] == "MOUSESTATUSFLAG"): return mouseStatusFlag
            elif (words[1] == "KEYBOARDSTATUS"): return keyStat;
        elif (words[0] == "GUIO"): #"GUIO":OBJECTPAGENAME:OBJECTNAME:DATANAME
            try: return getObject(self, words[1], words[2]).data[words[3]]
            except: self.IPC.write_SystemMessage("  Data Search Failed, Data Point Unreachable: <{:s}>".format(str(dataName)))
        elif (words[0] == "PRD_IN"): #"PRD_IN":TARGETMANAGER:DATANAME
            try: return self.IPC.get_PRD_IN(words[1], words[2])
            except: self.IPC.write_SystemMessage("  Data Search Failed, Data Point Unreachable: <{:s}>".format(str(dataName)))
        else: self.IPC.write_SystemMessage("  Data Search Failed, Data Does Not Exist: <{:s}>".format(str(dataName)))
        return NONE

    if (dataNames is not NONE):
        results = dict()
        if type(dataNames) is list:
            for dataName in dataNames: results[dataName] = search(dataName)
        elif type(dataNames) is str:
            results[dataNames] = search(dataNames)
        elif type(dataNames) is not NoneType: self.IPC.write_SystemMessage("  Data Search Failed, Unacceptable dataNames Type: <{:s}>".format(str(dataNames))); return NONE
        if (len(results) > 0): return results
        else: return NONE
    else: return NONE

def resultsInterpreter(self, results):
    if (len(results) > 0):
        for result in results:
            resultGenerator = result[0]
            resultsGenerated = result[1]
            for resultLine in resultsGenerated:
                if type(resultLine) is list: #List Type Result Analysis
                    if resultLine[0] == "FUNCTION_MANAGER": #Activate Manager Function
                        if   resultLine[1] == "DEVMODE_ON": setDevMode(self, True)
                        elif resultLine[1] == "DEVMODE_OFF": setDevMode(self, False)
                        elif resultLine[1] == "GUIOSEARCH_ON": self.searchGUIO = True
                        elif resultLine[1] == "GUIOSEARCH_OFF": self.searchGUIO = False
                        elif resultLine[1] == "SELECTPRIORITYGUIO": selectPriorityGUIO(self);
                        elif resultLine[1] == "LOADPAGE": loadPage(self, resultLine[2])
                    elif resultLine[0] == "SET_DATA_GUIO": #Set GUIO Data
                        try: getObject(self, resultLine[1].split(":")[0], resultLine[1].split(":")[1]).data[result[1].split(":")[2]] = resultLine[2]
                        except: self.IPC.write_SystemMessage("  Result Handling Failed: <{:s}>".format(str(resultLine)))
                    elif resultLine[0] == "SYNC_DATA_GUIO_GUIO": #Sync GUIO Data with another GUIO Data
                        try: 
                            getObject(self, resultLine[1].split(":")[0], resultLine[1].split(":")[1]).data[resultLine[1].split(":")[2]] = getObject(self, resultLine[2].split(":")[0], resultLine[2].split(":")[1]).data[resultLine[2].split(":")[2]]; 
                            getObject(self, resultLine[1].split(":")[0], resultLine[1].split(":")[1]).data["GUF"] = True
                        except: self.IPC.write_SystemMessage("  Result Handling Failed, Data Point Unreachable: <{:s}>".format(str(resultLine)))
                    elif resultLine[0] == "SYNC_DATA_GUIO_MANAGER": #Sync GUIO Data with Manager Data
                        try: getObject(self, resultLine[1].split(":")[0], resultLine[1].split(":")[1]).data[resultLine[1].split(":")[2]] = dataSearch(self, resultLine[3])
                        except: self.IPC.write_SystemMessage("  Result Handling Failed, Data Point Unreachable: <{:s}>".format(str(resultLine)))
                    elif resultLine[0] == "SEND_SYS_MSG": self.IPC.write_SystemMessage("  SYSTEM MESSAGE FROM GUIO: {:s}".format(str(resultLine[1:])));
                    elif resultLine[0] == "SEND_FAR": 
                        requestResult = self.IPC.send_FARequest(resultLine[1], resultLine[2], dataSearch(self, resultLine[3:])) #Attempt to Register FAR
                        if (requestResult != "MNF" and requestResult != "BLR"): 
                            resultGenerator.data["FAR"] = [resultLine[1], requestResult] #Register RequestID to the Requester Object
                            resultGenerator.data["FARESULT"] = NONE

                    else: self.IPC.write_SystemMessage("  Result Handling Failed, Unrecognizable Result: {:s}".format(str(resultLine))) #Unknown Result Handling

                elif type(resultLine) is str: #String Type Result Analysis
                    if resultLine == "COMMAND1": print("STRING DETECTED")
                    else: print("STRING DETECTED1")

def loadPage(self, pageName):
    #Page Existence Check
    if pageName in self.GUIOs: self.IPC.write_SystemMessage("  Loading Page '{:s}'".format(pageName))
    else: self.IPC.write_SystemMessage("  Page Load Failed: Page '{:s}' Not Found".format(pageName)); return 0
    #Reset Canvas
    self.canvas.delete("all")
    #Release the GUIO of the previous page
    if (self.currentPage != ""): self.GUIOs[self.currentPage][1][self.lastSelectedGUIO].processData(userInput = ("M:RELEASED", self.lastSelectedHitBoxList))
    #Call Page Load Commands
    resultsInterpreter(self, self.GUIOs[pageName][0])
    #Process GUIOs in LOAD mode
    for GUIObject in self.GUIOs[pageName][1]:
        GUIObject.processData(data = dataSearch(self, GUIObject.requestData(load = True)))
        GUIObject.data["GUF"] = True
    #CurrentPage Edit
    self.currentPage = pageName
    self.lastSelectedGUIO = -1
    selectPriorityGUIO(self)
    self.IPC.write_SystemMessage("  Page {:s} Loaded! <{:d} GUI Objects Present>".format(pageName, len(self.GUIOs[self.currentPage][1])))

def setDevMode(self, switch = True):
    self.devMode = switch; self.canvas.delete(self.canvasLabels_manager); self.canvasLabels_manager.clear()
    for pageName in self.GUIOs:
        for GUIObject in self.GUIOs[pageName][1]: 
            GUIObject.data["DM"] = switch; GUIObject.data["GUF"] = True

def drawGUIObjects(self):
    #GUIObjects Drawing
    for GUIObject in self.GUIOs[self.currentPage][1]:
        if (GUIObject.draw(self.canvas)):
            for intrusionIndex in GUIObject.gIntrusions:
                self.GUIOs[self.currentPage][1][intrusionIndex].draw(self.canvas, bypassGUF = True);
                
    #Development Mode Objects Drawing
    if self.devMode == True:
        self.canvas.delete(self.canvasLabels_manager); self.canvasLabels_manager.clear()
        self.canvasLabels_manager.append(self.canvas.create_text(1280, 12, text = "[MS]: {:s}     [KS]: {:s}".format(str(mouseStatus), str(keyStat)), fill = "white", font = ("Times New Roman", 10, "bold")))
    self.canvas.pack()

def getObject(self, pageName, objectName = ""):
    if pageName in self.GUIOs: #Page Found
        if (objectName != ""):
            for GUIObject in self.GUIOs[pageName][1]:
                if (GUIObject.data["NAME"] == objectName): return GUIObject #Object Found
            self.IPC.write_SystemMessage("  Object '{:s}' Not Found In '{:s}'".format(objectName, pageName)); return NONE
        else: return self.GUIOs[pageName];
    self.IPC.write_SystemMessage("  Page Not Found '{:s}'".format(pageName)); return NONE

def selectPriorityGUIO(self):
    if (self.searchGUIO == True):
        results = []; currentObjectIndex = -1; selectedObjectHitList = []
        for i in range (len(self.GUIOs[self.currentPage][1])):
            hitBoxList = self.GUIOs[self.currentPage][1][i].data["HB"]; hitList = []
            for k in range (len(hitBoxList)):
                if isPointInPolygon((mouseStatus[MOUSE_XPOS], mouseStatus[MOUSE_YPOS]), hitBoxList[k][:-1]): hitList.append(k);
            if ((len(hitList) > 0) and (self.GUIOs[self.currentPage][1][i].data["LAYER"] >= currentObjectIndex)): currentObjectIndex = i; selectedObjectHitList = hitList;  (mouseStatus[MOUSE_XPOS], mouseStatus[MOUSE_YPOS])

        if (self.lastSelectedGUIO == -1): #Approaching From Outside
            if (currentObjectIndex != -1): results.append([self.GUIOs[self.currentPage][1][currentObjectIndex], self.GUIOs[self.currentPage][1][currentObjectIndex].processData(userInput = ("M:HOVERED", selectedObjectHitList, (mouseStatus[MOUSE_XPOS], mouseStatus[MOUSE_YPOS])))])
        else: #Approaching From an Object
            if (currentObjectIndex == -1): results.append([self.GUIOs[self.currentPage][1][self.lastSelectedGUIO], self.GUIOs[self.currentPage][1][self.lastSelectedGUIO].processData(userInput = ("M:RELEASED", selectedObjectHitList, (mouseStatus[MOUSE_XPOS], mouseStatus[MOUSE_YPOS])))])
            else:
                if ((self.lastSelectedGUIO != currentObjectIndex) or (len(self.lastSelectedHitBoxList) != len(selectedObjectHitList))): 
                    results.append([self.GUIOs[self.currentPage][1][self.lastSelectedGUIO], self.GUIOs[self.currentPage][1][self.lastSelectedGUIO].processData(userInput = ("M:RELEASED", selectedObjectHitList, (mouseStatus[MOUSE_XPOS], mouseStatus[MOUSE_YPOS])))])
                    results.append([self.GUIOs[self.currentPage][1][self.lastSelectedGUIO], self.GUIOs[self.currentPage][1][currentObjectIndex].processData(userInput = ("M:HOVERED", selectedObjectHitList, (mouseStatus[MOUSE_XPOS], mouseStatus[MOUSE_YPOS])))])
        self.lastSelectedGUIO = currentObjectIndex
        self.lastSelectedHitBoxList = selectedObjectHitList
        return results
    else: return [[NONE, NONE]]

def isPointInPolygon(point, polygon):
    return Point(point).within(Polygon(polygon))

def isPolygonInPolygon(polygon1, polygon2):
    return Polygon(polygon1).intersects(Polygon(polygon2))

def textInConfinementToArray(texts, confinementBeginner = "<", confinementEnder = ">"):
    if (len(texts) > 0):
        if type(texts) is list:
            string = texts[0]; 
            for i in range (len(texts) - 1): string += texts[i + 1]
        elif type(texts) is str:
            string = texts
    else: return NONE
    elements = []; counter = 0; counter2 = 0; singular = True
    while counter < (len(string)):
        if string[counter] == confinementBeginner:
            counter += 1; counter2 = 1; dataStartIndex = counter;
            while (1):
                if string[counter] == confinementBeginner: counter2 += 1; singular = False
                elif string[counter] == confinementEnder: counter2 -= 1;
                if (counter2 == 0): break;
                else: counter += 1
            if (singular): elements.append(string[dataStartIndex:counter])
            else: elements.append(textInConfinementToArray(string[dataStartIndex:counter], confinementBeginner, confinementEnder))
            singular = True
        counter += 1;
    return elements



#AUXIALLRY FUNCTIONS END --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#INPUT EVENT FUNCTIONS ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def bindKeys(tkinter):
    tkinter.bind("<Key>", keyEvent)
    tkinter.bind("<KeyRelease>", keyReleaseEvent)
    tkinter.bind("<Button>", clickMouse)
    tkinter.bind("<ButtonRelease>", releaseMouse)
    tkinter.bind("<Motion>", mouseMoved)
    tkinter.bind("<MouseWheel>", mouseWheelMoved)
    mouseStatusFlag = 0b000000000

def keyEvent(event):
    keyEventFlagIndex = 0; lastClickedKeyCodeIndex = 1; lastClickedKeyIndex = 2; shiftCheckIndex = 3

    keyStat[lastClickedKeyCodeIndex] = event.keycode

    if keyStat[lastClickedKeyCodeIndex] == 8: #BACKSAPCE
        keyStat[lastClickedKeyIndex] = "BACKSPACE"
    elif keyStat[lastClickedKeyCodeIndex] == 16: #SHIFT
        keyStat[shiftCheckIndex] = 1; return 0
    elif keyStat[lastClickedKeyCodeIndex] == 37: #ARROW LEFT
        if keyStat[shiftCheckIndex] == 1: keyStat[lastClickedKeyIndex] = "SHIFTLEFT"
        else: keyStat[lastClickedKeyIndex] = "LEFT"
    elif keyStat[lastClickedKeyCodeIndex] == 38: #ARROW UP
        if keyStat[shiftCheckIndex] == 1: keyStat[lastClickedKeyIndex] = "SHIFTUP"
        else: keyStat[lastClickedKeyIndex] = "UP"
    elif keyStat[lastClickedKeyCodeIndex] == 39: #ARROW RIGHT
        if keyStat[shiftCheckIndex] == 1: keyStat[lastClickedKeyIndex] = "SHIFTRIGHT"
        else: keyStat[lastClickedKeyIndex] = "RIGHT"
    elif keyStat[lastClickedKeyCodeIndex] == 40: #ARROW DOWN
        if keyStat[shiftCheckIndex] == 1: keyStat[lastClickedKeyIndex] = "SHIFTDOWN"
        else: keyStat[lastClickedKeyIndex] = "DOWN"
    elif keyStat[lastClickedKeyCodeIndex] == 45: #INSERT
        keyStat[lastClickedKeyIndex] = "INSERT"
    elif keyStat[lastClickedKeyCodeIndex] >= 65 and keyStat[lastClickedKeyCodeIndex] <= 90:
        if keyStat[shiftCheckIndex] == 0: keyStat[lastClickedKeyIndex] = chr(keyStat[lastClickedKeyCodeIndex] + 32)
        else: keyStat[lastClickedKeyIndex] = chr(keyStat[lastClickedKeyCodeIndex])
    elif keyStat[lastClickedKeyCodeIndex] >= 48 and keyStat[lastClickedKeyCodeIndex] <= 57:
        if keyStat[shiftCheckIndex] == 0: keyStat[lastClickedKeyIndex] = chr(keyStat[lastClickedKeyCodeIndex])
        else:
            if keyStat[lastClickedKeyCodeIndex] == 48: keyStat[lastClickedKeyIndex] = chr(41)
            elif keyStat[lastClickedKeyCodeIndex] == 49: keyStat[lastClickedKeyIndex] = chr(33)
            elif keyStat[lastClickedKeyCodeIndex] == 50: keyStat[lastClickedKeyIndex] = chr(64)
            elif keyStat[lastClickedKeyCodeIndex] == 51: keyStat[lastClickedKeyIndex] = chr(35)
            elif keyStat[lastClickedKeyCodeIndex] == 52: keyStat[lastClickedKeyIndex] = chr(36)
            elif keyStat[lastClickedKeyCodeIndex] == 53: keyStat[lastClickedKeyIndex] = chr(37)
            elif keyStat[lastClickedKeyCodeIndex] == 54: keyStat[lastClickedKeyIndex] = chr(94)
            elif keyStat[lastClickedKeyCodeIndex] == 55: keyStat[lastClickedKeyIndex] = chr(38)
            elif keyStat[lastClickedKeyCodeIndex] == 56: keyStat[lastClickedKeyIndex] = chr(42)
            elif keyStat[lastClickedKeyCodeIndex] == 57: keyStat[lastClickedKeyIndex] = chr(40)
    elif keyStat[lastClickedKeyCodeIndex] == 186:
        if keyStat[shiftCheckIndex] == 0: keyStat[lastClickedKeyIndex] = chr(59)
        else: keyStat[lastClickedKeyIndex] = chr(58)
    elif keyStat[lastClickedKeyCodeIndex] == 187:
        if keyStat[shiftCheckIndex] == 0: keyStat[lastClickedKeyIndex] = chr(61)
        else: keyStat[lastClickedKeyIndex] = chr(43)
    elif keyStat[lastClickedKeyCodeIndex] == 188:
        if keyStat[shiftCheckIndex] == 0: keyStat[lastClickedKeyIndex] = chr(44)
        else: keyStat[lastClickedKeyIndex] = chr(60)
    elif keyStat[lastClickedKeyCodeIndex] == 189:
        if keyStat[shiftCheckIndex] == 0: keyStat[lastClickedKeyIndex] = chr(45)
        else: keyStat[lastClickedKeyIndex] = chr(95)
    elif keyStat[lastClickedKeyCodeIndex] == 190:
        if keyStat[shiftCheckIndex] == 0: keyStat[lastClickedKeyIndex] = chr(46)
        else: keyStat[lastClickedKeyIndex] = chr(62)
    elif keyStat[lastClickedKeyCodeIndex] == 191:
        if keyStat[shiftCheckIndex] == 0: keyStat[lastClickedKeyIndex] = chr(47)
        else: keyStat[lastClickedKeyIndex] = chr(63)
    elif keyStat[lastClickedKeyCodeIndex] == 192:
        if keyStat[shiftCheckIndex] == 0: keyStat[lastClickedKeyIndex] = chr(96)
        else: keyStat[lastClickedKeyIndex] = chr(126)
    elif keyStat[lastClickedKeyCodeIndex] == 219:
        if keyStat[shiftCheckIndex] == 0: keyStat[lastClickedKeyIndex] = chr(91)
        else: keyStat[lastClickedKeyIndex] = chr(123)
    elif keyStat[lastClickedKeyCodeIndex] == 220:
        if keyStat[shiftCheckIndex] == 0: keyStat[lastClickedKeyIndex] = chr(92)
        else: keyStat[lastClickedKeyIndex] = chr(124)
    elif keyStat[lastClickedKeyCodeIndex] == 221:
        if keyStat[shiftCheckIndex] == 0: keyStat[lastClickedKeyIndex] = chr(93)
        else: keyStat[lastClickedKeyIndex] = chr(125)
    elif keyStat[lastClickedKeyCodeIndex] == 222:
        if keyStat[shiftCheckIndex] == 0: keyStat[lastClickedKeyIndex] = chr(39)
        else: keyStat[lastClickedKeyIndex] = chr(34)
    else: return 0
    keyStat[keyEventFlagIndex] = 1

def keyReleaseEvent(event):
    keyStat[1] = event.keycode
    if keyStat[1] == 16: keyStat[3] = 0
def clickMouse(event):
    global mouseStatusFlag
    if (event.num == 1): mouseStatusFlag |= MOUSE_LEFTCLICKED;
    elif (event.num == 2): mouseStatusFlag |= MOUSE_WHEELCLICKED
    elif (event.num == 3): mouseStatusFlag |= MOUSE_RIGHTCLICKED
def releaseMouse(event):
    global mouseStatusFlag
    if (event.num == 1): mouseStatusFlag |= MOUSE_LEFTRELEASED
    elif (event.num == 2): mouseStatusFlag |= MOUSE_WHEELRELEASED
    elif (event.num == 3): mouseStatusFlag |= MOUSE_RIGHTRELEASED
def mouseMoved(event):
    global mouseStatusFlag; mouseStatusFlag |= MOUSE_CURSORMOVED
    global mouseStatus; mouseStatus[MOUSE_XPOS] = event.x; mouseStatus[MOUSE_YPOS] = event.y
def mouseWheelMoved(event):


    global mouseStatusFlag
    if int(event.delta / 120) == 1:
        if (int(event.state) == 8): mouseStatusFlag |= MOUSE_WHEELMOVEDUP;
        elif (int(event.state) == 9): mouseStatusFlag |= MOUSE_WHEELMOVEDRIGHT;
    elif int(event.delta / 120) == -1:
        if (int(event.state) == 8): mouseStatusFlag |= MOUSE_WHEELMOVEDDOWN;
        elif (int(event.state) == 9): mouseStatusFlag |= MOUSE_WHEELMOVEDLEFT;

#INPUT EVENT FUNCTIONS END ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------