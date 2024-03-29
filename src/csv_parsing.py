import csv
import io
import chess.pgn


def csv_get_emv_dict():
    emv_dict = dict()
    with open('../results/emv.csv', newline='') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            emv_dict[row['elo_rank']] = float(row['emv'])

    return emv_dict


def csv_convert_moves_to_pgn(name: str, moves_str, white_elo, black_elo):
    pgn = io.StringIO(moves_str)
    game = chess.pgn.read_game(pgn)
    game.headers["WhiteElo"] = white_elo
    game.headers["BlackElo"] = black_elo
    with open("../games/pgn/" + name + ".pgn", 'w+') as file:
        file.write(game.__str__())


def csv_create_basic_pgn(filepath: str):
    with open(filepath, newline='') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            csv_convert_moves_to_pgn(row['white_id'] + " vs " + row['black_id'] + "," + row['created_at'],
                                     row['moves'],
                                     row['white_rating'],
                                     row['black_rating'])
