from src.盤面 import 盤面
from src.駒 import *
from src.手 import 手

def print_board(board):
    int2kanji_map = {
        0: '一', 1: '二', 2: '三', 3: '四', 4: '五', 5: '六', 6: '七', 7: '八', 8: '九'
    }
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
    print()

def input_move(board):
    return "a"

def main():
    board = 盤面()
    print_board(board)
    print_mochigoma(board)

if __name__ == "__main__":
    main()