from dataclasses import replace
from 駒 import *
from .手 import 手

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

    def is_oute(self, turn):
        is_oute = False
        if turn == "先手":
            enemy_moves = self.generate_board_moves("後手")
        else:
            enemy_moves = self.generate_board_moves("先手")
        for move in enemy_moves:
            if move.to_pos == self.ou_position[turn]:
                is_oute = True
                break
        return is_oute
    
    # 盤面の手のリストを返す
    def generate_board_moves(self, turn):
        moves = []
        # 盤面を探索
        for x in range(9):
            for y in range(9):
                # 自駒の場合
                if self.is_jigoma(x, y, turn):
                    koma = self.board[x][y]
                    # 手を生成
                    for dx, dy in koma.relative_moves():
                        nx, ny = x + dx, y + dy
                        while self.is_on_board(nx, ny):
                            # 移動先が空マスの場合
                            if self.has_no_koma(nx, ny):
                                moves.append(
                                    手(koma, (x, y), (nx, ny))
                                )
                            # 移動先が敵駒の場合
                            elif self.is_tekigoma(nx, ny, turn):
                                moves.append(
                                    手(koma, (x, y), (nx, ny), komadori=self.board[nx][ny])
                                )
                                break
                            # 移動先が自駒の場合
                            elif self.is_jigoma(nx, ny, turn):
                                break
                            # 連続移動できない場合
                            if not koma.is_continuous(dx, dy):
                                break
                            nx += dx
                            ny += dy
        return moves

    # 打ち手のリストを返す
    def generate_uchite(self, turn):
        moves = []
        for koma in self.motigoma[turn]:
            for nx in range(9):
                for ny in range(9):
                    # 打ち先が空マスの場合
                    if self.has_no_koma(nx, ny):
                        moves.append(
                            手(koma, None, (nx, ny), uchite=True)
                        )
        return moves

    # 将棋固有のルールを手に適応
    def filter_shogi_rules(self, board_moves, uchite_moves):
        board_legal_moves = []
        uchite_legal_moves = []
        legal_moves = []
        # 成りのルールを適応
        for move in board_moves:
            board_legal_moves.append(move)
            if move.koma.can_nari():
                if move.koma.sente_or_gote() == "先手":
                    if 0 <= move.from_pos[1] <=2 or 0 <= move.to_pos[1] <=2:
                        board_legal_moves.append(replace(move, nari=True))
                elif move.koma.sente_or_gote() == "後手":
                    if 6 <= move.from_pos[1] <=8 or 6 <= move.to_pos[1] <=8:
                        board_legal_moves.append(replace(move, nari=True))
            
        # 二歩のルールを適応
        for move in uchite_moves:
            if not isinstance(move.koma, 歩):
                uchite_legal_moves.append(move)
                continue
            nifu = False
            x = move.to_pos[0]
            for y in range(9):
                koma = self.board[x][y]
                if (
                    koma is not None
                    and isinstance(koma, 歩)
                    and koma.sente_or_gote() == move.koma.sente_or_gote()
                    and not koma.is_nari()
                ):
                    nifu = True
                    break
            if not nifu:
                uchite_legal_moves.append(move)
        
        # 行き所のない駒のルールを適応
        for move in board_legal_moves + uchite_legal_moves:
            if isinstance(move.koma, (歩, 香)):
                if move.koma.sente_or_gote() == "先手" and move.to_pos[1] == 0 and move.nari == False:
                    continue
                elif move.koma.sente_or_gote() == "後手" and move.to_pos[1] == 8 and move.nari == False:
                    continue
                legal_moves.append(move)
            elif isinstance(move.koma, 桂):
                if move.koma.sente_or_gote() == "先手" and move.to_pos[1] in (0, 1) and move.nari == False:
                    continue
                elif move.koma.sente_or_gote() == "後手" and move.to_pos[1] in (7, 8) and move.nari == False:
                    continue
                legal_moves.append(move)
            else:
                legal_moves.append(move)
        return legal_moves

        