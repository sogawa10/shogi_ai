from 駒 import *

class 盤面:
    def __init__(self):
        # board[x][y] : 右上が原点で，横が「x」，縦が「y」
        # fu fu fu fu fu fu fu fu fu 
        #    ka                hi
        # ky ke gi ki ou ki gi ke ky
        self.board = [[None for y in range(9)] for x in range(9)]

        for x in range(9):
            fu = 歩("先手", x=x, y=6)
            self.board[x][6] = fu
        ka = 角("先手", x=7, y=7)
        self.board[7][7] = ka
        hi = 飛("先手", x=1, y=7)
        self.board[1][7] = hi
        for x in (0,8):
            ky = 香("先手", x=x, y=8)
            self.board[x][8] = ky
        for x in (1,7):
            ke = 桂("先手", x=x, y=8)
            self.board[x][8] = ke
        for x in (2,6):
            gi = 銀("先手", x=x, y=8)
            self.board[x][8] = gi
        for x in (3,5):
            ki = 金("先手", x=x, y=8)
            self.board[x][8] = ki
        ou = 王("先手", x=4, y=8)
        self.board[4][8] = ou

        for x in range(9):
            fu = 歩("後手", x=x, y=2)
            self.board[x][2] = fu
        ka = 角("後手", x=1, y=1)
        self.board[1][1] = ka
        hi = 飛("後手", x=7, y=1)
        self.board[7][1] = hi
        for x in (0,8):
            ky = 香("後手", x=x, y=0)
            self.board[x][0] = ky
        for x in (1,7):
            ke = 桂("後手", x=x, y=0)
            self.board[x][0] = ke
        for x in (2,6):
            gi = 銀("後手", x=x, y=0)
            self.board[x][0] = gi
        for x in (3,5):
            ki = 金("後手", x=x, y=0)
            self.board[x][0] = ki
        ou = 王("後手", x=4, y=0)
        self.board[4][0] = ou

        self.motigoma = {
            "先手":[],
            "後手":[]
        }

        self.ou_position = {
            "先手":(4,8),
            "後手":(4,0)
        }

        self.turn = "先手"

    