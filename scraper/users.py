import sys
from pathlib import Path
import os
import jsonlines

def get_usernames():
    
    # The number for the intermediate files we will be using
    x = sys.argv[1]

    # The set of users we have already visited
    visited = set()

    # Add scraped users to visited set
    users_jsonl_path = str(Path(__file__).parent.parent / "data" / f"users_{x}.jsonl")
    if os.path.exists(users_jsonl_path):
        with jsonlines.open(users_jsonl_path) as reader:
            for line in reader:
                visited.add(line[0])

    # Add missing users to visited set
    missing_users_path = str(Path(__file__).parent.parent / "data" / f"missing_users_{x}.txt")
    if os.path.exists(missing_users_path):
        with open(missing_users_path) as reader:
            for line in reader:
                visited.add(line.strip())

    # The set of users to visit
    usernames = set()

    # Add usernames to usernames set
    usernames_path = str(Path(__file__).parent.parent / "data" / f"usernames_{x}.txt")
    if os.path.exists(usernames_path):
        with open(usernames_path) as reader:
            for line in reader:
                usernames.add(line.strip())
    
    # Remove usernames we have already visited
    usernames -= visited

    return usernames

def scrape_users():
    
    usernames = get_usernames()

    print(usernames)

scrape_users()