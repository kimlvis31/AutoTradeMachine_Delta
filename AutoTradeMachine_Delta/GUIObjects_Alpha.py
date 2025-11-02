"""
    FA: Function Activation
    DM: Developer Mode
    GUF: Graphics Update Flag
    CM: Current Mode
    HB: Hit Box
    DR: Data Request
    SM: Switch Mode
"""

from inspect import _void
from pickle import NONE
import time
import os
import tkinter
import math
import random
from tkinter.tix import COLUMN
from PIL import Image, ImageTk, ImageDraw, ImageFont
from shapely.geometry import Point, Polygon

import CTGO_Alpha

path_PROJECT = os.path.dirname(os.path.realpath(__file__))
path_MANAGER = os.path.join(path_PROJECT + r"\data\m_GUI")
path_IMAGES = os.path.join(path_MANAGER + r"\imgs")

MOUSE_CURSORMOVED    = 0b000000001
MOUSE_LEFTCLICKED    = 0b000000010
MOUSE_RIGHTCLICKED   = 0b000000100
MOUSE_WHEELCLICKED   = 0b000001000
MOUSE_LEFTRELEASED   = 0b000010000
MOUSE_RIGHTRELEASED  = 0b000100000
MOUSE_WHEELRELEASED  = 0b001000000
MOUSE_WHEELMOVEDUP   = 0b010000000
MOUSE_WHEELMOVEDDOWN = 0b100000000

#GUI OBJECTS ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#OBJECT "BUTTON_TYPE_A" ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
class button_typeA:
    def __init__(self, initData, CTGOFileData):
        self.data = dict(); self.data["NAME"] = "#UNDEFINED#"; 
        self.data["COORD_X"] = 100; self.data["COORD_Y"] = 100; self.data["WIDTH"] = 100; self.data["HEIGHT"] = 100; 
        self.data["HB"] = []; 
        self.data["TEXT"] = ""; self.data["TEXTSIZE"] = 12; self.data["TEXTFILL"] = "white"
        self.data["LAYER"] = 0; 
        self.data["FA"] = []; 
        self.data["CM"] = "DEFAULT"; 
        self.data["GUF"] = False; 
        self.data["DM"] = False;
        self.data["DREQ_R"] = []; self.data["DREQ_R_TIMER_TRIGGER"] = 1; self.data["DREQ_R_TIMER"] = 0; self.data["DREQ_L"] = []; self.data["UF"] = []; self.data["FAR"] = NONE; self.data["FARESULT"] = NONE
        self.graphics = {"DEFAULT": [], "HOVERED": [], "CLICKED": [], "INACTIVE": []}; 
        self.canvasLabels = []; 
        self.gIntrusions = []; 
        self.showData = False;
        self.lastUserInput = ""

        for words in initData:
            if words[0] == "NAME":       self.data["NAME"]     = words[1]
            elif words[0] == "COORD_X":  self.data["COORD_X"]  = int(words[1])
            elif words[0] == "COORD_Y":  self.data["COORD_Y"]  = int(words[1])
            elif words[0] == "WIDTH":    self.data["WIDTH"]    = int(words[1])
            elif words[0] == "HEIGHT":   self.data["HEIGHT"]   = int(words[1])
            elif words[0] == "TEXT":     self.data["TEXT"]     = words[1]
            elif words[0] == "TEXTSIZE": self.data["TEXTSIZE"] = int(words[1])
            elif words[0] == "TEXTFILL": self.data["TEXTFILL"] = words[1]
            elif words[0] == "LAYER":    self.data["LAYER"]    = int(words[1])
            elif words[0] == "CM":       self.data["CM"]       = str(words[1])
            elif words[0] == "DREQ_R":   self.data["DREQ_R"].append(words[1])
            elif words[0] == "DREQ_L":   self.data["DREQ_L"].append(words[1])
            elif words[0] == "UF":       self.data["UF"].append(words[1:])
            elif words[0] == "HB":
                for i in range (len(words[1:])): self.data["HB"].append([(int(words[i+1].split(",")[0]), int(words[i+1].split(",")[1]))])
                self.data["HB"][len(self.data["HB"])].append(self.data["HB"][len(self.data["HB"])][0])
            elif words[0] == "FA":
                if words[1] == "SET_DATA_GUIO": self.data["FA"].append([words[1], words[2], textToList(words[3:])]);
                else: self.data["FA"].append(words[1:])
            elif words[0] == "MODE":
                for i in range (len(words[2:])):
                    gType = words[i+2].split(":")[0]; gContent = words[i+2].split(":")[1]
                    if (gType == "IMAGE"): self.graphics[words[1]].append(ImageTk.PhotoImage(Image.open(os.path.join(path_IMAGES + r"/{}".format(gContent))).resize((self.data["WIDTH"], self.data["HEIGHT"]), Image.LANCZOS)))
                    elif (gType == "CANVAS"): self.graphics[words[1]].append(gContent)
                    elif (gType == "CTGO"): self.graphics[words[1]].append(CTGO_Alpha.CTGO(gContent, CTGOFileData));
                    
        if (len(self.data["HB"]) == 0):
            self.data["HB_DEFAULT"] = [(self.data["COORD_X"], self.data["COORD_Y"]), 
                                       (self.data["COORD_X"] + self.data["WIDTH"], self.data["COORD_Y"]), 
                                       (self.data["COORD_X"] + self.data["WIDTH"], self.data["COORD_Y"] + self.data["HEIGHT"]),
                                       (self.data["COORD_X"], self.data["COORD_Y"] + self.data["HEIGHT"]),
                                       (self.data["COORD_X"], self.data["COORD_Y"])]
            self.data["HB"].append(self.data["HB_DEFAULT"])
        else: self.data["HB_DEFAULT"] = self.data["HB"][0]
        changeCM(self, self.data["CM"])

        for i in range (len(self.data["UF"])):
            uFunctionLines = ""
            for uFunctionLine in self.data["UF"][i]:
                if uFunctionLine == "TAB": uFunctionLines += "\t"
                elif uFunctionLine == "NEXTLINE": uFunctionLines += "\n"
                else: uFunctionLines += uFunctionLine
            self.data["UF"][i] = compile(uFunctionLines, '<string>', 'exec')

    def requestData(self, load = False):
        if (load == False):
            if (len(self.data["DREQ_L"]) > 0): return self.data["DREQ_L"]
            else: return NONE
        else:
            if (len(self.data["DREQ_R"]) > 0):
                if ((time.time_ns() - self.data["DREQ_R_TIMER"]) > (1e9 * self.data["DREQ_R_TIMER_TRIGGER"])): 
                    self.data["DREQ_R_TIMER"] = time.time_ns()
                    return self.data["DREQ_R"]
                else: return NONE
            else: return NONE

    def processData(self, data = NONE, userInput = NONE):
        results = []
        if (userInput is not NONE):
            if (self.data["CM"] != "INACTIVE"):
                if (userInput[0] == "M:RELEASED"): changeCM(self, "DEFAULT")
                elif (userInput[0] == "M:HOVERED"): changeCM(self, "HOVERED")
                elif (userInput[0] == "M:CLICKED_L"): changeCM(self, "CLICKED")
                elif (userInput[0] == "M:RELEASED_L"): changeCM(self, "HOVERED"); results += (self.data["FA"]); 
            if (userInput[0] == "M:RELEASED_R"):
                if (self.lastUserInput == "M:CLICKED_R" and (self.data["DM"] == True)): self.showData = not(self.showData); self.data["GUF"] = True;
            self.lastUserInput = userInput[0];

        if (data is not NONE):
            ldic = locals()
            for uFunctions in self.data["UF"]: 
                try: exec(uFunctions, globals(), ldic); results.append(ldic['ufRESULT'])
                except Exception as e: print("ERROR OCCURED: " + str(e))

        if (len(results) > 0): return results
        else: return NONE

    def draw(self, canvas, bypassGUF = False):
        if (self.data["GUF"] or bypassGUF) == True:
            for i in range (len(self.canvasLabels)): canvas.delete(self.canvasLabels[i])
            self.canvasLabels.clear()
            for i in range (len(self.graphics[self.data["CM"]])):
                gType = type(self.graphics[self.data["CM"]][i])
                if gType is str: self.canvasLabels.append(drawCanvasObjects(canvas, self.graphics[self.data["CM"]][i]))
                elif gType is ImageTk.PhotoImage: self.canvasLabels.append(canvas.create_image(self.data["COORD_X"], self.data["COORD_Y"], image = self.graphics[self.data["CM"]][i], anchor = "nw"));
                elif gType is CTGO_Alpha.CTGO: self.canvasLabels.append(self.graphics[self.data["CM"]][i].draw(canvas, self.data["COORD_X"], self.data["COORD_Y"]))
            self.canvasLabels.append(canvas.create_text(self.data["COORD_X"] + self.data["WIDTH"] / 2, self.data["COORD_Y"] + self.data["HEIGHT"] / 2, text = self.data["TEXT"], font = ("Times New Roman", self.data["TEXTSIZE"], "bold"), fill = self.data["TEXTFILL"], anchor = "center"))
            if (self.data["DM"] == True):
                if (self.showData == True):
                    self.canvasLabels.append(canvas.create_text(self.data["COORD_X"], self.data["COORD_Y"] + self.data["HEIGHT"] + 5, 
                                                                text = "NAME: {:s}\nX: {:d}, Y: {:d}, LAYER: {:d}\nFA: {:s}\nMODE: {:s}".format(self.data["NAME"], self.data["COORD_X"], self.data["COORD_Y"], self.data["LAYER"], str(self.data["FA"]), self.data["CM"]),
                                                                font = ("Times New Roman", 8), fill = "white", anchor = "nw"))
                self.canvasLabels.append(canvas.create_line(*[a for x in self.data["HB"] for a in x], width = 1, fill = "orange"))
            self.data["GUF"] = False
            return True
        return False
