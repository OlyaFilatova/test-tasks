###
# CLI Script that reads files located in the
# same folder as the script and counts words.
# Limitations:
# - subfolders are not supported
# - only simple words supported (ex. hyphens are not supported)
# - script does not know about semantics
# To use the script:
# 1. Install python
# 2. Put script in the same folder as files that have words to count.
# 3. Run `python counter.py`
###
import asyncio
from collections import Counter
import os
from pathlib import Path
import re


STOPWORDS = {"the", "and", "for", "are", "but", "not",
             "with", "from", "that", "this", "was", "were", "been",
             "have"}


async def readfile(filename: Path):
    with open(filename) as file:
        lines = []
        while line := file.readline():
            lines.append(line)
            await asyncio.sleep(0)
    return "".join(lines)


def tokenize_words(text):
    words = re.findall(r"[\w]+", text.lower())

    words = [
        word for word in words
        if len(word) >= 3 and word not in STOPWORDS
    ]
    return words


def get_filepaths():
    dirpath = Path(__file__).resolve().parent

    filenames = os.listdir(dirpath)
    scriptname = os.path.basename(__file__)

    filepaths = [
        dirpath / filename
        for filename in filenames
        if os.path.isfile(dirpath / filename) and filename != scriptname
    ]

    return filepaths


async def count_words():
    filepaths = get_filepaths()

    filelines = await asyncio.gather(*[
        readfile(filepath) for filepath in filepaths
    ])
    text = " ".join(filelines)
    words = tokenize_words(text)

    word_counter = Counter(words)

    return word_counter


async def main():
    word_counter = await count_words()

    top_ten = word_counter.most_common(10)

    for word_count in top_ten:
        print(f"{word_count[0]} {word_count[1]}")


asyncio.run(main())
