import logging
import time
import argparse
import os
from subprocess import call
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, NoSuchWindowException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
from webdriver_manager.chrome import ChromeDriverManager
import sys

# Json read
def read_file(path):
    with open(path, "r") as rf:
        values = json.load(rf)
    return values

Testcnf = read_file('./TestConfig.json')
chaplist = []

# if len(sys.argv)>1:
#     chaplist = sys.argv[1].split(':')
for chap in Testcnf:
    if len(Testcnf[chap]) != 0:
        chaplist.append(chap)
print(chaplist)


# Connection Setup Locators
search_locator = "//span[@class='rc-select-selection__clear']"
search = (By.XPATH, search_locator)
search_field_locator = "//input[@class='rc-select-search__field']"
clear_input = "//i[contains(text(),'×')]"
clear_text = (By.XPATH, clear_input)
search_field = (By.XPATH, search_field_locator)
connect_locator = '//button[@id="csConnectBtn"]'
connection = (By.XPATH, connect_locator)
Connected = str()

# Product Capability Locators
product_capability_locator = "//img[@alt='Product Capability']"
product = (By.XPATH, product_capability_locator)
project_field_locator = "//input[@id='pcNewProjectNameInputField']"
project_name = (By.XPATH, project_field_locator)
save_button = "//button[@id='pcNewProjectNameSaveBtn']"
save = (By.XPATH, save_button)
load_vif_locator = '//*[@id="pcLoadXmlVifFileBtn"]'
load = (By.XPATH, load_vif_locator)
ok_locator = "//button[contains(text(),'Ok')]"
ok = (By.XPATH, ok_locator)
dut_type_locator = "//button[@id='pcPort1DutTypeComboBox']"
dut_type = (By.XPATH, dut_type_locator)
test_config_locator = "//img[@alt='Test Config']"
test_config = (By.XPATH, test_config_locator)

# Json read
def read_file(path):
    with open(path, "r") as rf:
        values = json.load(rf)
    return values

MOI_json = read_file('./MOI.json')
settings_json = read_file('./settings.json')
SelectedTC = read_file('./Testcase.json')
SelectedTest= read_file('./TestConfig.json')
print("##############################################################################")
Input_project = settings_json["TesterInfo"]["ProjectName"]
input_IP = settings_json["TesterInfo"]["TesterIP"]
VIF_Path = settings_json["TesterInfo"]["VIFPath"]
print("##############################################################################")

os.system('py ./server.py')
#server.open_C2_server_application()
time.sleep(10)

