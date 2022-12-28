'''
Nebulous Fleet Command Battle Report Analyzer
Author: Grathew
12/28/2022
Version 0.0.1

This program will read in the battle reports from Nebulous Fleet Command 
and turn them into hopefuly useful data

Grathew does admit he doesn't understand statistics so who knows what this
satistical analysis will look like.
'''

import json
import os
from pprint import pprint

SettingsDict = {}

try:
    SettingsFile = open("settings.txt","r")
    SettingsDict = json.load(SettingsFile)
    SettingsFile.close()
except:
    print("Settings file isn't found.")
    print("Creating settings file.")
    SettingsFile = open("settings.txt","w")
    
    print("Please follow prompts.")
    SettingsDict["NebulousPath"] = input("Please enter the path to Nebulous Fleet Command: ")
    SettingsDict["OutputPath"] = input("Please enter the path to the folder you want this program to save things: ")
    SettingsDict["PlayerName"] = input("Please enter your player name: ").lower()
    print("Answer the following quesiton with yes or no.")
    SettingsDict["MatchJson"] = input("Would you like to save your logs as json: ").lower()
    print("Answer the following quesiton with yes or no.")
    SettingsDict["FleetJson"] = input("Would you like to save your fleet sats as json: ").lower()
    print("Answer the following quesiton with yes or no.")
    SettingsDict["StarterFleets"] = input("Would you like to save the Starter Fleets stats as json: ").lower()
    print("Answer the following quesiton with yes or no.")
    SettingsDict["ShipJson"] = input("Would you like to save your ship stats as json: ").lower()
    print("Answer the following quesiton with yes or no.")
    SettingsDict["MissileJson"] = input("Would you like to save your missile stats as json: ").lower()
    print("Answer the following quesiton with yes or no.")
    SettingsDict["PlayerJson"] = input("Would you like to save your global stats as json: ").lower()
    print("Answer the following quesiton with yes or no.")
    SettingsDict["DebugMode"] = input("Would you like to run the app in debug mode: ").lower()
    
    json.dump(SettingsDict,SettingsFile)
    SettingsFile.close()

if SettingsDict["DebugMode"] == "yes":
    print("SettingsDict")
    pprint(SettingsDict)
    print("\n")

if os.path.exists(SettingsDict["OutputPath"]):
    print("\n")
    print("Output location found. Continuing...")
    print("\n")
else:
    os.mkdir(SettingsDict["OutputPath"]) 

SavesPath = SettingsDict["NebulousPath"] + "\\saves"
if os.path.exists(SavesPath):
    if SettingsDict["DebugMode"] == "yes":
        print("debugging file search")
        print("Path we are looking from: " + SavesPath)
        print("\n")
        print("walking though saves looking for files")
        print("\n")
        for(root, dirs, file) in os.walk(SavesPath):
            for f in file:
                if '.fleet' in f:
                    print("Fleet found " + f)
                if '.missile' in f:
                    print("Missile found " + f)
                if '.ship' in f:
                    print("Ship found " + f)
                if '.xml' in f:
                    print("Report found " + f)
        print("\n")
        print("Check and see if it has found everything you'd expect. If not yell at Grathew. He's on the Nebulous Discord or the Git.")
        print("\n")
else:
    print("Could not find required file tree. Please check your settings file and varify your Nebulous location.")

#open and read Fleets
if SettingsDict["FleetJson"] == "yes":
    FleetPath = SavesPath + "\\Fleets"
    if os.path.exists(FleetPath):
        FleetFolder = os.walk(FleetPath)
        FleetFiles = []
        for root, dirs, files in FleetFolder:
            for name in files:
                if name.endswith('.fleet'):
                    FleetFiles.append(name)
        if SettingsDict["DebugMode"] == "yes":
            print("Fleets")
            pprint(FleetFiles)
            print("\n")
        
    else:
        print("Could not find the Fleets folder. Please check your Nebulous\\Saves for the Fleets folder.") 
    
#open and read Missle Templates
if SettingsDict["MissileJson"] == "yes":
    MissilePath = SavesPath + "\\MissileTemplates"
    if os.path.exists(MissilePath):
        MissileFolder = os.listdir(MissilePath)
        MissileFiles = []
        for f in range(len(MissileFolder)):
            if MissileFolder[f].endswith('.missile'):
                MissileFiles.append(MissileFolder[f])
        if SettingsDict["DebugMode"] == "yes":
            print("Missiles")
            pprint(MissileFiles)
            print("\n")
        for missile in MissileFiles:
            MissileDict = {"Sockets":[]}
            WorkingFile = open(MissilePath + "\\" + missile, "r")
            if not os.path.exists(SettingsDict["OutputPath"] + "\\Missiles"):
                os.mkdir(SettingsDict["OutputPath"] + "\\Missiles")
            WorkingOutput = open(SettingsDict["OutputPath"] + "\\Missiles" + "\\" + missile.split(".")[0] + ".txt", "w")
            WorkingFileLines = WorkingFile.readlines()
            lineNumber = 0
            while lineNumber < len(WorkingFileLines):
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
                            else:
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
  
                lineNumber = lineNumber + 1
            json.dump(MissileDict,WorkingOutput)
            WorkingOutput.close()

        print("\n")
        
        
    else:
        print("Could not find the MissileTemplates folder. Please check your Nebulous\\Saves for the MissileTemplates folder.") 

#open and read ships
if SettingsDict["ShipJson"] == "yes":
    ShipPath = SavesPath + "\\ShipTemplates"
    if os.path.exists(ShipPath):
        ShipFolder = os.listdir(ShipPath)
        ShipFiles = []
        for f in range(len(ShipFolder)):
            if ShipFolder[f].endswith('.ship'):
                ShipFiles.append(ShipFolder[f])
        if SettingsDict["DebugMode"] == "yes":
            print("Ships")
            pprint(ShipFiles)
            print("\n")
        '''
        read and .json saved ships, cross reference with fleets. Store stats, on the ship per ship level. 
        '''
    else:
        print("Could not find the Fleets folder. Please check your Nebulous\\Saves for the ShipTemplates folder.")
        
#open and read Battle Reports
if SettingsDict["MatchJson"] == "yes":
    ReportPath = SavesPath + "\\SkirmishReports"
    if os.path.exists(ReportPath):
        ReportFolder = os.listdir(ReportPath)
        ReportFiles = []
        for f in range(len(ReportFolder)):
            if ReportFolder[f].endswith('.xml'):
                ReportFiles.append(ReportFolder[f])
        if SettingsDict["DebugMode"] == "yes":
            print("Reports")   
            pprint(ReportFiles)
            print("\n")
    else:
        print("Could not find the SkirmishReports folder. Please check your Nebulous\\Saves for the SkirmishReports folder.")
