import xml.etree.ElementTree as ET
from openpyxl import Workbook, Border, Side, Style
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl.drawing.image import Image
from io import BytesIO

# Load the first XML file
Golden = ET.parse('C:\\GRL\\USBPD-C2-Browser-App\\Report\\TempReport\\C2EPR\\CN13_FW69_2023_10_10-17_37_42\\New_Run1_Rep0_2023_10_10-05_37_42\\PDMerged\\PD_Merged.xml')
root1 = Golden.getroot()

# Load the second XML file
Generated = ET.parse('C:\\GRL\\USBPD-C2-Browser-App\\Report\\TempReport\\C2EPR\\CA02-1.6.17.24_2023_10_10-15_23_05\\New_Run1_Rep0_2023_10_10-03_23_05\\PDMerged\\PD_Merged.xml')
root2 = Generated.getroot()

# Initialize the XLSX workbook and worksheet
workbook = Workbook()
worksheet = workbook.active

# Set column headers
worksheet.append(['tcID', 'conditionID', 'checkID', 'score (XML1)', 'score (XML2)', 'Match'])

# Iterate through the first XML to extract the relevant data
data1 = {}
for test in root1.findall('.//test'):
    tcID = test.get('tcID')
    condition_elem = test.find('.//conditionID')
    conditionID = condition_elem.get('conditionID') if condition_elem is not None else None
    check_elem = test.find('.//checkID')
    checkID = check_elem.get('checkID') if check_elem is not None else None
    score_elem = test.find('.//score')
    score = score_elem.get('value') if score_elem is not None else None
    data1[(tcID, conditionID, checkID)] = score

# Iterate through the second XML to extract the relevant data
data2 = {}
for test in root2.findall('.//test'):
    tcID = test.get('tcID')
    condition_elem = test.find('.//conditionID')
    conditionID = condition_elem.get('conditionID') if condition_elem is not None else None
    check_elem = test.find('.//checkID')
    checkID = check_elem.get('checkID') if check_elem is not None else None
    score_elem = test.find('.//score')
    score = score_elem.get('value') if score_elem is not None else None
    data2[(tcID, conditionID, checkID)] = score

# Compare the two datasets and write the results to the worksheet
for key, value1 in data1.items():
    value2 = data2.get(key)
    if value2 is not None:
        match = "Match" if value1 == value2 else "Different"
        worksheet.append([key[0], key[1], key[2], value1, value2, match])

# Save the workbook to a file
workbook.save('comparison_results.xlsx')
