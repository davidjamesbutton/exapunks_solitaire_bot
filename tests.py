import unittest
import utils
from card import SuitCard, RankCard
from cardStack import CardStack
from game import Game
from priorityQueue import MinPriorityQueue, MaxPriorityQueue

class TestCardClass(unittest.TestCase):

    def test_can_receive(self):
        cards = utils.generate_card_list()
        for card_one in cards:
            count = 0
            for card_two in cards:
                if card_one.can_receive(card_two):
                    count += 1
            if type(card_one) is RankCard:
                if card_one.rank == 6:
                    self.assertEqual(0, count)
                else:
                    self.assertEqual(2, count)
            elif type(card_one) is SuitCard:
                self.assertEqual(4, count)

    def test_eq(self):
        cards = utils.generate_card_list()
        for card_one in cards:
            count = 0
            for card_two in cards:
                if card_one == card_two:
                    count += 1
            if type(card_one) is RankCard:
                self.assertEqual(2, count)
            if type(card_one) is SuitCard:
                self.assertEqual(4, count)

    def test_hash(self):
        cards = utils.generate_card_list()
        for card_one in cards:
            count = 0
            for card_two in cards:
                if hash(card_one) == hash(card_two):
                    count += 1
            if type(card_one) is RankCard:
                self.assertEqual(2, count)
            if type(card_one) is SuitCard:
                self.assertEqual(4, count)

class TestCardStackClass(unittest.TestCase):

    def test_init_cards(self):
        card_stack = CardStack([1, 2, 3])
        self.assertEqual(3, len(card_stack))

    def test_append(self):
        card_stack = CardStack()
        c1 = RankCard('B', 6)
        c2 = RankCard('R', 7)
        c3 = RankCard('B', 8)
        c4 = RankCard('R', 9)
        c5 = RankCard('B', 10)

        card_stack.append([c5])
        self.assertEqual(1, len(card_stack))
        self.assertFalse(card_stack.is_solved)

        card_stack.append([c4, c3, c2, c1])
        self.assertEqual(5, len(card_stack))
        self.assertTrue(card_stack.is_solved)

    def test_peek(self):
        c1 = RankCard('B', 6)
        c2 = RankCard('R', 7)

        card_stack = CardStack([c1])
        peeked_card = card_stack.peek()
        self.assertEqual(6, peeked_card.rank)

        card_stack.append([c2])
        peeked_card_2 = card_stack.peek()
        self.assertEqual(7, peeked_card_2.rank)

    def test_pop(self):
        c1 = RankCard('B', 6)
        c2 = RankCard('R', 7)
        c3 = RankCard('B', 8)
        c4 = RankCard('R', 9)
        c5 = RankCard('B', 10)
        card_stack = CardStack([c1, c2, c3, c4, c5])

        popped_cards = card_stack.pop()
        self.assertEqual(1, len(popped_cards))
        self.assertEqual(4, len(card_stack))
        self.assertEqual(10, popped_cards[0].rank)

        popped_cards = card_stack.pop(3)
        self.assertEqual(3, len(popped_cards))
        self.assertEqual(1, len(card_stack))
        self.assertEqual(9, popped_cards[-1].rank)

    def test_can_receive(self):
        c3 = RankCard('B', 8)
        c4 = RankCard('R', 9)
        c5 = RankCard('B', 10)

        card_stack = CardStack([c5])

        self.assertFalse(card_stack.can_receive(c3))
        self.assertTrue(card_stack.can_receive(c4))

    def test_hash(self):
        c1 = RankCard('B', 8)
        c2 = RankCard('B', 9)
        c3 = RankCard('B', 8)
        c4 = RankCard('B', 9)
        card_stack_one = CardStack([c1, c2])
        card_stack_two = CardStack([c3, c4])

        self.assertEqual(hash(card_stack_one), hash(card_stack_two))

    def test_solved(self):
        cards = [SuitCard('B', 'S')] * 3 + [RankCard('B', 10)]
        card_stack = CardStack(cards)
        self.assertFalse(card_stack.is_solved)

    def test_enumerate_movable_cards(self):
        card_stack = CardStack()
        self.assertEqual(0, len(card_stack.enumerate_movable_cards()))

        card_stack = CardStack([SuitCard('B', 'S')])
        self.assertEqual(1, len(card_stack.enumerate_movable_cards()))

        card_stack = CardStack([SuitCard('B', 'S')] * 3)
        self.assertEqual(3, len(card_stack.enumerate_movable_cards()))