#OBJECT "BUTTON_TYPE_A" END -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#OBJECT "SWITCH_TYPE_A" ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
class switch_typeA:
    def __init__(self, initData, CTGOFileData):
        self.data = dict(); self.data["NAME"] = "#UNDEFINED#"; 
        self.data["COORD_X"] = 100; self.data["COORD_Y"] = 100; self.data["WIDTH"] = 100; self.data["HEIGHT"] = 100; 
        self.data["HB"] = []; 
        self.data["LAYER"] = 0; 
        self.data["FA1"] = []; 
        self.data["FA2"] = [];
        self.data["CM"] = "OFFDEFAULT"; 
        self.data["GUF"] = False; 
        self.data["DM"] = False;
        self.data["SM"] = False;
        self.data["DREQ_R"] = []; self.data["DREQ_R_TIMER_TRIGGER"] = 1; self.data["DREQ_R_TIMER"] = 0; self.data["DREQ_L"] = []; self.data["UF"] = []; self.data["FAR"] = NONE; self.data["FARESULT"] = NONE
        self.graphics = {"ONDEFAULT": [], "ONHOVERED": [], "ONCLICKED": [], "OFFDEFAULT": [], "OFFHOVERED": [], "OFFCLICKED": [], "INACTIVE": []}; 
        self.canvasLabels = []; 
        self.gIntrusions = []; 
        self.showData = False;
        self.lastUserInput = ""
        
        for words in initData:
            if words[0] == "NAME":      self.data["NAME"]    = words[1]
            elif words[0] == "COORD_X": self.data["COORD_X"] = int(words[1])
            elif words[0] == "COORD_Y": self.data["COORD_Y"] = int(words[1])
            elif words[0] == "WIDTH":   self.data["WIDTH"]   = int(words[1])
            elif words[0] == "HEIGHT":  self.data["HEIGHT"]  = int(words[1])
            elif words[0] == "LAYER":   self.data["LAYER"]   = int(words[1])
            elif words[0] == "CM":      self.data["CM"]      = words[1]
            elif words[0] == "DREQ_R":  self.data["DREQ_R"].append(words[1])
            elif words[0] == "DREQ_L":  self.data["DREQ_L"].append(words[1])
            elif words[0] == "UF":      self.data["UF"].append(words[1:])
            elif words[0] == "HB":
                for i in range (len(words[1:])): self.data["HB"].append([(int(words[i+1].split(",")[0]), int(words[i+1].split(",")[1]))])
                self.data["HB"][len(self.data["HB"])].append(self.data["HB"][len(self.data["HB"])][0])
            elif words[0] == "FA1":
                if words[1] == "SET_DATA_GUIO": self.data["FA1"].append([words[1], words[2], textToList(words[3:])]);
                else: self.data["FA1"].append(words[1:])
            elif words[0] == "FA2":
                if words[1] == "SET_DATA_GUIO": self.data["FA2"].append([words[1], words[2], textToList(words[3:])]);
                else: self.data["FA2"].append(words[1:])
            elif words[0] == "MODE":
                for i in range (len(words[2:])):
                    gType = words[i+2].split(":")[0]; gContent = words[i+2].split(":")[1]
                    if (gType == "IMAGE"): self.graphics[words[1]].append(ImageTk.PhotoImage(Image.open(os.path.join(path_IMAGES + r"/{}".format(gContent))).resize((self.data["WIDTH"], self.data["HEIGHT"]), Image.LANCZOS)))
                    elif (gType == "CANVAS"): self.graphics[words[1]].append(gContent)
                    elif (gType == "CTGO"): self.graphics[words[1]].append(CTGO_Alpha.CTGO(gContent, CTGOFileData))
                    
        if (len(self.data["HB"]) == 0):
            self.data["HB_DEFAULT"] = [(self.data["COORD_X"], self.data["COORD_Y"]), 
                                       (self.data["COORD_X"] + self.data["WIDTH"], self.data["COORD_Y"]), 
                                       (self.data["COORD_X"] + self.data["WIDTH"], self.data["COORD_Y"] + self.data["HEIGHT"]),
                                       (self.data["COORD_X"], self.data["COORD_Y"] + self.data["HEIGHT"]),
                                       (self.data["COORD_X"], self.data["COORD_Y"])]
            self.data["HB"].append(self.data["HB_DEFAULT"])
        else: self.data["HB_DEFAULT"] = self.data["HB"][0]
        changeCM(self, self.data["CM"])

        for i in range (len(self.data["UF"])):
            uFunctionLines = ""
            for uFunctionLine in self.data["UF"][i]:
                if uFunctionLine == "TAB": uFunctionLines += "\t"
                elif uFunctionLine == "NEXTLINE": uFunctionLines += "\n"
                else: uFunctionLines += uFunctionLine
            self.data["UF"][i] = compile(uFunctionLines, '<string>', 'exec')

    def requestData(self, load = False):
        if (load == False):
            if (len(self.data["DREQ_R"]) > 0):
                if ((time.time_ns() - self.data["DREQ_R_TIMER"]) > (1e9 * self.data["DREQ_R_TIMER_TRIGGER"])): 
                    self.data["DREQ_R_TIMER"] = time.time_ns()
                    return self.data["DREQ_R"]
                else: return NONE
            else: return NONE
        else:
            if (len(self.data["DREQ_L"]) > 0): return self.data["DREQ_L"]
            else: return NONE

    def processData(self, data = NONE, userInput = NONE):
        results = []
        if (userInput is not NONE):
            if (userInput[0] == "M:RELEASED"):
                if self.data["SM"] == True: changeCM(self, "ONDEFAULT")
                elif self.data["SM"] == False: changeCM(self, "OFFDEFAULT")
            elif (userInput[0] == "M:HOVERED"):
                if self.data["SM"] == True: changeCM(self, "ONHOVERED")
                elif self.data["SM"] == False: changeCM(self, "OFFHOVERED")
            elif (userInput[0] == "M:CLICKED_L"):
                if self.data["SM"] == True: changeCM(self, "ONCLICKED")
                elif self.data["SM"] == False: changeCM(self, "OFFCLICKED")
            elif (userInput[0] == "M:RELEASED_L"):
                if self.data["SM"] == True: changeCM(self, "OFFHOVERED"); self.data["SM"] = False; results += (self.data["FA2"]) #"ON" to "OFF" 
                elif self.data["SM"] == False: changeCM(self, "ONHOVERED"); self.data["SM"] = True; results += (self.data["FA1"]) #"OFF" to "ON"
            elif (userInput[0] == "M:RELEASED_R"):
                if (self.lastUserInput == "M:CLICKED_R" and (self.data["DM"] == True)): self.showData = not(self.showData); self.data["GUF"] = True;
            self.lastUserInput = userInput[0]
        if (data is not NONE):
            ldic = locals()
            for uFunctions in self.data["UF"]: 
                try: exec(uFunctions, globals(), ldic); results.append(ldic['ufRESULT'])
                except Exception as e: print("ERROR OCCURED: " + str(e))

        if (len(results) > 0): return results
        else: return NONE

    def draw(self, canvas, bypassGUF = False):
        if (self.data["GUF"] or bypassGUF) == True:
            for i in range (len(self.canvasLabels)): canvas.delete(self.canvasLabels[i])
            self.canvasLabels.clear()
            for i in range (len(self.graphics[self.data["CM"]])):
                gType = type(self.graphics[self.data["CM"]][i])
                if gType is str: self.canvasLabels.append(drawCanvasObjects(canvas, self.graphics[self.data["CM"]][i]))
                elif gType is ImageTk.PhotoImage: self.canvasLabels.append(canvas.create_image(self.data["COORD_X"], self.data["COORD_Y"], image = self.graphics[self.data["CM"]][i], anchor = "nw"));
                elif gType is CTGO_Alpha.CTGO: self.canvasLabels.append(self.graphics[self.data["CM"]][i].draw(canvas, self.data["COORD_X"], self.data["COORD_Y"]))
            if (self.data["DM"] == True):
                if (self.showData == True):
                    self.canvasLabels.append(canvas.create_text(self.data["COORD_X"], self.data["COORD_Y"] + self.data["HEIGHT"] + 5, 
                                                                text = "NAME: {:s}\nX: {:d}, Y: {:d}, LAYER: {:d}\nFA1: {:s}\nFA2: {:s}\nMODE: {:s}".format(self.data["NAME"], self.data["COORD_X"], self.data["COORD_Y"], self.data["LAYER"], str(self.data["FA1"]), str(self.data["FA2"]), self.data["CM"]),
                                                                font = ("Times New Roman", 8), fill = "white", anchor = "nw"))
                self.canvasLabels.append(canvas.create_line(*[a for x in self.data["HB"] for a in x], width = 1, fill = "orange"))
            self.data["GUF"] = False
            return True
        return False

    def changeSMode(self, mode):
        if (self.data["SM"] != mode):
            if (mode == True):
                if self.data["CM"] == "OFFDEFAULT": self.data["CM"] = "ONDEFAULT"
                elif self.data["CM"] == "OFFHOVERED": self.data["CM"] = "ONHOVERED"
                elif self.data["CM"] == "OFFCLICKED": self.data["CM"] = "ONCLICKED"
            else:
                if self.data["CM"] == "ONDEFAULT": self.data["CM"] = "OFFDEFAULT"
                elif self.data["CM"] == "ONHOVERED": self.data["CM"] = "OFFHOVERED"
                elif self.data["CM"] == "ONCLICKED": self.data["CM"] = "OFFCLICKED"
            self.data["GUF"] = True; self.data["SM"] = mode
