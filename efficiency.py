from typing import List

import layouts
import text as t

FINGER_TRAVEL_DISTANCE_WEIGHT = .4
CONSECUTIVE_FINGER_WEIGHT = .1
CONSECUTIVE_HAND_WEIGHT = .1
DOMINANT_HAND_WEIGHT = .1
PINKY_USAGE_WEIGHT = .1

LAYOUT_SIZE: (int, int) = (4, 10)

DISTANCE_MAP: List[float] = [
    .3, .3, .3, .3, .7, .7, .3, .3, .3, .3,
    .0, .0, .0, .0, 0., 0., .5, .0, .0, .0,
    .5, .5, .5, .5, 1., 1., .5, .5, .5, .5
]

FINGER_MAP: List[int] = [
    1, 2, 3, 4, 4, 5, 5, 6, 7, 8,
    1, 2, 3, 4, 4, 5, 5, 6, 7, 8,
    1, 2, 3, 4, 4, 5, 5, 6, 7, 8,
]


def index_to_pos(index: int) -> (int, int):
    return int(index / LAYOUT_SIZE[1]), index % LAYOUT_SIZE[1]


def pos_to_index(pos: (int, int)) -> int:
    return pos[0] * LAYOUT_SIZE[1] + pos[1]


def finger_travel_distance_penalty(layout: List[str], letter: str) -> float:
    return DISTANCE_MAP[layout.index(letter)]


def consecutive_finger_penalty(layout: List[str], prev_letter: str, current_letter: str) -> float:
    prev_finger = FINGER_MAP[layout.index(prev_letter)]
    current_finger = FINGER_MAP[layout.index(current_letter)]
    if prev_finger != current_finger:
        return 0
    prev_pos = index_to_pos(layout.index(prev_letter))
    current_pos = index_to_pos(layout.index(current_letter))
    if prev_pos == current_pos:
        return .2
    if prev_pos[0] == current_pos[0] or prev_pos[1] == current_pos[1]:
        return .5
    if abs(prev_pos[0] - current_pos[0]) == 2 or abs(prev_pos[1] - current_pos[1]) == 2:
        return 1
    return .6


def consecutive_hand_penalty(layout: List[str], prev_letter: str, current_letter: str) -> float:
    prev_hand = index_to_pos(layout.index(prev_letter))[1] > 4
    current_hand = index_to_pos(layout.index(current_letter))[1] > 4
    return 1 if prev_hand == current_hand else 0


def dominant_hand_penalty(layout: List[str], current_letter: str) -> float:
    return 1 if index_to_pos(layout.index(current_letter))[1] <= 4 else 0


def pinky_usage_penalty(layout: List[str], letter: str) -> float:
    row, col = index_to_pos(layout.index(letter))
    if row == 1:
        return 0
    return 1 if col == 0 or col == 9 else 0


def calculate_step(layout: List[str], prev_letter: str, current_letter: str) -> float:
    distance_penalty = FINGER_TRAVEL_DISTANCE_WEIGHT * finger_travel_distance_penalty(layout, current_letter)
    hand_penalty = DOMINANT_HAND_WEIGHT * dominant_hand_penalty(layout, current_letter)
    pinky_penalty = PINKY_USAGE_WEIGHT * pinky_usage_penalty(layout, current_letter)
    if not prev_letter:
        return sum([
            distance_penalty,
            hand_penalty,
            pinky_penalty
        ])
    finger_penalty = CONSECUTIVE_FINGER_WEIGHT * consecutive_finger_penalty(layout, prev_letter, current_letter)
    keys_penalty = CONSECUTIVE_HAND_WEIGHT * consecutive_hand_penalty(layout, prev_letter, current_letter)
    return sum([
        distance_penalty,
        finger_penalty,
        keys_penalty,
        hand_penalty,
        pinky_penalty
    ])


def calculate(layout: List[str], text: str) -> float:
    text = t.prepare_text(text)
    sum = 0
    for i in range(len(text)):
        sum += calculate_step(
            layout,
            None if i == 0 else text[i - 1], text[i]
        )
    return sum / len(text)


print(calculate(layouts.qwerty, t.load_text(t.TEXT_PATH)))
