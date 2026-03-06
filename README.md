# Character.AI Scraper and Analysis Code by Owen Lee and Kenneth Joseph

Welcome to the code release for [_A Large-Scale Analysis of Public-Facing, Community-Built Chatbots on Character.AI_](https://arxiv.org/abs/2505.13354) by Owen Lee and Kenneth Joseph.

## The Dataset

Please email the lead author for the dataset. For more information, see [data/DATASET.md](data/DATASET.md).

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

Your central dataset of scraped users will be saved in `data/users.jsonl`. This is a [jsonlines](https://jsonlines.org/) file, where each line is a JSON array. Its format is as follows:

| Column | Field | Type |
| --- | --- | --- |
| 0 | Username | String |
| 1 | Display Name | String |
| 2 | Follower Count | Integer |
| 3 | Following Count | Integer |
| 4 | Interactions | Integer |
| 5 | Bio | String |
| 6 | Characters | Array |
| 7 | Following | Array |

**Step 1:** Run `scraper/split_users.py` to create lists of users to scrape next. This script will read from `data/homepage.txt`, `data/users.jsonl`, and `data/missing_users.txt`. If the latter two files do not exist the first time you run this script, that is ok. This script takes one mandatory command-line argument, an integer specifying how many lists of usernames to make. For example, this would be the result of running `python scraper/split_users.py 5`:

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
| `data/usernames_0.txt` | `data/users_0.jsonl` |
| `data/users_0.jsonl` | `data/missing_users_0.txt` |
| `data/missing_users_0.txt` |  |
| `data/scraped_users.txt` (only relevant when `snowball` is used) |  |
| `data/missing_users.txt` (only relevant when `snowball` is used) |  |

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

Here is a guide to the various data files that will be created when scraping characters:

| Filename | Description |
| --- | --- |
| `data/characters.jsonl` | The central dataset of scraped characters. More details about the format of this file can be found below. |
| `data/missing_characters.txt` | The central list of characters that no longer exist since we first discovered them. |
| `data/characters_[NUMBER].txt` | Several lists of characters to scrape, each identified by a number in the filename. |
| `data/characters_[NUMBER].jsonl` | Several partial character datasets. Each is collected by an instance of the scraper, and each is identified by a number in the filename. |
| `data/missing_characters_[NUMBER].txt` | Several partial lists of missing characters. Each is collected by an instance of the scraper, and each is identified by a number in the filename. |

Your central dataset of scraped characters will be saved in `data/characters.jsonl`. This is another [jsonlines](https://jsonlines.org/) file, where each line is a JSON array. Its format is as follows:

| Column | Field | Type |
| --- | --- | --- |
| 0 | URL | String |
| 1 | Creator | String |
| 2 | Interactions | Integer |
| 3 | Likes | Integer |
| 4 | Name | String |
| 5 | Tagline | String |
| 6 | Greeting | String |
| 7 | Description | String |
| 8 | Definition | String |

**Step 1:** Run `scraper/split_characters.py` to create lists of characters to scrape next. This script will read from `data/users.jsonl`, `data/characters.jsonl`, and `data/missing_characters.txt`. If the latter two files do not exist the first time you run this script, that is ok. This script takes one mandatory and one optional command-line argument:

1. An integer specifying how many lists of characters to make. For example, if you want to make 3 lists of characters, run `python scraper/split_characters.py 3`.
2. (Optional) An integer specifying the maximum number of characters you wish to scrape per user. For example, if you only want to scrape 5 characters per user, run `python scraper/split_characters.py 3 5`. If you have already begun scraping characters, the script will read from `data/characters.jsonl` to ensure that you do not scrape beyond the limit you set.

| Input Files | Output Files |
| --- | --- |
| `data/users.jsonl` | `data/characters_0.txt` |
| `data/characters.jsonl` | `data/characters_1.txt` |
| `data/missing_characters.txt` | `data/characters_2.txt` |

**Step 2:** On each computer you intend to scrape with, clone the repo and run `authenticate.py`.

Use different accounts to avoid being ratelimited. Do not use an account where you have changed its name because your old name can still appear in some greetings. This will preserve functionality in the scraper that replaces your name with "{{user}}" whenever it finds your username in a greeting.

Visit a character and make sure that your browser is zoomed out enough to see the right side panel without having to click anything.

Place one list of characters `data/characters_[NUMBER].txt` in the `data` directory on each computer.

**Step 3:** Run `data/characters.py` on each computer to start scraping characters. This script takes one mandatory and one optional command-line argument:

1. An integer specifying which list of characters to scrape from. For example, if you want this instance to scrape from `data/characters_2.txt`, run `python scraper/characters.py 2`.
2. (Optional) The keyword "moderated." In [September 2025](https://www.cnbc.com/2025/09/30/disney-cease-and-desist-characterai-copyright.html), Character.AI responded to a cease and desist letter from Disney by removing chatbots that violated Disney's copyright. Although users are no longer able to find and chat with these characters, those with the link can still see the greeting and creator. If you want to include these moderated characters in your character dataset, run `python scraper/characters.py 2 moderated`. Otherwise, they will be marked missing.

| Input Files | Output Files |
| --- | --- |
| `data/characters_2.txt` | `data/characters_2.jsonl` |
| `data/characters_2.jsonl` | `data/missing_characters_2.txt` |
| `data/missing_characters_2.txt` |  |

**Step 4:** You will know an instance of the scraper is done when it terminates without error. When you are done with a round of scraping, transfer all data files `data/characters_[NUMBER].jsonl` and `data/missing_characters_[NUMBER].txt` onto one machine. It's ok if not every computer is done; any characters missed this time around will be included again in the next round.

**Step 5:** Run `scraper/merge_characters.py` to append all data collected this round to the central data files. This takes one mandatory command-line argument, an integer, which must be greater than any of the identifying numbers in the filenames. For example, this would be the result of running `python scraper/merge_users.py 3`:

| Input Files | Output Files |
| --- | --- |
| `data/characters.jsonl` | `data/characters.jsonl` |
| `data/characters_0.jsonl` | `data/missing_characters.txt` |
| `data/characters_1.jsonl` |  |
| `data/characters_2.jsonl` |  |
| `data/missing_characters.txt` |  |
| `data/missing_characters_0.txt` |  |
| `data/missing_characters_1.txt` |  |
| `data/missing_characters_2.txt` |  |

**Step 6:** Repeat from step 1 until you are satisfied with your sample of characters.