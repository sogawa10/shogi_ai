from .駒 import 駒

class 飛(駒):
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
                        (0,-1),
                (1, 0),         (-1, 0),
                        (0, 1)
            ]
        
    def is_continuous(self, dx, dy):
        return (dx, dy) == (0,-1) or (dx, dy) == (-1,0) or (dx, dy) == (1, 0) or (dx, dy) == (0, 1)
    
    def symbol(self):
        if self.nari:
            symbol = "龍"
        else:
            symbol = "飛"
        return symbol
    