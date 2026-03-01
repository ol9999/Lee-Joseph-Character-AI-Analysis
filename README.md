# Lee-Joseph-Character-AI-Analysis
Welcome to the code release for [_A Large-Scale Analysis of Public-Facing, Community-Built Chatbots on Character.AI_](https://arxiv.org/abs/2505.13354) by Owen Lee and Kenneth Joseph.

## Using the Scraper

### Preparation

Use Python 3.10 because `undetected_chromedriver` does not work in the newest versions of Python.

First, run `scraper/authenticate.py` and log into your Character.AI account. Now you will stay signed in. This script will also create a new directory named `data`.

### Scraping the Homepage

We start the scraping process by gathering all usernames on the homepage. Run `scraper/homepage.py`. This will create a new file called `data/homepage.txt` containing all usernames found on the homepage. Be aware that if this file already exists, the script will overwrite it.

The homepage scraper only collects usernames from the "Featured", "Popular", and "Trending" sections, in addition to the category tabs (e.g. "Anime", "Assistant", "Creative"). If you wish to collect usernames from elsewhere on the homepage (e.g. "Try these" or "Try saying"), feel free to add them manually to `data/homepage.txt`.

### Scraping Users

We build our sample of users from a snowball sampling strategy. Starting with the usernames from the homepage, we begin visiting user profiles and collecting data from them. We continually find new users to scrape by seeing who our already-scraped users are following.

The provided code enables you to scrape in parallel between multiple computers. Here is a guide to the various data files that will be created when scraping users:

| Filename | Description |
| --- | --- |
| `data/users.jsonl` | The central dataset of scraped users. More details about the format of this file can be found below. |
| `data/missing_users.txt` | The central list of users that no longer exist since we first discovered them. |
| `data/usernames_[NUMBER].txt` | Several lists of usernames to scrape, each identified by a number in the filename. |
| `data/users_[NUMBER].jsonl` | Several partial user datasets. Each is collected by an instance of the scraper, and each is identified by a number in the filename. |
| `data/missing_users_[NUMBER].txt` | Several partial lists of missing users. Each is collected by an instance of the scraper, and each is identified by a number in the filename |
| `data/scraped_users.txt` | The full list of usernames we have already scraped. |

**Step 1:** Run `scraper/split_users.py` to create lists of users to scrape next. This script will read from `data/homepage.txt`, `data/users.jsonl`, and `data/missing_users.txt`. The latter two files will not exist the first time you run this script; that is ok. This script takes one mandatory command-line argument, an integer specifying how many lists of usernames to make. For example, this would be the result of running `python scraper/split_users.py 5`:

| Input Files | Output Files |
| --- | --- |
| `data/homepage.txt` | `data/usernames_0.txt` |
| `data/users.jsonl` | `data/usernames_1.txt` |
| `data/missing_users.txt` | `data/usernames_2.txt` |
|  | `data/usernames_3.txt` |
|  | `data/usernames_4.txt` |

**Step 2:** On each computer you intend to scrape with, clone the repo and run `authenticate.py`. Use different accounts to avoid being ratelimited. Place one list of usernames `data/usernames_[NUMBER].txt` in the `data` directory on each computer.

**Step 3:** Run `scraper/users.py` on each computer to start scraping user profiles. This script takes one mandatory and one optional command-line argument:
1. An integer specifying which list of usernames to scrape from. For example, if you want this instance to scrape from `data/usernames_0.txt`, run `python scraper/users.py 0`.
2. (Optional) The keyword "snowball." If you run `python scraper/users.py 0 snowball`, the scraper will continue scraping beyond the initial batch of usernames using the snowball sampling strategy outlined above. Recomended if you are only using one machine.

| Input Files | Output Files |
| --- | --- |
| `usernames_0.txt` | `users_0.jsonl` |
| `users_0.jsonl` | `missing_users_0.txt` |
| `missing_users_0.txt` |  |
| `scraped_users.txt` (only relevant when `snowball` is used) |  |
| `missing_users.txt` (only relevant when `snowball` is used) |  |

**Step 4:** You will know an instance of the scraper is done when it terminates without error. When you are done with a round of scraping, transfer all data files `data/users_[NUMBER].jsonl` and `data/missing_users_[NUMBER].txt` onto one machine. It's ok if not every computer is done; any users missed this time around will be included again in the next round.

**Step 5:** Run `scraper/merge_users.py` to append all data collected this round to the central data files. This takes one mandatory command-line argument, an integer, which must be greater than any of the identifying numbers in the filenames. For example, this would be the result of running `python scraper/merge_users.py 5`:

| Input Files | Output Files |
| --- | --- |
| `data/users.jsonl` | `data/users.jsonl` |
| `data/users_0.jsonl` | `data/scraped_users.txt` |
| `data/users_1.jsonl` | `data/missing_users.txt` |
| `data/users_2.jsonl` |  |
| `data/users_3.jsonl` |  |
| `data/users_4.jsonl` |  |
| `data/missing_users.txt` |  |
| `data/missing_users_0.txt` |  |
| `data/missing_users_1.txt` |  |
| `data/missing_users_2.txt` |  |
| `data/missing_users_3.txt` |  |
| `data/missing_users_4.txt` |  |

**Step 6:** Repeat from step 1 until you are satisfied with your sample of users. Transfer new versions of `data/scraped_users.txt` and `data/missing_users.txt` to any computer that you are running with `snowball` enabled.

### Scraping Characters

Here is a guide to the various data files that will be created during this step:

| Filename | Description |
| --- | --- |
| `data/characters.jsonl` | The central dataset of users you have scraped. More about the format of this file later. |
| `data/missing_characters.txt` | The central list of characters we have found to be missing. |
| `data/characters_{x}.txt` | Several lists of characters to scrape, each identified by an integer in place of `{x}` in the filename |
| `data/characters_{x}.jsonl` | Several datasets of scraped characters for each instance of the scraper, each identified by an integer in place of `{x}` in the filename. |
| `data/missing_characters_{x}.txt` | Several lists of characters found to be missing for each instance of the scraper, each identified by an integer in place of `{x}` in the filename. |


- Now we will prepare to scrape characters. Run scraper/split_characters.py. It takes two command line arguments. The first is an int that specifies the number of lists to make. The second is optional, and it places a limit on the number of characters per user to scrape. If you have already started scraping some characters, it will use data from characters.jsonl to make sure you do not scrape beyond the limit you set. This will output files characters_x.txt.
- When you scrape characters, it is very important that you are not using an account where you have changed your display name.
- You must be zoomed out enough for the panel on the right to be visible automatically! (can I include an image?)
- To scrape characters, run characters.py. It takes two command line arguments. The first is the file number, and the second is "moderated" which will include moderate characters in our data.
- To merge characters, run merge_characters.py. This works the exact same way as merge_users.py. It takes one command line argument, the number of files to merge.