class TestGameClass(unittest.TestCase):

    def test_setup_random(self):
        game = Game.setup_random()

        card_count = sum(len(stack) for stack in game.all_card_stacks)
        self.assertEqual(36, card_count)

        unique_cards = set()
        for stack in game.all_card_stacks:
            for card in stack:
                unique_cards.add(card)
        self.assertEqual(14, len(unique_cards))

    def test_enumerate_cards(self):
        game = Game.setup_random()

        moves = game.enumerate_moves()
        self.assertTrue(len(moves) > 0)

        for move in moves:
            self.assertTrue(len(move.cards) > 0)
            top_move_card = move.cards[0]
            to_stack = game.all_card_stacks[move.to_stack_index]
            self.assertTrue(to_stack.can_receive(top_move_card))

    def test_apply_move(self):
        game = Game.setup_random()
        game_hash = hash(game)

        moves = game.enumerate_moves()

        for move in moves:
            next_game = game.apply_move(move)

            card_count_next_game = sum(len(stack) for stack in next_game.all_card_stacks)
            self.assertEqual(36, card_count_next_game)

            card_count_game = sum(len(stack) for stack in game.all_card_stacks)
            self.assertEqual(36, card_count_game)

            self.assertEqual(game_hash, hash(game))
            self.assertNotEqual(hash(game), hash(next_game))

            card_count = len(move.cards)

            from_stack = next_game.all_card_stacks[move.from_stack_index]
            from_initial_cards = 4
            if move.from_stack_index == len(next_game.all_card_stacks) - 1:
                from_initial_cards = 0
            if from_initial_cards - card_count != len(from_stack):
                self.assertEqual(from_initial_cards - card_count, len(from_stack))

            to_stack = next_game.all_card_stacks[move.to_stack_index]
            to_initial_cards = 4
            if move.to_stack_index == len(next_game.all_card_stacks) - 1:
                to_initial_cards = 0
            self.assertEqual(to_initial_cards + card_count, len(to_stack))

class Comparable:
    def __init__(self, number):
        self.number = number
    def __lt__(self, other):
        return self.number < other.number

class TestMinPriorityQueueClass(unittest.TestCase):

    def test_primitives(self):
        queue = MinPriorityQueue()
        nums = [5, 1, 10, 3, -1]
        for num in nums:
            queue.enqueue(num)
        for num in sorted(nums):
            self.assertEqual(num, queue.dequeue())

    def test_objects(self):
        queue = MinPriorityQueue()
        nums = [5, 1, 10, 3, -1]
        for num in nums:
            queue.enqueue(Comparable(num))
        for num in sorted(nums):
            self.assertEqual(num, queue.dequeue().number)

class TestMaxPriorityQueueClass(unittest.TestCase):

    def test_primitives(self):
        queue = MaxPriorityQueue()
        nums = [5, 1, 10, 3, -1]
        for num in nums:
            queue.enqueue(num)
        for num in sorted(nums, reverse=True):
            self.assertEqual(num, queue.dequeue())

    def test_objects(self):
        queue = MaxPriorityQueue()
        nums = [5, 1, 10, 3, -1]
        for num in nums:
            queue.enqueue(Comparable(num))
        for num in sorted(nums, reverse=True):
            self.assertEqual(num, queue.dequeue().number)

if __name__ == '__main__':
    unittest.main()