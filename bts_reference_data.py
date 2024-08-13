import os
import time
import zipfile
import logging
import pandas as pd
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
 
# Configuration
tmp_dir = '/tmp'  # Temporary directory for storing downloaded files
output_dir = 'C:/Users/bjagadis/csv_file'  # The base directory where final output files will be saved
geckodriver_path = 'C:/Users/bjagadis/OneDrive - Reed Elsevier Group ICO Reed Elsevier Inc/Desktop/geckodriver.exe'  # Update this path to your Geckodriver executable

if not os.path.exists(tmp_dir):
    os.makedirs(tmp_dir)
# Setup logging
logging.basicConfig(
    filename=os.path.join(tmp_dir,'data_loader.log'),
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
 
firefox_options = Options()
firefox_options.add_argument('-headless')
firefox_options.set_preference("browser.download.dir", tmp_dir)
firefox_options.set_preference("browser.download.folderList", 2)
firefox_options.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/zip")
 
# Configuration dictionary for each table
CONFIG = {
    "bts_aircraft_types_raw": {
        "url": "https://www.transtats.bts.gov/DL_SelectFields.aspx?gnoyr_VQ=GDD",
        "file_pattern": "T_AIRCRAFT_TYPE",
        "fields": ["ac_group", "ac_typeid", "begin_date", "end_date", "long_name", "manufacturer", "short_name", "ssd_name"],
        "type_casting": {
            "begin_date": "date",
            "end_date": "date"
        }
    },
    "bts_carrier_decodes_raw": {
        "url": "https://www.transtats.bts.gov/DL_SelectFields.aspx?gnoyr_VQ=GDH",
        "file_pattern": "T_CARRIER_DECODE",
        "fields": ["airline_id", "carrier", "carrier_entity", "carrier_group", "carrier_group_new", "carrier_name", "region", "start_date_source", "thru_date_source", "unique_carrier", "unique_carrier_entity", "unique_carrier_name", "wac"],
        "type_casting": {
            "start_date_source": "date",
            "thru_date_source": "date"
        }
    },
    "bts_master_coordinates_raw": {
        "url": "https://www.transtats.bts.gov/DL_SelectFields.aspx?gnoyr_VQ=FLL",
        "file_pattern": "T_MASTER_COORDINATE",
        "fields": ["airport", "airport_country_code_iso", "airport_country_name", "airport_id", "airport_is_closed", "display_airport_city_name_full", "display_airport_name", "display_city_market_name_full", "lat_degrees", "lat_hemisphere", "lat_minutes", "lat_seconds", "latitude", "lon_degrees", "lon_hemisphere", "lon_minutes", "lon_seconds", "longitude", "utc_local_time_variation"],
        "type_casting": {
            "latitude": "float",
            "longitude": "float"
        }
    },
    "bts_world_area_codes_raw": {
        "url": "https://www.transtats.bts.gov/DL_SelectFields.aspx?gnoyr_VQ=GEI",
        "file_pattern": "T_WORLD_AREA_CODE",
        "fields": ["capital", "comments", "country_code_iso", "country_short_name", "country_type", "is_latest", "sovereignty", "start_date", "state_code", "state_fips", "state_name", "thru_date", "wac", "wac_name", "wac_seq_id2", "world_area_name"],
        "type_casting": {
            "start_date": "date",
            "thru_date": "date"
        }
    }
}
 
def download_source_file(dag_id: str, unique_id: str, table_name: str, table_config: dict) -> str:
    logging.info(f"Starting download for {table_name}.")
    url_ = table_config["url"]
    download_directory = os.path.join(tmp_dir, dag_id, unique_id, table_name)
 
    os.makedirs(download_directory, exist_ok=True)
 
    browser_page = webdriver.Firefox(service=Service(geckodriver_path), options=firefox_options)
    browser_page.get(url_)
 
    try:
        checkbox = WebDriverWait(browser_page, 10).until(
            EC.element_to_be_clickable((By.ID, "chkAllVars"))
        )
        if not checkbox.is_selected():
            checkbox.click()
 
        download_button = WebDriverWait(browser_page, 10).until(
            EC.element_to_be_clickable((By.ID, "btnDownload"))
        )
        download_button.click()
 
        time.sleep(10)  # Wait for the download to complete
        logging.info(f"Downloaded file for {table_name}.")
        
    finally:
        browser_page.quit()
 
    return download_directory
 
def extract_source_file(dag_id: str, unique_id: str, table_name: str, table_config: dict) -> pd.DataFrame:
    logging.info(f"Starting extraction for {table_name}.")
    download_directory = os.path.join(tmp_dir, dag_id, unique_id, table_name)
    pattern = table_config["file_pattern"]
 
    target = None
    for filename in os.listdir(download_directory):
        if filename.startswith(pattern) and filename.endswith(".zip"):
            target = os.path.join(download_directory, filename)
            break
 
    if not target:
        logging.error(f"No matching zip file found for {table_name}.")
        raise FileNotFoundError("No matching zip file found.")
 
    with zipfile.ZipFile(target, 'r') as zip_ref:
        zip_ref.extractall(download_directory)
        os.remove(target)
        logging.info(f"Extracted files for {table_name} successfully.")
 
    csv_file_path = [os.path.join(download_directory, file) for file in os.listdir(download_directory) if file.endswith('.csv')][0]
 
    df = pd.read_csv(csv_file_path)
    logging.info(f"CSV file extracted and loaded into DataFrame: {csv_file_path}")
 
    return df
 
def process_dataframe_for_output(dag_id: str, unique_id: str, table_name: str, table_config: dict, df: pd.DataFrame) -> pd.DataFrame:
    logging.info(f"Starting processing for {table_name}.")
    
    keep_fields = table_config.get("fields", [])
    df = df[keep_fields]
 
    type_casting = table_config.get("type_casting", {})
    for field, dtype in type_casting.items():
        if dtype == "date":
            df[field] = pd.to_datetime(df[field])
        elif dtype == "float":
            df[field] = df[field].astype(float)
        else:
            df[field] = df[field].astype(dtype)
 
    logging.info(f"DataFrame processed for table: {table_name}")
 
    return df
 
def save_dataframe(dag_id: str, unique_id: str, table_name: str, df: pd.DataFrame):
    output_directory = os.path.join(output_dir, dag_id, unique_id, table_name)
    os.makedirs(output_directory, exist_ok=True)
 
    output_file_path = os.path.join(output_directory, f"{table_name}.csv")
    df.to_csv(output_file_path, index=False)
    logging.info(f"DataFrame saved to {output_file_path}")
 
def main_loader(dag_id: str, unique_id: str, table_name: str, publish_date: str):
    logging.info(f"Starting main loader for {table_name}.")
    table_config = CONFIG[table_name]
    
    download_source_file(dag_id, unique_id, table_name, table_config)
    
    df = extract_source_file(dag_id, unique_id, table_name, table_config)
    
    df = process_dataframe_for_output(dag_id, unique_id, table_name, table_config, df)
    
    save_dataframe(dag_id, unique_id, table_name, df)
 
    print(df.head())
 
# Example usage:
# main_loader("dag_id_example", "unique_id_example", "bts_carrier_decodes_raw", "2024-08-13")