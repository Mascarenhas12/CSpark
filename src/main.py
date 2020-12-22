from collections import Callable
from os import path
from csparkconfig import CSparkConfig
from cspark import CSpark
from selectmenu import SelectMenu
from utils import clear_screen, bold, clear_before


def error_menu(message: str, again_action: Callable, back_action: Callable):
    print('')
    return SelectMenu(
        message=f"Error: {message}",
        choices={'1. Try again': again_action, '2. Go back': lambda: clear_before(back_action)}
    )


def action_exit():
    clear_screen()
    print("Thank you for using CSpark!")
    print("Have a great day :)")
    print("\n")
    print(bold("Exited successfully!"))
    exit(0)


def action_select_game():
    clear_screen()
    print(bold('Select Game -> Select PGN\n'))

    pgn_path = input("PGN file path: ")
    if not path.exists(pgn_path):
        return error_menu(f"File Not Found", action_select_game(),
                          start_menu.select_action).select_action()

    clear_screen()
    print(bold('Select Game -> Select Player Colour\n'))
    colour = SelectMenu(["white", "black"]).select("Choose which side to play:")
    global config
    global cspark
    config = CSparkConfig(pgn_path, colour)
    cspark = CSpark(config)

    return start_menu.select_action()


def action_advance_position(direction: int = 1):
    global current_pos
    clear_screen()
    forward = direction * int(input("Move how many positions?"))
    board = cspark.get_position(current_pos + forward)
    print(bold(board))
    if board != "Position outside of scope":
        current_pos += forward
    return analysis_menu.select_action()


def action_previous_position():
    return action_advance_position(-1)


def action_estimate_position():
    return analysis_menu.select_action()


def action_guess_move():
    return analysis_menu.select_action()


def action_show_position():
    global current_pos
    board = cspark.get_position(current_pos)
    print(bold(board))
    return analysis_menu.select_action()


if __name__ == "__main__":
    config = CSparkConfig
    cspark = CSpark
    current_pos = 0

    start_menu = SelectMenu({
        '1. Select Game': action_select_game,
        '2. Analyse Game': lambda: analysis_menu.select_action(clear_before=True),
        '0. Exit': action_exit
    }, message='Start Menu')

    analysis_menu = SelectMenu({
        '1. Show Position': action_show_position,
        '2. Advance Position': action_advance_position,
        '3. Previous Position': action_previous_position,
        '4. Estimate Position': action_estimate_position,
        '5. Guess Next Move': action_guess_move,
        '6. Return To Start Menu': lambda: start_menu.select_action(clear_before=True),
        '0. Exit': action_exit
    }, message='Analysis Menu')

    clear_screen()

    start_menu.select_action()
