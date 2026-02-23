# Text-based tic-tac-toe game.
# Written by Leoni Franco Paz.
# Email: leonifrancopaz@hotmail.com
import argparse
import itertools
import os
import sys


HORIZONTAL_PLANE = ("top", "middle", "bottom")
VERTICAL_PLANE = ("left", "middle", "right")


def clear_grid(grid):
    """Replace each cell in the grid with a space."""
    for k, v in grid.items():
        if not isinstance(v, dict):
            grid[k] = ' '
        elif isinstance(v, dict):
            grid[k] = clear_grid(v)
    else:
        return grid


def check_tie(grid):
    """Check if the conditions for a tie are met."""
    cells = []
    for h in HORIZONTAL_PLANE:
        for v in VERTICAL_PLANE:
            cells.append(grid[h][v])

    return ' ' not in cells


def check_win(grid):
    """Check if the conditions for a win is met."""
    lines = []

    # Iterate over the grid's diagonal line from top left to bottom right.
    line = ''
    for h, v in zip(HORIZONTAL_PLANE, VERTICAL_PLANE):
        line += grid[h][v]
    lines.append(line)

    # Iterate over the grid's diagonal line from bottom left to top right.
    line = ''
    for h, v in zip(HORIZONTAL_PLANE, VERTICAL_PLANE[-1::-1]):
        line += grid[h][v]
    lines.append(line)

    # Iterate over the grid's rows.
    for h in HORIZONTAL_PLANE:
        line = ''
        for v in VERTICAL_PLANE:
            line += grid[h][v]
        lines.append(line)

    # Iterate over the grid's columns.
    for v in VERTICAL_PLANE:
        line = ''
        for h in HORIZONTAL_PLANE:
            line += grid[h][v]
        lines.append(line)

    return ("OOO" in lines) or ("XXX" in lines)


def print_grid(grid):
    """Print the grid in a readable format."""
    print(" {0} │ {1} │ {2}".format(*grid["top"].values()))
    print("───┼───┼───")
    print(" {0} │ {1} │ {2}".format(*grid["middle"].values()))
    print("───┼───┼───")
    print(" {0} │ {1} │ {2}\n".format(*grid["bottom"].values()))


def prompt_player_input(grid, player):
    """Prompt the player for input."""
    first_iteration = True

    while True:
        if not first_iteration:
            player_input = input("Invalid input, try again: ").split()
        elif first_iteration:
            player_input = input(player + "'s turn: ").split()
            first_iteration = False

        try:
            if all((len(player_input) == 1,
                    player_input[0] == "center",
                    grid["middle"]["middle"] == ' ')):
                return ("middle", "middle")
            elif all((len(player_input) == 2,
                      player_input[0] in HORIZONTAL_PLANE,
                      player_input[1] in VERTICAL_PLANE,
                      grid[player_input[0]][player_input[1]] == ' ')):
                return (player_input[0], player_input[1])
        except IndexError:
            pass
        except KeyError:
            pass


def prompt_yes_or_no(question):
    """Ask a yes or no question and return the user's answer."""
    first_iteration = True
    while True:
        if not first_iteration:
            user_input = input("Invalid input, try again (Y/n): ").strip()
        elif first_iteration:
            user_input = input(question).strip()
            first_iteration = False

        if user_input in ('N', 'n', 'Y', 'y'):
            return user_input


def play():
    """Play tic-tac-toe."""
    grid = {"top": {"left": ' ', "middle": ' ', "right": ' '},
            "middle": {"left": ' ', "middle": ' ', "right": ' '},
            "bottom": {"left": ' ', "middle": ' ', "right": ' '}}
    scoreboard = {'O': 0, 'X': 0}
    turn_order = ('X', 'O')

    while True:
        for player in itertools.cycle(turn_order):
            os.system("CLS")
            print_grid(grid)
            player_input = prompt_player_input(grid, player)
            grid[player_input[0]][player_input[1]] = player
            if check_tie(grid):
                os.system("CLS")
                print_grid(grid)
                print("Tie!", end="\n\n")
                break
            elif check_win(grid):
                scoreboard[player] += 1
                os.system("CLS")
                print_grid(grid)
                print(player + " wins!", end="\n\n")
                break

        print("O:", scoreboard['O'])
        print("X:", scoreboard['X'], end="\n\n")

        user_input = prompt_yes_or_no("Play again? (Y/n): ")

        if user_input in ('N', 'n'):
            break
        elif user_input in ('Y', 'y'):
            grid = clear_grid(grid)


def main():
    parser = argparse.ArgumentParser(
        prog='tictactoe',
        description='Text-based tic-tac-toe game.',
        epilog=("In order to input a move one must type the level followed by "
                "a side (e.g., top left, center, bottom right).")
        )

    args = parser.parse_args()

    play()


if __name__ == '__main__':
    sys.exit(main())
