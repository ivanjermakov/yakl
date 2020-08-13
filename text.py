import functools
import re
from collections import Counter

text_path = 'text.txt'


def load_text(path: str) -> str:
    with open(path) as text:
        return text.read()


def prepare_text(text: str) -> str:
    return ''.join(re.findall(r'[a-zA-Z]', text))


def count_letter_frequency(text: str) -> list:
    return sorted(
        list(Counter(text).items()),
        key=functools.cmp_to_key(lambda k1, k2: k2[1] - k1[1])
    )


text = prepare_text(load_text(text_path))
print(count_letter_frequency(text))
