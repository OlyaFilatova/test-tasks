###
# CLI Script that reads files located in the same folder as the script and counts words.
# Limitations:
# - subfolders are not supported
# - hashes and dashes are not supported
# - script does not know about semantics
# To use the script:
# 1. Install python
# 2. Put script in the same folder as files that have words to count.
# 3. Run `python counter.py` 
###
import asyncio
from collections import Counter
import os
import re


STOPWORDS = {"the", "and", "for", "are", "but", "not",
"with", "from", "that", "this", "was", "were", "been",
"have"}

async def readfile(filename: str):
    with open(filename) as file:
        lines = []
        while line := file.readline():
            lines.append(line)
            await asyncio.sleep(0)
    return "".join(lines)

async def main():
    filenames = os.listdir("./")
    scriptname = os.path.basename(__file__)
    filenames = [filename for filename in filenames if os.path.isfile(filename) and filename != scriptname]
    
    filelines = await asyncio.gather(*[readfile(filename) for filename in filenames])
    text = " ".join(filelines)
    words = re.findall(r"[\w]+", text.lower())

    words = [word for word in words if len(word) >= 3 and word not in STOPWORDS]

    word_counter = Counter(words)

    top_ten = word_counter.most_common(10)

    for word_count in top_ten:
        print(f"{word_count[0]} {word_count[1]}")

asyncio.run(main())