#OBJECT "SWITCH_TYPE_A" END -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#OBJECT "SLIDER_TYPE_A" ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
class slider_typeA:
    def __init__(self, initData, CTGOFileData):
        self.sliderGOffset = 5

        self.data = dict(); self.data["NAME"] = "#UNDEFINED#"; 
        self.data["COORD_X"] = 100; self.data["COORD_Y"] = 100; self.data["WIDTH"] = 100; self.data["HEIGHT"] = 20; 
        self.data["LAYER"] = 0; 
        self.data["FA"] = []; 
        self.data["CM"] = "DEFAULT"; 
        self.data["GUF"] = False; 
        self.data["DM"] = False;
        self.data["SLIDERDIRECTION"] = "HORIZONTAL"; self.data["SLIDERVALUE"] = 50; self.data["SLIDERLENGTH"] = 20;
        self.data["SHOWVALUE"] = 0; self.data["SHOWVALUECOLOR"] = (0, 0, 0); self.data["SHOWVALUEDECIMALPOINTS"] = 3
        self.data["DREQ_R"] = []; self.data["DREQ_R_TIMER_TRIGGER"] = 0.01; self.data["DREQ_R_TIMER"] = 0; self.data["DREQ_L"] = []; self.data["UF"] = []; self.data["FAR"] = NONE; self.data["FARESULT"] = NONE
        self.graphics = {"RAIL_G_DEFAULT": [], "RAIL_G_HOVERED": [], "SLIDER_G_DEFAULT": [], "SLIDER_G_HOVERED": [], "SLIDER_G_CLICKED": []};
        self.canvasLabels = []; 
        self.gIntrusions = []; 
        self.showData = False;
        self.lastUserInput = ""
        
        self.gStatus = [0, 0]
        self.lastClickedPoint = 0

        self.sliderGraphicsParams = []

        self.reCalculateSliderParameters();

        for words in initData:
            if words[0] == "NAME":      self.data["NAME"]    = words[1]
            elif words[0] == "COORD_X": self.data["COORD_X"] = int(words[1])
            elif words[0] == "COORD_Y": self.data["COORD_Y"] = int(words[1])
            elif words[0] == "WIDTH": self.data["WIDTH"] = int(words[1]); self.reCalculateSliderParameters();
            elif words[0] == "HEIGHT": self.data["HEIGHT"] = int(words[1]); self.reCalculateSliderParameters();
            elif words[0] == "LAYER":   self.data["LAYER"] = int(words[1])
            elif words[0] == "CM":      self.data["CM"] = words[1]
            elif words[0] == "SLIDERDIRECTION": self.data["SLIDERDIRECTION"] = words[1]; self.reCalculateSliderParameters();
            elif words[0] == "SLIDERVALUE": self.data["SLIDERVALUE"] = max([int(words[1]), 100]); self.reCalculateSliderParameters();
            elif words[0] == "SLIDERLENGTH": self.data["SLIDERLENGTH"] = max([int(words[1]), 50]); self.reCalculateSliderParameters();
            elif words[0] == "SHOWVALUECOLOR": self.data["SHOWVALUECOLOR"] = (int(words[1]), int(words[2]), int(words[3]))
            elif words[0] == "SHOWVALUEDECIMALPOINTS": self.data["SHOWVALUEDECIMALPOINTS"] = int(words[1])
            elif words[0] == "DREQ_R":  self.data["DREQ_R"].append(words[1])
            elif words[0] == "DREQ_L":  self.data["DREQ_L"].append(words[1])
            elif words[0] == "UF":      self.data["UF"].append(words[1:]);
            elif words[0] == "FA":
                if words[1] == "SET_DATA_GUIO": self.data["FA"].append([words[1], words[2], textToList(words[3:])]);
                else: self.data["FA"].append(words[1:])
            elif ((words[0] == "RAIL_G_DEFAULT") or (words[0] == "RAIL_G_HOVERED")):
                for i in range (len(words[1:])):
                    gType = words[i+1].split(":")[0]; gContent = words[i+1].split(":")[1]
                    if (gType == "IMAGE"): self.graphics[words[0]].append(ImageTk.PhotoImage(Image.open(os.path.join(path_IMAGES + r"/{}".format(gContent))).resize((self.data["WIDTH"], self.data["HEIGHT"]), Image.LANCZOS)))
                    elif (gType == "CTGO"): self.graphics[words[0]].append(CTGO_Alpha.CTGO(gContent + ",WIDTH=" + str(self.data["WIDTH"]) + ",HEIGHT=" + str(self.data["HEIGHT"]), CTGOFileData))
            elif ((words[0] == "SLIDER_G_DEFAULT") or (words[0] == "SLIDER_G_HOVERED") or (words[0] == "SLIDER_G_CLICKED")):
                for i in range (len(words[1:])):
                    gType = words[i+1].split(":")[0]; gContent = words[i+1].split(":")[1]
                    if (gType == "IMAGE"): self.graphics[words[0]].append(ImageTk.PhotoImage(Image.open(os.path.join(path_IMAGES + r"/{}".format(gContent))).resize((self.data["WIDTH"], self.data["HEIGHT"]), Image.LANCZOS)))
                    elif (gType == "CTGO"): 
                        self.sliderGraphicsParams.append((words[0], gContent, CTGOFileData))
                        self.graphics[words[0]].append(CTGO_Alpha.CTGO(gContent + ",WIDTH=" + str(self.sliderWidthPixel) + ",HEIGHT=" + str(self.sliderHeightPixel), CTGOFileData))
        #Rail HitBox
        self.data["HB"] = [[(self.data["COORD_X"], self.data["COORD_Y"]), 
                                    (self.data["COORD_X"] + self.data["WIDTH"], self.data["COORD_Y"]), 
                                    (self.data["COORD_X"] + self.data["WIDTH"], self.data["COORD_Y"] + self.data["HEIGHT"]),
                                    (self.data["COORD_X"], self.data["COORD_Y"] + self.data["HEIGHT"]),
                                    (self.data["COORD_X"], self.data["COORD_Y"])]]
        #Slider HitBox
        self.data["HB"].append([(self.sliderPosX, self.sliderPosY),
                                (self.sliderPosX + self.sliderWidthPixel, self.sliderPosY),
                                (self.sliderPosX + self.sliderWidthPixel, self.sliderPosY + self.sliderHeightPixel),
                                (self.sliderPosX, self.sliderPosY + self.sliderHeightPixel),
                                (self.sliderPosX, self.sliderPosY)])

        self.data["SHOWVALUE"] = "{:.{prec}f}".format(self.data["SLIDERVALUE"], prec = self.data["SHOWVALUEDECIMALPOINTS"]);

        for i in range (len(self.data["UF"])):
            uFunctionLines = ""
            for uFunctionLine in self.data["UF"][i]:
                if uFunctionLine == "TAB": uFunctionLines += "\t"
                elif uFunctionLine == "NEXTLINE": uFunctionLines += "\n"
                else: uFunctionLines += uFunctionLine
            self.data["UF"][i] = compile(uFunctionLines, '<string>', 'exec')

    def requestData(self, load = False):
        if (load == False):
            if ((time.time_ns() - self.data["DREQ_R_TIMER"]) > (1e9 * self.data["DREQ_R_TIMER_TRIGGER"])):
                returnData = []
                self.data["DREQ_R_TIMER"] = time.time_ns()
                if (len(self.data["DREQ_R"]) > 0): returnData += self.data["DREQ_R"]
                if (self.gStatus == [1, 2]): returnData += ["MANAGER:MOUSESTATUS"]
                if (len(returnData) > 0): return returnData
                else: return NONE
            else: return NONE
        else:
            if (len(self.data["DREQ_L"]) > 0): return self.data["DREQ_L"]
            else: return NONE

    def processData(self, data = NONE, userInput = NONE):
        results = []
        if (userInput is not NONE):
            if (userInput[0] == "M:HOVERED"):
                if self.gStatus != [1, 2]:
                    if (len(userInput[1]) == 1): self.gStatus = [1, 0]; self.data["GUF"] = True;
                    elif (len(userInput[1]) == 2): self.gStatus = [1, 1]; self.data["GUF"] = True;
            elif (userInput[0] == "M:RELEASED"):
                self.gStatus = [0, 0]; self.data["GUF"] = True;
            elif (userInput[0] == "M:CLICKED_L"):
                if (self.gStatus == [1, 1]):
                    if (self.data["SLIDERDIRECTION"] == "HORIZONTAL"): self.lastClickedPoint = userInput[2][0]
                    elif (self.data["SLIDERDIRECTION"] == "VERTICAL"): self.lastClickedPoint = userInput[2][1]
                    self.gStatus = [1, 2];
                    self.data["GUF"] = True;
                    results.append(["FUNCTION_MANAGER", "GUIOSEARCH_OFF"])
                elif (self.gStatus == [1, 0]):
                    if (self.data["SLIDERDIRECTION"] == "HORIZONTAL"): clickedValue = (userInput[2][0] - self.data["COORD_X"] - self.sliderGOffset - self.sliderWidthPixel / 2) / self.railPixelLength * 100
                    elif (self.data["SLIDERDIRECTION"] == "VERTICAL"): clickedValue = ((self.data["COORD_Y"] + self.railPixelLength + self.sliderGOffset + self.sliderHeightPixel / 2) - userInput[2][1]) / self.railPixelLength * 100
                    if clickedValue > 100: clickedValue = 100
                    elif clickedValue < 0: clickedValue = 0
                    self.data["SLIDERVALUE"] = clickedValue; self.data["SHOWVALUE"] = "{:.{prec}f}".format(self.data["SLIDERVALUE"], prec = self.data["SHOWVALUEDECIMALPOINTS"]); self.reCalculateSliderParameters(); self.reCalculateSliderHitBox();
                    if Point(userInput[2]).within(Polygon(self.data["HB"][1][:-1])): self.gStatus = [1, 1];
                    else: self.gStatus = [1, 0];
                    self.data["GUF"] = True;
                    results += (self.data["FA"])
            elif (userInput[0] == "M:RELEASED_L"):
                if (self.gStatus == [1, 2]):
                    self.gStatus = [0, 0]
                    if Point((userInput[2][0], userInput[2][1])).within(Polygon(self.data["HB"][0][:-1])): self.gStatus = [1, 0];
                    if Point((userInput[2][0], userInput[2][1])).within(Polygon(self.data["HB"][1][:-1])): self.gStatus = [1, 1];
                    self.data["GUF"] = True;
                    results.append(["FUNCTION_MANAGER", "GUIOSEARCH_ON"])
                    results.append(["FUNCTION_MANAGER", "SELECTPRIORITYGUIO"])

            elif (userInput[0] == "M:RELEASED_R"):
                if (self.lastUserInput == "M:CLICKED_R" and (self.data["DM"] == True)): self.showData = not(self.showData); self.data["GUF"] = True;
            self.lastUserInput = userInput[0]

        if (data is not NONE):
            if (self.gStatus == [1, 2]):
                if (self.data["SLIDERDIRECTION"] == "HORIZONTAL"): clickedValue = (data["MANAGER:MOUSESTATUS"][0] - (self.data["COORD_X"] + self.sliderGOffset + self.sliderWidthPixel / 2)) / self.railPixelLength * 100
                elif (self.data["SLIDERDIRECTION"] == "VERTICAL"): clickedValue = ((self.data["COORD_Y"] + self.railPixelLength + self.sliderGOffset + self.sliderHeightPixel / 2) - data["MANAGER:MOUSESTATUS"][1]) / self.railPixelLength * 100
                if clickedValue > 100: clickedValue = 100
                elif clickedValue < 0: clickedValue = 0
                self.data["SLIDERVALUE"] = clickedValue; self.data["SHOWVALUE"] = "{:.{prec}f}".format(self.data["SLIDERVALUE"], prec = self.data["SHOWVALUEDECIMALPOINTS"]); self.reCalculateSliderParameters(); self.reCalculateSliderHitBox();
                self.data["GUF"] = True;
                results += (self.data["FA"])

            ldic = locals()
            for uFunctions in self.data["UF"]:
                try: exec(uFunctions, globals(), ldic); results.append(ldic['ufRESULT'])
                except Exception as e: print("ERROR OCCURED: " + str(e))

        if (len(results) > 0): return results
        else: return NONE

    def draw(self, canvas, bypassGUF = False):
        if (self.data["GUF"] or bypassGUF) == True:
            for i in range (len(self.canvasLabels)): canvas.delete(self.canvasLabels[i])
            self.canvasLabels.clear()

            keyword = ""
            if self.gStatus[0] == 0: keyword = "RAIL_G_DEFAULT"
            elif self.gStatus[0] == 1: keyword = "RAIL_G_HOVERED"
            for i in range (len(self.graphics[keyword])):
                gType = type(self.graphics[keyword][i])
                if gType is ImageTk.PhotoImage: self.canvasLabels.append(canvas.create_image(self.data["COORD_X"], self.data["COORD_Y"], image = self.graphics[keyword][i], anchor = "nw"));
                elif gType is CTGO_Alpha.CTGO: self.canvasLabels.append(self.graphics[keyword][i].draw(canvas, self.data["COORD_X"], self.data["COORD_Y"]))
                
            keyword = ""
            if self.gStatus[1] == 0: keyword = "SLIDER_G_DEFAULT"
            elif self.gStatus[1] == 1: keyword = "SLIDER_G_HOVERED"
            elif self.gStatus[1] == 2: keyword = "SLIDER_G_CLICKED"
            for i in range (len(self.graphics[keyword])):
                gType = type(self.graphics[keyword][i])
                if gType is ImageTk.PhotoImage: self.canvasLabels.append(canvas.create_image(self.sliderPosX, self.sliderPosY, image = self.graphics[keyword][i], anchor = "nw"));
                elif gType is CTGO_Alpha.CTGO: self.canvasLabels.append(self.graphics[keyword][i].draw(canvas, self.sliderPosX, self.sliderPosY))

            if (self.data["DM"] == True):
                if (self.showData == True):
                    self.canvasLabels.append(canvas.create_text(self.data["COORD_X"], self.data["COORD_Y"] + self.data["HEIGHT"] + 5, 
                                                                text = "NAME: {:s}\nX: {:d}, Y: {:d}, LAYER: {:d}\nFA: {:s}\nVALUE: {:f}\nMODE: {:s}".format(self.data["NAME"], self.data["COORD_X"], self.data["COORD_Y"], self.data["LAYER"], str(self.data["FA"]), (self.data["SLIDERVALUE"]), self.data["CM"]),
                                                                font = ("Times New Roman", 8), fill = "white", anchor = "nw"))
                self.canvasLabels.append(canvas.create_line(*[a for x in self.data["HB"][0] for a in x], width = 1, fill = "orange"))
                self.canvasLabels.append(canvas.create_line(*[a for x in self.data["HB"][1] for a in x], width = 1, fill = "orange"))
            self.data["GUF"] = False
            return True
        return False

    def reCalculateSliderParameters(self):
        if (self.data["SLIDERDIRECTION"] == "HORIZONTAL"):
            self.sliderWidthPixel = int(self.data["WIDTH"] * self.data["SLIDERLENGTH"] / 100)
            self.sliderHeightPixel = self.data["HEIGHT"] - self.sliderGOffset * 2
            self.railPixelLength = self.data["WIDTH"] - self.sliderGOffset * 2 - self.sliderWidthPixel
            self.sliderPosX = self.data["COORD_X"] + self.sliderGOffset + self.railPixelLength * self.data["SLIDERVALUE"] / 100
            self.sliderPosY = self.data["COORD_Y"] + self.sliderGOffset

        elif (self.data["SLIDERDIRECTION"] == "VERTICAL"):
            self.sliderWidthPixel = self.data["WIDTH"] - self.sliderGOffset * 2
            self.sliderHeightPixel = int(self.data["HEIGHT"] * self.data["SLIDERLENGTH"] / 100)
            self.railPixelLength = self.data["HEIGHT"] - self.sliderGOffset * 2 - self.sliderHeightPixel
            self.sliderPosX = self.data["COORD_X"] + self.sliderGOffset
            self.sliderPosY = (self.data["COORD_Y"] + self.railPixelLength + self.sliderGOffset) - (self.railPixelLength * self.data["SLIDERVALUE"] / 100)

        #Update Slider Graphics
        for i in range (len(self.sliderGraphicsParams)): self.graphics[self.sliderGraphicsParams[i][0]].append(CTGO_Alpha.CTGO(self.sliderGraphicsParams[i][1] + ",WIDTH=" + str(self.sliderWidthPixel) + ",HEIGHT=" + str(self.sliderHeightPixel), self.sliderGraphicsParams[i][2]))

    def reCalculateSliderHitBox(self):
        self.data["HB"][1] = [(self.sliderPosX, self.sliderPosY),
                              (self.sliderPosX + self.sliderWidthPixel, self.sliderPosY),
                              (self.sliderPosX + self.sliderWidthPixel, self.sliderPosY + self.sliderHeightPixel),
                              (self.sliderPosX, self.sliderPosY + self.sliderHeightPixel),
                              (self.sliderPosX, self.sliderPosY)]

