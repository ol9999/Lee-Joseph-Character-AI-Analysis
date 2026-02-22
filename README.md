# Lee-Joseph-Character-AI-Analysis
A Large-Scale Analysis of Public-Facing, Community-Built Chatbots on Character.AI: Code Release

instructions for scraping:
- use Python 3.10.6. undetected_chromedriver will not work in newer version of Python
- first, create a Character.AI account
- after cloning the repo, you first want to run scraper/authenticate.py. Log into your account. Now, you will remain logged in any time the scraper launches.
- you will find that this script also created a new folder called "data"
- to scrape the homepage, run scraper/homepage.py
- this will make a new file called "usernames.txt" in the data folder, and it is the set of usernames scraped from the homepage.
- This code is slightly different than what we used for our paper due to site updates. Before, you could visit the homepage without signing in, and so in this state, "for you" was not affected by any account activity that could influence the recommendation algorithm. This is not true anymore, and they also added a couple more rows called "popular" and "trending". Also the categories at the bottom have been updated since then.
- This code only uses the Featured, Popular, Trending, and the different categories at the bottom (e.g. anime, assistant, creative, etc.). If you want to use anything else like from Try These or Try Saying, feel free to do that manually because that's what we did.