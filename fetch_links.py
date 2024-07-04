import os
import time
from urllib.parse import urlparse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Directory setup
output_dir = "output_files"
input_dir = "input_URLs"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
if not os.path.exists(input_dir):
    os.makedirs(input_dir)


# Create unique output file names
def get_output_file_names():
    existing_files = os.listdir(output_dir)
    max_number = 0
    for file_name in existing_files:
        try:
            num = int(
                file_name.replace("output", "")
                .replace("output_separated", "")
                .replace(".txt", "")
            )
            if num > max_number:
                max_number = num
        except ValueError:
            continue
    return f"output{max_number + 1}.txt", f"output_separated{max_number + 1}.txt"


# Function to fetch links
def fetch_links_from_url(url):
    driver_path = r"C:\Program Files\Edge Driver\msedgedriver.exe"  # Path to EdgeDriver
    options = webdriver.EdgeOptions()
    options.use_chromium = True
    options.add_argument("--headless")
    driver = webdriver.Edge(executable_path=driver_path, options=options)

    driver.get(url)
    wait = WebDriverWait(driver, 10)
    urls = []

    try:
        vpn_elements = wait.until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "card-list-item"))
        )

        for vpn_element in vpn_elements:
            title_element = vpn_element.find_element(By.TAG_NAME, "a")
            ActionChains(driver).move_to_element(title_element).click(
                title_element
            ).perform()
            wait.until(EC.new_window_is_opened)
            driver.switch_to.window(driver.window_handles[1])
            vpn_url = driver.current_url
            urls.append(vpn_url)
            driver.close()
            driver.switch_to.window(driver.window_handles[0])

        return urls

    except Exception as e:
        print(f"Error fetching links from {url}: {e}")
        return []
    finally:
        driver.quit()


# Function to write URLs to files
def write_urls_to_files(url_list, initial_url, output_file, output_separated_file):
    with open(output_file, "a") as f:
        for url in url_list:
            f.write(url + "\n")

    with open(output_separated_file, "a") as f:
        f.write(f"URLs from {initial_url}:\n")
        for url in url_list:
            f.write(url + "\n")
        f.write("\n")


# Main function
def main():
    output_file, output_separated_file = get_output_file_names()

    # Check if input file exists and is not empty
    input_file_path = os.path.join(input_dir, "input.txt")
    if os.path.exists(input_file_path) and os.path.getsize(input_file_path) > 0:
        with open(input_file_path, "r") as file:
            urls = [line.strip() for line in file.readlines()]
    else:
        urls = []
        while True:
            url = input("Enter a URL (or 'done' to finish): ").strip()
            if url.lower() == "done":
                break
            if urlparse(url).scheme in ["http", "https"]:
                urls.append(url)
            else:
                print(f"Invalid URL: {url}")

    # Fetch links from each URL
    for url in urls:
        fetched_urls = fetch_links_from_url(url)
        if fetched_urls:
            write_urls_to_files(fetched_urls, url, output_file, output_separated_file)
        else:
            print(f"No URLs found for {url}")

    print(f"URLs have been written to {output_file} and {output_separated_file}")


if __name__ == "__main__":
    main()