#OBJECT "SLIDER_TYPE_A" END -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#OBJECT "TEXTINPUTBOX_TYPE_A" ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
class textInputBox_typeA:
    def __init__(self, initData, CTGOFileData):
        self.data = dict(); self.data["NAME"] = "#UNDEFINED#"; 
        self.data["COORD_X"] = 100; self.data["COORD_Y"] = 100; self.data["WIDTH"] = 100; self.data["HEIGHT"] = 100; 
        self.data["HB"] = [];
        self.data["LAYER"] = 0; 
        self.data["FA"] = []; 
        self.data["CM"] = "DEFAULT"; 
        self.data["GUF"] = False; 
        self.data["DM"] = False;
        self.data["DREQ_R"] = []; self.data["DREQ_R_TIMER_TRIGGER"] = 0.01; self.data["DREQ_R_TIMER"] = 0; self.data["DREQ_L"] = []; self.data["UF"] = []; self.data["FAR"] = NONE; self.data["FARESULT"] = NONE
        self.graphics = {"DEFAULT": [], "HOVERED": [], "CLICKED": [], "ACTIVATED": [], "INACTIVE": []}; 
        self.canvasLabels = []; 
        self.gIntrusions = []; 
        self.showData = False;
        self.lastUserInput = ""

        for words in initData:
            if words[0] == "NAME":       self.data["NAME"]     = words[1]
            elif words[0] == "COORD_X":  self.data["COORD_X"]  = int(words[1])
            elif words[0] == "COORD_Y":  self.data["COORD_Y"]  = int(words[1])
            elif words[0] == "WIDTH":    self.data["WIDTH"]    = int(words[1])
            elif words[0] == "HEIGHT":   self.data["HEIGHT"]   = int(words[1])
            elif words[0] == "TEXT":     self.data["TEXT"]     = words[1]
            elif words[0] == "TEXTSIZE": self.data["TEXTSIZE"] = int(words[1])
            elif words[0] == "TEXTFILL": self.data["TEXTFILL"] = words[1]
            elif words[0] == "LAYER":    self.data["LAYER"]    = int(words[1])
            elif words[0] == "CM":       self.data["CM"]       = str(words[1])
            elif words[0] == "DREQ_R":   self.data["DREQ_R"].append(words[1])
            elif words[0] == "DREQ_L":   self.data["DREQ_L"].append(words[1])
            elif words[0] == "UF":       self.data["UF"].append(words[1:])
            elif words[0] == "HB":
                for i in range (len(words[1:])): self.data["HB"].append([(int(words[i+1].split(",")[0]), int(words[i+1].split(",")[1]))])
                self.data["HB"][len(self.data["HB"])].append(self.data["HB"][len(self.data["HB"])][0])
            elif words[0] == "FA":
                if words[1] == "SET_DATA_GUIO": self.data["FA"].append([words[1], words[2], textToList(words[3:])]);
                else: self.data["FA"].append(words[1:])
            elif words[0] == "MODE":
                for i in range (len(words[2:])):
                    gType = words[i+2].split(":")[0]; gContent = words[i+2].split(":")[1]
                    if (gType == "CTGO"): self.graphics[words[1]].append(CTGO_Alpha.CTGO(gContent + ",WIDTH=" + str(self.data["WIDTH"]) + ",HEIGHT=" + str(self.data["HEIGHT"]), CTGOFileData))
                    
        if (len(self.data["HB"]) == 0):
            self.data["HB_DEFAULT"] = [(self.data["COORD_X"], self.data["COORD_Y"]), 
                                       (self.data["COORD_X"] + self.data["WIDTH"], self.data["COORD_Y"]), 
                                       (self.data["COORD_X"] + self.data["WIDTH"], self.data["COORD_Y"] + self.data["HEIGHT"]),
                                       (self.data["COORD_X"], self.data["COORD_Y"] + self.data["HEIGHT"]),
                                       (self.data["COORD_X"], self.data["COORD_Y"])]
            self.data["HB"].append(self.data["HB_DEFAULT"])
        else: self.data["HB_DEFAULT"] = self.data["HB"][0]
        changeCM(self, self.data["CM"])
        
        self.gOffset = 8
        self.data["TEXT"] = ""
        self.fontType = "Courier"
        self.fontColor = "white"
        self.fontSize = int(self.data["HEIGHT"] - self.gOffset * 2.5)
        self.fontPixelWidth = self.fontSize * 0.8005
        
        self.reSamplingFactor = 4
        self.textImage = Image.new(mode = "RGBA", size = (self.data["WIDTH"] * self.reSamplingFactor, self.data["HEIGHT"] * self.reSamplingFactor), color = (0, 0, 0, 0))
        self.font_PIL = ImageFont.truetype("times.ttf", self.fontSize * self.reSamplingFactor)
        
        self.displayBoxPosition = 0
        self.charBoxIntervals = [0]

        self.cursorTimer = 0; self.cursorShow = False;

        self.selectionBox = [0, 0]
        
        self.textImageWidth = self.data["WIDTH"] - self.gOffset * 2;
        self.textImageHeight = self.data["HEIGHT"] - self.gOffset * 2
        self.textAnchor = "L"
        self.uneditedImage = 0
        self.croppedImage = 0
        self.resized = 0

        for i in range (len(self.data["UF"])):
            uFunctionLines = ""
            for uFunctionLine in self.data["UF"][i]:
                if uFunctionLine == "TAB": uFunctionLines += "\t"
                elif uFunctionLine == "NEXTLINE": uFunctionLines += "\n"
                else: uFunctionLines += uFunctionLine
            self.data["UF"][i] = compile(uFunctionLines, '<string>', 'exec')

    def requestData(self, load = False):
        if (load == False):
            if ((time.time_ns() - self.data["DREQ_R_TIMER"]) > (1e9 * self.data["DREQ_R_TIMER_TRIGGER"])):
                self.data["DREQ_R_TIMER"] = time.time_ns()
                returnData = []
                if (len(self.data["DREQ_R"]) > 0): returnData += self.data["DREQ_R"]
                if (self.data["CM"] == "ACTIVATED"): returnData += ["MANAGER:MOUSESTATUSFLAG", "MANAGER:MOUSESTATUS", "MANAGER:KEYBOARDSTATUS"]
                if (len(returnData) > 0): return returnData
                else: return NONE
            else: return NONE
        else:
            if (len(self.data["DREQ_L"]) > 0): return self.data["DREQ_L"]
            else: return NONE

    def processData(self, data = NONE, userInput = NONE):
        results = []
        if (userInput is not NONE):
            if (self.data["CM"] != "INACTIVE"):
                if (userInput[0] == "M:RELEASED"): 
                    if ((self.data["CM"] == "HOVERED") or (self.data["CM"] == "CLICKED")): changeCM(self, "DEFAULT")
                elif (userInput[0] == "M:HOVERED"): 
                    if not(self.data["CM"] == "ACTIVATED"): changeCM(self, "HOVERED")
                elif (userInput[0] == "M:CLICKED_L"): 
                    changeCM(self, "CLICKED");
                    clickedPositionX_Rel = userInput[2][0] - (self.data["COORD_X"] + self.gOffset); clickedPositionY_Rel = userInput[2][1] - (self.data["COORD_Y"] + self.gOffset)
                    #Clicked Inside the TextBox
                    if ((0 <= clickedPositionX_Rel) and (clickedPositionX_Rel <= self.textImageWidth) and (0 <= clickedPositionY_Rel) and (clickedPositionY_Rel <= self.textImageHeight)):
                        self.cursorShow = True
                        clickedPosition_Abs = clickedPositionX_Rel + self.displayBoxPosition
                        indexA = 0
                        for i in range (len(self.charBoxIntervals)):
                            if (clickedPosition_Abs >= self.charBoxIntervals[i]): indexA = i;
                        self.selectionBox = [indexA, indexA]
                        if (indexA < len(self.charBoxIntervals) - 1):
                            if (clickedPosition_Abs >= (self.charBoxIntervals[indexA] + (self.charBoxIntervals[indexA + 1] - self.charBoxIntervals[indexA]) / 2)): self.selectionBox = [indexA + 1, indexA + 1]
                    #Clicked Outside the TextBox
                    else: self.selectionBox = [-1, -1]
                    results.append(["FUNCTION_MANAGER", "GUIOSEARCH_OFF"])

                elif (userInput[0] == "M:RELEASED_L"): 
                    if (self.cursorShow == True):
                        changeCM(self, "ACTIVATED")
                        results.append(["FUNCTION_MANAGER", "GUIOSEARCH_ON"])
                        results.append(["FUNCTION_MANAGER", "SELECTPRIORITYGUIO"])
                    else:
                        changeCM(self, "HOVERED")
                        results.append(["FUNCTION_MANAGER", "GUIOSEARCH_ON"])
                elif (userInput[0] == "M:MOVED"):
                    if ((self.data["CM"] == "CLICKED") and (self.selectionBox != [-1, -1])):
                        clickedPosition_Rel = userInput[2][0] - (self.data["COORD_X"] + self.gOffset)
                        clickedPosition_Abs = clickedPosition_Rel + self.displayBoxPosition
                        indexA = 0
                        for i in range (len(self.charBoxIntervals)):
                            if (clickedPosition_Abs >= self.charBoxIntervals[i]): indexA = i
                        self.selectionBox[1] = indexA
                        if (indexA < len(self.charBoxIntervals) - 1):
                            if (clickedPosition_Abs >= (self.charBoxIntervals[indexA] + (self.charBoxIntervals[indexA + 1] - self.charBoxIntervals[indexA]) / 2)): self.selectionBox[1] = indexA + 1
                        if (clickedPosition_Rel < 0): self.calculateDisplayBoxPosition("L")
                        elif (clickedPosition_Rel > self.textImageWidth): self.calculateDisplayBoxPosition("R")
                        self.data["GUF"] = True
            if (userInput[0] == "M:RELEASED_R"):
                if (self.lastUserInput == "M:CLICKED_R" and (self.data["DM"] == True)): self.showData = not(self.showData); self.data["GUF"] = True;
            self.lastUserInput = userInput[0];

        if (data is not NONE):
            if (data["MANAGER:MOUSESTATUSFLAG"] & MOUSE_LEFTCLICKED):
                if not(Point((data["MANAGER:MOUSESTATUS"][0], data["MANAGER:MOUSESTATUS"][1])).within(Polygon(self.data["HB"][0][:-1]))): self.selectionBox = [-1, -1]; changeCM(self, "DEFAULT");

            if (data["MANAGER:KEYBOARDSTATUS"][0]):
                keyPressed = data["MANAGER:KEYBOARDSTATUS"][2]
                if (len(keyPressed) == 1):
                    if (self.selectionBox[0] == self.selectionBox[1]):
                        self.data["TEXT"] = self.data["TEXT"][:self.selectionBox[0]] + keyPressed + self.data["TEXT"][self.selectionBox[1]:]
                        self.calculateCharBoxIntervals()
                        self.selectionBox[0] += 1; self.selectionBox[1] += 1;
                        self.calculateDisplayBoxPosition("R")
                        self.data["GUF"] = True
                    else:
                        smallerIndex = int(min(self.selectionBox)); largerIndex = int(max(self.selectionBox))
                        self.data["TEXT"] = self.data["TEXT"][:smallerIndex] + keyPressed + self.data["TEXT"][largerIndex:]
                        self.calculateCharBoxIntervals()
                        self.selectionBox = [smallerIndex + 1, smallerIndex + 1]
                        self.calculateDisplayBoxPosition("R")
                        self.data["GUF"] = True
                elif (keyPressed == "BACKSPACE"):
                    if (self.selectionBox[0] == self.selectionBox[1]):
                        if (self.selectionBox[0] > 0):
                            self.data["TEXT"] = self.data["TEXT"][:self.selectionBox[0]-1] + self.data["TEXT"][self.selectionBox[0]:]
                            self.selectionBox = [self.selectionBox[0] - 1, self.selectionBox[0] - 1];
                            self.calculateCharBoxIntervals()
                            self.calculateDisplayBoxPosition("L")
                            self.data["GUF"] = True
                    else:
                        smallerIndex = int(min(self.selectionBox)); largerIndex = int(max(self.selectionBox))
                        self.data["TEXT"] = self.data["TEXT"][:smallerIndex] + self.data["TEXT"][largerIndex:]
                        self.calculateCharBoxIntervals()
                        self.selectionBox = [smallerIndex, smallerIndex]
                        self.calculateDisplayBoxPosition("L")
                        self.data["GUF"] = True

                elif (keyPressed == "LEFT"):
                    smallerIndex = int(min(self.selectionBox)); largerIndex = int(max(self.selectionBox))
                    if (smallerIndex > 0): 
                        #Move the SelectionBox
                        if (smallerIndex == largerIndex): self.selectionBox = [smallerIndex - 1, smallerIndex - 1];
                        else: self.selectionBox = [smallerIndex, smallerIndex];
                        #Move the DisplayBoxPosition
                        self.calculateDisplayBoxPosition("L")
                        self.cursorShow = True
                        self.data["GUF"] = True
                elif (keyPressed == "RIGHT"):
                    smallerIndex = int(min(self.selectionBox)); largerIndex = int(max(self.selectionBox))
                    if (largerIndex < len(self.data["TEXT"])): 
                        #Move the SelectionBox
                        if (smallerIndex == largerIndex): self.selectionBox = [largerIndex + 1, largerIndex + 1]; 
                        else: self.selectionBox = [largerIndex, largerIndex]; 
                        #Move the DisplayBoxPosition
                        self.calculateDisplayBoxPosition("R")
                        self.cursorShow = True
                        self.data["GUF"] = True
                        

            ldic = locals()
            for uFunctions in self.data["UF"]: 
                try: exec(uFunctions, globals(), ldic); results.append(ldic['ufRESULT'])
                except Exception as e: print("ERROR OCCURED: " + str(e))

        if ((self.data["CM"] == "ACTIVATED") and ((time.time_ns() - self.cursorTimer) > 5e8)): self.cursorShow = not(self.cursorShow); self.cursorTimer = time.time_ns(); self.data["GUF"] = True;

        if (len(results) > 0): return results
        else: return NONE

    def draw(self, canvas, bypassGUF = False):
        if (self.data["GUF"] or bypassGUF) == True:
            for i in range (len(self.canvasLabels)): canvas.delete(self.canvasLabels[i])
            self.canvasLabels.clear()

            for i in range (len(self.graphics[self.data["CM"]])): self.canvasLabels.append(self.graphics[self.data["CM"]][i].draw(canvas, self.data["COORD_X"], self.data["COORD_Y"]))

            imageLength = int(self.font_PIL.getlength(self.data["TEXT"])) + 10

            self.textImage = Image.new(mode = "RGBA", size = (imageLength, self.textImageHeight * self.reSamplingFactor), color = (255, 255, 255, 0))
            textDraw = ImageDraw.Draw(self.textImage)

            textDraw.text((0, self.textImageHeight * self.reSamplingFactor / 2),
                      self.data["TEXT"],
                      fill = (255, 255, 255, 255),
                      font = self.font_PIL,
                      anchor = 'lm', spacing = 3, align = 'left',
                      stroke_fill = (255, 25, 255, 255), stroke_width = 0)
            
            #Cursor and Selection Box Drawing
            if ((self.data["CM"] == "ACTIVATED") or (self.data["CM"] == "CLICKED")):
                indexFlip = self.selectionBox[0] > self.selectionBox[1]
                if (indexFlip == True): indexes = [self.selectionBox[1], self.selectionBox[0]]
                else: indexes = [self.selectionBox[0], self.selectionBox[1]]
                
                #Selection Box Drawing
                if (self.selectionBox[0] != self.selectionBox[1]):
                    selectionBoxImage = Image.new(mode = "RGBA", size = (imageLength, self.textImageHeight * self.reSamplingFactor), color = (255, 255, 255, 0))
                    selectionBoxDraw = ImageDraw.Draw(selectionBoxImage)
                    #print((indexes[0], indexes[1]))
                    #print((self.charBoxIntervals[indexes[0]] * self.reSamplingFactor, self.charBoxIntervals[indexes[1]] * self.reSamplingFactor))
                    selectionBoxDraw.rectangle((self.charBoxIntervals[indexes[0]] * self.reSamplingFactor, 0, self.charBoxIntervals[indexes[1]] * self.reSamplingFactor, self.textImageHeight * self.reSamplingFactor), fill = (0, 160, 230, 100), width = 0)
                    self.textImage = Image.alpha_composite(self.textImage, selectionBoxImage)

                #Cursor Drawing
                if (self.cursorShow == True):
                    cursorImage = Image.new(mode = "RGBA", size = (imageLength, self.textImageHeight * self.reSamplingFactor), color = (255, 255, 255, 0))
                    cursorDraw = ImageDraw.Draw(cursorImage)
                    if (indexFlip == True): cursorDraw.rectangle((self.charBoxIntervals[indexes[0]] * self.reSamplingFactor, 0, self.charBoxIntervals[indexes[0]] * self.reSamplingFactor + 4, self.textImageHeight * self.reSamplingFactor), fill = (0, 0, 0, 255), width = 0)
                    else: cursorDraw.rectangle((self.charBoxIntervals[indexes[1]] * self.reSamplingFactor, 0, self.charBoxIntervals[indexes[1]] * self.reSamplingFactor + 4, self.textImageHeight * self.reSamplingFactor), fill = (0, 0, 0, 255), width = 0)
                    self.textImage = Image.alpha_composite(self.textImage, cursorImage)
            
            self.textImage = self.textImage.crop((self.displayBoxPosition * self.reSamplingFactor, 0, (self.displayBoxPosition + self.textImageWidth + 1) * self.reSamplingFactor, self.textImageHeight * self.reSamplingFactor))
            self.textImage = ImageTk.PhotoImage(self.textImage.resize((int(self.textImage.size[0] / self.reSamplingFactor), int(self.textImage.size[1] / self.reSamplingFactor)), resample=Image.LANCZOS))
            self.canvasLabels.append(canvas.create_image(self.data["COORD_X"] + self.gOffset, self.data["COORD_Y"] + self.gOffset, image = self.textImage, anchor = "nw"))
            

            if (self.data["DM"] == True):
                if (self.showData == True):
                    self.canvasLabels.append(canvas.create_text(self.data["COORD_X"], self.data["COORD_Y"] + self.data["HEIGHT"] + 5, 
                                                                text = "NAME: {:s}\nX: {:d}, Y: {:d}, LAYER: {:d}\nFA: {:s}\nMODE: {:s}\nTEXT: {:s}".format(self.data["NAME"], self.data["COORD_X"], self.data["COORD_Y"], self.data["LAYER"], str(self.data["FA"]), self.data["CM"], self.data["TEXT"]),
                                                                font = ("Times New Roman", 8), fill = "white", anchor = "nw"))
                self.canvasLabels.append(canvas.create_line(*[a for x in self.data["HB"] for a in x], width = 1, fill = "orange"))
            self.data["GUF"] = False
            return True
        return False

    def calculateCharBoxIntervals(self):
        self.charBoxIntervals = [0]
        for i in range (len(self.data["TEXT"])): self.charBoxIntervals.append((self.font_PIL.getlength(self.data["TEXT"][i]) / self.reSamplingFactor) + self.charBoxIntervals[i])

    def calculateDisplayBoxPosition(self, anchor):
        if (anchor == "L"):
            if (self.displayBoxPosition > self.charBoxIntervals[self.selectionBox[1]]): self.displayBoxPosition = self.charBoxIntervals[self.selectionBox[1]]
        elif (anchor == "R"):
            if (self.displayBoxPosition + self.textImageWidth < self.charBoxIntervals[self.selectionBox[1]]): self.displayBoxPosition = self.charBoxIntervals[self.selectionBox[1]] - self.textImageWidth


