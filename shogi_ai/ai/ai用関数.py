import random
from shogi_ai.駒 import *
from shogi_ai.対局用.対局用関数 import *

# 盤面ハッシュ
board_hashes = {}

# 初手の定石
def opening_move(board):
    joseki_moves = []
    board_moves = board.generate_board_moves(board.turn)
    uchite = board.generate_uchite(board.turn)
    legal_moves = board.filter_shogi_rules(board_moves, uchite)
    if board.move_count <= 2:
        if board.turn == "先手":
            joseki = [
                ((6, 6), (6, 5)),
                ((1, 6), (1, 5))
            ]
        else:
            joseki = [
                ((2, 2), (2, 3)),
                ((7, 2), (7, 3))
            ]
    elif board.move_count <= 4:
        if board.turn == "先手":
            joseki = [
                ((6, 6), (6, 5)),
                ((5, 6), (5, 5)),
                ((1, 6), (1, 5)),
                ((1, 5), (1, 4))
            ]
        else:
            joseki = [
                ((2, 2), (2, 3)),
                ((3, 2), (3, 3)),
                ((7, 2), (7, 3)),
                ((7, 3), (7, 4))
            ]
    for move in legal_moves:
        if (move.from_pos, move.to_pos) in joseki:
            joseki_moves.append(move)
    if joseki_moves:
        return random.choice(joseki_moves)
    return None

# 盤面評価用関数
def evaluate(board):
    piece_values = {
        王: {"王": 15000, "玉": 15000},
        歩: {"歩": 100, "と": 700},
        金: {"金": 690},
        銀: {"銀": 640, "全": 670},
        桂: {"桂": 450, "圭": 630},
        香: {"香": 430, "杏": 630},
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
    # 入玉阻止
    my_y = board.ou_position[board.turn][1]
    if my_y <= 4:
        if my_y == 0:
            score += 400
        elif my_y == 1:
            score += 300
        elif my_y == 2:
            score += 200
        elif my_y == 3:
            score += 100
        elif my_y == 4:
            score += 50
    enemy_y = board.ou_position[enemy][1]
    if enemy_y >= 4:
        if enemy_y == 8:
            score -= 400
        elif enemy_y == 7:
            score -= 300
        elif enemy_y == 6:
            score -= 200
        elif enemy_y == 5:
            score -= 100
        elif enemy_y == 4:
            score -= 50
    return score

# 木探索
def tree_search(board, position_history, depth, alpha, beta):
    # 盤面ハッシュによる軽量化
    root_key = position_key(board)
    if root_key in board_hashes and board_hashes[root_key][0] >= depth:
        return board_hashes[root_key][1], 1
    # リーフ
    if board.is_checkmate(board.turn):
        board_hashes[root_key] = (depth, -100000 + depth)
        return -100000 + depth, 1
    if position_history[root_key] == 4:
        board_hashes[root_key] = (depth, -100000 + depth)
        return -100000 + depth, 1
    if depth == 0:
        score = evaluate(board)
        board_hashes[root_key] = (depth, score)
        return score, 1
    # ノード
    captur_moves = []
    nari_moves = []
    other_moves = []
    best_score = float('-inf')
    total_nodes = 1
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
        key = position_key(board)
        position_history[key] = position_history.get(key, 0) + 1
        score, node_count = tree_search(board, position_history, depth-1, -1*beta, -1*alpha)
        score = -score
        total_nodes += node_count
        board.ando_move(history)
        position_history[key] -= 1
        if position_history[key] == 0:
            del position_history[key]
        best_score = max(best_score, score)
        alpha = max(alpha, best_score)
        if alpha >= beta:
            break
    board_hashes[root_key] = (depth, best_score)
    return best_score, total_nodes
