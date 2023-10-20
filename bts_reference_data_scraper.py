import boto3
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
import zipfile
import os
import re
import time
from datetime import date

today = date.today()
print("today's date is {}".format(today))

# S3 account information
# sts_client = boto3.client('sts')
# cdp_role_arn = 'arn:aws:iam::537054356694:role/consumer-prod-cdpe-fm-traffic'
# cdp_session_name = 'cdp_consumer_datasynthesis'
# assumed_role = sts_client.assume_role(
#     RoleArn=cdp_role_arn,
#     RoleSessionName=cdp_session_name
# )
#
# aes_tickets_data_engineering = boto3.Session(
#     aws_access_key_id=assumed_role['Credentials']['AccessKeyId'],
#     aws_secret_access_key=assumed_role['Credentials']['SecretAccessKey'],
#     aws_session_token=assumed_role['Credentials']['SessionToken']
# )
# aes_s3 = aes_tickets_data_engineering.client("s3")

# Specify the download directory path
download_directory = "/scratch/BTS_Referance_Data/"
# download_directory = "/Users/nerallapallya/PycharmProjects/BTS_reference_data"
# Configure Chrome options to set the download directory
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option('prefs', {
    'download.default_directory': download_directory
})
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--headless')
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--disable-extensions')
chrome_options.add_argument('--disable-gpu')
chrome_options.binary_location = '/usr/bin/google-chrome'


# The SELENIUM_SERVER_URL environment variable must be set in your Docker container
carrier_url = "https://www.transtats.bts.gov/DL_SelectFields.aspx?gnoyr_VQ=GDH&QO_fu146_anzr=N8vn6v10%20f722146%20gnoyr5"
carrier_browser = webdriver.Chrome(options=chrome_options)
carrier_browser.get(carrier_url)
# carrier_pattern = r'^T_CARRIER_DECODE_*\.zip$'
carrier_pattern = 'DL_SelectFields.zip'
carrier_target = None
# response = requests.get(main_url)

world_area_code_url = "https://www.transtats.bts.gov/DL_SelectFields.aspx?gnoyr_VQ=GEI&QO_fu146_anzr=N8vn6v10%20f722146%20gnoyr5"
wac_browser = webdriver.Chrome(options=chrome_options)
wac_browser.get(world_area_code_url)
# wac_patter = r'^T_WAC_COUNTRY_STATE_*\.zip$'
wac_pattern = 'DL_SelectFields.zip'
wac_target = None

aircraft_type_url = "https://www.transtats.bts.gov/DL_SelectFields.aspx?gnoyr_VQ=GDD&QO_fu146_anzr=N8vn6v10%20f722146%20gnoyr5"
at_browser = webdriver.Chrome(options=chrome_options)
at_browser.get(aircraft_type_url)
# wac_patter = r'^T_WAC_COUNTRY_STATE_*\.zip$'
at_pattern = 'DL_SelectFields.zip'
at_target = None

master_coordinates_url = "https://www.transtats.bts.gov/DL_SelectFields.aspx?gnoyr_VQ=FLL&QO_fu146_anzr=N8vn6v10%20f722146%20gnoyr5"
mc_browser = webdriver.Chrome(options=chrome_options)
mc_browser.get(master_coordinates_url)
# wac_patter = r'^T_WAC_COUNTRY_STATE_*\.zip$'
mc_pattern = 'DL_SelectFields.zip'
mc_target = None

# upload S3 loacation
# bucket_name = "squad-reference-data-ops-restricted-cdp-us-east-1"
bucket_name = "squad-reference-data-ops-restricted-cdp-us-east-1"
object_key1 = "Carrier_decode/{}".format(today) + "/"
object_key2 = "World_area_codes/{}".format(today) + "/"
object_key3 = "Aircraft_type/{}".format(today) + "/"
object_key4 = "Master_Coordinates/{}".format(today) + "/"

carrier_file = download_directory + "T_CARRIER_DECODE.csv"
wac_file = download_directory + "T_WAC_COUNTRY_STATE.csv"
at_file = download_directory + "T_AIRCRAFT_TYPES.csv"
mc_file = download_directory + "T_MASTER_CORD.csv"


# download carrier_decode file

try:
    checkbox = carrier_browser.find_element(By.ID, "chkAllVars")
    if not checkbox.is_selected():
        checkbox.click()
