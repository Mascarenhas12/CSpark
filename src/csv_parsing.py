import csv
import io
import chess.pgn

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


def csv_extract_ranked_move_prob_data(filepath: str, rank: str):
    with open(filepath, newline='') as csv_file:
        with open('../results/move_prob_data' + rank + '.csv', 'w') as result:
            move_prob = {}
            result.write("move_rank,occurrences\n")
            reader = csv.DictReader(csv_file)

            for row in reader:
                if rank != row['elo_rank']:
                    continue
                if row['move_rank'] not in move_prob:
                    move_prob[row['move_rank']] = 0
                move_prob[row['move_rank']] += 1

            for key in move_prob:
                result.write("" + key + "," + str(move_prob[key]) + "\n")


def csv_get_emv_dict() -> dict:
    emv_dict = dict()
    with open('../results/emv.csv', newline='') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            emv_dict[row['elo_rank']] = float(row['emv'])

    return emv_dict


def csv_create_ranked_move_prob_dict(rank: str) -> dict:
    with open('../results/move_prob_data' + rank + '.csv', 'r') as csv_file:
        reader = csv.DictReader(csv_file)
        move_prob = {}

        for row in reader:
            move_prob[row['move_rank']] = row['occurrences']

    return move_prob
