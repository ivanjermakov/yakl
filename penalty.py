from typing import List

from Bigram import Bigram
from StepPenalty import StepPenalty
from TextPenaly import TotalPenalty

SPACE = ' '

FINGER_TRAVEL_DISTANCE_WEIGHT = .4
CONSECUTIVE_FINGER_WEIGHT = .1
CONSECUTIVE_HAND_WEIGHT = .1
DOMINANT_HAND_WEIGHT = .1
PINKY_USAGE_WEIGHT = .1

LAYOUT_SIZE: (int, int) = (4, 10)

DISTANCE_MAP: List[float] = [
    .3, .3, .3, .3, .7, .7, .3, .3, .3, .3,
    .0, .0, .0, .0, .5, .5, .0, .0, .0, .0,
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


def calculate_step(layout: List[str], prev_letter: str, current_letter: str) -> StepPenalty:
    if current_letter == SPACE:
        return StepPenalty.zero()

    travel_distance_p_w = FINGER_TRAVEL_DISTANCE_WEIGHT * finger_travel_distance_penalty(layout, current_letter)
    dominant_hand_p_w = DOMINANT_HAND_WEIGHT * dominant_hand_penalty(layout, current_letter)
    pinky_usage_p_w = PINKY_USAGE_WEIGHT * pinky_usage_penalty(layout, current_letter)

    if not prev_letter or prev_letter == SPACE:
        return StepPenalty(
            travel_distance_p_w,
            0,
            0,
            dominant_hand_p_w,
            pinky_usage_p_w
        )

    consecutive_finger_p_w = CONSECUTIVE_FINGER_WEIGHT * consecutive_finger_penalty(layout, prev_letter, current_letter)
    consecutive_hand_p_w = CONSECUTIVE_HAND_WEIGHT * consecutive_hand_penalty(layout, prev_letter, current_letter)

    return StepPenalty(
        travel_distance_p_w,
        consecutive_finger_p_w,
        consecutive_hand_p_w,
        dominant_hand_p_w,
        pinky_usage_p_w
    )


def calculate(layout: List[str], text: str) -> TotalPenalty:
    step_penalties: List[StepPenalty] = []
    for i in range(len(text)):
        step_penalties.append(
            calculate_step(
                layout,
                None if i == 0 else text[i - 1], text[i]
            )
        )
    return TotalPenalty(step_penalties)


def calculate_bigrams(layout: List[str], bigrams: List[Bigram]) -> TotalPenalty:
    step_penalties: List[StepPenalty] = []
    for bigram in bigrams:
        step_penalties.append(calculate_step(layout, bigram.first, bigram.next).mult(bigram.probability * 100))
    return TotalPenalty(step_penalties)
