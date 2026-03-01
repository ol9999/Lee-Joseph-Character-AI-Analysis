# Lee-Joseph-Character-AI-Analysis
Welcome to the code release for [_A Large-Scale Analysis of Public-Facing, Community-Built Chatbots on Character.AI_](https://arxiv.org/abs/2505.13354) by Owen Lee and Kenneth Joseph.

## Using the Scraper

### Preparation

When setting up your environment, use Python 3.10 because `undetected_chromedriver` does not work with the newest versions of Python.

The first thing you need to do after cloning this repo and setting up your environment is to run `scraper/authenticate.py` and log into your Character.AI account. Close the browser when you are done. From now on, you will remain logged in any time the scraper launches. Your browser data will be saved in `scraper/browser_data`. This script should have also created a new directory called `data`. It is safe to run this script whenever you want.

### Scraping the Homepage

To scrape the homepage, run `scraper/homepage.py`. This will make a new file called `data/homepage.txt`, which is the set of usernames found on the homepage. Be aware that if this file already exists, the script will overwrite it. If this script is working properly, you will see it click on each of the categories (e.g. "Anime", "Assistant", "Creative").

This code has been slightly modified from my original code to address site updates. For example, you used to be able to view the homepage without an account, meaning you could see the "For you" section without its contents being biased to your account activity. This iteration of the code only collects usernames from the "Featured", "Popular", and "Trending" sections, in addition to the aforementioned genre categories (e.g. "Anime"). If you wish to collect usernames from elsewhere on the homepage (e.g. "Try these" or "Try saying"), feel free to add them manually to `data/homepage.txt` because that is what we did.




- Before you are able to start scraping users, you need to have run authenticate.py and homepage.py. Then, run split_users.py. This will take one command line argument, an integer, which is the number of lists of usernames to make. The script will create files called usernames_0.txt, ..., usernames_n-1.txt, depending on how many files you specify. There will be no duplicates between the lists, and the lists will not contain any usernames for any users you have already scraped.
- You are now ready to start scraping user profiles. Run users.py. It takes one mandatory and one optional command line argument. The first is the number of the file to scrape from. For example, if you want to scrape from usernames_5.txt, run users.py 5. The second will make the script continue to scrape users beyond the initial list. If you want to do that, pass "snowball" as the second command line argument, i.e. run user.py 5 snowball.
- When you are done with this round of scraping, get all of your data files onto one machine and run merge_users.py. This will append all of your new data to users.jsonl and missing_users.txt. It will also create scraped_users.txt, which is a list of all currently scraped users, which you can put in the data directory in future scraping rounds if you are doing snowball sampling.
- Repeat steps starting from running split_users.py until you are satisfied with your sample.
- Now we will prepare to scrape characters. Run scraper/split_characters.py. It takes two command line arguments. The first is an int that specifies the number of lists to make. The second is optional, and it places a limit on the number of characters per user to scrape. If you have already started scraping some characters, it will use data from characters.jsonl to make sure you do not scrape beyond the limit you set. This will output files characters_x.txt.
- When you scrape characters, it is very important that you are not using an account where you have changed your display name.
- You must be zoomed out enough for the panel on the right to be visible automatically! (can I include an image?)
- To scrape characters, run characters.py. It takes two command line arguments. The first is the file number, and the second is "moderated" which will include moderate characters in our data.
- To merge characters, run merge_characters.py. This works the exact same way as merge_users.py. It takes one command line argument, the number of files to merge.