# data = "hello how are you and how are you doing ?"
# words = data.split()
# # words = ["hello","how","are","you","and","how","are","you","doing","?"]
# word_mapping = {}

# for word in words:
#     if word in word_mapping.keys():
#         word_mapping[word] += 1
#     else:
#         word_mapping[word] = 1

# print(word_mapping)

import sys

for line in sys.stdin:
    words = line.split()
    for word in words:
        print(f"{word}\t1")