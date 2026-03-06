# Character.AI Dataset by Owen Lee and Kenneth Joseph

Please email the lead author for the dataset. Unzip it and place `users.jsonl`, `characters.jsonl`, and `5per.txt` in the `data` directory.

## users.jsonl

Our dataset of users is `users.jsonl`. This is a [jsonlines](https://jsonlines.org/) file, where each row is a JSON array. There are 1,266,245 rows with 8 columns each. Every row follows this format:

| Index | Field | Type |
| --- | --- | --- |
| 0 | Username | String |
| 1 | Display Name | String |
| 2 | Follower Count | Integer |
| 3 | Following Count | Integer |
| 4 | Interactions | Integer |
| 5 | Bio | String |
| 6 | Characters | Array of String |
| 7 | Following | Array of String |

The `Username` field can be considered the unique ID for a user. To visit a user's page, visit `https://character.ai/profile/<THEIR_USERNAME>`. The `Following` field lists the usernames of whom a user follows.

This data was collected between July 11, 2024, and January 15, 2025, and so might not be up to date. For example, these users might have created more characters since then. Some users may have also been deleted and their profiles are no longer accessible.

## characters.jsonl

Our dataset of characters is `characters.jsonl`. This is another [jsonlines](https://jsonlines.org/) file, where each row is a JSON array. There are 3,859,313 rows with 9 columns each. Every row follows this format:

| Index | Field | Type |
| --- | --- | --- |
| 0 | Character URL | String |
| 1 | Creator | String |
| 2 | Interactions | Integer |
| 3 | Likes | Integer |
| 4 | Name | String |
| 5 | Tagline | String |
| 6 | Greeting | String |
| 7 | Description | String |
| 8 | Definition | String |

The `Character URL` field can be considered the unique ID for a character. These links come from the `Characters` field in `users.jsonl`. The `Creator` field records the username of the user that created this character.

This data was collected between July 11, 2024, and January 15, 2025, and so might not be up to date. For example, these characters might have received more interactions since then. Some characters may have also been deleted and are no longer accessible.

There was a bug in our original scraper code that prevented the scraper from collecting the `Creator`, `Name`, `Tagline`, and part of the `Greeting` fields from characters with greetings that were long enough to displace these fields above the height of the window. The 193,570 characters affected by this bug can be found by searching for rows where the character's `Name` is an empty string. If you wish to amend this error, you can scrape these characters again using the scraper code in this repo, which no longer has this problem.

## 5per.txt

For our analysis, we only considered a maximum of 5 characters per user. The list of 3,023,955 characters we considered is stored in `5per.txt`. If you wish to analyze the sample of 5 characters per user that we used, filter `characters.jsonl`, keeping rows only when `Character URL` appears in `5per.txt`. However, if you want to filter your own sample of x characters per user, you may find this example code useful:

```
import pandas as pd
import jsonlines

headers = [
    "Character URL",
    "Creator",
    "Interactions",
    "Likes",
    "Name",
    "Tagline",
    "Greeting",
    "Description",
    "Definition"
]

df_data = []
with jsonlines.open("characters.jsonl") as reader:
    for row in reader:
        df_data.append(row)

df = pd.DataFrame(df_data, columns=headers)

characters_5per = df.sample(frac=1).groupby("Creator").head(5).sort_values("Creator")
```