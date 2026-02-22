import undetected_chromedriver as uc
from pathlib import Path
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time
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
    
def scroll(swiper_wrapper, next):
    users = set()

    while True:
        users.update(str(user.text[4:]) for user in swiper_wrapper.find_elements(By.CLASS_NAME, 'truncate'))
        try:
            next.click()
        except:
            break
    
    users.update(str(user.text[4:]) for user in swiper_wrapper.find_elements(By.CLASS_NAME, 'truncate'))
    users.update(str(user.text[4:]) for user in swiper_wrapper.find_elements(By.CLASS_NAME, 'truncate'))
    users.update(str(user.text[4:]) for user in swiper_wrapper.find_elements(By.CLASS_NAME, 'truncate'))
    users.update(str(user.text[4:]) for user in swiper_wrapper.find_elements(By.CLASS_NAME, 'truncate'))
    
    return users

def homepage():

    driver = init_driver("https://character.ai/")

    # Start building the set of profiles to explore from the featured, popular, trending, and category tabs
    user_list = set()

    # Featured
    featured = driver.find_elements(By.XPATH, '/html/body/div[1]/div/main/div/div/div/main/div/div[1]/ol/div/li[2]/div/div[2]/div/div[1]/child::*')

    for slide in featured:
        print(str(slide.find_element(By.XPATH, './a/div/div/div/div/div/div[1]/div').get_attribute("textContent")))

    # /html/body/div[1]/div/main/div/div/div/main/div/div[1]/ol/div/li[2]/div/div[2]/div/div[1]
    # /html/body/div[1]/div/main/div/div/div/main/div/div[1]/ol/div/li[2]/div/div[2]/div/div[1]/div[1]/a/div/div/div/div/div/div[1]/div
    # /html/body/div[1]/div/main/div/div/div/main/div/div[1]/ol/div/li[2]/div/div[2]/div/div[1]/div[19]/a/div/div/div/div/div/div[1]/div
    # /html/body/div[1]/div/main/div/div/div/main/div/div[1]/ol/div/li[2]/div/div[2]/div/div[1]/div[14]/a/div/div/div/div/div/div[1]/div

    # featured_next = driver.find_element(By.XPATH, '/html/body/div[1]/div/main/div/div/div/main/div/div[1]/ol/div/li[2]/div/div[2]/div/div[3]')
    # user_list.update(scroll(featured, featured_next))

    # # For You
    # for_you = driver.find_element(By.XPATH, '/html/body/div/div/div/main/div/div/main/div/div/div[1]/ol/div/li[1]/div/div[2]/div/div[1]')
    # fy_next = driver.find_element(By.XPATH, '/html/body/div/div/div/main/div/div/main/div/div/div[1]/ol/div/li[1]/div/div[2]/div/div[3]')
    # user_list.update(scroll(for_you, fy_next))

    # # Featured
    # featured = driver.find_element(By.XPATH, '/html/body/div/div/div/main/div/div/main/div/div/div[1]/ol/div/li[2]/div/div[2]/div/div[1]')
    # featured_next = driver.find_element(By.XPATH, '/html/body/div/div/div/main/div/div/main/div/div/div[1]/ol/div/li[2]/div/div[2]/div/div[3]')
    # user_list.update(scroll(featured, featured_next))

    # # Categories
    # category_swiper = driver.find_element(By.XPATH, '/html/body/div/div/div/main/div/div/main/div/div/div[1]/ol/div/div[3]/div[1]/div/div[1]')

    # explored_categories = set()
    # while True:
        
    #     try:
    #         cat_name = 'Philosophy'

    #         for cat in category_swiper.find_elements(By.CLASS_NAME, 'swiper-slide-fully-visible'):
    #             if cat not in explored_categories:

    #                 cat.click()
    #                 cat_name = str(cat.text)
                    
    #                 # Find the next button
    #                 while True:
    #                     try:
    #                         cat_char_next = driver.find_element(By.XPATH, '/html/body/div/div/div/main/div/div/main/div/div/div[1]/ol/div/div[3]/div[@*]/li/div/div[2]/div/div[3]')
    #                         break
    #                     except:
    #                         continue
                        
    #                 # Find the wrapper
    #                 while True:
    #                     try:
    #                         wrap = driver.find_element(By.XPATH, '/html/body/div/div/div/main/div/div/main/div/div/div[1]/ol/div/div[3]/div[@*]/li/div/div[2]/div/div[1]')
    #                         break
    #                     except:
    #                         continue
    #                 actions = ActionChains(driver)
    #                 actions.move_to_element(wrap).perform()

    #                 user_list.update(scroll(wrap, cat_char_next))

    #                 explored_categories.add(cat)

    #         if cat_name == 'Philosophy':
    #             # Click the Politics button
    #             driver.find_element(By.XPATH, '/html/body/div/div/div/main/div/div/main/div/div/div[1]/ol/div/div[3]/div[1]/div/div[1]/div[16]/button').click()

    #             # Find the next button
    #             while True:
    #                 try:
    #                     cat_char_next = driver.find_element(By.XPATH, '/html/body/div/div/div/main/div/div/main/div/div/div[1]/ol/div/div[3]/div[@*]/li/div/div[2]/div/div[3]')
    #                     break
    #                 except:
    #                     continue
                    
    #             # Find the wrapper
    #             while True:
    #                 try:
    #                     wrap = driver.find_element(By.XPATH, '/html/body/div/div/div/main/div/div/main/div/div/div[1]/ol/div/div[3]/div[@*]/li/div/div[2]/div/div[1]')
    #                     break
    #                 except:
    #                     continue
    #             actions = ActionChains(driver)
    #             actions.move_to_element(wrap).perform()
                
    #             user_list.update(scroll(wrap, cat_char_next))

    #             break

    #     except:
    #         pass

    #     finally:
    #         try:
    #             # Click next to see more categories
    #             driver.find_element(By.XPATH, '/html/body/div/div/div/main/div/div/main/div/div/div[1]/ol/div/div[3]/div[1]/div/div[3]').click()
    #         except:
    #             pass

    # driver.quit()
    # user_list.discard('')

    # with jsonlines.open('homepage.jsonl', mode='w') as writer:
    #     for user in user_list:
    #         writer.write(user)

    return

homepage()