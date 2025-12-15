from .駒 import 駒

class 角(駒):
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