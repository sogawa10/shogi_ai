from .駒 import 駒

class 王(駒):
    def can_nari(self):
        return False
        
    def relative_moves(self):
        return [
            (1,-1), (0,-1), (-1,-1),
            (1, 0),         (-1, 0),
            (1, 1), (0, 1), (-1, 1)
        ]

    def is_continuous(self, dx, dy):
        return False
    
    def symbol(self):
        if self.sente_gote == "先手":
            symbol = "王"
        else:
            symbol = "玉"
        return symbol
