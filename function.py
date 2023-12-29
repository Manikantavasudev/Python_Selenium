import csv
import json
import xml.etree.ElementTree as ET
import xlsxwriter  # Import the xlsxwriter library

# Load the settings from the JSON file
with open("settings.json", "r") as readfile:
    settings = json.load(readfile)

# Load the golden and generated XML files
treeGolden = ET.parse(settings['Golden_path'])
GDroot = treeGolden.getroot()

treeGenerated = ET.parse(settings['Generated_path'])
GRroot = treeGenerated.getroot()

# Access the nameVendor element from the golden and generated XML
Golden = GDroot.find(".//nameVendor").text
Generated = GRroot.find(".//nameVendor").text

# Create dictionaries to store data from both XML files
data_1 = {}
data_2 = {}

# Extract information from the Golden XML file
for test_element in GDroot.findall(".//test"):
    tc_id = test_element.get("tcID")
    title = test_element.find("title").text.strip()
    score_value = test_element.find("score").get("value")

    data_1[tc_id] = {"title": title, "score_value": score_value}

# Extract information from the Generated XML file
for test_element in GRroot.findall(".//test"):
    tc_id = test_element.get("tcID")
    title = test_element.find("title").text.strip()
    score_value = test_element.find("score").get("value")

    data_2[tc_id] = {"title": title, "score_value": score_value}

# Define the XLSX file path
xlsx_file_path = "matched_data.xlsx"

# Create a list to hold the matched data
matched_data = []

# Initialize the XLSX workbook and worksheet
workbook = xlsxwriter.Workbook(xlsx_file_path)
worksheet = workbook.add_worksheet()

# Define cell formats for green and red text
green_format = workbook.add_format({'font_color': 'green'})
red_format = workbook.add_format({'font_color': 'red'})

# Write headers to the XLSX file
worksheet.write_row(0, 0, ["tcID", "Title", Golden, Generated, "Result"])

# Iterate over the matched data and add it to the worksheet
row = 1  # Start writing from the second row
for tc_id, data in data_1.items():
    if tc_id in data_2:
        title_1 = data["title"]
        title_2 = data_2[tc_id]["title"]
        score_value_1 = data["score_value"]
        score_value_2 = data_2[tc_id]["score_value"]

        if title_1 == title_2 and score_value_1 == score_value_2:
            result = "Match"
            result_format = green_format  # Use green text for "Match"
        else:
            result = "Mismatch"
            result_format = red_format  # Use red text for "Mismatch"

        worksheet.write(row, 0, tc_id)
        worksheet.write(row, 1, title_1)
        worksheet.write(row, 2, score_value_1)
        worksheet.write(row, 3, score_value_2)
        worksheet.write(row, 4, result, result_format)  # Apply the format

        row += 1

# Close the workbook to save changes
workbook.close()

print(f"Matching data saved to '{xlsx_file_path}' in XLSX format.")
