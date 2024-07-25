import os
import re
import time
import zipfile
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.common.by import By
from datetime import date
today = date.today()
print("Today's date is {}".format(today))

# Specify the download directory path
download_directory = "/home/jaga/bts_refrence_data/dsg-cirium-ticketsdatasynthesis-bts-reference/downloads"
profile = FirefoxProfile()
profile.set_preference("browser.download.dir", download_directory)
profile.set_preference("browser.download.folderList", 2)
profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/octet-stream")
# Set up Firefox options with the custom profile
firefox_options = Options()
firefox_options.headless = True
firefox_options.profile = profile
geckodriver_path = '/usr/local/bin/geckodriver'

urls_patterns = [
    ("https://www.transtats.bts.gov/DL_SelectFields.aspx?gnoyr_VQ=GDH&QO_fu146_anzr=N8vn6v10%20f722146%20gnoyr5", 'T_CARRIER_DECODE'),
    ("https://www.transtats.bts.gov/DL_SelectFields.aspx?gnoyr_VQ=GEI&QO_fu146_anzr=N8vn6v10%20f722146%20gnoyr5", 'T_WAC_COUNTRY_STATE'),
    ("https://www.transtats.bts.gov/DL_SelectFields.aspx?gnoyr_VQ=GDD&QO_fu146_anzr=N8vn6v10%20f722146%20gnoyr5", 'T_AIRCRAFT_TYPES'),
    ("https://www.transtats.bts.gov/DL_SelectFields.aspx?gnoyr_VQ=FLL&QO_fu146_anzr=N8vn6v10%20f722146%20gnoyr5", 'T_MASTER_CORD')
]
# Download and extract files
for url, pattern in urls_patterns:
    browser = webdriver.Firefox(executable_path=geckodriver_path, options=firefox_options)
    browser.get(url)
    target = None
    
    # Select all variables and download the file
    try:
        checkbox = browser.find_element(By.ID, "chkAllVars")
        if not checkbox.is_selected():
            checkbox.click()
    except Exception as e:
        print(f"An error occurred while selecting checkbox: {str(e)}")
    
    try:
        download_link = browser.find_element(By.ID, "btnDownload")
        download_link.click()
    except Exception as e:
        print(f"An error occurred while clicking download: {str(e)}")
    
    time.sleep(10)
    # Find the downloaded file and extract it
    for filename in os.listdir(download_directory):
        if re.match(pattern, filename):
            target = os.path.join(download_directory, filename)
            break
    if not target:
        print(f"No matching zip file found for pattern {pattern}.")
    if target:
        with zipfile.ZipFile(target, 'r') as zip_ref:
            zip_ref.extractall(download_directory)
            print(f"File '{target}' successfully extracted.")
            os.remove(target)
    time.sleep(10)
print("All files downloaded and extracted successfully.")