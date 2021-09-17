import csv
from collections import Counter

from text import load_text

text = load_text()
pairs = []
total = 0

for prev, curr in zip(text, text[1:]):
    if prev == ' ' or curr == ' ' or prev == '.':
        continue
    pairs.append(prev + curr)
    total += 1

counter = Counter(pairs)
with open('sample/bigrams.csv', 'w') as csv_file:
    fieldnames = ['first', 'next', 'count']
    writer = csv.writer(csv_file)
    writer.writerow(fieldnames)
    for key, value in counter.most_common():
        writer.writerow(list(key) + [value / total])
