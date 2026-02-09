from .駒 import 駒

class 角(駒):
    def can_nari(self):
        return True
        
    def relative_moves(self):
        if self.nari:
            return [
                (1,-1), (0,-1), (-1,-1),
                (1, 0),         (-1, 0),
                (1, 1), (0, 1), (-1, 1)
            ]
        else:
            return [
                (1,-1),         (-1,-1),

                (1, 1),         (-1, 1)
            ]

    def is_continuous(self, dx, dy):
        return (dx, dy) == (1,-1) or (dx, dy) == (-1,-1) or (dx, dy) == (1, 1) or(dx, dy) == (-1, 1)
    
    def symbol(self, player_sente_or_gote = "先手"):
        if player_sente_or_gote == "先手":
            if self.sente_gote == "先手":
                if self.nari:
                    symbol = "↑馬"
                else:
                    symbol = "↑角"
            else:
                if self.nari:
                    symbol = "↓馬"
                else:
                    symbol = "↓角"
        else:
            if self.sente_gote == "先手":
                if self.nari:
                    symbol = "↓馬"
                else:
                    symbol = "↓角"
            else:
                if self.nari:
                    symbol = "↑馬"
                else:
                    symbol = "↑角"
        return symbol  
