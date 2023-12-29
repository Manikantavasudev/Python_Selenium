from selenium import webdriver
import cv2

# Replace with the URL of the web page
web_page_url = "https://example.com"
# Replace with the XPath to the image element you want to capture
image_xpath = '//img[@src="../../images/Setup Images/Static_EPR.png"]'
# Replace with the path to the user-provided reference image
reference_image_path = "reference_image.png"

# Initialize the web driver (make sure to specify your browser driver)
driver = webdriver.Chrome()
driver.get(web_page_url)

try:
    # Find the image element using XPath
    image_element = driver.find_element_by_xpath(image_xpath)

    # Capture a screenshot of the image
    screenshot_path = "screenshot.png"
    image_element.screenshot(screenshot_path)

    # Load the user-provided reference image
    reference_image = cv2.imread(reference_image_path)

    # Load the captured screenshot
    screenshot_image = cv2.imread(screenshot_path)

    # Compare the two images
    difference = cv2.absdiff(reference_image, screenshot_image)

    # Define a threshold for acceptable differences (adjust as needed)
    threshold = 10000

    # Check if the images are similar
    if cv2.countNonZero(difference) < threshold:
        print("Images are similar.")
    else:
        print("Images are different.")

    # Optionally, save the difference image for further analysis
    cv2.imwrite("difference_image.png", difference)

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # Close the web driver
    driver.quit()
