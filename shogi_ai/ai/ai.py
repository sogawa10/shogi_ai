from concurrent.futures import ProcessPoolExecutor, as_completed
import random
from shogi_ai.対局用.盤面 import 盤面
from shogi_ai.ai.ai用関数 import *

def evaluate(board, move, depth):
    new_board = board.copy()
    new_board = new_board.apply_move(move)
    score = -1 * tree_search(new_board, depth-1, float('-inf'), float('inf'))
    return score, move

def ai_think(board, depth=3):
    best_move = None
    best_score = float('-inf')
    board_moves = board.generate_board_moves(board.turn)
    uchite = board.generate_uchite(board.turn)
    legal_moves = board.filter_shogi_rules(board_moves, uchite)
    random.shuffle(legal_moves)
    with ProcessPoolExecutor() as executor:
        futures = [
            executor.submit(evaluate, board, move, depth)
            for move in legal_moves
        ]
        for future in as_completed(futures):
            score, move = future.result()
            if score > best_score:
                best_score = score
                best_move = move
                print(f"\r\033[K現在の最善手: {best_move.to_string()}  評価値: {best_score}", end="")
    print("\r\033[K最終結果: " + best_move.to_string() + "  評価値: " + str(best_score))
    return best_move