#OBJECT "TEXTINPUTBOX_TYPE_A" END -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#OBJECT "TEXTBOX_TYPE_A" --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
class textBox_typeA:
    def __init__(self, initData, CTGOFileData):
        self.data = dict(); self.data["NAME"] = "#UNDEFINED#"; 
        self.data["COORD_X"] = 100; self.data["COORD_Y"] = 100; self.data["WIDTH"] = 100; self.data["HEIGHT"] = 100; 
        self.data["HB"] = [[(0,0),(0,0),(0,0),(0,0)]];
        self.data["TEXT"] = ""; self.data["TEXTSIZE"] = 12; self.data["TEXTFILL"] = "white"
        self.data["LAYER"] = 0;
        self.data["CM"] = "DEFAULT";
        self.data["GUF"] = False; 
        self.data["DM"] = False;
        self.data["DREQ_R"] = []; self.data["DREQ_R_TIMER_TRIGGER"] = 1; self.data["DREQ_R_TIMER"] = 0; self.data["DREQ_L"] = []; self.data["UF"] = []; self.data["FAR"] = NONE; self.data["FARESULT"] = NONE
        self.graphics = {"DEFAULT": []}; 
        self.canvasLabels = []; 
        self.gIntrusions = []; 
        self.showData = False;
        self.lastUserInput = ""
        self.linkedData = 0

        for words in initData:
            if words[0] == "NAME":       self.data["NAME"]     = words[1]
            elif words[0] == "COORD_X":  self.data["COORD_X"]  = int(words[1])
            elif words[0] == "COORD_Y":  self.data["COORD_Y"]  = int(words[1])
            elif words[0] == "WIDTH":    self.data["WIDTH"]    = int(words[1])
            elif words[0] == "HEIGHT":   self.data["HEIGHT"]   = int(words[1])
            elif words[0] == "TEXT":     self.data["TEXT"]     = words[1]
            elif words[0] == "TEXTSIZE": self.data["TEXTSIZE"] = int(words[1])
            elif words[0] == "TEXTFILL": self.data["TEXTFILL"] = words[1]
            elif words[0] == "LAYER":    self.data["LAYER"]    = int(words[1])
            elif words[0] == "DREQ_R":   self.data["DREQ_R"].append(words[1])
            elif words[0] == "DREQ_L":   self.data["DREQ_L"].append(words[1])
            elif words[0] == "UF":       self.data["UF"].append(words[1:])
            elif words[0] == "MODE":
                for i in range (len(words[2:])):
                    gType = words[i+2].split(":")[0]; gContent = words[i+2].split(":")[1]
                    if (gType == "IMAGE"): self.graphics[words[1]].append(ImageTk.PhotoImage(Image.open(os.path.join(path_IMAGES + r"/{}".format(gContent))).resize((self.data["WIDTH"], self.data["HEIGHT"]), Image.LANCZOS)))
                    elif (gType == "CANVAS"): self.graphics[words[1]].append(gContent)
                    elif (gType == "CTGO"): self.graphics[words[1]].append(CTGO_Alpha.CTGO(gContent, CTGOFileData));
                    
        if (len(self.data["HB"]) == 0):
            self.data["HB_DEFAULT"] = [(self.data["COORD_X"], self.data["COORD_Y"]), 
                                       (self.data["COORD_X"] + self.data["WIDTH"], self.data["COORD_Y"]), 
                                       (self.data["COORD_X"] + self.data["WIDTH"], self.data["COORD_Y"] + self.data["HEIGHT"]),
                                       (self.data["COORD_X"], self.data["COORD_Y"] + self.data["HEIGHT"]),
                                       (self.data["COORD_X"], self.data["COORD_Y"])]
            self.data["HB"].append(self.data["HB_DEFAULT"])
        else: self.data["HB_DEFAULT"] = self.data["HB"][0]
        changeCM(self, self.data["CM"])

        for i in range (len(self.data["UF"])):
            uFunctionLines = ""
            for uFunctionLine in self.data["UF"][i]:
                if uFunctionLine == "TAB": uFunctionLines += "\t"
                elif uFunctionLine == "NEXTLINE": uFunctionLines += "\n"
                else: uFunctionLines += uFunctionLine
            self.data["UF"][i] = compile(uFunctionLines, '<string>', 'exec')

    def requestData(self, load = False):
        if (load == False):
            if (len(self.data["DREQ_R"]) > 0):
                if ((time.time_ns() - self.data["DREQ_R_TIMER"]) > (1e9 * self.data["DREQ_R_TIMER_TRIGGER"])): 
                    self.data["DREQ_R_TIMER"] = time.time_ns()
                    return self.data["DREQ_R"]
                else: return NONE
            else: return NONE
        else:
            if (len(self.data["DREQ_L"]) > 0): return self.data["DREQ_L"]
            else: return NONE

    def processData(self, data = NONE, userInput = NONE):
        results = []
        if (userInput is not NONE):
            if (userInput[0] == "M:RELEASED_R"):
                if (self.lastUserInput == "M:CLICKED_R" and (self.data["DM"] == True)): self.showData = not(self.showData); self.data["GUF"] = True;
            self.lastUserInput = userInput[0]; 

        if (data is not NONE):
            try: self.linkedData = data[self.data["DREQ_L"][0]]; self.data["GUF"] = True
            except: 
                try: self.linkedData = data[self.data["DREQ_R"][0]]; self.data["GUF"] = True
                except: self.linkedData = "#NO LINKAGE#"

            ldic = locals()
            for uFunctions in self.data["UF"]:
                try: exec(uFunctions, globals(), ldic); results.append(ldic['ufRESULT'])
                except Exception as e: print("ERROR OCCURED: " + str(e))

        return NONE

    def draw(self, canvas, bypassGUF = False):
        if (self.data["GUF"] or bypassGUF) == True:
            for i in range (len(self.canvasLabels)): canvas.delete(self.canvasLabels[i])
            self.canvasLabels.clear()
            for i in range (len(self.graphics[self.data["CM"]])):
                gType = type(self.graphics[self.data["CM"]][i])
                if gType is str: self.canvasLabels.append(drawCanvasObjects(canvas, self.graphics[self.data["CM"]][i]))
                elif gType is ImageTk.PhotoImage: self.canvasLabels.append(canvas.create_image(self.data["COORD_X"], self.data["COORD_Y"], image = self.graphics[self.data["CM"]][i], anchor = "nw"));
                elif gType is CTGO_Alpha.CTGO: self.canvasLabels.append(self.graphics[self.data["CM"]][i].draw(canvas, self.data["COORD_X"], self.data["COORD_Y"]))
            self.canvasLabels.append(canvas.create_text(self.data["COORD_X"] + self.data["WIDTH"] / 2, self.data["COORD_Y"] + self.data["HEIGHT"] / 2, text = self.data["TEXT"], font = ("Times New Roman", self.data["TEXTSIZE"], "bold"), fill = self.data["TEXTFILL"], anchor = "center"))
            if (self.data["DM"] == True):
                if (self.showData == True):
                    self.canvasLabels.append(canvas.create_text(self.data["COORD_X"], self.data["COORD_Y"] + self.data["HEIGHT"] + 5, 
                                                                text = "NAME: {:s}\nX: {:d}, Y: {:d}, LAYER: {:d}".format(self.data["NAME"], self.data["COORD_X"], self.data["COORD_Y"], self.data["LAYER"]),
                                                                font = ("Times New Roman", 8), fill = "white", anchor = "nw"))
                self.canvasLabels.append(canvas.create_line(*[a for x in self.data["HB"] for a in x], width = 1, fill = "orange"))
            self.data["GUF"] = False
            return True
        return False

