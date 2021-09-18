import random
from copy import deepcopy
from typing import *

from penalty import calculate_bigrams
from text import load_bigram_frequency

ALPHABET = 'abcdefghijklmnopqrstuvwxyz.,;/'


def generate_layout() -> List[str]:
    layout = list(ALPHABET)
    random.shuffle(layout)
    return layout


def mutate_layout(layout: List[str], permutations: int) -> List[str]:
    permutations_even = permutations if permutations % 2 == 0 else permutations + 1
    positions = random.sample(range(0, 30), permutations_even)
    for i in range(permutations_even // 2):
        layout = swap_positions(layout, positions[2 * i], positions[2 * i + 1])
    return layout


def swap_positions(layout: List[str], i1: int, i2: int) -> List[str]:
    new_layout = deepcopy(layout)
    prev = layout[i2]
    new_layout[i2] = new_layout[i1]
    new_layout[i1] = prev
    return new_layout


def format_layout(layout: List[str]):
    return f'{"".join(layout)}\n' \
           f'.{"-" * 19}.\n' \
           f'|{"|".join(layout[:10])}|\n' \
           f'|{"|".join(layout[10:20])}|\n' \
           f'|{"|".join(layout[20:])}|\n' \
           f'\'{"-" * 19}\''


def search(parent, depth, width, current_depth=0, min_penalty=1) -> List[str]:
    print(f'depth: {current_depth}')
    if current_depth == depth:
        return parent
    optimal = []
    for i in range(width):
        layout = mutate_layout(parent, (depth - current_depth) * 3)
        total_penalty = calculate_bigrams(layout, bigrams).sum()
        if total_penalty < min_penalty:
            optimal = layout
            min_penalty = total_penalty
            print(total_penalty)
    return search(optimal if optimal else parent, depth, width, current_depth + 1, min_penalty)


bigrams = load_bigram_frequency()

layout = search(generate_layout(), 10, 10000)
print(format_layout(layout))
print(calculate_bigrams(layout, bigrams))
