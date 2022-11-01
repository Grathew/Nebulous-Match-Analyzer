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

savesPath = SettingsDict["NebulousPath"] + "\\saves"
if os.path.exists(savesPath):
    if SettingsDict["DebugMode"] == "yes":
        print("debugging file search")
        print(savesPath)
        print("walking though saves looking for files")
        for(root, dirs, file) in os.walk(savesPath):
            for f in file:
                if '.fleet' in f:
                    print("Fleet found " + f)
                if '.missile' in f:
                    print("Missile found " + f)
                if '.ship' in f:
                    print("Ship found " + f)
                if '.xml' in f:
                    print("Report found " + f)
else:
    print("Could not find file tree. Please check your settings file and varify your Nebulous Instal location.")


