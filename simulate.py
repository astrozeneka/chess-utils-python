from stockfish import Stockfish
import chess
import random
import numpy as np


def softmax_selection(top_moves, temperature=0.5):
    scores = np.array([m['Centipawn'] for m in top_moves])
    # Apply softmax with temperature and numerical stability
    scaled_scores = scores / temperature
    # Subtract max for numerical stability (prevents overflow in exp)
    scaled_scores = scaled_scores - np.max(scaled_scores)
    exp_scores = np.exp(scaled_scores)
    probabilities = exp_scores / exp_scores.sum()
    #print("->", top_moves, probabilities, exp_scores)
    chosen_idx = np.random.choice(len(top_moves), p=probabilities)
    return top_moves[chosen_idx]['Move']


if __name__ == '__main__':
    # Claude, find
    stockfish_black = Stockfish(path="/opt/homebrew/bin/stockfish") # or "stockfish" if it's in PATH
    stockfish_black.set_elo_rating(1200)
    stockfish_white = Stockfish(path="/opt/homebrew/bin/stockfish") # or "stockfish" if it's in PATH
    stockfish_white.set_elo_rating(1100)

    for s in [stockfish_black, stockfish_white]:
        s.update_engine_parameters({
            "Threads": 2,
            # "Minimum Thinking Time": 30,
            "Hash": 2048
        })

    # Start FEN
    start_fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

    # Print to unicode
    board = chess.Board(start_fen)

    move_list = []
    for i in range(300):

        if board.is_game_over():
            print(f"Game over after {i} moves")
            if board.is_checkmate():
                winner = "Black" if board.turn == chess.WHITE else "White"
                print(f"Checkmate! {winner} wins!")
            elif board.is_stalemate():
                print("Stalemate!")
            else:
                print(f"Draw: {board.result()}")
            break

        # Select the engine
        engine = stockfish_white if board.turn == chess.WHITE else stockfish_black
        engine.set_fen_position(board.fen())
        top_moves = engine.get_top_moves(5)
        if any([a['Mate'] is not None for a in top_moves]):
            selected_move = random.choice([m for m in top_moves if m['Mate'] is not None])['Move']
        else:
            selected_move = softmax_selection(top_moves, temperature=0.7) # Deterministic with low temperature

        #if not best_move:
        #    print("No valid moves available")
        #    break
        move_list.append(selected_move)

        # Apply the move to the board
        board.push_uci(selected_move)

    # Open games.txt and append the game in PGN format
    with open("games.txt", "a") as f:
        game_pgn = board.board_fen() + " " + " ".join(move_list) + "\n"
        f.write(game_pgn)

    print("Final board generated")
    print()