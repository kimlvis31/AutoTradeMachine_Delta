#Custom-designed Tkinter Graphics Object

import os
import tkinter
from PIL import Image, ImageTk, ImageDraw
from pickle import NONE

RESAMPLINGFACTOR = 4

class CTGO:
    def __init__(self, gContent, fileData):
        self.definition = dict()
        gContent = gContent.split(",")
        for content in gContent: content = content.split("="); self.definition[content[0].strip()] = content[1].strip()
        self.definition["WIDTH"] = int(self.definition["WIDTH"]); self.definition["HEIGHT"] = int(self.definition["HEIGHT"])
        
        self.image = Image.new(mode = "RGBA", size = (self.definition["WIDTH"] * RESAMPLINGFACTOR, self.definition["HEIGHT"] * RESAMPLINGFACTOR), color = (0, 0, 0, 0))
        draw = ImageDraw.Draw(self.image)
        
        self.HB = []

        for data in fileData:
            if (data[0] == self.definition["NAME"]):
                paramIndex = 0
                for drawContent in data[1:]:
                    params = dict(); drawContent = drawContent.split(",");
                    for param in drawContent: param = param.split("="); params[param[0].strip()] = param[1].strip();
                    #HitBox -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
                    if (params["TYPE"] == "HB"):
                        try:
                            arr = textInConfinementToArray(params["POINTS"], "(", ")");
                            for line in arr: self.HB.append((int(line.split(":")[0]) / 100 * self.definition["WIDTH"],int(line.split(":")[1]) / 100 * self.definition["HEIGHT"]))
                        except: pass;
                    #HitBox END -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

                    #Drawing Lines ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
                    if (params["TYPE"] == "LINE"): #Drawing Lines
                        arr = textInConfinementToArray(params["POINTS"], "(", ")"); points = []
                        for line in arr: points.append((int(line.split(":")[0]) / 100 * RESAMPLINGFACTOR * self.definition["WIDTH"],int(line.split(":")[1]) / 100 * RESAMPLINGFACTOR * self.definition["HEIGHT"]))
                        draw.line(tuple(points), fill = (int(params["FILL_R"]), int(params["FILL_G"]), int(params["FILL_B"]), int(params["FILL_A"])), width = int(params["WIDTH"]))
                    #Drawing Lines END ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
                    
                    #Drawing A Rectangle ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
                    elif (params["TYPE"] == "RECTANGLE"): #Drawing A Rectangle
                        drawParamMarkers = []
                        for i in range (9): drawParamMarkers.append(self.definition["PARAM" + str(paramIndex)]); paramIndex += 1
                        draw.rectangle([(int(params["X0"]) / 100 * RESAMPLINGFACTOR * self.definition["WIDTH"], int(params["Y0"]) / 100 * RESAMPLINGFACTOR * self.definition["HEIGHT"]), 
                                        (int(params["X1"]) / 100 * RESAMPLINGFACTOR * self.definition["WIDTH"], int(params["Y1"]) / 100 * RESAMPLINGFACTOR * self.definition["HEIGHT"])], 
                                  fill = (int(drawParamMarkers[0]), int(drawParamMarkers[1]), int(drawParamMarkers[2]), int(drawParamMarkers[3])), 
                                  outline = (int(drawParamMarkers[4]), int(drawParamMarkers[5]), int(drawParamMarkers[6]), int(drawParamMarkers[7])), 
                                  width = int(drawParamMarkers[8]) * RESAMPLINGFACTOR)
                    #Drawing A Rectangle END ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
                    
                    #Drawing A Rounded Rectangle --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
                    elif (params["TYPE"] == "ROUNDED_RECTANGLE"): #Drawing A Rectangle
                        drawParamMarkers = []
                        for i in range (11): drawParamMarkers.append(self.definition["PARAM" + str(paramIndex)]); paramIndex += 1
                        corners = []
                        for i in range (4):
                            if drawParamMarkers[10][i] == "T": corners.append(True)
                            elif drawParamMarkers[10][i] == "F": corners.append(False)
                        x0 = int(params["X0"]) / 100 * self.definition["WIDTH"] * RESAMPLINGFACTOR; y0 = int(params["Y0"]) / 100 * self.definition["HEIGHT"] * RESAMPLINGFACTOR
                        x1 = int(params["X1"]) / 100 * self.definition["WIDTH"] * RESAMPLINGFACTOR; y1 = int(params["Y1"]) / 100 * self.definition["HEIGHT"] * RESAMPLINGFACTOR
                        draw.rounded_rectangle((x0, y0, x1, y1), 
                                  fill = (int(drawParamMarkers[0]), int(drawParamMarkers[1]), int(drawParamMarkers[2]), int(drawParamMarkers[3])), 
                                  outline = (int(drawParamMarkers[4]), int(drawParamMarkers[5]), int(drawParamMarkers[6]), int(drawParamMarkers[7])), 
                                  width = int(drawParamMarkers[8]) * RESAMPLINGFACTOR,
                                  corners = tuple(corners),
                                  radius = min([(min([x1 - x0, y1 - y0]) / 2 - 1), (int(drawParamMarkers[9]) * RESAMPLINGFACTOR)]))
                    #Drawing A Rounded Rectangle END ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
                break;
        self.image = ImageTk.PhotoImage(self.image.resize((self.definition["WIDTH"], self.definition["HEIGHT"]), resample=Image.LANCZOS))

    def draw(self, canvas, xCoord, yCoord):
        return canvas.create_image(xCoord, yCoord, image = self.image, anchor = "nw")
    
#AUXILLARY FUNCTIONS --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
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
                if counter2 == 0: break;
                else: counter += 1
            if (singular): elements.append(string[dataStartIndex:counter])
            else: elements.append(textInConfinementToArray(string[dataStartIndex:counter], confinementBeginner, confinementEnder))
            singular = True
        counter += 1
    return elements

#AUXILLARY FUNCTIONS END ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------