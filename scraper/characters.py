import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import chrome_version
from pathlib import Path
import os
import sys
import jsonlines

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

def string_to_int(number):

    if len(number) == 0:
        return 0
    
    number = number.replace(",", "")

    order_of_magnitude = number[-1]

    if order_of_magnitude == "k":
        return int(float(number[:-1]) * 1000)
    elif order_of_magnitude == "m":
        return int(float(number[:-1]) * 1000000)
    else:
        return int(number)

def get_characters(x):
    
    # The set of characters we have already visited
    visited = set()

    # Add this iteration of scraped characters to visited set
    characters_jsonl_path = str(Path(__file__).parent.parent / "data" / f"characters_{x}.jsonl")
    if os.path.exists(characters_jsonl_path):
        with jsonlines.open(characters_jsonl_path) as reader:
            for line in reader:
                visited.add(line[0])

    # Add this iteration of missing characters to visited set
    missing_characters_path = str(Path(__file__).parent.parent / "data" / f"missing_characters_{x}.txt")
    if os.path.exists(missing_characters_path):
        with open(missing_characters_path) as reader:
            for line in reader:
                visited.add(line.strip())

    # Characters to scrape
    characters = set()

    # Add characters to characters set
    characters_path = str(Path(__file__).parent.parent / "data" / f"characters_{x}.txt")
    if os.path.exists(characters_path):
        with open(characters_path) as reader:
            for line in reader:
                characters.add(line.strip())
    else:
        print(f"Cannot find the file {characters_path}. Did you pass the correct number to the script?")
        raise Exception
    
    # Remove characters we have already visited
    characters -= visited

    return characters

def scrape_character(driver):
    
    character_data = {}

    # Set description and definition to None by default
    character_data["description"] = None
    character_data["definition"] = None

    # Checks for the flag and 3 dots buttons on the right side panel
    buttons = WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="chat-details"]/div[2]/div[2]/child::button')))

    # The flag is always there, but the 3 dots are only there if the character has a description and/or definition
    if len(buttons) == 2:
        buttons[1].click()
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/div/div/button'))).click()

        # The html elements for the description and definition
        details = driver.find_elements(By.XPATH, '/html/body/div[4]/div/child::div')

        # Wait until the description and/or definition load
        WebDriverWait(details[-1], 20).until(EC.any_of(
            EC.text_to_be_present_in_element((By.XPATH, 'div/p'), "Description"),
            EC.text_to_be_present_in_element((By.XPATH, 'div/p'), "Definition")
        ))

        for detail in details:
            detail_title = str(detail.find_element(By.XPATH, 'div/p').text).lower()
            detail_body = str(detail.find_element(By.XPATH, 'p').text)
            character_data[detail_title] = detail_body

    # We need to get your username so that if it appears in the greeting, we can replace it with {{user}}
    your_username = str(driver.find_element(By.XPATH, '/html/body/div[1]/div/main/div/div/div/aside/div/div[1]/div/div/div[3]/button/div/div[2]/div/p').text)

    character_data["greeting"] = str(WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="chat-messages"]/div[1]/div[1]/div/div/div[1]/div/div[1]/div[1]/div[2]/div[2]/div/div[1]'))).text).replace(your_username, "{{user}}")

    character_data["name"] = str(driver.find_element(By.XPATH, '//*[@id="chat-messages"]/div[2]/div/div/a[2]/p').text)

    character_data["title"] = str(driver.find_element(By.XPATH, '//*[@id="chat-messages"]/div[2]/div/div/p').text)

    character_data["creator"] = str(driver.find_element(By.XPATH, '//*[@id="chat-messages"]/div[2]/div/div/div/a').text)[4:]

    character_data["interactions"] = string_to_int(str(driver.find_element(By.XPATH, '//*[@id="chat-details"]/div[1]/div/div[2]').text).removesuffix(" interactions"))

    character_data["likes"] = string_to_int(str(driver.find_element(By.XPATH, '//*[@id="chat-details"]/div[2]/div[1]/div/button[1]').text))

    return character_data

def scrape_characters():

    # The number for the intermediate files we will be using
    x = sys.argv[1]

    characters = get_characters(x)

    driver = init_driver("https://character.ai")

    for character in characters:
        
        driver.get(character)

        character_data = scrape_character(driver)

        print()
        print([character, character_data["interactions"], character_data["likes"]])
        print()

scrape_characters()