import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
import chrome_version
from pathlib import Path
import os
import sys
import jsonlines

def get_characters(x):
    
    # The set of characters we have already visited
    visited = set()

    # Add this iteration of scraped characters to visited set
    characters_jsonl_path = str(Path(__file__).parent.parent / "data" / f"characters_{x}.jsonl")
    if os.path.exists(characters_jsonl_path):
        with jsonlines.open(characters_jsonl_path) as reader:
            for line in reader:
                visited.add(line[0])

    # Add this iteration of missing characters to visited set
    missing_characters_path = str(Path(__file__).parent.parent / "data" / f"missing_characters_{x}.txt")
    if os.path.exists(missing_characters_path):
        with open(missing_characters_path) as reader:
            for line in reader:
                visited.add(line.strip())

    # Characters to scrape
    characters = set()

    # Add characters to characters set
    characters_path = str(Path(__file__).parent.parent / "data" / f"characters_{x}.txt")
    if os.path.exists(characters_path):
        with open(characters_path) as reader:
            for line in reader:
                characters.add(line.strip())
    else:
        print(f"Cannot find the file {characters_path}. Did you pass the correct number to the script?")
        raise Exception
    
    # Remove characters we have already visited
    characters -= visited

    return characters

def scrape_characters():

    # The number for the intermediate files we will be using
    x = sys.argv[1]

    characters = get_characters(x)

    print(characters)

scrape_characters()