class WebAutomation:
    def __init__(self):
        self.driver = None
        self.connection_load = 15

    def initialize_driver(self):
        
        options = webdriver.ChromeOptions()
        options.add_argument("start-maximized")
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.driver = webdriver.Chrome(executable_path=r'D:\chromedriver-win32\chromedriver.exe')

    def perform_actions(self):
        try:
            self.driver.get("http://localhost:5001")
            self.driver.maximize_window()
            time.sleep(10)
            wait = WebDriverWait(self.driver, 20)
            wait.until(EC.element_to_be_clickable(clear_text)).click()
            time.sleep(1)
            wait.until(EC.element_to_be_clickable(search_field)).send_keys(input_IP)
            time.sleep(3)
            wait.until(EC.element_to_be_clickable(connection)).click()
            time.sleep(10)
            connected_element_locator = "//b[text()='Connected']"
            wait.until(EC.presence_of_element_located((By.XPATH, connected_element_locator)))
            print("Connected")
            wait.until(EC.element_to_be_clickable(product)).click()
            wait.until(EC.element_to_be_clickable(project_name)).clear()
            time.sleep(5)
            wait.until(EC.element_to_be_clickable(project_name)).send_keys(Input_project)
            time.sleep(5)
            wait.until(EC.element_to_be_clickable(save)).click()

            # Load VIF file here
            vif_path = settings_json["TesterInfo"]["VIFPath"]
            vifelm = self.driver.find_element(By.XPATH, '//*[@id="vif-file-upload"]')
            print(vif_path)
            vifelm.send_keys(vif_path)
            time.sleep(5)

            # Navigation to Test Config page
            test_config_page = '//*[@alt="Test Config"]'
            test_config = (By.XPATH, test_config_page)
            select_all_MOI_title = "//span[contains(text(),'C2 Test Cases')]"
            select_all_MOI = (By.XPATH, select_all_MOI_title)
            all_support_certificate_button = "//button[@id='tcCertificationComboBox']"
            all_support_certificate = (By.XPATH, all_support_certificate_button)
            Expand_test_list = "//input[@id='tcExpandTestListCheckBox']"
            click_expand_test = (By.XPATH, Expand_test_list)

            wait.until(EC.element_to_be_clickable(test_config)).click()
            wait.until(EC.element_to_be_clickable(click_expand_test)).click()
            time.sleep(5)
            for Chapter in SelectedTest:
                if Chapter in chaplist:
                    for testname in SelectedTest[Chapter]:
                        print(testname, end="")
                        try:
                            testelm = self.driver.find_element(By.XPATH, f"//span[contains(text(), '{testname}')]")
                            print(testname)
                            self.driver.execute_script("arguments[0].click();", testelm)
                            time.sleep(0.5)
                        except Exception as ex:
                            print(f'Testcase {testname} not available in UI')

            # To start execution
            start_execution = self.driver.find_element(By.XPATH, "//button[@id='tcStartAndStopExecutionBtn']").click()
            print("Test execution is started")
            time.sleep(15)

            # Wait for the Test Execution to complete and track the LIVE BUTTON
            run_status = True
            while run_status:
                try:
                    # Check if Unlive button is displayed
                    sts = self.driver.find_element(By.XPATH,
                                                   "//img[@src='../../images/chartIcons/PNG/Live.png']").is_displayed()
                    if sts:
                        time.sleep(60)  # Wait for live button status to be displayed
                        try:
                            self.driver.find_element(By.XPATH, "//span[contains(text(),'Results')]").click()
                        except Exception as e:
                            print("Result tab is not clickable")
                            try:
                                self.driver.find_element(By.XPATH, "//button[contains(text(),'ok')]").click()
                                time.sleep(4)
                                print("try: clicked popup ok")
                                self.driver.find_element(By.XPATH, "//span[contains(text(),'Results')]").click()
                                print("try: clicked Result tab")
                            except Exception as A:
                                self.driver.refresh()
                                time.sleep(8)
                                try:
                                    self.driver.find_element(By.XPATH, "//span[contains(text(),'Results')]").click()
                                    print("Catch: try: result tab is clickable")
                                except Exception as z:
                                    self.driver.refresh()
                                    time.sleep(8)
                                    self.driver.find_element(By.XPATH, "//span[contains(text(),'Results')]").click()
                                    print("Catch: Catch: result tab is clickable")
                except Exception as x:
                    print("Test execution completed")
                    run_status = False  # Exit the loop
                    
            # Navigation to Report page
            report_tab = '//*[@alt="Report"]'
            report_page = (By.XPATH, report_tab)
            wait.until(EC.element_to_be_clickable(report_page)).click()
            print("Navigated to Report page")
            time.sleep(30)
            report = "html/body/div[1]/div/div[2]/div[2]/div[2]/div/div[5]/div/div/div/div/div[1]/div[5]/p[2]"
            self.driver.find_element(By.XPATH, report).is_displayed()
            
            time.sleep(90)
            
            # Define the XPath expression
            report_xpath = "html/body/div[1]/div/div[2]/div[2]/div[2]/div/div[5]/div/div/div/div/div[1]/div[5]/p[2]"

            # Find the element
            report_element = self.driver.find_element(By.XPATH, report_xpath)

            # Check if the element is displayed
            if report_element.is_displayed():
                # Get the text value of the element
                report_value = report_element.text

                # To open 'settings.json'
                with open('settings.json', 'r') as json_file:
                    settings = json.load(json_file)

                # Add report_value to existing_data
                settings['Generated_path'] = report_value

                # Save the updated JSON back to the file
                with open('settings.json', 'w') as json_file:
                    json.dump(settings, json_file)
                
                time.sleep(90)
                os.system('py ./fetch.py')

        except (NoSuchElementException, NoSuchWindowException) as e:
            logging.exception("Unable to connect to Tester")
#server.close_C2_server_application()
if __name__ == '__main__':
    automation = WebAutomation()
    automation.initialize_driver()
    automation.perform_actions()
