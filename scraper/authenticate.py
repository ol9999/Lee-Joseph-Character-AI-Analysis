import undetected_chromedriver as uc
import chrome_version
from pathlib import Path
import time

chrome_options = uc.ChromeOptions()

browser_data_path = str(Path(__file__).parent / "browser_data")
chrome_options.add_argument("--user-data-dir=" + browser_data_path)

chrome_version_number = int(chrome_version.get_chrome_version().split(".")[0])
driver = uc.Chrome(use_subprocess=True, options=chrome_options, version_main=chrome_version_number)

driver.get("https://character.ai")
driver.maximize_window()
while True:
    time.sleep(10000)