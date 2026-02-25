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

def string_to_int(number):
    
    number = number.replace(",", "")

    order_of_magnitude = number[-1]

    if order_of_magnitude == "k":
        return int(float(number[:-1]) * 1000)
    else:
        return int(number)

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

    # Because some users don't have a bio, the index of the character list varies. However, it is always the last element on the profile. Also, if the try statement fails, that means the user does not exist, so return None.
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

def scrape_user_following(driver):
    
    # Find the following button. This might be under the second or third div on their profile because they may or may not have a display name that is different from their username.
    following_button = driver.find_element(By.XPATH, '/html/body/div[1]/div/main/div/div/div/main/div/child::*/div/button[2]')

    # Calculate number of followers
    following_count = string_to_int(str(following_button.text).removesuffix(" Following"))

    # If 0, return empty set, 0

    # Click the following button

    # Scroll

    # When done scrolling, return set of all users followed, num following
    
    return set(), following_count

def scrape_user(driver):
    
    user_data = {}

    # Collects the user's characters and checks if the user does not exist
    characters = scrape_user_characters(driver)
    if type(characters) != set:
        return None
    
    user_data["characters"] = characters

    user_data["following"], user_data["following_count"] = scrape_user_following(driver)

    return user_data

def scrape_users():
    
    usernames = get_usernames()

    driver = init_driver("https://character.ai")

    for username in usernames:
        
        driver.get(f"https://character.ai/profile/{username}")

        user_data = scrape_user(driver)

        if type(user_data) != dict:
            print(f"user {username} does not exist")
            continue

        user_data["username"] = username

        print(f"User {username} is following {user_data['following_count']} accounts")

        # Check if dne

        # write to file

scrape_users()