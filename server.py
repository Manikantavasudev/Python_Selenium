import os
import socket
import time

# Change the working directory to the GRL-C2 Browser App installation folder
app_folder = os.path.join("C:\\", "Program Files (x86)", "GRL-C2_Browser_App")
# C:\Program Files (x86)\GRL-C2_Browser_App
serverpath = app_folder.replace("\\", "/")
print(app_folder)

#to open the Server
def open_C2_server_application():
    """
    Open C2_server_application
    """
    expected_value = 0
    os.chdir(serverpath)
    server_open = os.system("start cmd /c C2BrowserApp.exe")
    assert server_open == expected_value, "Value is Miss-Match {} and {} can't able to open the Application".format(
        server_open, expected_value)
    
    time.sleep(10)

# Call the function to open the application
open_C2_server_application()

#to Close the Server
def close_C2_server_application():
    """
    Close the C2BrowserApp server application
    """
    expected_value = 0
    time.sleep(5)
    server_close = os.system("taskkill /f /im C2BrowserApp.exe")
    print(server_close)
    assert server_close == expected_value, "Value is Miss-Match {} and {} can't able to close the Application".format(
        server_close, expected_value)

