from src.盤面 import 盤面
from src.駒 import *
from src.手 import 手

def print_board(board):
    int2kanji_map = {
        0: '一', 1: '二', 2: '三', 3: '四', 4: '五', 5: '六', 6: '七', 7: '八', 8: '九'
    }
    print()
    print("　　　　　　　　　　　　　　▽後手　")
    print("９　８　７　６　５　４　３　２　１　")
    print()
    for y in range(9):
        for x in range(8, -1, -1):
            if board.board[x][y] == None:
                print("・", end='　')
            else:
                print(board.board[x][y].symbol(), end='　')
        print(" ", end='')
        print(int2kanji_map[y])
    print("　△先手　　　　　　　　　　　　　　")
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
    input_move = input(board.turn + "の手番> ").strip().split()

    # 移動
    if  len(input_move) in (4, 5):
        try:
            fx, fy, tx, ty = map(int, input_move[:4])
        except ValueError:
            return None
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
        if not (0 <= tx < 9 and 0 <= ty < 9):
            return None
        for koma in board.mochigoma[board.turn]:
            if type(koma) is kanji2class[input_move[0]]:
                return 手(koma, None, (tx, ty), uchite=True)
        return None
    return None

def main():
    board = 盤面()
    print_board(board)
    print_mochigoma(board)
    input_move(board)

if __name__ == "__main__":
    main()