# cat data.txt | python mapper.py | sort | python reducer.py

import sys
from collections import defaultdict

word_count = defaultdict(int)
for line in sys.stdin:
    word, count = line.split("\t")
    word_count[word] += int(count)

for word, count in word_count.items():
    print(f"{word}\t{count}")