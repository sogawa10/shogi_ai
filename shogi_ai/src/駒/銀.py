from .駒 import 駒

class 銀(駒):
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
                    (1,-1), (0,-1), (-1,-1),
                    
                    (1, 1),         (-1, 1),
                ]
            else:
                return [
                    (1,-1),         (-1,-1),
                    
                    (1, 1), (0, 1), (-1, 1)
                ]
    
    def is_continuous(self, dx, dy):
        return False
    
    def symbol(self):
        if self.nari:
            symbol = "金"
        else:
            symbol = "銀"
        return symbol
