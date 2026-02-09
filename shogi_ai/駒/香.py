from .駒 import 駒

class 香(駒):
    def can_nari(self):
        return True
        
    def relative_moves(self):
        if self.nari:
            if self.sente_gote == "先手":
                return [
                    (1,-1), (0,-1), (-1,-1),
                    (1, 0),         (-1, 0),
                            (0, 1)
                ]
            else:
                return [
                            (0,-1),
                    (1, 0),         (-1, 0),
                    (1, 1), (0, 1), (-1, 1)
                ]
        else:
            if self.sente_gote == "先手":
                return [
                            (0,-1),
                ]
            else:
                return [
                            (0, 1)
                ]
    
    def is_continuous(self, dx, dy):
        if self.nari:
            return False
        else:
            if self.sente_gote == "先手":
                return (dx, dy) == (0,-1)
            else:
                return (dx, dy) == (0, 1)
    
    def symbol(self, player_sente_or_gote = "先手"):
        if player_sente_or_gote == "先手":
            if self.sente_gote == "先手":
                if self.nari:
                    symbol = "↑金"
                else:
                    symbol = "↑香"
            else:
                if self.nari:
                    symbol = "↓金"
                else:
                    symbol = "↓香"
        else:
            if self.sente_gote == "先手":
                if self.nari:
                    symbol = "↓金"
                else:
                    symbol = "↓香"
            else:
                if self.nari:
                    symbol = "↑金"
                else:
                    symbol = "↑香"   
        return symbol
