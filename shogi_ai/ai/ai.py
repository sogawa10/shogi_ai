from concurrent.futures import ProcessPoolExecutor, as_completed
import random
from shogi_ai.ai.ai用関数 import *

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

def evaluate(board, move, depth):
    history = board.apply_move(move)
    score = -1 * tree_search(board, depth-1, float('-inf'), float('inf'))
    board.ando_move(history)
    return score, move

def ai_think(board, depth):
    if board.move_count <= 4:
        move = opening_move(board)
        if move is not None:
            print("最終結果: 定石手を選択しました")
            return move
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