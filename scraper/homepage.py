import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import chrome_version
from pathlib import Path

def init_driver(page, signed_in=True):
    chrome_options = uc.ChromeOptions()

    if signed_in:
        browser_data_path = str(Path(__file__).parent / "browser_data")
        chrome_options.add_argument("--user-data-dir=" + browser_data_path)
    
    chrome_version_number = int(chrome_version.get_chrome_version().split(".")[0])
    driver = uc.Chrome(use_subprocess=True, options=chrome_options, version_main=chrome_version_number)
    
    # Launch page
    driver.get(page)
    driver.maximize_window()
    
    return driver

def homepage():

    driver = init_driver("https://character.ai/")

    # Start building the set of usernames to visit from the featured, popular, trending, and category tabs
    username_set = set()

    # Featured
    featured = driver.find_elements(By.XPATH, '/html/body/div[1]/div/main/div/div/div/main/div/div[1]/ol/div/li[2]/div/div[2]/div/div[1]/child::*/a/div/div/div/div/div/div[1]/div')

    for username in featured:
        username_set.add(str(username.get_attribute("textContent"))[4:])

    # Popular
    popular = driver.find_elements(By.XPATH, '/html/body/div[1]/div/main/div/div/div/main/div/div[1]/ol/div/li[3]/div/div[2]/div/div[1]/child::*/a/div/div/div/div/div/div[1]/div')

    for username in popular:
        username_set.add(str(username.get_attribute("textContent"))[4:])

    # Trending
    trending = driver.find_elements(By.XPATH, '/html/body/div[1]/div/main/div/div/div/main/div/div[1]/ol/div/li[4]/div/div[2]/div/div[1]/child::*/a/div/div/div/div/div/div[1]/div')

    for username in trending:
        username_set.add(str(username.get_attribute("textContent"))[4:])

    # Categories
    category_buttons = driver.find_elements(By.XPATH, '/html/body/div[1]/div/main/div/div/div/main/div/div[1]/ol/div/div[4]/div[1]/div/div[1]/child::*/button')
    next_category_button = driver.find_element(By.XPATH, '/html/body/div[1]/div/main/div/div/div/main/div/div[1]/ol/div/div[4]/div[1]/div/div[3]')

    for category_button in category_buttons:
        while True:
            try:
                category_button.click()
                break
            except:
                next_category_button.click()
        
        category = WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.XPATH, '/html/body/div[1]/div/main/div/div/div/main/div/div[1]/ol/div/div[4]/child::*/li/div/div[2]/div/div[1]/child::*/a/div/div/div/div/div/div[1]/div')))

        for username in category:
            username_set.add(str(username.get_attribute("textContent"))[4:])
    
    data_file_path = str(Path(__file__).parent.parent / "data" / "homepage.txt")
    with open(data_file_path, mode="w") as writer:
        for username in username_set:
            writer.write(username + "\n")

    return

homepage()