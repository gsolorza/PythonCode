import textfsm
from pprint import pprint
import sys
import os

deviceType = "extreme_exos"
baseFolder = os.getcwd()
devicesFolder = os.path.join(baseFolder, "OUTPUT")
deviceList = os.listdir(devicesFolder)
templateFolder = "/Users/georgesolorzano/Google Drive/PythonCode/Assessment/ntc-templates/templates"
devicesData = []

def getDevicesData():
    for device in deviceList:
        data = {device: []}
        path = os.path.join(devicesFolder, device)
        showCommandFile = os.listdir(path)
        for fileName in showCommandFile:
            command = fileName.replace(" ", "_").strip(".txt")
            filePath = os.path.join(path, fileName)
            showFile = open(filePath).read()
            templateName = deviceType+"_"+command+".textfsm"
            templatePath = os.path.join(templateFolder, templateName)
            templateFile = open(templatePath)
            template = textfsm.TextFSM(templateFile)
            regex = template.ParseTextToDicts(showFile)
            parseOutput = []
            for item in regex:
                parseLower = dict((k.lower(), v) for k,v in item.items())
                parseOutput.append(parseLower)
            output = {command: parseOutput}
            data[device].append(output)
        devicesData.append(data)
    return devicesData