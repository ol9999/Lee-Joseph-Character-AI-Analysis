from pathlib import Path
import os
import jsonlines
import sys

n = int(sys.argv[1])

usernames = set()

visited = set()

# Add all scraped users to visited set
users_jsonl_path = str(Path(__file__).parent.parent / "data" / "users.jsonl")
if os.path.exists(users_jsonl_path):
    with jsonlines.open(users_jsonl_path) as reader:
        for line in reader:
            visited.add(line[0])

# Add all missing users to visited set
missing_users_path = str(Path(__file__).parent.parent / "data" / "missing_users.txt")
if os.path.exists(missing_users_path):
    with open(missing_users_path) as reader:
        for line in reader:
            visited.add(line.strip())

# Add usernames from homepage to usernames set
homepage_path = str(Path(__file__).parent.parent / "data" / "homepage.txt")
if os.path.exists(homepage_path):
    with open(homepage_path) as reader:
        for line in reader:
            usernames.add(line.strip())

# Add usernames from following section of scraped users
if os.path.exists(users_jsonl_path):
    with jsonlines.open(users_jsonl_path) as reader:
        for line in reader:
            usernames.update(set(line[-1]))

usernames -= visited

# Divide the usernames into n bins
bins = [[] for x in range(n)]
for i, username in enumerate(usernames):
    x = i % n
    bins[x].append(username)

# Write each bin to a file
for x in range(n):
    bin_path = str(Path(__file__).parent.parent / "data" / f"usernames_{str(x)}.txt")
    with open(bin_path, mode="w") as writer:
        for username in bins[x]:
            writer.write(username + "\n")