except Exception as e:
    print(f"An error occurred: {str(e)}")

try:
    download_link = carrier_browser.find_element(By.ID, "btnDownload")  # Replace with the actual identifier
    download_link.click()
except Exception as e:
    print(f"An error occurred: {str(e)}")

time.sleep(10)

# unzip carrier_decode zip and delete the zip file
for filename in os.listdir(download_directory):
    if re.match(carrier_pattern, filename):
        carrier_target = os.path.join(download_directory, filename)
        break

if not carrier_target:
    print("No matching zip file found.")

if carrier_target:
    with zipfile.ZipFile(carrier_target, 'r') as zip_ref:
        zip_ref.extractall(download_directory)
        print(f"File '{carrier_target}' successfully extracted.")
        os.remove(carrier_target)

time.sleep(10)

# download world_area_code file
try:
    checkbox = wac_browser.find_element(By.ID, "chkAllVars")
    if not checkbox.is_selected():
        checkbox.click()
except Exception as e:
    print(f"An error occurred: {str(e)}")

try:
    download_link = wac_browser.find_element(By.ID, "btnDownload")  # Replace with the actual identifier
    download_link.click()

except Exception as e:
    print(f"An error occurred: {str(e)}")

time.sleep(10)

# unzip worlds_area_codes zip and delete the zip file
for filename in os.listdir(download_directory):
    if re.match(wac_pattern, filename):
        wac_target = os.path.join(download_directory, filename)
        break

if not wac_target:
    print("No matching zip file found.")

if wac_target:
    with zipfile.ZipFile(wac_target, 'r') as zip_ref:
        zip_ref.extractall(download_directory)
        print(f"File '{wac_target}' successfully extracted.")
        os.remove(wac_target)

time.sleep(10)

# download aircraft_type file
try:
    checkbox = at_browser.find_element(By.ID, "chkAllVars")
    if not checkbox.is_selected():
        checkbox.click()
except Exception as e:
    print(f"An error occurred: {str(e)}")

try:
    download_link = at_browser.find_element(By.ID, "btnDownload")  # Replace with the actual identifier
    download_link.click()
except Exception as e:
    print(f"An error occurred: {str(e)}")

time.sleep(10)

# unzip aircraft_type zip and delete the zip file
for filename in os.listdir(download_directory):
    if re.match(at_pattern, filename):
        at_target = os.path.join(download_directory, filename)
        break

if not at_target:
    print("No matching zip file found.")

if at_target:
    with zipfile.ZipFile(at_target, 'r') as zip_ref:
        zip_ref.extractall(download_directory)
        print(f"File '{at_target}' successfully extracted.")
        os.remove(at_target)

time.sleep(10)

# download master_coordinate file
try:
    checkbox = mc_browser.find_element(By.ID, "chkAllVars")
    if not checkbox.is_selected():
        checkbox.click()
except Exception as e:
    print(f"An error occurred: {str(e)}")

try:
    download_link = mc_browser.find_element(By.ID, "btnDownload")  # Replace with the actual identifier
    download_link.click()
except Exception as e:
    print(f"An error occurred: {str(e)}")

time.sleep(10)

# unzip master_coordinate zip and delete the zip file
for filename in os.listdir(download_directory):
    if re.match(mc_pattern, filename):
        mc_target = os.path.join(download_directory, filename)
        break

if not mc_target:
    print("No matching zip file found.")

if mc_target:
    with zipfile.ZipFile(mc_target, 'r') as zip_ref:
        zip_ref.extractall(download_directory)
        print(f"File '{mc_target}' successfully extracted.")
        os.remove(mc_target)

time.sleep(10)

# # upload world area code file
# aes_s3.upload_file(
#     Filename=download_directory + "/{}".format(wac_file),
#     Bucket=bucket_name,
#     Key=object_key1
# )
#
# # upload carrier decode file
# aes_s3.upload_file(
#     Filename=download_directory + "/{}".format(carrier_file),
#     Bucket=bucket_name,
#     Key=object_key2
# )
#
# # upload aircraft_type file
# aes_s3.upload_file(
#     Filename=download_directory + "/{}".format(at_file),
#     Bucket=bucket_name,
#     Key=object_key3
# )
#
# # upload master_coordinate file
# aes_s3.upload_file(
#     Filename=download_directory + "/{}".format(mc_file),
#     Bucket=bucket_name,
#     Key=object_key4
# )

