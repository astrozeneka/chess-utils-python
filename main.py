from stockfish import Stockfish
import chess

if __name__ == '__main__':
    # Claude, find
    stockfish_black = Stockfish(path="/opt/homebrew/bin/stockfish") # or "stockfish" if it's in PATH
    stockfish_black.set_elo_rating(500)
    stockfish_white = Stockfish(path="/opt/homebrew/bin/stockfish") # or "stockfish" if it's in PATH
    stockfish_white.set_elo_rating(1500)

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
        best_move = engine.get_best_move()

        #if not best_move:
        #    print("No valid moves available")
        #    break
        move_list.append(best_move)

        # Apply the move to the board
        board.push_uci(best_move)

    print(board.unicode())

    print()