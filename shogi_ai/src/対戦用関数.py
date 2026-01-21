from src.盤面 import 盤面
from src.駒 import *
from src.手 import 手

def print_board(board):
    int2kanji_map = {
        0: '一', 1: '二', 2: '三', 3: '四', 4: '五', 5: '六', 6: '七', 7: '八', 8: '九'
    }
    print()
    print("———————————————————————————————————————————————————————————————————————")
    print(" 　　 　　 　　 　　 　　 　　 　　 ▽後手 　")
    print(" ９　 ８　 ７　 ６　 ５　 ４　 ３　 ２　 １　")
    print()
    for y in range(9):
        for x in range(8, -1, -1):
            if board.board[x][y] == None:
                print(" ・", end='　')
            else:
                print(board.board[x][y].symbol(), end='　')
        print(" ", end='')
        print(int2kanji_map[y])
        print()
    print("　 △先手 　　 　　 　　 　　 　　 　　 　　 ")
    print()

def print_mochigoma(board):
    print("先手 持駒：", end='')
    for koma in board.mochigoma["先手"]:
        print(koma.symbol(), end='　')
    print()
    print("後手 持駒：", end='')
    for koma in board.mochigoma["後手"]:
        print(koma.symbol(), end='　')
    print()

def input_move(board):
    print()
    print("☆ 入力例 ☆")
    print("移動：fx fy tx ty [成]")
    print("打つ：駒 tx ty")
    print()
    input_move = input(board.turn + "の手番> ").strip().split()

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

# 持将棋の判定用（入玉判定）
def ou_is_in_enemy_zone(board):
    _ , ys = board.ou_position["先手"]
    _ , yg = board.ou_position["後手"]
    return ys <= 2 or yg >= 6

# 持将棋の判定用（点数計算）
def count_jishogi_points(board, turn):
    score = 0
    for y in range(9):
        for x in range(9):
            koma = board.board[x][y]
            if koma is None or koma.sente_or_gote() != turn:
                continue
            if isinstance(koma, 王):
                continue
            if isinstance(koma, 飛) or isinstance(koma, 角):
                score += 5
            else:
                score += 1
    for koma in board.mochigoma[turn]:
        if isinstance(koma, 飛) or isinstance(koma, 角):
            score += 5
        else:
            score += 1
    return score