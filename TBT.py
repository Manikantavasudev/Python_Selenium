import json
import xml.etree.ElementTree as ET
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os  # Import the os module

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

# Initialize the Google Sheets connection
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

# Get the path to the credentials file in the same directory as the script
script_directory = os.path.dirname(os.path.abspath(__file__))
credentials_path = os.path.join(script_directory, "path/to/your-credentials.json")

credentials = ServiceAccountCredentials.from_json_keyfile_name(credentials_path, scope)
gc = gspread.authorize(credentials)

# Open the Google Sheet by URL
sheet_url = "https://docs.google.com/spreadsheets/d/1eLy3vJnsVUK9ZVITw0uLhKdcK7L3FozPhJqiW73W1WE/edit#gid=792134518"
worksheet = gc.open_by_url(sheet_url).sheet1  # Use the appropriate sheet index or title

# Clear existing data in the Google Sheet
worksheet.clear()

# Write headers to the Google Sheet
worksheet.append_row(["tcID", "Title", Golden, Generated, "Result"])

# Iterate over the matched data and add it to the Google Sheet
for tc_id, data in data_1.items():
    if tc_id in data_2:
        title_1 = data["title"]
        title_2 = data_2[tc_id]["title"]
        score_value_1 = data["score_value"]
        score_value_2 = data_2[tc_id]["score_value"]

        if title_1 == title_2 and score_value_1 == score_value_2:
            result = "Match"
        else:
            result = "Mismatch"

        # Write data to the Google Sheet
        worksheet.append_row([tc_id, title_1, score_value_1, score_value_2, result])

print(f"Matching data saved to '{sheet_url}' in Google Sheets.")
