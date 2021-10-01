from cardStack import CardStack
from card import RankCard, SuitCard
import random
import utils
import copy

class Game:

    NUM_STD_CARD_STACKS = 9

    @classmethod
    def setup_random(cls):
        cards = utils.generate_card_list()
        random.shuffle(cards)
        standard_card_stacks = []
        for i in range(cls.NUM_STD_CARD_STACKS):
            stack_cards = cards[(i * 4):(i * 4) + 4]
            standard_card_stacks.append(CardStack(stack_cards))
        spare_card_stack = CardStack()
        return cls(standard_card_stacks, spare_card_stack)

    @classmethod
    def setup_hash(cls, game_hash):
        '''10R,DR,DR|...|...|6R'''
        valid, reason = cls.__validate_hash(game_hash)
        if not valid:
            raise Exception(f"Invalid game hash provided: ${reason}")

        # ["10R,DR", "6R,9B", ...]"
        stack_strs = game_hash.split("|")

        std_card_stacks = []
        std_stack_strs = stack_strs[:-1]
        for stack_str in std_stack_strs:
            cards_list = []
            # ["10R", "DR"]
            card_strs = stack_str.split(",")
            for card_str in card_strs:
                card = cls.__get_card_from_str(card_str)
                cards_list.append(card)
            std_card_stacks.append(CardStack(cards_list))

        spare_stack_str = stack_strs[-1]
        spare_card_list = []
        if spare_stack_str is not None and spare_stack_str != "":
            spare_card = cls.__get_card_from_str(spare_stack_str)
            spare_card_list.append(spare_card)
        spare_card_stack = CardStack(spare_card_list)

        return Game(std_card_stacks, spare_card_stack)

    @staticmethod
    def __get_card_from_str(str):
        rank_or_suit = str[:-1]
        colour = str[-1]
        if rank_or_suit.isdigit():
            return RankCard(colour, int(rank_or_suit))
        else:
           return SuitCard(colour, rank_or_suit)


    @staticmethod
    def __validate_hash(game_hash):
        if game_hash is None:
            return False, "Hash is None"

        if game_hash == "":
            return False, "Hash is empty string"

        pipes_count = game_hash.count("|")
        if pipes_count != 9:
            return False, f"Expected 9 pipes but found ${pipes_count}"

        stack_strs = game_hash.split("|")
        card_strs = ','.join(stack_strs).split(',')

        # TODO

        return True, None

    def __init__(self, standard_card_stacks, spare_card_stack):
        self.standard_card_stacks = standard_card_stacks
        self.spare_card_stack = spare_card_stack
        self.all_card_stacks = self.standard_card_stacks + [self.spare_card_stack]

    def __hash__(self):
        return hash(tuple(self.all_card_stacks))

    def __eq__(self, other):
        return type(other) is Game and hash(self) == hash(other)

    def __repr__(self):
        return '\n'.join((str(stack) for stack in self.all_card_stacks))

    def enumerate_moves(self):
        moves = []

        # If spare cell is empty, any bottom card from any stack
        # can potentially move there
        spare_card_stack_index = len(self.all_card_stacks) - 1
        if self.spare_card_stack.is_empty():
            for from_stack_index, from_stack in enumerate(self.standard_card_stacks):
                if from_stack.is_solved or from_stack.is_empty():
                    continue
                card = from_stack.peek()
                move = Move([card], from_stack_index, spare_card_stack_index)
                moves.append(move)


        # For every card from every stack, if a bottom card
        # from another standard stack can receive card(s) then move is valid
        # for from_stack_index, from_stack in enumerate(self.all_card_stacks):
        #     if from_stack.is_solved:
        #         continue
        #     for from_card_index, from_stack_card in enumerate(from_stack):
        #         for to_stack_index, to_stack in enumerate(self.standard_card_stacks):
        #             if to_stack.is_solved:
        #                 continue
        #             if from_stack_index == to_stack_index:
        #                 continue
        #             if to_stack.can_receive(from_stack_card):
        #                 cards = from_stack[from_card_index:]
        #                 move = Move(cards, from_stack_index, to_stack_index)
        #                 moves.append(move)

        # For every card from every stack, if a bottom card
        # from another standard stack can receive card(s) then move is valid
        for from_stack_index, from_stack in enumerate(self.all_card_stacks):
            if from_stack.is_empty() or from_stack.is_solved:
                continue
            movable_cards = from_stack.enumerate_movable_cards()
            if len(movable_cards) == 0:
                continue
            for to_stack_index, to_stack in enumerate(self.standard_card_stacks):
                if to_stack.is_solved:
                    continue
                if from_stack_index == to_stack_index:
                    continue
                for card_group in movable_cards:
                    if to_stack.can_receive(card_group[0]):
                        move = Move(card_group, from_stack_index, to_stack_index)
                        moves.append(move)

        return moves

    def is_solved(self):
        return sum([1 for card_stack in self.standard_card_stacks if card_stack.is_solved]) == 8

    def apply_move(self, move):
        next_game = copy.deepcopy(self)
        if len(move.cards) == 0:
            return next_game
        next_game.move_cards(move.from_stack_index, move.to_stack_index, len(move.cards))
        return next_game

    def move_cards(self, from_stack_index, to_stack_index, count):
        from_stack = self.all_card_stacks[from_stack_index]
        to_stack = self.all_card_stacks[to_stack_index]

        moving_cards = from_stack.pop(count)

        top_moving_card = moving_cards[0]
        if not to_stack.can_receive(top_moving_card):
            bottom_stack_card = to_stack.peek()
            raise Exception(f'Illegal move - attempted to move {top_moving_card} onto {bottom_stack_card}')

        self.all_card_stacks[to_stack_index].append(moving_cards)

class Move:
    def __init__(self, cards, from_stack_index, to_stack_index):
        self.cards = cards
        self.from_stack_index = from_stack_index
        self.to_stack_index = to_stack_index

    def __repr__(self):
        from_stack = self.from_stack_index + 1
        to_stack = self.to_stack_index + 1

        return f'Move {self.cards} from stack {from_stack} to {to_stack}'