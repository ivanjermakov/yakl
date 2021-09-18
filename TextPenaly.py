from typing import *

from StepPenalty import StepPenalty


class TotalPenalty:
    distance: float
    finger: float
    keys: float
    hand: float
    pinky: float

    def __init__(self, step_penalties: List[StepPenalty]) -> None:
        self.distance = sum(map(lambda s: s.distance, step_penalties)) / len(step_penalties)
        self.finger = sum(map(lambda s: s.finger, step_penalties)) / len(step_penalties)
        self.keys = sum(map(lambda s: s.keys, step_penalties)) / len(step_penalties)
        self.hand = sum(map(lambda s: s.hand, step_penalties)) / len(step_penalties)
        self.pinky = sum(map(lambda s: s.pinky, step_penalties)) / len(step_penalties)

    def __repr__(self) -> str:
        return f'[' \
               f'\n\tdistance:\t{round(self.distance, 4)}' \
               f'\n\tfinger:\t\t{round(self.finger, 4)}' \
               f'\n\tkeys:\t\t{round(self.keys, 4)}' \
               f'\n\thand:\t\t{round(self.hand, 4)}' \
               f'\n\tpinky:\t\t{round(self.pinky, 4)}' \
               f'\n\t------------------' \
               f'\n\ttotal:\t\t{round(self.sum(), 4)}' \
               f'\n]'

    def as_list(self) -> List[float]:
        return [
            self.distance,
            self.finger,
            self.keys,
            self.hand,
            self.pinky
        ]

    def sum(self) -> float:
        return sum(self.as_list())
