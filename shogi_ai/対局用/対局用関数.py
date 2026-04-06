from shogi_ai.駒 import *
from shogi_ai.対局用.手 import 手

def print_board(board, last_move, player_sente_or_gote = "先手"):
    int2kanji_map = {
        0: '一', 1: '二', 2: '三', 3: '四', 4: '五', 5: '六', 6: '七', 7: '八', 8: '九'
    }
    if player_sente_or_gote == "先手":
        print()
        print("———————————————————————————————————————————————————————————————————————")
        print()
        if last_move is not None:
            print("直前の手：", last_move.to_string(player_sente_or_gote))
            print()
        print(" ９　 ８　 ７　 ６　 ５　 ４　 ３　 ２　 １　")
        print()
        for y in range(9):
            for x in range(8, -1, -1):
                if board.board[x][y] == None:
                    print(" ・", end='　')
                else:
                    print(board.board[x][y].symbol(player_sente_or_gote), end='　')
            print(" ", end='')
            print(int2kanji_map[y])
            print()
        print()
    else:
        print()
        print("———————————————————————————————————————————————————————————————————————")
        print()
        if last_move is not None:
            print("直前の手：", last_move.to_string(player_sente_or_gote))
            print()
        print(" １　 ２　 ３　 ４　 ５　 ６　 ７　 ８　 ９　")
        print()
        for y in range(8, -1, -1):
            for x in range(9):
                if board.board[x][y] == None:
                    print(" ・", end='　')
                else:
                    print(board.board[x][y].symbol(player_sente_or_gote), end='　')
            print(" ", end='')
            print(int2kanji_map[y])
            print()
        print()

def print_mochigoma(board, player_sente_or_gote = "先手"):
    print("先手 持駒：", end='')
    for koma in board.mochigoma["先手"]:
        print(koma.symbol(player_sente_or_gote), end='　')
    print()
    print("後手 持駒：", end='')
    for koma in board.mochigoma["後手"]:
        print(koma.symbol(player_sente_or_gote), end='　')
    print()

def input_move(board):
    print()
    print("☆ 入力例 ☆")
    print("移動：fx fy tx ty [成]")
    print("打つ：駒 tx ty")
    print()
    input_move = input(board.turn + "の手番> ").strip()

    # 移動
    if  len(input_move) in (4, 5):
        try:
            fx, fy, tx, ty = map(int, input_move[:4])
        except ValueError:
            return None
        fx, fy, tx, ty = fx - 1, fy - 1, tx - 1, ty - 1
        if not (0 <= fx < 9 and 0 <= fy < 9 and 0 <= tx < 9 and 0 <= ty < 9):
            return None
        if len(input_move) == 5:
            if input_move[4] != "成":
                return None
            nari = True
        else:
            nari = False
        koma = board.board[fx][fy]
        if koma is None:
            return None
        return 手(koma, (fx, fy), (tx, ty), nari=nari)
    
    # 打ち
    if len(input_move) == 3 and input_move[0] in {"歩","角","飛","金","銀","桂","香"}:
        kanji2class = {
            "歩":歩, "角":角, "飛":飛, "金":金, "銀":銀, "桂":桂, "香":香
        }
        try:
            tx, ty = map(int, input_move[1:])
        except ValueError:
            return None
        tx, ty = tx - 1, ty - 1
        if not (0 <= tx < 9 and 0 <= ty < 9):
            return None
        for koma in board.mochigoma[board.turn]:
            if type(koma) is kanji2class[input_move[0]]:
                return 手(koma, None, (tx, ty), uchite=True)
        return None
    return None