#OBJECT "TEXTBOX_TYPE_A" END ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#OBJECT "LISTBOX_TYPE_A" --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
class listBox_typeA:
    def __init__(self, initData, CTGOFileData):
        self.data = dict(); self.data["NAME"] = "#UNDEFINED#"; 
        self.data["COORD_X"] = 100; self.data["COORD_Y"] = 100; self.data["WIDTH"] = 100; self.data["HEIGHT"] = 100; 
        self.data["HB"] = [[(0,0),(0,0),(0,0),(0,0)]];
        self.data["LAYER"] = 0;
        self.data["CM"] = "DEFAULT";
        self.data["GUF"] = False; 
        self.data["DM"] = False;
        self.data["DREQ_R"] = []; self.data["DREQ_R_TIMER_TRIGGER"] = 1; self.data["DREQ_R_TIMER"] = 0; self.data["DREQ_L"] = []; self.data["UF"] = []; self.data["FAR"] = NONE; self.data["FARESULT"] = NONE
        self.graphics = {"DEFAULT": [], "HOVERED": [], "ELEMENTBOX": []};
        self.canvasLabels = []; 
        self.gIntrusions = []; 
        self.showData = False;
        self.lastUserInput = ""

        #GUIO Unique Parameters
        self.data["n_COLUMNS"] = 3
        self.data["n_ROWS"] = 500
        self.data["e_WIDTH"] = 200
        self.data["e_HEIGHT"] = 50
        self.e_DATA = dict()
        self.e_gOffset = 5
        self.data["dw_POSITION"] = {"X": 0, "Y": 0}
        self.reSamplingFactor = 4
        self.elementBoxImage = None

        for words in initData:
            if words[0] == "NAME":       self.data["NAME"]     = words[1]
            elif words[0] == "COORD_X":  self.data["COORD_X"]  = int(words[1])
            elif words[0] == "COORD_Y":  self.data["COORD_Y"]  = int(words[1])
            elif words[0] == "WIDTH":    self.data["WIDTH"]    = int(words[1])
            elif words[0] == "HEIGHT":   self.data["HEIGHT"]   = int(words[1])
            elif words[0] == "LAYER":    self.data["LAYER"]    = int(words[1])
            elif words[0] == "DREQ_R":   self.data["DREQ_R"].append(words[1])
            elif words[0] == "DREQ_L":   self.data["DREQ_L"].append(words[1])
            elif words[0] == "UF":       self.data["UF"].append(words[1:])
            elif words[0] == "MODE": #Must be defiend lastest
                for i in range (len(words[2:])):
                    gType = words[i+2].split(":")[0]; gContent = words[i+2].split(":")[1]
                    if (words[1] == "ELEMENTBOX"):
                        if (gType == "IMAGE"): self.graphics[words[1]].append(ImageTk.PhotoImage(Image.open(os.path.join(path_IMAGES + r"/{}".format(gContent))).resize((self.data["e_WIDTH"], self.data["e_HEIGHT"]), Image.LANCZOS)))
                        elif (gType == "CTGO"): self.graphics[words[1]].append(CTGO_Alpha.CTGO(gContent + ",WIDTH=" + str(self.data["e_WIDTH"]) + ",HEIGHT=" + str(self.data["e_HEIGHT"]), CTGOFileData))
                    else:
                        if (gType == "IMAGE"): self.graphics[words[1]].append(ImageTk.PhotoImage(Image.open(os.path.join(path_IMAGES + r"/{}".format(gContent))).resize((self.data["WIDTH"], self.data["HEIGHT"]), Image.LANCZOS)))
                        elif (gType == "CANVAS"): self.graphics[words[1]].append(gContent)
                        elif (gType == "CTGO"): self.graphics[words[1]].append(CTGO_Alpha.CTGO(gContent, CTGOFileData));
            #Reading GUIO Unique Parameters Values
            elif words[0] == "N_COLUMNS": self.data["n_COLUMNS"] = int(words[1])
            elif words[0] == "N_ROWS":    self.data["n_ROWS"]    = int(words[1])
            elif words[0] == "E_WIDTH":   self.data["e_WIDTH"]   = int(words[1])
            elif words[0] == "E_HEIGHT":  self.data["e_HEIGHT"]  = int(words[1])
                    
        if (len(self.data["HB"]) == 0):
            self.data["HB_DEFAULT"] = [(self.data["COORD_X"], self.data["COORD_Y"]), 
                                       (self.data["COORD_X"] + self.data["WIDTH"], self.data["COORD_Y"]), 
                                       (self.data["COORD_X"] + self.data["WIDTH"], self.data["COORD_Y"] + self.data["HEIGHT"]),
                                       (self.data["COORD_X"], self.data["COORD_Y"] + self.data["HEIGHT"]),
                                       (self.data["COORD_X"], self.data["COORD_Y"])]
            self.data["HB"].append(self.data["HB_DEFAULT"])
        else: self.data["HB_DEFAULT"] = self.data["HB"][0]

        changeCM(self, self.data["CM"])

        #Compile Unique Functions
        for i in range (len(self.data["UF"])):
            uFunctionLines = ""
            for uFunctionLine in self.data["UF"][i]:
                if uFunctionLine == "TAB": uFunctionLines += "\t"
                elif uFunctionLine == "NEXTLINE": uFunctionLines += "\n"
                else: uFunctionLines += uFunctionLine
            self.data["UF"][i] = compile(uFunctionLines, '<string>', 'exec')

        #GUIO Unique Parameters
        self.dw_gOffset = 5
        self.data["dw_WIDTH"]  = self.data["WIDTH"] - 2 * self.dw_gOffset
        self.data["dw_HEIGHT"] = self.data["HEIGHT"] - 2 * self.dw_gOffset

        for i in range (self.data["n_COLUMNS"]):
            tempColumn = dict()
            for j in range (self.data["n_ROWS"]):

                tempElement = {"TEXT"            : "C{:d} R{:d}".format(i, j),
                               "TEXTFILL"        : (255, 255, 255, 255),
                               "TEXTSIZE"        : 12,
                               "TEXTSTYLE"       : 'bold',
                               "TEXTANCHOR"      : 'mm',
                               "TEXTSTROKEFILL"  : (0, 0, 0, 255),
                               "TEXTSTROKEWIDTH" : 0,
                               "BOXFILL"         : (50, 50, 50, 255),
                               "BOXOUTLINEFILL"  : (30, 30, 30, 255),
                               "BOXOUTLINEWIDTH" : 0,
                               "TEXTLINESPACING" : 3}
                tempColumn[j] = tempElement
            self.e_DATA[i] = tempColumn

        #DisplayBox Image Generation
        self.elementBoxImage = None
        self.elementBoxImageCropped = None
        self.updateElementBoxImage() 
        self.cropDisplayedImage()

    def requestData(self, load = False):
        if (load == False):
            if (len(self.data["DREQ_R"]) > 0):
                if ((time.time_ns() - self.data["DREQ_R_TIMER"]) > (1e9 * self.data["DREQ_R_TIMER_TRIGGER"])): 
                    self.data["DREQ_R_TIMER"] = time.time_ns()
                    return self.data["DREQ_R"]
                else: return NONE
            else: return NONE
        else:
            if (len(self.data["DREQ_L"]) > 0): return self.data["DREQ_L"]
            else: return NONE

    def processData(self, data = NONE, userInput = NONE):
        results = []
        if (userInput is not NONE):
            if (userInput[0] == "M:RELEASED"): changeCM(self, "DEFAULT")
            elif (userInput[0] == "M:HOVERED"): changeCM(self, "HOVERED")
            elif (userInput[0] == "M:WHEEL_UP"):
                self.data["dw_POSITION"]["Y"] -= self.data["e_HEIGHT"] / 2
                if self.data["dw_POSITION"]["Y"] < 0: self.data["dw_POSITION"]["Y"] = 0 #Parameter Boundary Control
                self.cropDisplayedImage()
                self.data["GUF"] = True
            elif (userInput[0] == "M:WHEEL_DOWN"):
                self.data["dw_POSITION"]["Y"] += self.data["e_HEIGHT"] / 2
                if self.data["dw_POSITION"]["Y"] + self.data["dw_HEIGHT"] > len(self.e_DATA[0]) * self.data["e_HEIGHT"]:  #Parameter Boundary Control
                    self.data["dw_POSITION"]["Y"] = len(self.e_DATA[0]) * self.data["e_HEIGHT"] - self.data["dw_HEIGHT"] #Parameter Boundary Control
                    if self.data["dw_POSITION"]["Y"] < 0: self.data["dw_POSITION"]["Y"] = 0 #Parameter Boundary Control
                self.cropDisplayedImage()
                self.data["GUF"] = True
            elif (userInput[0] == "M:WHEEL_LEFT"):
                self.data["dw_POSITION"]["X"] -= self.data["e_WIDTH"] / 2
                if self.data["dw_POSITION"]["X"] < 0: self.data["dw_POSITION"]["X"] = 0 #Parameter Boundary Control
                self.cropDisplayedImage()
                self.data["GUF"] = True
            elif (userInput[0] == "M:WHEEL_RIGHT"):
                self.data["dw_POSITION"]["X"] += self.data["e_WIDTH"] / 2
                if self.data["dw_POSITION"]["X"] + self.data["dw_WIDTH"] > len(self.e_DATA) * self.data["e_WIDTH"]:  #Parameter Boundary Control
                    self.data["dw_POSITION"]["X"] = len(self.e_DATA) * self.data["e_WIDTH"] - self.data["dw_WIDTH"] #Parameter Boundary Control
                    if self.data["dw_POSITION"]["X"] < 0: self.data["dw_POSITION"]["X"] = 0 #Parameter Boundary Control
                self.cropDisplayedImage()
                self.data["GUF"] = True
            elif (userInput[0] == "M:RELEASED_R"):
                if (self.lastUserInput == "M:CLICKED_R" and (self.data["DM"] == True)): self.showData = not(self.showData); self.data["GUF"] = True;
            self.lastUserInput = userInput[0];

        if (data is not NONE):
            ldic = locals()
            for uFunctions in self.data["UF"]:
                try: exec(uFunctions, globals(), ldic); results.append(ldic['ufRESULT'])
                except Exception as e: print("ERROR OCCURED: " + str(e))
            
        if (len(results) > 0): return results
        else: return NONE

    def draw(self, canvas, bypassGUF = False):
        if (self.data["GUF"] or bypassGUF) == True:
            for i in range (len(self.canvasLabels)): canvas.delete(self.canvasLabels[i])
            self.canvasLabels.clear()

            #Draw Display Window Graphics ("DEFAULT" or "HOVERED")
            for i in range (len(self.graphics[self.data["CM"]])):
                gType = type(self.graphics[self.data["CM"]][i])
                if gType is str: self.canvasLabels.append(drawCanvasObjects(canvas, self.graphics[self.data["CM"]][i]))
                elif gType is ImageTk.PhotoImage: self.canvasLabels.append(canvas.create_image(self.data["COORD_X"], self.data["COORD_Y"], image = self.graphics[self.data["CM"]][i], anchor = "nw"));
                elif gType is CTGO_Alpha.CTGO: self.canvasLabels.append(self.graphics[self.data["CM"]][i].draw(canvas, self.data["COORD_X"], self.data["COORD_Y"]))
            
            #Draw Element Box
            self.canvasLabels.append(canvas.create_image(self.data["COORD_X"] + self.dw_gOffset, self.data["COORD_Y"] + self.dw_gOffset, image = self.elementBoxImageCropped, anchor = "nw"))

            if (self.data["DM"] == True):
                if (self.showData == True):
                    self.canvasLabels.append(canvas.create_text(self.data["COORD_X"], self.data["COORD_Y"] + self.data["HEIGHT"] + 5, 
                                                                text = "NAME: {:s}\nX: {:d}, Y: {:d}, LAYER: {:d}".format(self.data["NAME"], self.data["COORD_X"], self.data["COORD_Y"], self.data["LAYER"]),
                                                                font = ("Times New Roman", 8), fill = "white", anchor = "nw"))
                self.canvasLabels.append(canvas.create_line(*[a for x in self.data["HB"] for a in x], width = 1, fill = "orange"))
            self.data["GUF"] = False
            return True
        return False

    def updateElementBoxImage(self):
        eBoxSize = (self.data["n_COLUMNS"] * self.data["e_WIDTH"] * self.reSamplingFactor, self.data["n_ROWS"] * self.data["e_HEIGHT"] * self.reSamplingFactor)
        self.elementBoxImage = Image.new(mode = "RGBA", size = eBoxSize, color = (0, 0, 0, 0))
        elementBoxImageDraw = ImageDraw.Draw(self.elementBoxImage)
        for i in range (self.data["n_COLUMNS"]):
            for j in range (self.data["n_ROWS"]):
                elementBoxImageDraw.rectangle((i * self.data["e_WIDTH"]  * self.reSamplingFactor + self.e_gOffset, j * self.data["e_HEIGHT"] * self.reSamplingFactor + self.e_gOffset, (i + 1) * self.data["e_WIDTH"]  * self.reSamplingFactor - self.e_gOffset, (j + 1) * self.data["e_HEIGHT"] * self.reSamplingFactor - self.e_gOffset),
                                                                                                                                        fill = self.e_DATA[i][j]["BOXFILL"], outline = self.e_DATA[i][j]["BOXOUTLINEFILL"], width = self.e_DATA[i][j]["BOXOUTLINEWIDTH"]) #Box Boundary Draw
                elementBoxImageDraw.text(((i + 0.5) * self.data["e_WIDTH"] * self.reSamplingFactor, (j + 0.5) * self.data["e_HEIGHT"] * self.reSamplingFactor),
                    text = self.e_DATA[i][j]["TEXT"],
                    fill = self.e_DATA[i][j]["TEXTFILL"],
                    font = ImageFont.truetype("times.ttf", self.e_DATA[i][j]["TEXTSIZE"] * self.reSamplingFactor),
                    anchor = self.e_DATA[i][j]["TEXTANCHOR"], 
                    spacing = self.e_DATA[i][j]["TEXTLINESPACING"], 
                    align = 'left',
                    stroke_fill = self.e_DATA[i][j]["TEXTSTROKEFILL"], stroke_width = self.e_DATA[i][j]["TEXTSTROKEWIDTH"])
                
        self.elementBoxImage = self.elementBoxImage.resize((int(eBoxSize[0] / self.reSamplingFactor), int(eBoxSize[1] / self.reSamplingFactor)), resample=Image.LANCZOS)

    def cropDisplayedImage(self):
        self.elementBoxImageCropped = ImageTk.PhotoImage(self.elementBoxImage.crop((self.data["dw_POSITION"]["X"], self.data["dw_POSITION"]["Y"], self.data["dw_POSITION"]["X"] + self.data["dw_WIDTH"], self.data["dw_POSITION"]["Y"] + self.data["dw_HEIGHT"])))

