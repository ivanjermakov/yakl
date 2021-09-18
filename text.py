import csv
import functools
from collections import Counter

from Bigram import Bigram

TEXT_PATH = 'sample/sample.txt'
BIGRAM_PATH = 'sample/bigrams.csv'


def load_text() -> str:
    with open(TEXT_PATH) as text:
        return text.read()


def load_bigram_frequency() -> list[Bigram]:
    """

    :rtype: object
    """
    bigrams = []
    with open(BIGRAM_PATH) as csv_file:
        for i, row in enumerate(csv.reader(csv_file)):
            if i == 0: continue
            bigrams.append(Bigram(row[0], row[1], float(row[2])))
    return bigrams


def count_letter_frequency(text: str) -> list:
    return sorted(
        list(Counter(text).items()),
        key=functools.cmp_to_key(lambda k1, k2: k2[1] - k1[1])
    )
