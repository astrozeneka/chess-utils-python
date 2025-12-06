from stockfish import Stockfish

if __name__ == '__main__':
    # Claude, find
    stockfish = Stockfish(path="/opt/homebrew/bin/stockfish")  # or "stockfish" if it's in PATH

    # Configure
    stockfish.update_engine_parameters({
        "Threads": 2,
        "Minimum Thinking Time": 30,
        "Hash": 2048
    })

    # Set a position using FEN
    stockfish.set_fen_position("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")

    print()