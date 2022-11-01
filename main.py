'''
Nebulous Fleet Command Battle Report Analyzer
Author: Grathew
11/1/2022
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
            for line in WorkingFile:
                if line.__contains__("Designation"):
                    data = line.split(">")[1]
                    data = data.split("<")[0]
                    MissileDict["Designation"] = data
                
                if line.__contains__("Nickname"):
                    data = line.split(">")[1]
                    data = data.split("<")[0]
                    MissileDict["Nickname"] = data
                
                if line.__contains__("cost"):
                    data = line.split(">")[1]
                    data = data.split("<")[0]
                    MissileDict["cost"] = data

                if line.__contains__("BodyKey"):
                    data = line.split(">")[1]
                    data = data.split("<")[0]
                    MissileDict["Body"] = data
                    
                if line.__contains__("<MissileSocket>"):
                    while not line.__contains__("</MissileSocket>"):
                        SocketDict = {}
                        if line.__contains__("Size"):
                            data = line.split(">")[1]
                            data = data.split("<")[0]
                            SocketDict["size"] = data

                        if line.__contains__("ActiveSeekerSettings"):
                            ActiveSeekerDict = {"Type":"Active Seeker"}
                            while not line.__contains__("</InstalledComponent>"):
                                if line.__contains__("ComponentKey"):
                                    data = line.split(">")[1]
                                    data = data.split("<")[0]
                                    ActiveSeekerDict["Component Name"] = data

                                if line.__contains__("Mode"):
                                    data = line.split(">")[1]
                                    data = data.split("<")[0]
                                    ActiveSeekerDict["Mode"] = data                            
                                
                                if line.__contains__("RejectUnvalidated"):
                                    data = line.split(">")[1]
                                    data = data.split("<")[0]
                                    ActiveSeekerDict["Reject Unvalidated"] = data

                                if line.__contains__("DetectPDTargets"):
                                    data = line.split(">")[1]
                                    data = data.split("<")[0]
                                    ActiveSeekerDict["Detect Point Defence Targets"] = data                            
                                line = WorkingFile.readline()
                            
                                SocketDict["Seeker"] = ActiveSeekerDict
                            
                        if line.__contains__("DirectGuidanceSettings"):
                            GuidenceDict = {"Type":"Direct Guidence"}
                            while not line.__contains__("</InstalledComponent>"):
                                if line.__contains__("ComponentKey"):
                                    data = line.split(">")[1]
                                    data = data.split("<")[0]
                                    GuidenceDict["Component Name"] = data

                                if line.__contains__("Role"):
                                    data = line.split(">")[1]
                                    data = data.split("<")[0]
                                    GuidenceDict["Role"] = data                            
                                
                                if line.__contains__("HotLaunch"):
                                    data = line.split(">")[1]
                                    data = data.split("<")[0]
                                    GuidenceDict["Hot Launch"] = data

                                if line.__contains__("SelfDestructOnLost"):
                                    data = line.split(">")[1]
                                    data = data.split("<")[0]
                                    GuidenceDict["Self Destruct On Lost"] = data    
                                    
                                if line.__contains__("Maneuvers"):
                                    data = line.split(">")[1]
                                    data = data.split("<")[0]
                                    GuidenceDict["Termnal Maneuvers"] = data                                    
                                line = WorkingFile.readline()
                    
                    MissileDict["Sockets"].append(SocketDict)                    
                    line = WorkingFile.readline()


            json.dump(MissileDict,WorkingOutput)

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
