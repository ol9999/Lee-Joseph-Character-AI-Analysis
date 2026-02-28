import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
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

def get_usernames(x, snowball=False):

    # The set of users we have already visited
    visited = set()

    # Add scraped users to visited set
    scraped_users_path = str(Path(__file__).parent.parent / "data" / "scraped_users.txt")
    if os.path.exists(scraped_users_path):
        with open(scraped_users_path) as reader:
            for line in reader:
                visited.add(line.strip())

    # Add this iteration of scraped users to visited set
    users_jsonl_path = str(Path(__file__).parent.parent / "data" / f"users_{x}.jsonl")
    if os.path.exists(users_jsonl_path):
        with jsonlines.open(users_jsonl_path) as reader:
            for line in reader:
                visited.add(line[0])

    # Add missing users to visited set
    all_missing_users_path = str(Path(__file__).parent.parent / "data" / f"missing_users.txt")
    if os.path.exists(all_missing_users_path):
        with open(all_missing_users_path) as reader:
            for line in reader:
                visited.add(line.strip())

    # Add this iteration of missing users to visited set
    new_missing_users_path = str(Path(__file__).parent.parent / "data" / f"missing_users_{x}.txt")
    if os.path.exists(new_missing_users_path):
        with open(new_missing_users_path) as reader:
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
    else:
        print(f"Cannot find the file {usernames_path}. Did you pass the correct number to the script?")
        raise Exception
    
    # If snowball, add usernames from following section of scraped users
    if snowball and os.path.exists(users_jsonl_path):
        with jsonlines.open(users_jsonl_path) as reader:
            for line in reader:
                usernames.update(set(line[-1]))
    
    # Remove usernames we have already visited
    usernames -= visited

    return usernames, visited

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

def scrape_user_following(driver, max_following=10000):
    
    # Find the following button. This might be under the second or third div on their profile because they may or may not have a display name that is different from their username.
    following_button = driver.find_element(By.XPATH, '/html/body/div[1]/div/main/div/div/div/main/div/child::*/div/button[2]')

    # Calculate number of following
    following_count = string_to_int(str(following_button.text).removesuffix(" Following"))

    if following_count == 0:
        return set(), 0

    following_button.click()

    scrollable_div = driver.find_element(By.XPATH, '//*[@id="scrollableDiv"]/div/div')

    # Scroll until you hit the bottom or reach the maximum number of following per user. I set this to 10k because the scraper gets extremely slow the longer it scrolls down the following list. Also 10k is when they start abbreviating the following count from 9,999 to 10.0k. I cannot remember if the abbreviated following counts are rounded up or down, and if they are rounded up, then we will never reach what we think is the end of the list.
    while True:
        try:
            scrollable_div.find_element(By.XPATH, f'a[{min(following_count, max_following)}]')
            break
        except:
            driver.execute_script("document.querySelector('#scrollableDiv').scrollBy(0,1000)")

    # Get all of this user's following
    following_list = scrollable_div.find_elements(By.XPATH, 'child::a/div[2]/p[1]')

    following_set = set()
    for user in following_list:
        following_set.add(str(user.text))

    return following_set, following_count

def scrape_user(driver):
    
    user_data = {}

    # Collects the user's characters and checks if the user does not exist
    characters = scrape_user_characters(driver)
    if type(characters) != set:
        return None
    
    user_data["characters"] = characters

    # Collects the user's following and following count
    user_data["following"], user_data["following_count"] = scrape_user_following(driver)

    # Collects the user's display name, which may or may not be the same as their username.
    user_data["display_name"] = str(driver.find_element(By.XPATH, '//*[@id="main-content"]/div/div[1]').text)

    # Find the followers button. This might be under the second or third div on their profile because they may or may not have a display name that is different from their username.
    followers_button = driver.find_element(By.XPATH, '/html/body/div[1]/div/main/div/div/div/main/div/child::*/div/button[1]')

    # Calculate number of followers
    user_data["followers_count"] = string_to_int(str(followers_button.text).removesuffix(" Followers"))

    # Calculate number of interactions
    user_data["interactions"] = string_to_int(str(driver.find_element(By.XPATH, '//*[@id="main-content"]/div/child::div/p').text).removesuffix(" Interactions"))

    # Because the display name might be different than the username, the index of the bio might be different. However, it always third from last.
    bio = driver.find_elements(By.XPATH, '//*[@id="main-content"]/div/child::div')[-3]
    
    # If the user does not have a bio, then we have mistakenly selected the followers, following, and interactions row as the bio. We can check for this because the bio does not have any descendants, but the aforementioned row has them.
    if len(bio.find_elements(By.XPATH, 'descendant::*')) == 0:
        user_data["bio"] = str(bio.text)
    else:
        user_data["bio"] = None

    return user_data

def scrape_users():

    # The number for the intermediate files we will be using
    x = sys.argv[1]

    # Whether we will continue scraping users beyond our initial list
    snowball = (len(sys.argv) == 3) and (sys.argv[2] == "snowball")
    
    usernames, visited = get_usernames(x, snowball)

    driver = init_driver("https://character.ai")

    while len(usernames) > 0:
        
        username = usernames.pop()
        visited.add(username)

        driver.get(f"https://character.ai/profile/{username}")

        # If we encounter an error, restart the browser and try again
        try:
            user_data = scrape_user(driver)
        except:
            usernames.add(username)
            visited.discard(username)
            driver.quit()
            driver = init_driver("https://character.ai")
            continue

        # If this user is missing, document that and move on
        if type(user_data) != dict:
            new_missing_users_path = str(Path(__file__).parent.parent / "data" / f"missing_users_{x}.txt")
            with open(new_missing_users_path, mode="a") as writer:
                writer.write(username + "\n")
            continue

        if snowball:
            usernames.update(user_data["following"] - visited)

        # Add this user to the dataset
        users_jsonl_path = str(Path(__file__).parent.parent / "data" / f"users_{x}.jsonl")
        with jsonlines.open(users_jsonl_path, mode="a") as writer:
            line = [
                username,
                user_data["display_name"],
                user_data["followers_count"],
                user_data["following_count"],
                user_data["interactions"],
                user_data["bio"],
                list(user_data["characters"]),
                list(user_data["following"])
            ]
            writer.write(line)
        
scrape_users()