from card import RankCard, SuitCard

class CardStack:
    def __init__(self, cards=[]):
        self.card_stack = [card for card in cards]
        self.is_solved = self.__calc_is_solved()

    def __repr__(self):
        return str(self.card_stack)

    def __len__(self):
        return len(self.card_stack)

    def __iter__(self):
        return self.card_stack.__iter__()

    def __getitem__(self, item):
        return self.card_stack[item]

    def __hash__(self):
        return hash(tuple(self.card_stack))

    def __eq__(self, other):
        return type(other) is CardStack and hash(self) == hash(other)

    def append(self, cards):
        if self.is_solved:
            raise Exception("Cannot append to a solved stack!")

        self.card_stack = self.card_stack + cards
        self.is_solved = self.__calc_is_solved()

    def peek(self):
        return self.card_stack[-1]

    def pop(self, count=1):
        if self.is_solved:
            raise Exception("Cannot pop from a solved stack!")

        popped_cards = self.card_stack[len(self.card_stack)-count:]

        if len(popped_cards) != count:
            raise Exception(f'Expected to pop {count} cards but only removed {len(popped_cards)}')

        self.card_stack = self.card_stack[:-count]

        self.is_solved = self.__calc_is_solved()

        return popped_cards

    def is_empty(self):
        return len(self.card_stack) == 0

    def can_receive(self, card):
        return self.is_empty() or self.peek().can_receive(card)

    def __calc_is_solved(self):
        if len(self.card_stack) < 4:
            return False

        first_card = self.card_stack[0]

        if type(first_card) is RankCard and len(self.card_stack) != 5:
            return False
        if type(first_card) is SuitCard and len(self.card_stack) != 4:
            return False

        current_card = first_card
        for i in range(1, len(self.card_stack)):
            next_card = self.card_stack[i]
            if not current_card.can_receive(next_card):
                return False
            current_card = next_card
        return True

    def enumerate_movable_cards(self):
        if self.is_solved or self.is_empty():
            return []

        current_card = self.card_stack[-1]
        movable_card_lists = [[current_card]]
        for card_index in range(len(self.card_stack)-2, -1, -1):
            next_card = current_card
            current_card = self.card_stack[card_index]
            if not current_card.can_receive(next_card):
                break
            movable_card_lists.append(self.card_stack[card_index:])

        return movable_card_lists


