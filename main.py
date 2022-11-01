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
    SettingsDict["PlayerName"] = input("Please enter your player name: ").lower()
    print("Answer the following quesiton with yes or no.")
    SettingsDict["MatchJson"] = input("Would you like to save your logs as json: ").lower()
    print("Answer the following quesiton with yes or no.")
    SettingsDict["FleetJson"] = input("Would you like to save your fleet sats as json: ").lower()
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

SavesPath = SettingsDict["NebulousPath"] + "\\saves"
if os.path.exists(SavesPath):
    if SettingsDict["DebugMode"] == "yes":
        print("debugging file search")
        print(SavesPath)
        print("walking though saves looking for files")
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
        print("Check and see if it has found everything you'd expect. If not yell at Grathew. He's on the Nebulous Discord or the Git.")
else:
    print("Could not find required file tree. Please check your settings file and varify your Nebulous location.")


#open and read Fleets
FleetPath = SavesPath + "\\Fleets"
if os.path.exists(FleetPath):
    FleetFolder = os.walk(FleetPath)
    FleetFiles = []
    for root, dirs, files in FleetFolder:
        for name in files:
            if name.endswith('.fleet'):
                FleetFiles.append(name)
else:
    print("Could not find the Fleets folder. Please check your Nebulous\\Saves for the Fleets folder.") 
    
    #open and read Missle Templates
MissilePath = SavesPath + "\\MissileTemplates"
if os.path.exists(MissilePath):
    MissileFolder = os.listdir(MissilePath)
    MissileFiles = []
    for f in range(len(MissileFolder)):
        if MissileFolder[f].endswith('.missile'):
            MissileFiles.append(MissileFolder[f])
else:
    print("Could not find the MissileTemplates folder. Please check your Nebulous\\Saves for the MissileTemplates folder.") 

#open and read ships
ShipPath = SavesPath + "\\ShipTemplates"
if os.path.exists(ShipPath):
    ShipFolder = os.listdir(ShipPath)
    ShipFiles = []
    for f in range(len(ShipFolder)):
        if ShipFolder[f].endswith('.ship'):
            ShipFiles.append(ShipFolder[f])
else:
    print("Could not find the Fleets folder. Please check your Nebulous\\Saves for the ShipTemplates folder.")
    
#open and read Battle Reports
ReportPath = SavesPath + "\\SkirmishReports"
if os.path.exists(ReportPath):
    ReportFolder = os.listdir(ReportPath)
    ReportFiles = []
    for f in range(len(ReportFolder)):
        if ReportFolder[f].endswith('.xml'):
            ReportFiles.append(ReportFolder[f])
else:
    print("Could not find the Fleets folder. Please check your Nebulous\\Saves for the SkirmishReports folder.")

print("Fleets")
pprint(FleetFiles)
print("Missiles")
pprint(MissileFiles)
print("Ships")
pprint(ShipFiles)
print("Reports")   
pprint(ReportFiles)