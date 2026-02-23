import sys
from pathlib import Path
import os
import jsonlines

def scrape_users():
    
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

    print(visited)

scrape_users()