#OBJECT "LISTBOX_TYPE_A" END ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#OBJECT "PASSIVEGRAPHICS_TYPE_A" ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
class passiveGraphics_typeA:
    def __init__(self, initData, CTGOFileData):
        self.data = dict(); self.data["NAME"] = "#UNDEFINED#"; 
        self.data["COORD_X"] = 100; self.data["COORD_Y"] = 100; self.data["WIDTH"] = 100; self.data["HEIGHT"] = 100; 
        self.data["HB"] = [[(0,0),(0,0),(0,0),(0,0)]];
        self.data["LAYER"] = 0;
        self.data["CM"] = "DEFAULT";
        self.data["GUF"] = False; 
        self.data["DM"] = False; self.data["FAR"] = NONE; self.data["FARESULT"] = NONE
        self.graphics = {"DEFAULT": []}; 
        self.canvasLabels = []; 
        self.gIntrusions = []; 
        self.showData = False;
        self.lastUserInput = ""

        for words in initData:
            if words[0] == "NAME":      self.data["NAME"]    = words[1]
            elif words[0] == "COORD_X": self.data["COORD_X"] = int(words[1])
            elif words[0] == "COORD_Y": self.data["COORD_Y"] = int(words[1])
            elif words[0] == "WIDTH":   self.data["WIDTH"]   = int(words[1])
            elif words[0] == "HEIGHT":  self.data["HEIGHT"]  = int(words[1])
            elif words[0] == "LAYER":   self.data["LAYER"]   = int(words[1])
            elif words[0] == "MODE":
                for i in range (len(words[2:])):
                    gType = words[i+2].split(":")[0]; gContent = words[i+2].split(":")[1]
                    if (gType == "IMAGE"): self.graphics[words[1]].append(ImageTk.PhotoImage(Image.open(os.path.join(path_IMAGES + r"/{}".format(gContent))).resize((self.data["WIDTH"], self.data["HEIGHT"]), Image.LANCZOS)))
                    elif (gType == "CANVAS"): self.graphics[words[1]].append(gContent)
                    elif (gType == "CTGO"): self.graphics[words[1]].append(CTGO_Alpha.CTGO(gContent, CTGOFileData));
                    
        if (len(self.data["HB"]) == 0):
            self.data["HB_DEFAULT"] = [(self.data["COORD_X"], self.data["COORD_Y"]), 
                                       (self.data["COORD_X"] + self.data["WIDTH"], self.data["COORD_Y"]), 
                                       (self.data["COORD_X"] + self.data["WIDTH"], self.data["COORD_Y"] + self.data["HEIGHT"]),
                                       (self.data["COORD_X"], self.data["COORD_Y"] + self.data["HEIGHT"]),
                                       (self.data["COORD_X"], self.data["COORD_Y"])]
            self.data["HB"].append(self.data["HB_DEFAULT"])
        else: self.data["HB_DEFAULT"] = self.data["HB"][0]
        changeCM(self, self.data["CM"])

    def requestData(self, load = False): return NONE

    def processData(self, data = NONE, userInput = NONE):
        if (userInput is not NONE):
            if (userInput[0] == "M:RELEASED_R"):
                if (self.lastUserInput == "M:CLICKED_R" and (self.data["DM"] == True)): self.showData = not(self.showData); self.data["GUF"] = True;
            self.lastUserInput = userInput[0];
        return NONE

    def draw(self, canvas, bypassGUF = False):
        if (self.data["GUF"] or bypassGUF) == True:
            for i in range (len(self.canvasLabels)): canvas.delete(self.canvasLabels[i])
            self.canvasLabels.clear()
            for i in range (len(self.graphics[self.data["CM"]])):
                gType = type(self.graphics[self.data["CM"]][i])
                if gType is str: self.canvasLabels.append(drawCanvasObjects(canvas, self.graphics[self.data["CM"]][i]))
                elif gType is ImageTk.PhotoImage: self.canvasLabels.append(canvas.create_image(self.data["COORD_X"], self.data["COORD_Y"], image = self.graphics[self.data["CM"]][i], anchor = "nw"));
                elif gType is CTGO_Alpha.CTGO: self.canvasLabels.append(self.graphics[self.data["CM"]][i].draw(canvas, self.data["COORD_X"], self.data["COORD_Y"]))
            if (self.data["DM"] == True):
                if (self.showData == True):
                    self.canvasLabels.append(canvas.create_text(self.data["COORD_X"], self.data["COORD_Y"] + self.data["HEIGHT"] + 5, 
                                                                text = "NAME: {:s}\nX: {:d}, Y: {:d}, LAYER: {:d}".format(self.data["NAME"], self.data["COORD_X"], self.data["COORD_Y"], self.data["LAYER"]),
                                                                font = ("Times New Roman", 8), fill = "white", anchor = "nw"))
                self.canvasLabels.append(canvas.create_line(*[a for x in self.data["HB"] for a in x], width = 1, fill = "orange"))
            self.data["GUF"] = False
            return True
        return False
    
