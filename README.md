# Lee-Joseph-Character-AI-Analysis
Welcome to the code release for [_A Large-Scale Analysis of Public-Facing, Community-Built Chatbots on Character.AI_](https://arxiv.org/abs/2505.13354) by Owen Lee and Kenneth Joseph.

## Using the Scraper

### Preparation

When setting up your environment, use Python 3.10 because `undetected_chromedriver` does not work with the newest versions of Python.

The first thing you need to do after cloning this repo and setting up your environment is to run `scraper/authenticate.py` and log into your Character.AI account. Close the browser when you are done. From now on, you will remain logged in any time the scraper launches. Your browser data will be saved in `scraper/browser_data`. This script should have also created a new directory called `data`. It is safe to run this script whenever you want.

### Scraping the Homepage

To scrape the homepage, run `scraper/homepage.py`. This will make a new file called `data/homepage.txt`, which is the set of usernames found on the homepage. Be aware that if this file already exists, the script will overwrite it. If this script is working properly, you will see it click on each of the categories (e.g. "Anime", "Assistant", "Creative").

This code has been slightly modified from my original code to address site updates. For example, you used to be able to view the homepage without an account, meaning you could see the "For you" section without its contents being biased to your account activity. This iteration of the code only collects usernames from the "Featured", "Popular", and "Trending" sections, in addition to the aforementioned genre categories (e.g. "Anime"). If you wish to collect usernames from elsewhere on the homepage (e.g. "Try these" or "Try saying"), feel free to add them manually to `data/homepage.txt` because that is what we did.

### Scraping Users

Here is a guide to the various data files that will be created during this step:
- `data/users.jsonl`: The central dataset of users you have scraped. More about the format of this file later.
- `data/missing_users.txt`: The central dataset of users we have found to be missing.
- `data/usernames_{x}.txt`: Several lists of usernames to scrape, each identified by an integer in place of the `x` in the filename.
- `data/users_{x}.jsonl`: Several datasets of users collected by each instance of the scraper, identified by an integer in place of the `x` in the filename.
- `data/missing_users_{x}.txt`: Several lists of users we have found to be missing, each identified by an integer in place of the `x` in the filename
- `data/scraped_users.txt`: A central list of usernames we have already scraped.

You can use one or more computers to scrape users. Whether you are using one computer or multiple, you need to run `scraper/split_users.py` to create lists of users to scrape. This script will read from `data/users.jsonl` and `data/missing_users.txt` to find users we have already visited (if this is your first round of scraping, these files will not exist yet and that is ok). The script will then read from `data/homepage.txt` and the Following column from `data/users.jsonl` to find users to scrape, excluding the ones we have already visited. This script takes one mandatory command-line argument, an integer specifying how many lists of usernames to make. This should probably be the same as the number of computers you will be using to scrape. For example, if you are using 3 computers, run `python scraper/split_users.py 3`, which will create `data/usernames_0.txt`, `data/usernames_1.txt`, and `data/usernames_2.txt`.

Now you are ready to start scraping user profiles. To do so, keep track of which computers will scrape which lists. Clone the repo on each of your computers and sign in using `scraper/authenticate.py`. You should use different accounts for each instance of the scraper because you might be ratelimited otherwise. Transfer the specific list of usernames to scrape onto its respective computer into the `data` directory.

Run `scraper/users.py` to start scraping users. This script takes one mandatory and one optional command-line argument. The first is an integer specifying which list to scrape from. For example, if you want this computer to scrape from `data/usernames_0.txt`, run `python scraper/users.py 0`. The second is a keyword `snowball`. If you include this second argument, i.e. you run `python scraper/users.py 0 snowball`, this instance of the scraper will continue scraping beyond the provided list by visiting usernames found in the Following section of each user. There is no reason not to do this if you are only using one computer, but if you are using multiple computers, you could end up scraping duplicates. Ideally, the computers would be able to read to and write from a central database, but the provided code does not do this. This script will create the file `data/users_{x}.jsonl` and `data/missing_users_{x}.txt`, where `x` is the first command line argument and the same number as the list of usernames it is reading from. The former is the dataset of users scraped from this instance of the scraper, and the latter is the list of users that are stale for some reason, having either been deleted, their username changed, etc. You will know that this script is done when it terminates without your interference and without raising an error.

When you are done with a round of scraping, put all data files `data/users_{x}.jsonl` and `data/missing_users_{x}.txt` onto one machine. It's ok if not every computer is done, any users not yet visited will just be included in the next batch of username lists. Now, run `scraper/merge_users.py`. This takes one mandatory command-line argument, an integer, which is the number of machines you are merging from. This must be greater than the highest `x` in the filenames. Otherwise, it will not merge all of your data but you wouldn't know because it doesn't raise an error. This will append all of your new data to `data/users.jsonl` and `data/missing_users.txt`, creating them if they do not already exist. It will also create `data/scraped_users.txt`, which is a list of all scraped usernames. If you are running any instances of the scraper with `snowball` enabled, you should put the updated `data/missing_users.txt` and `data/scraped_users.txt` in the `data` directory on the respective computers.

Repeat these steps starting from running `scraper/split_users.py`. Stop when you are satisfied with your sample.


- Now we will prepare to scrape characters. Run scraper/split_characters.py. It takes two command line arguments. The first is an int that specifies the number of lists to make. The second is optional, and it places a limit on the number of characters per user to scrape. If you have already started scraping some characters, it will use data from characters.jsonl to make sure you do not scrape beyond the limit you set. This will output files characters_x.txt.
- When you scrape characters, it is very important that you are not using an account where you have changed your display name.
- You must be zoomed out enough for the panel on the right to be visible automatically! (can I include an image?)
- To scrape characters, run characters.py. It takes two command line arguments. The first is the file number, and the second is "moderated" which will include moderate characters in our data.
- To merge characters, run merge_characters.py. This works the exact same way as merge_users.py. It takes one command line argument, the number of files to merge.