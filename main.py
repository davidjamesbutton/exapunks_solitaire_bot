from game import Game
from solver import solve
import time

def main():
    if True:
        games = 10
        timeout = 10
        get_stats(games, timeout)

    if False:
        game = Game.setup_random()
        print(game)
        print()
        moves = game.enumerate_moves()
        [print(move) for move in moves]

    if False:
        game_hash = "DR,7B,CB,9B|7R,HR,DR,SB|9B,10R,10B,6B|CB,8R,HR,6R|SB,CB,10R,HR|8B,SB,8B,6R|7B,10B,9R,9R|6B,8R,HR,CB|DR,7R,SB,DR|"
        game = Game.setup_hash(game_hash)
        print(game)
        print()
        solution = solve(game)
        for state in solution:
            print(state)
            print()

def get_stats(count, max_time):
    print(f"Solving {count} games with timeout of {max_time} sec")

    solved_games = []

    for i in range(count):
        print(f"Game {i+1}")
        game = Game.setup_random()

        start_time = time.time()
        solution = solve(game, max_time)
        elapsed_time = time.time() - start_time

        if solution:
            result = (len(solution), elapsed_time)
            solved_games.append(result)

    avg_moves = average([r[0] for r in solved_games])
    avg_time = average([r[1] for r in solved_games])
    print(f"Solved {len(solved_games)} games with averages - moves: {int(avg_moves)}, time: {round(avg_time, 2)} sec")


def average(list_nums):
    return sum(list_nums) / len(list_nums)

if __name__ == "__main__":
    main()