class StepPenalty:
    distance: float
    finger: float
    keys: float
    hand: float

    def __init__(self, distance: float, finger: float, keys: float, hand: float) -> None:
        self.distance = distance
        self.finger = finger
        self.keys = keys
        self.hand = hand

    def mult(self, factor: float):
        self.distance *= factor
        self.finger *= factor
        self.keys *= factor
        self.hand *= factor
        return self

    @classmethod
    def zero(cls):
        return StepPenalty(0, 0, 0, 0)
