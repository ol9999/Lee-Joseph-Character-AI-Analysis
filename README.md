# Lee-Joseph-Character-AI-Analysis
A Large-Scale Analysis of Public-Facing, Community-Built Chatbots on Character.AI: Code Release

instructions for scraping:
- use Python 3.10.6. undetected_chromedriver will not work in newer version of Python
- first, create a Character.AI account
- after cloning the repo, you first want to run scraper/authenticate.py. Log into your account. Now, you will remain logged in any time the scraper launches.
- you will find that this script also created a new folder called "data"
- to scrape the homepage, run scraper/homepage.py
- this will make a new file called "homepage.txt" in the data folder, and it is the set of usernames scraped from the homepage.
- This code is slightly different than what we used for our paper due to site updates. Before, you could visit the homepage without signing in, and so in this state, "for you" was not affected by any account activity that could influence the recommendation algorithm. This is not true anymore, and they also added a couple more rows called "popular" and "trending". Also the categories at the bottom have been updated since then.
- This code only uses the Featured, Popular, Trending, and the different categories at the bottom (e.g. anime, assistant, creative, etc.). If you want to use anything else like from Try These or Try Saying, feel free to do that manually because that's what we did.
- Before you are able to start scraping users, you need to have run authenticate.py and homepage.py. Then, run split_users.py. This will take one command line argument, an integer, which is the number of lists of usernames to make. The script will create files called usernames_0.txt, ..., usernames_n-1.txt, depending on how many files you specify. There will be no duplicates between the lists, and the lists will not contain any usernames for any users you have already scraped.
- You are now ready to start scraping user profiles. Run users.py. It takes one mandatory and one optional command line argument. The first is the number of the file to scrape from. For example, if you want to scrape from usernames_5.txt, run users.py 5. The second will make the script continue to scrape users beyond the initial list. If you want to do that, pass "snowball" as the second command line argument, i.e. run user.py 5 snowball.