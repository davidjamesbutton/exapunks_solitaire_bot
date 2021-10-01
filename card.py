class Card:
    def __init__(self, colour):
        self.colour = colour

    def can_receive(self, card):
        raise NotImplementedError()


class RankCard(Card):
    def __init__(self, colour, rank):
        super().__init__(colour)
        self.rank = rank

    def __repr__(self):
        return f'{self.rank}{self.colour}'

    def __hash__(self):
        return hash((self.colour, self.rank))

    def __eq__(self, other):
        return type(other) is RankCard and hash(self) == hash(other)

    def can_receive(self, card):
        if type(card) is not type(self):
            return False
        if card.rank != self.rank - 1:
            return False
        if card.colour == self.colour:
            return False
        return True


class SuitCard(Card):
    def __init__(self, colour, suit):
        super().__init__(colour)
        self.suit = suit

    def __repr__(self):
        return f'{self.suit}{self.colour}'

    def __hash__(self):
        return hash((self.colour, self.suit))

    def __eq__(self, other):
        return type(other) is SuitCard and hash(self) == hash(other)

    def can_receive(self, card):
        if type(card) is not type(self):
            return False
        if card.suit != self.suit:
            return False
        return True