# import os
import time
# # from selenium import webdriver
# # from selenium.webdriver.common.by import By
# # from selenium.webdriver.support import expected_conditions as EC
# # from selenium.webdriver.support.ui import WebDriverWait
# # import json

# # # Json read
# # def read_file(path):
# #     with open(path, "r") as rf:
# #         values = json.load(rf)
# #     return values

# # settings_json = read_file('./settings.json')
# # # Connection Setup Locators
# # user_locator = (By.XPATH, "//input[@id='user']")
# # password_locator = (By.XPATH, "//input[@id='password']")
# # User = settings_json["TesterInfo"]["User"]
# # Password = settings_json["TesterInfo"]["Password"]
# # login_locator = "//span[@class='btn']"

# # # Define the offline function for performing web automation actions
# # def offline(driver, v):
# #     try:
# #         # Wait for the element to be present and clickable
# #         wait = WebDriverWait(driver, 20)
# #         trace_path = v.replace("'", "")
# #         test_capture_folder_input = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@class='mode-name-input-field']")))
        
# #         # Interaction with the element
# #         test_capture_folder_input.clear()
# #         test_capture_folder_input.send_keys(trace_path)
# #         time.sleep(2)  # Adjust the delay as needed

# #         driver.find_element(By.XPATH, '//button[contains(text(),"Execute")]').click()
# #         time.sleep(30)  # Adjust the delay as needed

# #     except Exception as z:
# #         print("Unable to perform offline actions:", z)


# # class WebAutomation:
# #     def __init__(self):
# #         self.driver = None
# #         self.connection_load = 15

# #     def initialize_driver(self):
# #         options = webdriver.ChromeOptions()
# #         options.add_argument("start-maximized")
# #         options.add_experimental_option('excludeSwitches', ['enable-logging'])
# #         self.driver = webdriver.Chrome(executable_path=r'D:\chromedriver-win32\chromedriver.exe')

# #     def perform_actions(self):
# #         try:
# #             # Navigate to the URL
# #             self.driver.get("http://localhost:5001/v6.18.0.html#admin")
# #             self.driver.maximize_window()
# #             wait = WebDriverWait(self.driver, 20)

# #             # Find and interact with the user input field
# #             user_input = self.driver.find_element(*user_locator)
# #             user_input.click()
# #             user_input.send_keys(User)

# #             password_input = self.driver.find_element(*password_locator)
# #             password_input.click()
# #             password_input.send_keys(Password)

# #             # Find and interact with the login button
# #             login_button = self.driver.find_element(By.XPATH, login_locator)
# #             login_button.click()
# #             time.sleep(5)

# #             # Admin Icon click
# #             admin_icon_element_locator = "//img[@src='images/leftNavIcons/Admin Mode.png']"
# #             admin_icon = self.driver.find_element(By.XPATH, admin_icon_element_locator).click()
            
# #             # Call the offline function to perform web automation actions for each file
# #             offline(automation.driver, v)

# #         except Exception as z:
# #             print("Unable to perform actions:", z)
# #         finally:
# #             self.driver.quit()

# # if __name__ == '__main__':
# #     automation = WebAutomation()
# #     automation.initialize_driver()
# #     directory = "C:\\GRL\\OfflineTrace"
# #     fileCount = len(os.listdir(directory))
# #     print("File Count:" + str(fileCount))

# #     # # Iterate through files in the directory
# #     # for i in range(1, fileCount + 1):
# #     #     list_files = []
# #     #     path = os.path.join(directory, str(i))

# #     #     # Iterate through files in the subdirectory
# #     #     for root, dirs, files in os.walk(path):
# #     #         for file in files:
# #     #             list_files.append(os.path.join(root, file))

# #     #     v = list_files[0]
# #     #     print(v)

# #     #     automation.perform_actions()
        
# #     for i in range(1, fileCount+1):
# #         list = []
# #         path = "C:\\GRL\\OfflineTrace\\" + str(i)
# #         path = path.replace("'", "")
# #         for root, dirs, files in os.walk(path):
# #             for file in files:
# #                 list.append(os.path.join(root, file))
# #         v = list[0]
# #         print(v)
# #        automation.perform_actions()

# directory = "C:\\GRL\\OfflineTrace"
# fileCount = len(os.listdir(directory))
# for i in range(1, fileCount+1): 
#     path = "C:\\GRL\\OfflineTrace\\" + str(i)
#     path = path.replace("'", "")
#     GRltracefile = []   # Use os.walk() to traverse the directory tree
#     for root, _, files in os.walk(path):
#         for file in files:
#             if not file.endswith(".xml"):  # Check if the file has a .xml extension
#                 GRltracefile.append(os.path.join(root, file))
#         print(GRltracefile)

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from PIL import Image
from io import BytesIO
import pytesseract
import time

# Initialize a web driver
driver = webdriver.Chrome(executable_path=r'D:\chromedriver-win32\chromedriver.exe')
driver.maximize_window()

# Open a webpage that triggers a tooltip on hover
driver.get("http://localhost:5001/v6.18.3.html")

# Find an element that triggers the tooltip on hover
trigger_element = driver.find_element(By.XPATH, "//img[@src='../../images/sleep-info.png']")

# Create an ActionChains object for hovering
action = ActionChains(driver)
action.move_to_element(trigger_element).perform()

# Wait for the tooltip element to appear
tooltip_element = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//img[@src='../../images/sleep-info.png']")))

# Capture a screenshot of the tooltip element
screenshot = tooltip_element.screenshot_as_png

# Use OCR to extract text from the tooltip screenshot
tooltip_text = pytesseract.image_to_string(Image.open(BytesIO(screenshot)))

# Print the extracted tooltip text
print("Extracted Tooltip Text:", tooltip_text)

# Close the browser
driver.quit()
