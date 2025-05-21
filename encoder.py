from time import time
from math import log2
from chess import Board, pgn
from util import to_binary_string


def encode_for_web(file_bytes: str):
    start_time = time()

    file_bytes = list(file_bytes)
    file_bits_count = len(file_bytes) * 8
    file_bit_index = 0
    chess_board = Board()

    all_steps = [{
        "fen": chess_board.fen(),  # posisi awal
        "move": "START",
        "bit": "",
        "index": 0
    }]

    output_pgns = []  # Tempat menyimpan semua PGN

    while True:
        legal_moves = list(chess_board.generate_legal_moves())
        move_bits = {}

        max_binary_length = min(
            int(log2(len(legal_moves))),
            file_bits_count - file_bit_index
        )

        for index, legal_move in enumerate(legal_moves):
            move_binary = to_binary_string(index, max_binary_length)
            if len(move_binary) > max_binary_length:
                break
            move_bits[legal_move.uci()] = move_binary

        closest_byte_index = file_bit_index // 8
        file_chunk_pool = "".join([
            to_binary_string(byte, 8)
            for byte in file_bytes[closest_byte_index : closest_byte_index + 2]
        ])

        next_file_chunk = file_chunk_pool[
            file_bit_index % 8
            : file_bit_index % 8 + max_binary_length
        ]

        chosen_move = None
        for move_uci, move_binary in move_bits.items():
            if move_binary == next_file_chunk:
                chosen_move = move_uci
                break

        if chosen_move:
            chess_board.push_uci(chosen_move)
        else:
            # reset board & record it as restart
            all_steps.append({
                "fen": chess_board.fen(),
                "move": "RESTART",
                "bit": next_file_chunk,
                "index": file_bit_index + 1,
            })
            chess_board = Board()
            continue

        all_steps.append({
            "fen": chess_board.fen(),
            "move": chosen_move,
            "bit": next_file_chunk,
            "index": file_bit_index + 1,
        })

        file_bit_index += max_binary_length

        eof_reached = file_bit_index >= file_bits_count

        if (
            chess_board.legal_moves.count() <= 1
            or chess_board.is_insufficient_material()
            or chess_board.can_claim_draw()
            or eof_reached
        ):
            # Simpan state terakhir sebelum reset sebagai PGN
            if chess_board.move_stack:
                pgn_game = pgn.Game()
                pgn_game.add_line(chess_board.move_stack)
                output_pgns.append(str(pgn_game))

            all_steps.append({
                "fen": chess_board.fen(),
                "move": "RESET",
                "bit": "",
                "index": file_bit_index + 1,
            })
            chess_board.reset()

        if eof_reached:
            break

    print(
        f"Sukses encode {len(file_bytes)} byte jadi {len(all_steps)} langkah "
        f"({round(time() - start_time, 3)}s)"
    )

    return all_steps, output_pgns