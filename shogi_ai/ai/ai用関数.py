import random
from shogi_ai.駒 import *

# 盤面評価用関数
def evaluate(board):
    piece_values = {
        王: {"王": 15000, "玉": 15000},
        歩: {"歩": 100, "と": 700},
        金: {"金": 690},
        銀: {"銀": 640, "金": 670},
        桂: {"桂": 450, "金": 630},
        香: {"香": 430, "金": 630},
        飛: {"飛": 990, "龍": 1300},
        角: {"角": 890, "馬": 1150},
    }
    score = 0
    if board.turn == "先手":
        enemy = "後手"
    else:
        enemy = "先手"
    # 駒評価
    for y in range(9):
        for x in range(9):
            koma = board.board[x][y]
            if koma is None:
                continue
            if koma.sente_or_gote() == board.turn:
                score += piece_values[type(koma)][koma.symbol()[1]]
            else:
                score -= piece_values[type(koma)][koma.symbol()[1]]
    for koma in board.mochigoma[board.turn]:
        score += piece_values[type(koma)][koma.symbol()[1]] * 1.2
    for koma in board.mochigoma[enemy]:
        score -= piece_values[type(koma)][koma.symbol()[1]] * 1.2
    return score

# 木探索
def tree_search(board, depth, alpha, beta):
    # リーフ
    if board.is_checkmate(board.turn):
        return -100000 + depth
    if depth == 0:
        return evaluate(board)
    # ノード
    captur_moves = []
    nari_moves = []
    other_moves = []
    best_score = float('-inf')
    board_moves = board.generate_board_moves(board.turn)
    uchite = board.generate_uchite(board.turn)
    legal_moves = board.filter_shogi_rules(board_moves, uchite)
    for move in legal_moves:
        if move.komadori is not None:
            captur_moves.append(move)
        elif move.nari:
            nari_moves.append(move)
        else:
            other_moves.append(move)
    legal_moves = captur_moves + nari_moves + other_moves
    for move in legal_moves:
        history = board.apply_move(move)
        score = -1 * tree_search(board, depth-1, -1*beta, -1*alpha)
        board.ando_move(history)
        best_score = max(best_score, score)
        alpha = max(alpha, best_score)
        if alpha >= beta:
            break
    return best_score
