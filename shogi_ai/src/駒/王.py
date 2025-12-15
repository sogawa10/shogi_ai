from .駒 import 駒

class 王(駒):
    def relative_moves(self):
        return [
            (1,-1), (0,-1), (-1,-1),
            (1, 0),         (-1, 0),
            (1, 1), (0, 1), (-1, 1)
        ]