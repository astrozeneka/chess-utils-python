from stockfish import Stockfish
import chess

if __name__ == '__main__':
    # Claude, find
    stockfish = Stockfish(path="/opt/homebrew/bin/stockfish")  # or "stockfish" if it's in PATH

    # Configure
    stockfish.update_engine_parameters({
        "Threads": 2,
        "Minimum Thinking Time": 30,
        "Hash": 2048
    })

    # Start FEN
    start_fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

    # Print to unicode
    board = chess.Board(start_fen)

    for i in range(2):

        # Get best move from Stockfish
        best_move = stockfish.get_best_move()
        print(f"Best move: {best_move}")

        # Apply the move to the board
        board.push_uci(best_move)

    print(board.unicode())

    print()