import random
from shogi_ai.対局用.盤面 import 盤面
from shogi_ai.ai.ai用関数 import *

def ai_think(board, depth=3):
    best_move = None
    best_score = float('-inf')
    board_moves = board.generate_board_moves(board.turn)
    uchite = board.generate_uchite(board.turn)
    legal_moves = board.filter_shogi_rules(board_moves, uchite)
    random.shuffle(legal_moves)
    for move in legal_moves:
        new_board = board.copy()
        new_board = new_board.apply_move(move)
        # ここから並列処理して，全評価値が出てから比較するように変更予定したい
        score = -1 * tree_search(new_board, depth-1, float('-inf'), float('inf'))
        if score > best_score:
            best_score = score
            best_move = move
    print(f"AI評価値: {best_score}")
    return best_move