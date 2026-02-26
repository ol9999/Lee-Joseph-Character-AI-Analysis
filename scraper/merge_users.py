from pathlib import Path
import os
import jsonlines
import sys

n = int(sys.argv[1])

# To avoid duplicates, see which users are already in users.jsonl
old_users = set()
all_users_path = str(Path(__file__).parent.parent / "data" / "users.jsonl")
if os.path.exists(all_users_path):
    with jsonlines.open(all_users_path) as reader:
        for line in reader:
            old_users.add(line[0])

# Make a dictionary of all new scraped users
new_users = dict()
for x in range(n):
    new_users_path = str(Path(__file__).parent.parent / "data" / f"users_{x}.jsonl")
    if os.path.exists(new_users_path):
        with jsonlines.open(new_users_path) as reader:
            for line in reader:
                new_users[line[0]] = line

# Append all new users to users.jsonl
with jsonlines.open(all_users_path, mode="a") as writer:
    for username in new_users.keys():
        if username not in old_users:
            writer.write(new_users[username])

# To avoid duplicates, see which users are already in missing_users.txt
old_missing_users = set()
all_missing_users_path = str(Path(__file__).parent.parent / "data" / "missing_users.txt")
if os.path.exists(all_missing_users_path):
    with open(all_missing_users_path) as reader:
        for line in reader:
            old_missing_users.add(line.strip())

# Make a set of all new missing users
new_missing_users = set()
for x in range(n):
    new_missing_users_path = str(Path(__file__).parent.parent / "data" / f"missing_users_{x}.txt")
    if os.path.exists(new_missing_users_path):
        with open(new_missing_users_path) as reader:
            for line in reader:
                new_missing_users.add(line.strip())

new_missing_users -= old_missing_users

# Append all new missing users to missing_users.txt
with open(all_missing_users_path, mode="a") as writer:
    for username in new_missing_users:
        writer.write(username + "\n")