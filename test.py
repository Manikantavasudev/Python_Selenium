import xml.etree.ElementTree as ET
import json
with open("settings.json", "r") as readfile:
    settings = json.load(readfile)
treeVIF = ET.parse(settings['TesterInfo']['VIFPath'])
GDroot = treeVIF.getroot()

for child in GDroot[9]:
    # print(child.tag)
    if 'PD_Port_Type' in child.tag:
        print(child.text)