from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import time

# Configure the Edge WebDriver (replace with your actual WebDriver path if necessary)
driver_path = "C:\Program Files\Edge driver\msedgedriver.exe"
options = webdriver.EdgeOptions()
options.use_chromium = True
driver = webdriver.Edge(executable_path=driver_path, options=options)


def search_edge_extensions(search_text):
    attempts = 3
    for _ in range(attempts):
        try:
            driver.get(
                "https://microsoftedge.microsoft.com/addons/Microsoft-Edge-Extensions-Home"
            )  # Replace with your actual URL

            # Wait up to 10 seconds for the searchBox element to be present
            search_box = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "searchBox"))
            )

            search_box.send_keys(search_text)
            search_box.submit()

            # Example of retrieving extension IDs (modify as per your actual logic)
            extension_ids = []
            # Add your logic to fetch extension IDs here

            return extension_ids

        except NoSuchElementException:
            print("Element not found, retrying...")
            time.sleep(3)  # Adjust sleep time as needed
            continue

        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    print(f"Failed after {attempts} attempts.")
    return None


try:
    # Example usage:
    search_text = "free vpn"
    extension_ids = search_edge_extensions(search_text)
    if extension_ids:
        print("Extension IDs found:", extension_ids)
    else:
        print("Failed to retrieve extension IDs.")

finally:
    driver.quit()
