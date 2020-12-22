import os
from typing import Callable
import chess
import chess.pgn


def clear_screen():
    # for windows
    if os.name == 'nt':
        _ = os.system('cls')
    # for mac and linux(here, os.name is 'posix')
    else:
        _ = os.system('clear')


def clear_before(func: Callable):
    clear_screen()
    func()


def bold(text: str) -> str:
    return "\033[1m" + text + "\033[0m"


def extract_elo_from_pgn(pgn_path, colour):
    elo_dict = dict()
    with open(pgn_path, 'r') as pgn:
        game = chess.pgn.read_game(pgn)

    if colour == "white":
        elo_dict['elo'] = game.headers.get('WhiteElo')
        elo_dict['opponent_elo'] = game.headers.get('BlackElo')
    else:
        elo_dict['elo'] = game.headers.get('BlackElo')
        elo_dict['opponent_elo'] = game.headers.get('WhiteElo')

    return elo_dict


def estimated_move_value(emv_dict: dict, elo) -> float:
    # 1400-1499 elo is R14
    rank = "R" + str(int(elo) // 100)
    return emv_dict.get(rank)


def convert_dict_to_pawn_value(evaluation: dict) -> float:
    if evaluation.get('type') == "mate":
        polarity = (-1, 1)[evaluation.get('value') > 0]
        return 327.65 * polarity - 10 * evaluation.get('value')
    else:
        return evaluation.get('value') / 100
