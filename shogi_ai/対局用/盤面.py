from dataclasses import replace
from shogi_ai.駒 import *
from shogi_ai.対局用.手 import 手

class 盤面:
    def __init__(self):
        # board[x][y] : 右上が原点で，横が「x」，縦が「y」
        # fu fu fu fu fu fu fu fu fu 
        #    ka                hi
        # ky ke gi ki ou ki gi ke ky
        self.board = [[None for x in range(9)] for y in range(9)]

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

        self.mochigoma = {
            "先手":[],
            "後手":[]
        }

        self.ou_position = {
            "先手":(4,8),
            "後手":(4,0)
        }

        self.turn = "先手"
        self.move_count = 1
    
    def get_move_count(self):
        return self.move_count
    
    def change_turn(self):
        if self.turn == "先手":
            self.turn = "後手"
        else:
            self.turn = "先手"
    
    def change_ou_position(self, turn, nx, ny):
        self.ou_position[turn] = (nx, ny)

    def add_mochigoma(self, turn, koma):
        self.mochigoma[turn].append(koma)
    
    def remove_mochigoma(self, turn, koma):
        for k in self.mochigoma[turn]:
            if type(k) == type(koma):
                self.mochigoma[turn].remove(k)
                break

    def is_on_board(self, x, y):
        return 0 <= x < 9 and 0 <= y < 9
    
    def has_no_koma(self, x, y):
        return self.board[x][y] is None

    def is_jigoma(self, x, y, turn):
        koma = self.board[x][y]
        return koma is not None and koma.sente_or_gote() == turn

    def is_tekigoma(self, x, y, turn):
        koma = self.board[x][y]
        return koma is not None and koma.sente_or_gote() != turn
    
    def is_attacked(self, x, y, turn):
        if turn == "先手":
            enemy = "後手"
        else:
            enemy = "先手"
        moves = self.generate_board_moves(enemy)
        for move in moves:
            if move.to_pos == (x, y):
                return True
        return False
    
    def is_defended(self, x, y, turn):
        for fx in range(9):
            for fy in range(9):
                if not self.is_jigoma(fx, fy, turn):
                    continue
                koma = self.board[fx][fy]
                for dx, dy in koma.relative_moves():
                    nx, ny = fx + dx, fy + dy
                    while self.is_on_board(nx, ny):
                        if (nx, ny) == (x, y):
                            return True
                        if not self.has_no_koma(nx, ny):
                            break
                        if not koma.is_continuous(dx, dy):
                            break
                        nx += dx
                        ny += dy
        return False

    def is_oute(self, which_ou):
        is_oute = False
        if which_ou == "先手":
            enemy_moves = self.generate_board_moves("後手")
        else:
            enemy_moves = self.generate_board_moves("先手")
        for move in enemy_moves:
            if move.to_pos == self.ou_position[which_ou]:
                is_oute = True
                break
        return is_oute
    
    def is_checkmate(self, turn):
        is_checkmate = False
        if self.is_oute(turn):
            bm = self.generate_board_moves(turn)
            um = self.generate_uchite(turn)
            lm = self.filter_shogi_rules(bm, um, check_uchifuzume=False)
            if len(lm) == 0:
                is_checkmate = True
        return is_checkmate
    
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
        checked_types = []
        for koma in self.mochigoma[turn]:
            koma_type = type(koma)
            if koma_type in checked_types:
                continue
            checked_types.append(koma_type)
            for nx in range(9):
                for ny in range(9):
                    # 打ち先が空マスの場合
                    if self.has_no_koma(nx, ny):
                        moves.append(
                            手(koma, None, (nx, ny), uchite=True)
                        )
        return moves
    
    # 手を盤面に適用
    def apply_move(self, move):
        histry = {
            "move": move,
            "captured_nari": False
        }
        if move.uchite:
            tx, ty = move.to_pos
            new_koma = move.koma
            new_koma.x = tx
            new_koma.y = ty
            self.board[tx][ty] = new_koma
            self.remove_mochigoma(self.turn, new_koma)
        else:
            fx, fy = move.from_pos
            tx, ty = move.to_pos
            new_koma = self.board[fx][fy]
            if move.komadori is not None:
                cap_koma = move.komadori
                histry["captured_nari"] = cap_koma.is_nari()
                cap_koma.x = None
                cap_koma.y = None
                cap_koma.unaru()
                cap_koma.sente_gote = self.turn
                self.add_mochigoma(self.turn, cap_koma)
            new_koma.x = tx
            new_koma.y = ty
            self.board[fx][fy] = None
            self.board[tx][ty] = new_koma
            if move.nari:
                new_koma.naru()
            if isinstance(new_koma, 王):
                self.change_ou_position(self.turn, tx, ty)
        self.change_turn()
        self.move_count += 1
        return histry
    
    # 盤面を元に戻す
    def ando_move(self, histry):
        self.change_turn()
        self.move_count -= 1
        move = histry["move"]
        captured_nari = histry["captured_nari"]
        if move.uchite:
            tx, ty = move.to_pos
            koma = self.board[tx][ty]
            koma.x = None
            koma.y = None
            self.board[tx][ty] = None
            self.add_mochigoma(self.turn, koma)
        else:
            fx, fy = move.from_pos
            tx, ty = move.to_pos
            koma = self.board[tx][ty]
            koma.x = fx
            koma.y = fy
            self.board[fx][fy] = koma
            self.board[tx][ty] = None
            if move.komadori is not None:
                cap_koma = move.komadori
                self.remove_mochigoma(self.turn, cap_koma)
                if captured_nari:
                    cap_koma.naru()
                if self.turn == "先手":
                    enemy = "後手"
                else:
                    enemy = "先手"
                cap_koma.sente_gote = enemy
                cap_koma.x = tx
                cap_koma.y = ty
                self.board[tx][ty] = cap_koma
            if move.nari:
                koma.unaru()
            if isinstance(koma, 王):
                self.change_ou_position(self.turn, fx, fy)

    # 将棋固有のルールを手に適応
    def filter_shogi_rules(self, board_moves, uchite, check_uchifuzume=True):
        # 成りのルールを適応
        board_legal_moves = []
        for move in board_moves:
            board_legal_moves.append(move)
            if move.koma.can_nari() and not move.koma.is_nari():
                if self.turn == "先手":
                    if 0 <= move.from_pos[1] <=2 or 0 <= move.to_pos[1] <=2:
                        board_legal_moves.append(replace(move, nari=True))
                elif self.turn == "後手":
                    if 6 <= move.from_pos[1] <=8 or 6 <= move.to_pos[1] <=8:
                        board_legal_moves.append(replace(move, nari=True))
            
        # 二歩のルールを適応
        uchite_legal_moves = []
        for move in uchite:
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
                    and koma.sente_or_gote() == self.turn
                    and not koma.is_nari()
                ):
                    nifu = True
                    break
            if not nifu:
                uchite_legal_moves.append(move)
        
        # 行き所のない駒のルールを適応
        legal_moves1 = []
        for move in board_legal_moves + uchite_legal_moves:
            if isinstance(move.koma, (歩, 香)) and move.koma.is_nari() == False:
                if self.turn == "先手" and move.to_pos[1] == 0 and move.nari == False:
                    continue
                elif self.turn == "後手" and move.to_pos[1] == 8 and move.nari == False:
                    continue
                legal_moves1.append(move)
            elif isinstance(move.koma, 桂) and move.koma.is_nari() == False:
                if self.turn == "先手" and move.to_pos[1] in (0, 1) and move.nari == False:
                    continue
                elif self.turn == "後手" and move.to_pos[1] in (7, 8) and move.nari == False:
                    continue
                legal_moves1.append(move)
            else:
                legal_moves1.append(move)
        
        # 王手放置を除外
        legal_moves2 = []
        for move in legal_moves1:
            history = self.apply_move(move)
            if self.turn == "先手":
                enemy = "後手"
            else:
                enemy = "先手"
            if not self.is_oute(enemy):
                legal_moves2.append(move)
            self.ando_move(history)
        
        # 打ち歩詰めを除外
        final_moves = []
        if check_uchifuzume:
            for move in legal_moves2:
                history = self.apply_move(move)
                if move.uchite and isinstance(move.koma, 歩):
                    if self.is_checkmate(self.turn):
                        self.ando_move(history)
                        continue
                final_moves.append(move)
                self.ando_move(history)
        else:
            final_moves=legal_moves2
        return final_moves
