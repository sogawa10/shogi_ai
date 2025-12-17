from .駒 import 駒

class 飛(駒):
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
        return (dx, dy) == (1,-1) or (dx, dy) == (-1,-1) or (dx, dy) == (1, 1) or(dx, dy) == (-1, 1)
    