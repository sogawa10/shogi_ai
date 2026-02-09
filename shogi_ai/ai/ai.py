from concurrent.futures import ProcessPoolExecutor, as_completed
import random
from shogi_ai.ai.ai用関数 import *

def evaluate(board, move, position_history, depth):
    history = board.apply_move(move)
    key = position_key(board)
    position_history[key] = position_history.get(key, 0) + 1
    score = -1 * tree_search(board, position_history, depth-1, float('-inf'), float('inf'))
    position_history[key] -= 1
    if position_history[key] == 0:
        del position_history[key]
    board.ando_move(history)
    return score, move

def ai_think(board, position_history, depth, player_sente_or_gote):
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
            executor.submit(evaluate, board, move, position_history, depth)
            for move in legal_moves
        ]
        for future in as_completed(futures):
            score, move = future.result()
            if score > best_score:
                best_score = score
                best_move = move
                print(f"\r\033[K現在の最善手: {best_move.to_string(player_sente_or_gote)}  評価値: {best_score}", end="")
    print("\r\033[K最終結果: " + best_move.to_string(player_sente_or_gote) + "  評価値: " + str(best_score))
    return best_move