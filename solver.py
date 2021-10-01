from priorityQueue import MaxPriorityQueue
import time

class Node:
    def __init__(self, prev_node, game, move, depth, score):
        self.prev_node = prev_node
        self.game = game
        self.move = move
        self.depth = depth
        self.score = score

    def __lt__(self, other):
        # ie. worse than other object
        if self.score != other.score:
            return self.score < other.score
        return self.depth > other.score

def score_game(game):
    return sum(score_stack(card_stack) for card_stack in game.standard_card_stacks)

def score_stack(card_stack):
    if card_stack.is_solved:
        return 10

    return sum([1 for i in range(len(card_stack)-1) if card_stack[i].can_receive(card_stack[i+1])])

def ordered_cards(card_stack):
    cards_list = card_stack.card_stack
    num_ordered_cards = sum(1 for i in range(len(cards_list)-1) if cards_list[i].can_receive(cards_list[i]))
    return num_ordered_cards

def get_game_states(solved_node):
    return get_result_list(solved_node, lambda n: n.game)

def get_result_list(solved_node, data_func):
    states = []
    current = solved_node
    while current is not None:
        states.append(data_func(current))
        current = current.prev_node
    return list(reversed(states))

def get_moves(solved_node):
    return get_result_list(solved_node, lambda n: n.move)

def solve(game, max_time=60):
    priority_queue = MaxPriorityQueue()
    initial_node = Node(None, game, None, 0, 0)
    discovered_states = set([game])
    priority_queue.enqueue(initial_node)

    max_score = 0
    start_time = time.time()

    while time.time() - start_time < max_time and priority_queue:
        current_node = priority_queue.dequeue()

        if current_node.game.is_solved():
            return get_moves(current_node)

        for move in current_node.game.enumerate_moves():
            next_game = current_node.game.apply_move(move)

            if next_game not in discovered_states:
                discovered_states.add(next_game)
                depth = current_node.depth + 1
                game_score = score_game(next_game)
                next_node = Node(current_node, next_game, move, depth, game_score)

                priority_queue.enqueue(next_node)

    return None