class binaryIndicator_typeA:
    def __init__(self, initData, CTGOFileData):
        self.data = dict(); self.data["NAME"] = "#UNDEFINED#"; 
        self.data["COORD_X"] = 100; self.data["COORD_Y"] = 100; self.data["WIDTH"] = 100; self.data["HEIGHT"] = 100; 
        self.data["HB"] = [[(0,0),(0,0),(0,0),(0,0)]];
        self.data["LAYER"] = 0;
        self.data["CM"] = "STATE1";
        self.data["GUF"] = False; 
        self.data["DM"] = False;
        self.graphics = {"STATE1": [], "STATE2": []}; 
        self.data["DREQ_R"] = []; self.data["DREQ_L"] = []; self.data["UF"] = []; self.data["FAR"] = NONE; self.data["FARESULT"] = NONE
        self.canvasLabels = []; 
        self.gIntrusions = []; 
        self.showData = False;
        self.lastUserInput = ""
        self.linkedData = 0

        for words in initData:
            if words[0] == "NAME":      self.data["NAME"]    = words[1]
            elif words[0] == "COORD_X": self.data["COORD_X"] = int(words[1])
            elif words[0] == "COORD_Y": self.data["COORD_Y"] = int(words[1])
            elif words[0] == "WIDTH":   self.data["WIDTH"]   = int(words[1])
            elif words[0] == "HEIGHT":  self.data["HEIGHT"]  = int(words[1])
            elif words[0] == "LAYER":   self.data["LAYER"]   = int(words[1])
            elif words[0] == "DREQ_R":   self.data["DREQ_R"].append(words[1])
            elif words[0] == "DREQ_L":   self.data["DREQ_L"].append(words[1])
            elif words[0] == "UF":  self.data["UF"].append(words[1])
            elif words[0] == "MODE":
                for i in range (len(words[2:])):
                    gType = words[i+2].split(":")[0]; gContent = words[i+2].split(":")[1]
                    if (gType == "IMAGE"): self.graphics[words[1]].append(ImageTk.PhotoImage(Image.open(os.path.join(path_IMAGES + r"/{}".format(gContent))).resize((self.data["WIDTH"], self.data["HEIGHT"]), Image.LANCZOS)))
                    elif (gType == "CANVAS"): self.graphics[words[1]].append(gContent)
                    elif (gType == "CTGO"): self.graphics[words[1]].append(CTGO_Alpha.CTGO(gContent, CTGOFileData));
                    
        if (len(self.data["HB"]) == 0):
            self.data["HB_DEFAULT"] = [(self.data["COORD_X"], self.data["COORD_Y"]), 
                                       (self.data["COORD_X"] + self.data["WIDTH"], self.data["COORD_Y"]), 
                                       (self.data["COORD_X"] + self.data["WIDTH"], self.data["COORD_Y"] + self.data["HEIGHT"]),
                                       (self.data["COORD_X"], self.data["COORD_Y"] + self.data["HEIGHT"]),
                                       (self.data["COORD_X"], self.data["COORD_Y"])]
            self.data["HB"].append(self.data["HB_DEFAULT"])
        else: self.data["HB_DEFAULT"] = self.data["HB"][0]
        changeCM(self, self.data["CM"])

    def requestData(self, load = False):
        if (load == False):
            if (len(self.data["DREQ_R"]) > 0): return self.data["DREQ_R"]
            else: return NONE
        else:
            if (len(self.data["DREQ_L"]) > 0): return self.data["DREQ_L"]
            else: return NONE

    def processData(self, data = NONE, userInput = NONE):
        results = []
        if (userInput is not NONE):
            if (userInput[0] == "M:RELEASED_R"):
                if (self.lastUserInput == "M:CLICKED_R" and (self.data["DM"] == True)): self.showData = not(self.showData); self.data["GUF"] = True;
            self.lastUserInput = userInput[0]; 

        if (data is not NONE):
            try: self.linkedData = data[self.data["DREQ_L"][0]]; self.data["GUF"] = True
            except: 
                try: self.linkedData = data[self.data["DREQ_R"][0]]; self.data["GUF"] = True
                except: self.linkedData = "#NO LINKAGE#"

            ldic = locals()
            for uFunctions in self.data["UF"]: 
                try: exec(uFunctions, globals(), ldic); results.append(ldic['ufRESULT'])
                except Exception as e: print("ERROR OCCURED: " + str(e))
        return NONE

    def draw(self, canvas, bypassGUF = False):
        if (self.data["GUF"] or bypassGUF) == True:
            for i in range (len(self.canvasLabels)): canvas.delete(self.canvasLabels[i])
            self.canvasLabels.clear()
            for i in range (len(self.graphics[self.data["CM"]])):
                gType = type(self.graphics[self.data["CM"]][i])
                if gType is str: self.canvasLabels.append(drawCanvasObjects(canvas, self.graphics[self.data["CM"]][i]))
                elif gType is ImageTk.PhotoImage: self.canvasLabels.append(canvas.create_image(self.data["COORD_X"], self.data["COORD_Y"], image = self.graphics[self.data["CM"]][i], anchor = "nw"));
                elif gType is CTGO_Alpha.CTGO: self.canvasLabels.append(self.graphics[self.data["CM"]][i].draw(canvas, self.data["COORD_X"], self.data["COORD_Y"]))
            if (self.data["DM"] == True):
                if (self.showData == True):
                    self.canvasLabels.append(canvas.create_text(self.data["COORD_X"], self.data["COORD_Y"] + self.data["HEIGHT"] + 5, 
                                                                text = "NAME: {:s}\nX: {:d}, Y: {:d}, LAYER: {:d}".format(self.data["NAME"], self.data["COORD_X"], self.data["COORD_Y"], self.data["LAYER"]),
                                                                font = ("Times New Roman", 8), fill = "white", anchor = "nw"))
                self.canvasLabels.append(canvas.create_line(*[a for x in self.data["HB"] for a in x], width = 1, fill = "orange"))
            self.data["GUF"] = False
            return True
        return False

    def checkStatus(self, flag):
        if (flag == True): changeCM(self, "STATE1")
        elif (flag == False): changeCM(self, "STATE2")
#OBJECT "PASSIVEGRAPHICS_TYPE_A" END --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------



#GUI OBJECTS END ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#AUXILLARY FUNCTIONS --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def drawCanvasObjects(canvas, word):
    props = word.split(",")
    if props[0] == "LINE": print(props)
    #Expected - [0]: "RECT", [1]: x1, [2]: y1, [3]: x2, [4]: y2, [5]: fillColor, [6]: outlineWidth, [7]: outlineColor
    elif props[0] == "RECT": return canvas.create_rectangle(int(props[1]), int(props[2]), int(props[3]), int(props[4]), fill = props[5], width = props[6], outline = props[7])
    #Expected - [0]: "OVAL", [1]: x1, [2]: y1, [3]: x2, [4]: y2, [5]: fillColor, [6]: outlineWidth, [7]: outlineColor
    elif props[0] == "OVAL": return canvas.create_oval(int(props[1]), int(props[2]), int(props[3]), int(props[4]), fill = props[5], width = props[6], outline = props[7])
    #Expected - [0]: "ARC", [1]: x1, [2]: y1, [3]: x2, [4]: y2, [5]: fillColor, [6]: outlineWidth, [7]: outlineColor, [8]: start, [9]: extent
    elif props[0] == "ARC": return canvas.create_arc(int(props[1]), int(props[2]), int(props[3]), int(props[4]), fill = props[5], width = props[6], outline = props[7], start = int(props[8]), extent = int(props[9]))
    #Expected - [0]: "ARC_ARK", [1]: x1, [2]: y1, [3]: x2, [4]: y2, [5]: outlineWidth, [6]: outlineColor, [7]: start, [8]: extent
    elif props[0] == "ARC_ARK": return canvas.create_arc(int(props[1]), int(props[2]), int(props[3]), int(props[4]), width = props[5], outline = props[6], start = int(props[7]), extent = int(props[8]), style = tkinter.ARC)
    #Expected - [0]: "ARC_CHORD", [1]: x1, [2]: y1, [3]: x2, [4]: y2, [5]: outlineWidth, [6]: outlineColor, [7]: start, [8]: extent
    elif props[0] == "ARC_CHORD": return canvas.create_arc(int(props[1]), int(props[2]), int(props[3]), int(props[4]), fill = props[5], width = props[6], outline = props[7], start = int(props[8]), extent = int(props[9]), style = tkinter.CHORD)
    elif props[0] == "POLY": print(props)
    #Expected - [0]: "TEXT", [1]: x, [2]: y, [3]: text (singleWord), [4]: fontSize, [5]: textColor, [6]: anchor
    elif props[0] == "TEXT": return canvas.create_text(int(props[1]), int(props[2]), text = props[3], font = ("Times New Roman", int(props[4]), "bold"), fill = props[5], anchor = props[6])

#Check if the point is inside the rectangle
def isPointInsideRect(point, rect):
    if (point[0] >= rect[0]) and (point[0] <= rect[1]) and (point[1] >= rect[2]) and (point[1] <= rect[3]): return True
    else: return False

#Convert text into data format
def textToList(texts):
    #Text Editing, Concatenate if "texts" is in form of a list of strings
    if type(texts) is list:
        string = texts[0]; 
        for i in range (len(texts) - 1): string += texts[i + 1]
    elif type(texts) is str:
        string = texts

    elements = []; counter = 0
    while counter < (len(string)):
        if  string[counter:counter+2] == "I:":
            dataStart = counter + 2
            while (1):
                if ((counter == len(string)) or (string[counter] == "]") or (string[counter] == ",")): break;
                else: counter += 1
            elements.append(int(string[dataStart:counter]))
        elif  string[counter:counter+2] == "F:":
            dataStart = counter + 2
            while (1):
                if ((counter == len(string)) or (string[counter] == "]") or (string[counter] == ",")): break;
                else: counter += 1
            elements.append(float(string[dataStart:counter]))
        elif  string[counter:counter+2] == "S:":
            dataStart = counter + 2
            while (1):
                if ((counter == len(string)) or (string[counter] == "]") or (string[counter] == ",")): break;
                else: counter += 1
            elements.append(string[dataStart:counter])
        elif  string[counter:counter+2] == "B:":
            dataStart = counter + 2
            while (1):
                if ((counter == len(string)) or (string[counter] == "]") or (string[counter] == ",")): break;
                else: counter += 1
            elements.append(stringToBool(string[dataStart:counter]))
        elif  string[counter:counter+3] == "L:[":
            dataStart = counter + 2
            while (1):
                if (string[counter] == "]"): break;
                else: counter += 1
            elements.append(textToList(string[dataStart:counter+1]))
        counter += 1
    
    if (len(elements) == 0): return NONE
    elif (len(elements) == 1): return elements[0]
    else: return elements
    
def stringToBool(string):
    try:
        if (float(string) > 0): return True
        else: return False
    except:
        if (string == "False") or (string == "FALSE"): return False
        else: return True

def changeCM(self, modeTo):
    self.data["CM"] = modeTo;
    self.data["GUF"] = True;
    if (type(self.graphics[modeTo][0]) == CTGO_Alpha.CTGO):
        if ((len(self.graphics[modeTo][0].HB)) > 2): 
            ctgoHB = self.graphics[modeTo][0].HB; newHB = []
            for relativeCoord_point in ctgoHB: newHB.append((relativeCoord_point[0] + self.data["COORD_X"], relativeCoord_point[1] + self.data["COORD_Y"]))
            newHB.append(newHB[0])
            self.data["HB"] = [newHB]
        else: self.data["HB"] = [self.data["HB_DEFAULT"]]
   

#AUXILLARY FUNCTIONS END ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------