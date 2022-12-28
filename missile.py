'''
Splitting off Missle segment into it's own file for sanity's sake.
12/28/2022
'''
def basicInfo(MissileFile, MisslieDict):
    missle dict
    if WorkingFileLines[lineNumber].__contains__("Designation"):
        data = WorkingFileLines[lineNumber].split(">")[1]
        data = data.split("<")[0]
        MissileDict["Designation"] = data
    
    if WorkingFileLines[lineNumber].__contains__("Nickname"):
        data = WorkingFileLines[lineNumber].split(">")[1]
        data = data.split("<")[0]
        MissileDict["Nickname"] = data
    
    if WorkingFileLines[lineNumber].__contains__("Cost"):
        data = WorkingFileLines[lineNumber].split(">")[1]
        data = data.split("<")[0]
        MissileDict["Cost"] = data

    if WorkingFileLines[lineNumber].__contains__("BodyKey"):
        data = WorkingFileLines[lineNumber].split(">")[1]
        data = data.split("<")[0]
        MissileDict["Body"] = data
    return MissileDict


def SeekerHead():
    if WorkingFileLines[lineNumber].__contains__("<MissileSocket>"):
        while not WorkingFileLines[lineNumber].__contains__("</MissileSocket>"):
            if SettingsDict["DebugMode"] == "yes":
                print("Missile Socket Loop")
            SocketDict = {}
            if WorkingFileLines[lineNumber].__contains__("Size"):
                data = WorkingFileLines[lineNumber].split(">")[1]
                data = data.split("<")[0]
                SizeData = data

            if WorkingFileLines[lineNumber].__contains__("InstalledComponent"):
                
                if WorkingFileLines[lineNumber].__contains__("SeekerSettings"):

                    if WorkingFileLines[lineNumber].__contains__("Active"):
                        ActiveSeekerDict = {"Type":"Active Seeker"}
                    elif WorkingFileLines[lineNumber].__contains__("Passive"):
                        ActiveSeekerDict = {"Type":"Passive Seeker"}
                    elif WorkingFileLines[lineNumber].__contains__("Command"):
                        ActiveSeekerDict = {"Type":"Command Control"}
                    else:
                        ActiveSeekerDict = {"Type":"ERROR"}
                    ActiveSeekerDict["Component Size"] = SizeData
                    while not WorkingFileLines[lineNumber].__contains__("</InstalledComponent>"):
                        if SettingsDict["DebugMode"] == "yes":
                            print("Seeker Loop")
                            print(WorkingFileLines[lineNumber])
                        
                        if WorkingFileLines[lineNumber].__contains__("ComponentKey"):
                            data = WorkingFileLines[lineNumber].split(">")[1]
                            data = data.split("<")[0]
                            ActiveSeekerDict["Component Name"] = data

                        if WorkingFileLines[lineNumber].__contains__("Mode"):
                            data = WorkingFileLines[lineNumber].split(">")[1]
                            data = data.split("<")[0]
                            ActiveSeekerDict["Mode"] = data                            
                        
                        if WorkingFileLines[lineNumber].__contains__("RejectUnvalidated"):
                            data = WorkingFileLines[lineNumber].split(">")[1]
                            data = data.split("<")[0]
                            ActiveSeekerDict["Reject Unvalidated"] = data

                        if WorkingFileLines[lineNumber].__contains__("DetectPDTargets"):
                            data = WorkingFileLines[lineNumber].split(">")[1]
                            data = data.split("<")[0]
                            ActiveSeekerDict["Detect Point Defence Targets"] = data                            
                        lineNumber = lineNumber + 1
                    
                        SocketDict["Seeker"] = ActiveSeekerDict

def GuidenceSystem():         
    elif WorkingFileLines[lineNumber].__contains__("GuidanceSettings"):
    if WorkingFileLines[lineNumber].__contains__("Direct"):
        GuidenceDict = {"Type":"Direct"}
    elif WorkingFileLines[lineNumber].__contains__("Cruise"):
        GuidenceDict = {"Type":"Cruise"}
    else:
        GuidenceDict = {"Type":"ERROR"}
    GuidenceDict["Component Size"] = SizeData

    while not WorkingFileLines[lineNumber].__contains__("</InstalledComponent>"):
        if SettingsDict["DebugMode"] == "yes":
            print("Direct Guidence Loop")
        
        if WorkingFileLines[lineNumber].__contains__("ComponentKey"):
            data = WorkingFileLines[lineNumber].split(">")[1]
            data = data.split("<")[0]
            GuidenceDict["Component Name"] = data

        if WorkingFileLines[lineNumber].__contains__("Role"):
            data = WorkingFileLines[lineNumber].split(">")[1]
            data = data.split("<")[0]
            GuidenceDict["Role"] = data                            
        
        if WorkingFileLines[lineNumber].__contains__("HotLaunch"):
            data = WorkingFileLines[lineNumber].split(">")[1]
            data = data.split("<")[0]
            GuidenceDict["Hot Launch"] = data

        if WorkingFileLines[lineNumber].__contains__("SelfDestructOnLost"):
            data = WorkingFileLines[lineNumber].split(">")[1]
            data = data.split("<")[0]
            GuidenceDict["Self Destruct On Lost"] = data    
            
        if WorkingFileLines[lineNumber].__contains__("Maneuvers"):
            data = WorkingFileLines[lineNumber].split(">")[1]
            data = data.split("<")[0]
            GuidenceDict["Termnal Maneuvers"] = data                                    
        lineNumber = lineNumber + 1
    SocketDict["Guidence"] = GuidenceDict

def EngineSettings():
    elif WorkingFileLines[lineNumber].__contains__("MissileEngineSettings"):
        EngineDict ={"Component Size":SizeData}
        if SettingsDict["DebugMode"] == "yes":
            print("Found an Engine")
        while not WorkingFileLines[lineNumber].__contains__("</InstalledComponent>"):
            if SettingsDict["DebugMode"] == "yes":
                print("Engine Loop")
            if WorkingFileLines[lineNumber].__contains__("<A>"):
                data = WorkingFileLines[lineNumber].split(">")[1]
                data = data.split("<")[0]
                EngineDict["Range"]= data  
            if WorkingFileLines[lineNumber].__contains__("<B>"):
                data = WorkingFileLines[lineNumber].split(">")[1]
                data = data.split("<")[0]
                EngineDict["Speed"] = data  
            if WorkingFileLines[lineNumber].__contains__("<C>"):
                data = WorkingFileLines[lineNumber].split(">")[1]
                data = data.split("<")[0]
                EngineDict["Maneuverability"] = data
            lineNumber = lineNumber + 1
        SocketDict["Engine"] = EngineDict

def MissileCatchall():
    AuxComponentDict ={"Component Size":SizeData}
    if SettingsDict["DebugMode"] == "yes":
        print("Found Something Else")
    while not WorkingFileLines[lineNumber].__contains__("</InstalledComponent>"):

        if WorkingFileLines[lineNumber].__contains__("ComponentKey"):
            data = WorkingFileLines[lineNumber].split(">")[1]
            data = data.split("<")[0]
            name = data 
        lineNumber = lineNumber + 1
    SocketDict[name] = AuxComponentDict
    lineNumber = lineNumber + 1
    if len(SocketDict) > 0:
    MissileDict["Sockets"].append(SocketDict)                    
