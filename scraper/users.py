import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from pathlib import Path
import os
import sys
import jsonlines

def init_driver(page, signed_in=True):
    chrome_options = uc.ChromeOptions()

    if signed_in:
        browser_data_path = str(Path(__file__).parent / "browser_data")
        chrome_options.add_argument("--user-data-dir=" + browser_data_path)
    
    driver = uc.Chrome(use_subprocess=True, options=chrome_options)
    
    # Launch page
    driver.get(page)
    driver.maximize_window()
    
    return driver

def get_usernames():
    
    # The number for the intermediate files we will be using
    x = sys.argv[1]

    # The set of users we have already visited
    visited = set()

    # Add scraped users to visited set
    users_jsonl_path = str(Path(__file__).parent.parent / "data" / f"users_{x}.jsonl")
    if os.path.exists(users_jsonl_path):
        with jsonlines.open(users_jsonl_path) as reader:
            for line in reader:
                visited.add(line[0])

    # Add missing users to visited set
    missing_users_path = str(Path(__file__).parent.parent / "data" / f"missing_users_{x}.txt")
    if os.path.exists(missing_users_path):
        with open(missing_users_path) as reader:
            for line in reader:
                visited.add(line.strip())

    # The set of users to visit
    usernames = set()

    # Add usernames to usernames set
    usernames_path = str(Path(__file__).parent.parent / "data" / f"usernames_{x}.txt")
    if os.path.exists(usernames_path):
        with open(usernames_path) as reader:
            for line in reader:
                usernames.add(line.strip())
    
    # Remove usernames we have already visited
    usernames -= visited

    return usernames

def scrape_user_characters(driver):

# With bio and multiple characters
# /html/body/div[1]/div/main/div/div/div/main/div/div[6]/div/div[2]/div/a[1]

# No bio, no characters
# /html/body/div[1]/div/main/div/div/div/main/div/div[5]/div/div[2]/span

# No bio, some characters
# /html/body/div[1]/div/main/div/div/div/main/div/div[5]/div/div[2]/div/a[1]

    # Because some users don't have a bio, the index of the character list varies. However, it is always the last element on the profile. Also, if the try statement fails, that means the user does not exist.
    try:
        last_element_on_profile = driver.find_elements(By.XPATH, '/html/body/div[1]/div/main/div/div/div/main/div/div')[-1]
    except:
        return None

    # This checks for the presence of the message saying "This user hasn't made any Characters yet." If it is there, the user hasn't made any characters, so return an empty set.
    if len(last_element_on_profile.find_elements(By.XPATH, 'div/div[2]/span')) == 1:
        return set()

    # Get all of this user's characters
    character_list = last_element_on_profile.find_elements(By.XPATH, 'div/div[2]/div/child::a')

    characters_set = set()
    for character in character_list:
        characters_set.add(str(character.get_attribute("href")))

    return characters_set

def scrape_user(driver, username):
    
    user_data = {}

    # Collects the user's characters and checks if the user does not exist
    characters = scrape_user_characters(driver)
    if type(characters) != set:
        return None
    
    user_data["characters"] = characters

    return user_data

def scrape_users():
    
    usernames = get_usernames()

    driver = init_driver("https://character.ai")

    for username in usernames:
        
        driver.get(f"https://character.ai/profile/{username}")

        user_data = scrape_user(driver, username)

        if type(user_data) != dict:
            print(f"user {username} does not exist")
            continue

        user_data["username"] = username

        print(user_data)

        # Check if dne

        # write to file

scrape_users()