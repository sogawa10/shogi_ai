import random
import time
from copy import deepcopy
from shogi_ai.対局用.盤面 import 盤面
from shogi_ai.駒 import *
from shogi_ai.対局用.手 import 手
from shogi_ai.対局用.対局用関数 import *
from shogi_ai.ai.ai import ai_think

def vs_ai():
    depth = 4  # AIの思考深さ
    player_sente_or_gote = random.choice(["先手", "後手"])
    print()
    print("☆ あなたは「" + player_sente_or_gote + "」です ☆")
    if player_sente_or_gote == "先手":
        remainder = 1
    else:
        remainder = 0
    last_move = None
    board = 盤面()
    # 復元する場合は棋譜を入力
    position_history, position_sequence = board.load_kifu("")
    time.sleep(3)
    while True:
        if board.get_move_count() % 2 == remainder:
            # 盤面と持ち駒を表示し，手の入力を受け付ける
            print_board(board, last_move, player_sente_or_gote)
            print_mochigoma(board, player_sente_or_gote)
            in_move = input_move(board)
            if in_move is None:
                print("☆ 入力エラーです 正しく入力してください ☆")
                continue
            # 盤面の合法手を生成する
            board_moves = board.generate_board_moves(board.turn)
            uchite = board.generate_uchite(board.turn)
            legal_moves = board.filter_shogi_rules(board_moves, uchite)
            # 入力された手が合法手かどうか確認する
            for legal_move in legal_moves:
                if (
                    type(legal_move.koma) is type(in_move.koma)
                    and legal_move.from_pos == in_move.from_pos
                    and legal_move.to_pos == in_move.to_pos
                    and legal_move.nari == in_move.nari
                    and legal_move.uchite == in_move.uchite
                ):
                    last_move = deepcopy(legal_move)
                    history = board.apply_move(legal_move)
                    break
            else:
                print("☆ 非合法手です ☆")
                continue
        else:
            # 盤面と持ち駒を表示し，AIの思考を開始する
            print_board(board, last_move, player_sente_or_gote)
            print_mochigoma(board, player_sente_or_gote)
            print()
            print("AI思考中...")
            ai_move = ai_think(board, depth, player_sente_or_gote)
            last_move = deepcopy(ai_move)
            history = board.apply_move(ai_move)
        # 終了判定
        if board.is_checkmate(board.turn):
            if board.turn == "先手":
                enemy = "後手"
            else:
                enemy = "先手"
            print_board(board, last_move, player_sente_or_gote)
            print_mochigoma(board, player_sente_or_gote)
            print("「" + enemy + "」の勝利!!")
            print()
            break
        # 入玉宣言法
        if ou_is_in_enemy_zone(board):
            if not board.is_oute(board.turn):
                if board.turn == "先手":
                    point = 28
                else:
                    point = 27
                score, in_count = count_nyugyoku_points(board)
                if in_count >= 10 and score >= point:
                    print_board(board, last_move, player_sente_or_gote)
                    print_mochigoma(board, player_sente_or_gote)
                    print("入玉宣言法により...")
                    print("「" + board.turn + "」の勝利!!")
                    print()
                    break
        # 千日手判定
        key = position_key(board)
        is_oute = board.is_oute(board.turn)
        if is_oute:
            if board.turn == "先手":
                enemy = "後手"
            else:
                enemy = "先手"
        else:
            enemy = None
        position_history[key] = position_history.get(key, 0) + 1
        position_sequence.append((key, enemy))
        if position_history[key] == 4:
            print_board(board, last_move, player_sente_or_gote)
            print_mochigoma(board, player_sente_or_gote)
            first = 0
            for i, (past_key, _) in enumerate(position_sequence):
                if past_key == key:
                    first = i
                    break
            if position_sequence[first][1] is not None:
                start_index = first
            elif position_sequence[first - 1][1] is not None:
                start_index = first - 1
            else:
                start_index = None
            is_continuous_check = False
            if start_index is not None:
                oute_checker = position_sequence[start_index][1]
                is_continuous_check = True
                for i, (_, e) in enumerate(position_sequence[start_index:]):
                    if i % 2 == 1:
                        continue
                    if e != oute_checker:
                        is_continuous_check = False
                        break
            if is_continuous_check:
                print("連続王手の千日手です")
                print("「" + oute_checker + "」の反則負けです")
                print()
                break
            else:
                print("千日手です")
                print("引き分けです")
                print()
                break
        # 最大手数判定
        if board.get_move_count() - 1 >= 500:
            print_board(board, last_move, player_sente_or_gote)
            print_mochigoma(board, player_sente_or_gote)
            print("最大手数に達しました")
            print("引き分けです")
            print()
            break
