class Bigram:
    first: chr
    next: chr
    probability: float

    def __init__(self, first: chr, next: chr, probability: float):
        self.first = first
        self.next = next
        self.probability = probability

    def __repr__(self):
        return f'{self.first}{self.next},{self.probability}'
