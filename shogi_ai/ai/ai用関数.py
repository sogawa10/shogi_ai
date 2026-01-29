import random
from shogi_ai.駒 import *

# 飛車の位置判定
def where_hisha(board, turn):
    for y in range(9):
        for x in range(9):
            koma = board.board[x][y]
            if koma is not None and type(koma) is 飛 and koma.sente_or_gote() == turn:
                return x
    return None

# 飛車先の歩を突くボーナス
def hishasaki_bonus(board, turn):
    bonus = 0
    hisha_x = where_hisha(board, turn)
    if hisha_x is None:
        return 0
    if turn == "先手":
        home = 1
        y1 = 5
        y2 = 4
    else:
        home = 7
        y1 = 3
        y2 = 4
    koma1 = board.board[hisha_x][y1]
    if koma1 is not None and type(koma1) is 歩 and koma1.sente_or_gote() == turn:
        bonus += 100
    koma2 = board.board[hisha_x][y2]
    if koma2 is not None and type(koma2) is 歩 and koma2.sente_or_gote() == turn:
        bonus += 150
    if hisha_x != home and hisha_x != 0 and hisha_x != 8:
        bonus += 50
    return bonus

# 角道開けボーナス
def kakumichi_bonus(board, turn):
    bonus = 0
    hisha_x = where_hisha(board, turn)
    if turn == "先手":
        hisha_pos = 6
        x = 6
        y1 = 5
        y2 = 4
    else:
        hisha_pos = 2
        x = 2
        y1 = 3
        y2 = 4
    koma1 = board.board[x][y1]
    if koma1 is not None and type(koma1) is 歩 and koma1.sente_or_gote() == turn and hisha_x != hisha_pos:
        bonus += 80
    koma2 = board.board[x][y2]
    if koma2 is not None and type(koma2) is 歩 and koma2.sente_or_gote() == turn and hisha_x != hisha_pos:
        bonus += 30
    return bonus

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
    attacked_penalty = {
        王: 0,
        歩: 0.85,
        金: 0.6,
        銀: 0.65,
        桂: 0.7,
        香: 0.75,
        飛: 0.45,
        角: 0.5,
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
                if board.is_attacked(x, y, board.turn) and not board.is_defended(x, y, board.turn):
                    score += piece_values[type(koma)][koma.symbol()[1]] * attacked_penalty[type(koma)]
                else:
                    score += piece_values[type(koma)][koma.symbol()[1]]
            else:
                if board.is_attacked(x, y, enemy) and not board.is_defended(x, y, enemy):
                    score -= piece_values[type(koma)][koma.symbol()[1]] * attacked_penalty[type(koma)]
                else:
                    score -= piece_values[type(koma)][koma.symbol()[1]]
    for koma in board.mochigoma[board.turn]:
        score += piece_values[type(koma)][koma.symbol()[1]] * 1.1
    for koma in board.mochigoma[enemy]:
        score -= piece_values[type(koma)][koma.symbol()[1]] * 1.1
    # 定跡ボーナス
    if board.move_count <= 10: 
        score += (kakumichi_bonus(board, board.turn) - kakumichi_bonus(board, enemy))
        score += (hishasaki_bonus(board, board.turn) - hishasaki_bonus(board, enemy))
    return score

# 木探索
def tree_search(board, depth, alpha, beta):
    # リーフ
    if board.is_checkmate(board.turn):
        return -100000 + depth
    if depth == 0:
        return evaluate(board)
    # ノード
    best_score = float('-inf')
    board_moves = board.generate_board_moves(board.turn)
    uchite = board.generate_uchite(board.turn)
    legal_moves = board.filter_shogi_rules(board_moves, uchite)
    random.shuffle(legal_moves)
    for move in legal_moves:
        new_board = board.copy()
        new_board = new_board.apply_move(move)
        score = -1 * tree_search(new_board, depth-1, -1*beta, -1*alpha)
        best_score = max(best_score, score)
        alpha = max(alpha, best_score)
        if alpha >= beta:
            break
    return best_score
