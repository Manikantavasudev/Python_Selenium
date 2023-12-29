import os
import glob
import json

# Json read
def read_file(path):
    with open(path, "r") as rf:
        values = json.load(rf)
    return values

settings_json = read_file('./settings.json')
golden_path = settings_json['Golden_path'] 
generated_path = settings_json['Generated_path']

Gupdated_path = golden_path.replace("\\", "/")

# Use the glob module to get a list of files in the folder
files_in_folder = glob.glob(os.path.join(generated_path, '*'))

# Check if there are any files in the folder
if files_in_folder:
    # Get the latest file based on modification time
    latest_file = max(files_in_folder, key=os.path.getmtime)

    # To Fetch last name in the Given path
    last_name = os.path.basename(latest_file)

    # Concatenate folder_path and last_name to get the complete path
    file_path = os.path.join(generated_path, last_name)

    # Initialize a list to store the XML files
    xml_files = []

    # Use os.walk() to traverse the directory tree
    for root, _, files in os.walk(file_path):
        for file in files:
            if file.endswith(".xml"):  # Check if the file has a .xml extension
                xml_files.append(os.path.join(root, file))
                
    
    if xml_files:
        # Print the list of XML files
        for xml_file in xml_files:
            print(xml_file)
            break
        # Replace "\\" or "\" with "/"
        lastestpath = xml_file.replace("\\", "/")
        print(lastestpath)

        # To open 'settings.json'
        with open('settings.json', 'r') as json_file:
            settings = json.load(json_file)

        # Add report_value to existing_data
        settings['Generated_path'] = lastestpath        

        # Save the updated JSON back to the file
        with open('settings.json', 'w') as json_file:
            json.dump(settings, json_file)

os.system('py ./summary.py')
os.system('py ./function.py')
#os.system('py ./CompareDetails.py')
