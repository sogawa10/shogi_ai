from copy import deepcopy
from shogi_ai.対局用.盤面 import 盤面
from shogi_ai.ai.ai用関数 import *

def ai_think(board, depth=3):
    best_move = None
    best_score = float('-inf')
    board_moves = board.generate_board_moves(board.turn)
    uchite = board.generate_uchite(board.turn)
    legal_moves = board.filter_shogi_rules(board_moves, uchite)
    for move in legal_moves:
        new_board = deepcopy(board)
        new_board = new_board.apply_move(move)
        # ここのαとβあってるか確認
        score = -1 * tree_search(new_board, depth, float('-inf'), float('inf'))
        if score > best_score:
            best_move = move
    return best_move