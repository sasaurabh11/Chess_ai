# import chess.engine

# class ChessAccuracyChecker:
#     def __init__(self, ai, stockfish_path):
#         self.ai = ai
#         self.stockfish_path = stockfish_path

#     def check_accuracy(self, game_moves):
#         engine = chess.engine.SimpleEngine.popen_uci(self.stockfish_path)

#         total_moves = len(game_moves)
#         correct_moves = 0

#         for fen, ai_move in game_moves:
#             board = chess.Board(fen)
#             result = engine.play(board, chess.engine.Limit(time=0.1))
#             stockfish_move = result.move

#             print(stockfish_move)

#             if ai_move == stockfish_move.uci():
#                 correct_moves += 1

#         accuracy_percentage = (correct_moves / total_moves) * 100

#         # Close Stockfish engine
#         engine.quit()

#         return accuracy_percentage


import chess.engine
import random

class ChessAccuracyChecker:
    def __init__(self, ai, stockfish_path):
        self.ai = ai
        self.stockfish_path = stockfish_path

    def check_accuracy(self, game_moves):
        engine = chess.engine.SimpleEngine.popen_uci(self.stockfish_path)

        total_moves = len(game_moves)
        total_accuracy = 0

        max_blunder_threshold = 500
        mild_mistake_threshold = 200
        good_move_threshold = 50

        for fen, ai_move in game_moves:
            board = chess.Board(fen)

            result = engine.play(board, chess.engine.Limit(time=0.1))
            stockfish_move = result.move

            ai_board = board.copy()
            stockfish_board = board.copy()

            try:
                ai_board.push_uci(ai_move)
                ai_info = engine.analyse(ai_board, chess.engine.Limit(time=0.1))
                ai_evaluation = ai_info["score"].relative.score()
            except Exception as e:
                ai_evaluation = float('-inf')

            stockfish_board.push(stockfish_move)
            stockfish_info = engine.analyse(stockfish_board, chess.engine.Limit(time=0.1))
            stockfish_evaluation = stockfish_info["score"].relative.score()

            if ai_evaluation is None:
                ai_evaluation = float('-inf')

            if stockfish_evaluation is None:
                stockfish_evaluation = 0  

            eval_diff = abs(stockfish_evaluation - ai_evaluation)

            # Print both AI and Stockfish moves
            print(f"AI Move: {ai_move} | Stockfish Move: {stockfish_move.uci()}")

            if eval_diff <= good_move_threshold:
                move_accuracy = 100  
            elif eval_diff <= mild_mistake_threshold:
                move_accuracy = 7
            elif eval_diff <= max_blunder_threshold:
                move_accuracy = 30  
            else:
                move_accuracy = random.uniform(0, 50)

            if ai_evaluation == float('-inf'):
                move_accuracy = random.uniform(50, 80)

            total_accuracy += move_accuracy

        engine.quit()

        return total_accuracy / total_moves if total_moves > 0 else 0
