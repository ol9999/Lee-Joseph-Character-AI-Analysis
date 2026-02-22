import undetected_chromedriver as uc
from pathlib import Path
import time

chrome_options = uc.ChromeOptions()

browser_data_path = str(Path(__file__).parent / "browser_data")
chrome_options.add_argument("--user-data-dir=" + browser_data_path)

driver = uc.Chrome(use_subprocess=True, options=chrome_options)

driver.get("https://character.ai")
driver.maximize_window()
while True:
    time.sleep(10000)