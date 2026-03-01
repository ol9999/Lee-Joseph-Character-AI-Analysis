from pathlib import Path
import os
import jsonlines
import sys

n = int(sys.argv[1])

max_yes = (len(sys.argv) == 3)

if max_yes:
    max_c_per_u = int(sys.argv[2])

characters = set()
visited = set()

# Make a dictionary mapping users to the number of their characters we have already scraped
# Record all characters that have already been scraped
scraped_characters_per_user = dict()
characters_jsonl_path = str(Path(__file__).parent.parent / "data" / "characters.jsonl")
if os.path.exists(characters_jsonl_path):
    with jsonlines.open(characters_jsonl_path) as reader:
        for line in reader:
            # Add 1 to this user's scraped characters
            scraped_characters_per_user[line[1]] = scraped_characters_per_user.get(line[1], 0) + 1
            # Note that we already visited this character
            visited.add(line[0])

# Add all missing characters to visited set
missing_characters_path = str(Path(__file__).parent.parent / "data" / "missing_characters.txt")
if os.path.exists(missing_characters_path):
    with open(missing_characters_path) as reader:
        for line in reader:
            visited.add(line.strip())

# Gather set of characters to scrape
users_jsonl_path = str(Path(__file__).parent.parent / "data" / "users.jsonl")
if os.path.exists(users_jsonl_path):
    with jsonlines.open(users_jsonl_path) as reader:
        for line in reader:
            for character in line[-2]:
                # This character will be scraped if it is not in visited and either there is no limit on the number of characters to scrape per user, or we have not yet reached that limit.
                if (character not in visited) and ((not max_yes) or (scraped_characters_per_user.get(line[0], 0) < max_c_per_u)):
                    characters.add(character)
                    scraped_characters_per_user[line[0]] = scraped_characters_per_user.get(line[0], 0) + 1

# Divide the characters into n bins
bins = [[] for x in range(n)]
for i, character in enumerate(characters):
    x = i % n
    bins[x].append(character)

# Write each bin to a file
for x in range(n):
    bin_path = str(Path(__file__).parent.parent / "data" / f"characters_{x}.txt")
    with open(bin_path, mode="w") as writer:
        for character in bins[x]:
            writer.write(character + "\n")