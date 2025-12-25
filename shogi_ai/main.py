from dataclasses import replace
from src.盤面 import 盤面
from src.駒 import *
from src.手 import 手

# 駒文字 → クラス対応（必要に応じて調整）
UCHITE_MAP = {
    "P": 歩,
    "L": 香,
    "N": 桂,
    "S": 銀,
    "G": 金,
    "B": 角,
    "R": 飛,
}

def print_board(board):
    print("  0  1  2  3  4  5  6  7  8")
    for y in range(9):
        row = []
        for x in range(9):
            koma = board.board[x][y]
            if koma is None:
                row.append("・")
            else:
                row.append(koma.symbol())
        print(f"{y} " + " ".join(row))
    print()

def print_motigoma(board):
    print("先手 持駒:", end=" ")
    for k in board.motigoma["先手"]:
        print(k.symbol(), end=" ")
    print()
    print("後手 持駒:", end=" ")
    for k in board.motigoma["後手"]:
        print(k.symbol(), end=" ")
    print("\n")

def input_move(board):
    print(f"{board.turn} の手番")
    print("移動: fx fy tx ty [n]")
    print("打ち: K tx ty  (K=P,L,N,S,G,B,R)")
    s = input("> ").strip().split()

    # 打ち
    if len(s) == 3 and s[0] in UCHITE_MAP:
        kcls = UCHITE_MAP[s[0]]
        tx, ty = map(int, s[1:])

        # 持ち駒から1枚選ぶ
        for k in board.motigoma[board.turn]:
            if type(k) is kcls:
                return 手(k, None, (tx, ty), uchite=True)

        return None  # その駒を持っていない

    # 移動
    if len(s) in (4, 5):
        fx, fy, tx, ty = map(int, s[:4])
        nari = (len(s) == 5 and s[4] == "n")
        koma = board.board[fx][fy]
        if koma is None:
            return None
        return 手(koma, (fx, fy), (tx, ty), nari=nari)

    return None

def main():
    board = 盤面()  # 初期局面前提

    while True:
        print_board(board)
        print_motigoma(board)

        # 合法手生成
        bm = board.generate_board_moves(board.turn)
        um = board.generate_uchite(board.turn)
        legal_moves = board.filter_shogi_rules(bm, um)

        if len(legal_moves) == 0:
            if board.is_oute(board.turn):
                print(f"{board.turn} は詰みです．")
            else:
                print("合法手がありません．")
            break

        move = input_move(board)
        if move is None:
            print("入力エラー\n")
            continue

        # 合法性チェック（構造一致）
        ok = False
        for lm in legal_moves:
            if (
                lm.from_pos == move.from_pos
                and lm.to_pos == move.to_pos
                and lm.uchite == move.uchite
                and type(lm.koma) is type(move.koma)
                and lm.nari == move.nari
            ):
                move = lm
                ok = True
                break

        if not ok:
            print("非合法手です\n")
            continue

        board = board.apply_move(move)

if __name__ == "__main__":
    main()
