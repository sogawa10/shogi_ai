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
    
    def change_turn(self):
        if self.turn == "先手":
            self.turn = "後手"
        else:
            self.turn = "先手"
    
    def change_ou_position(self, turn, nx, ny):
        self.ou_position[turn] = (nx, ny)

    def add_motigoma(self, turn, koma):
        self.motigoma[turn].append(koma)
    
    def remove_motigoma(self, turn, koma):
        self.motigoma[turn].remove(koma)

    def is_on_board(self, x, y):
        return 0 <= x < 9 and 0 <= y < 9
    
    def has_no_koma(self, x, y):
        return self.board[x][y] is None

    def is_jigoma(self, x, y, turn):
        koma = self.board[x][y]
        return koma is not None and koma.sente_gote() == turn

    def is_tekigoma(self, x, y, turn):
        koma = self.board[x][y]
        return koma is not None and koma.sente_gote() != turn
    
    # 盤面の手のリストを返す
    def generate_board_moves(self, turn):
        

    # 持ち駒の手のリストを返す
    def generate_drop_moves(self, turn):


    # 将棋固有のルールを手に適応
    def filter_shogi_rules(self, moves, turn):
        

    # 盤面が王手状態かどうかを判定
    def filter_oute_rules(self, moves, turn):
        
