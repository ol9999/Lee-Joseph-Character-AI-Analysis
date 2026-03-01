from pathlib import Path
import os
import jsonlines
import sys

n = int(sys.argv[1])

# To avoid duplicates, see which characters are already in characters.jsonl
old_characters = set()
all_characters_path = str(Path(__file__).parent.parent / "data" / "characters.jsonl")
if os.path.exists(all_characters_path):
    with jsonlines.open(all_characters_path) as reader:
        for line in reader:
            old_characters.add(line[0])

# Make a dictionary of all new scraped characters
new_characters = dict()
for x in range(n):
    new_characters_path = str(Path(__file__).parent.parent / "data" / f"characters_{x}.jsonl")
    if os.path.exists(new_characters_path):
        with jsonlines.open(new_characters_path) as reader:
            for line in reader:
                new_characters[line[0]] = line

# Append all new characters to characters.jsonl
with jsonlines.open(all_characters_path, mode="a") as writer:
    for character in new_characters.keys():
        if character not in old_characters:
            writer.write(new_characters[character])

# To avoid duplicates, see which characters are already in missing_characters.txt
old_missing_characters = set()
all_missing_characters_path = str(Path(__file__).parent.parent / "data" / "missing_characters.txt")
if os.path.exists(all_missing_characters_path):
    with open(all_missing_characters_path) as reader:
        for line in reader:
            old_missing_characters.add(line.strip())

# Make a set of all new missing characters
new_missing_characters = set()
for x in range(n):
    new_missing_characters_path = str(Path(__file__).parent.parent / "data" / f"missing_characters_{x}.txt")
    if os.path.exists(new_missing_characters_path):
        with open(new_missing_characters_path) as reader:
            for line in reader:
                new_missing_characters.add(line.strip())

new_missing_characters -= old_missing_characters

# Append all new missing characters to missing_characters.txt
with open(all_missing_characters_path, mode="a") as writer:
    for character in new_missing_characters:
        writer.write(character + "\n")