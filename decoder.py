from time import time
from math import log2
from chess import pgn, Board
from util import get_pgn_games

def decode_for_web(pgn_string: str):
    start_time = time()
    total_move_count = 0

    games: list[pgn.Game] = get_pgn_games(pgn_string)
    output_data = ""

    all_steps = []

    for game_index, game in enumerate(games):
        chess_board = Board()

        game_moves = list(game.mainline_moves())
        total_move_count += len(game_moves)

        all_steps.append({
            "fen": chess_board.fen(),
            "move": "START",
            "bit": "",
            "index": len(output_data)
        })

        for move_index, move in enumerate(game_moves):
            legal_move_ucis = [
                legal_move.uci()
                for legal_move in list(chess_board.generate_legal_moves())
            ]

            move_binary = bin(legal_move_ucis.index(move.uci()))[2:]

            if game_index == len(games) - 1 and move_index == len(game_moves) - 1:
                max_binary_length = min(
                    int(log2(len(legal_move_ucis))),
                    8 - (len(output_data) % 8)
                )
            else:
                max_binary_length = int(log2(len(legal_move_ucis)))

            required_padding = max(0, max_binary_length - len(move_binary))
            move_binary = ("0" * required_padding) + move_binary

            output_data += move_binary

            chess_board.push_uci(move.uci())

            all_steps.append({
                "fen": chess_board.fen(),
                "move": move.uci(),
                "bit": move_binary,
                "index": len(output_data)
            })

    decoded_bytes = bytes([
        int(output_data[i * 8 : i * 8 + 8], 2)
        for i in range(len(output_data) // 8)
    ])

    print(
        f"\nsukses decode pgnya bang "
        + f"{len(games)} game(s), {total_move_count} total move(s)"
        + f" ({round(time() - start_time, 3)}s)."
    )

    return decoded_bytes, all_steps