def move2te(move, board):
    move = move.strip()
    if move[0] == "▲":
        move_turn = "先手"
    elif move[0] == "△":
        move_turn = "後手"
    else:
        return None
    if board.turn != move_turn:
        return None
    # 移動(成らず)
    if len(move) == 8 and move[4] == "(" and move[7] == ")":
        try:
            tx, ty, fx, fy = int(move[1]) - 1, int(move[2]) - 1, int(move[5]) - 1, int(move[6]) - 1
        except ValueError:
            return None
        if not (0 <= tx < 9 and 0 <= ty < 9 and 0 <= fx < 9 and 0 <= fy < 9):
            return None
        koma = board.board[fx][fy]
        if koma is None or move[3] != koma.symbol()[1]:
            return None
        cap_koma = board.board[tx][ty]
        if cap_koma is not None and cap_koma.sente_or_gote() == move_turn:
            return None
        te = 手(koma, (fx, fy), (tx, ty), komadori=cap_koma)
    # 移動(成り)
    elif len(move) == 9 and move[4] == "成" and move[5] == "(" and move[8] == ")":
        try:
            tx, ty, fx, fy = int(move[1]) - 1, int(move[2]) - 1, int(move[6]) - 1, int(move[7]) - 1
        except ValueError:
            return None
        if not (0 <= tx < 9 and 0 <= ty < 9 and 0 <= fx < 9 and 0 <= fy < 9):
            return None
        koma = board.board[fx][fy]
        if koma is None or move[3] != koma.symbol()[1]:
            return None
        cap_koma = board.board[tx][ty]
        if cap_koma is not None and cap_koma.sente_or_gote() == move_turn:
            return None
        te = 手(koma, (fx, fy), (tx, ty), nari=True, komadori=cap_koma)
    # 打ち
    elif len(move) == 5 and move[3] in {"歩","角","飛","金","銀","桂","香"} and move[4] == "打":
        kanji2class = {
            "歩":歩, "角":角, "飛":飛, "金":金, "銀":銀, "桂":桂, "香":香
        }
        try:
            tx, ty = int(move[1]) - 1, int(move[2]) - 1
        except ValueError:
            return None
        if not (0 <= tx < 9 and 0 <= ty < 9):
            return None
        found = False
        for koma in board.mochigoma[board.turn]:
            if type(koma) is kanji2class[move[3]]:
                found = True
                te = 手(koma, None, (tx, ty), uchite=True)
                break
        if not found:
            return None
    else:
        return None
    return te

# 千日手判定用（盤面をタプルに変換）
def serialize_board(board):
    outer = []
    for y in range(9):
        column = []
        for x in range(9):
            koma = board.board[x][y]
            if koma is None:
                column.append(None)
            else:
                column.append((koma.symbol(), koma.sente_or_gote()))
        outer.append(tuple(column))
    return tuple(outer)

# 千日手判定用（持ち駒を駒種ごとの枚数に正規化）
def serialize_mochigoma(mochigoma):
    counter = {}
    for koma in mochigoma:
        if type(koma).__name__ not in counter:
            counter[type(koma).__name__] = 1
        else:
            counter[type(koma).__name__] += 1
    return tuple(sorted(counter.items()))

# 千日手判定用（盤面の状態+持ち駒の状態+ターンを，==で比較可能なタプルに変換）
def position_key(board):
    board_key = tuple(
        serialize_board(board)
    )

    mochigoma_key = (
        serialize_mochigoma(board.mochigoma["先手"]),
        serialize_mochigoma(board.mochigoma["後手"])
    )

    return (board_key, mochigoma_key, board.turn)

# 入玉宣言法の判定用（入玉判定）
def ou_is_in_enemy_zone(board):
    _ , y = board.ou_position[board.turn]
    if board.turn == "先手":
        if y <= 2:
            return True
    else:
        if y >= 6:
            return True
    return False

# 入玉宣言法の判定用（点数計算）
def count_nyugyoku_points(board):
    score = 0
    in_count = 0
    if board.turn == "先手":
        enemy_zone = range(0, 3)
    else:
        enemy_zone = range(6, 9)
    for y in enemy_zone:
        for x in range(9):
            koma = board.board[x][y]
            if koma is None or koma.sente_or_gote() != board.turn:
                continue
            if isinstance(koma, 王):
                continue
            if isinstance(koma, 飛) or isinstance(koma, 角):
                score += 5
            else:
                score += 1
            in_count += 1
    for koma in board.mochigoma[board.turn]:
        if isinstance(koma, 飛) or isinstance(koma, 角):
            score += 5
        else:
            score += 1
    return score, in_count

def check_game_end(board, position_history, position_sequence):
    result = None
    result_type = None
    # 終了判定
    if board.is_checkmate(board.turn):
        if board.turn == "先手":
            result = "GOTE_WIN"
        else:
            result = "SENTE_WIN"
        result_type = "CHECKMATE"
    # 入玉宣言法
    if ou_is_in_enemy_zone(board):
        if not board.is_oute(board.turn):
            if board.turn == "先手":
                point = 28
            else:
                point = 27
            score, in_count = count_nyugyoku_points(board)
            if in_count >= 10 and score >= point:
                if board.turn == "先手":
                    result = "SENTE_WIN"
                else:
                    result = "GOTE_WIN"
                result_type = "NYUGYOKU"
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
            if oute_checker == "先手":
                result = "GOTE_WIN"
            else:
                result = "SENTE_WIN"
            result_type = "RENZOKU_OTE_SENNICHITE"
        else:
            result = "DRAW"
            result_type = "SENNICHITE"
    # 最大手数判定
    if board.get_move_count() - 1 >= 500:
        result = "DRAW"
        result_type = "MAX_MOVE"
    return result, result_type