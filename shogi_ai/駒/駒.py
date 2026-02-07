class 駒:
    def __init__(self, sente_gote, x, y, nari=False):
        self.sente_gote = sente_gote
        self.x = x
        self.y = y
        self.nari = nari

    def sente_or_gote(self):
        return self.sente_gote

    def move(self, nx, ny):
        self.x = nx
        self.y = ny

    def position(self):
        return (self.x, self.y)
    
    def naru(self):
        self.nari = True
    
    def unnari(self):
        self.nari = False
    
    def is_nari(self):
        return self.nari
    
    def is_motigoma(self):
        return self.x is None and self.y is None

    def can_nari(self):
        raise NotImplementedError

    def relative_moves(self):
        raise NotImplementedError
    
    def is_continuous(self, dx, dy):
        raise NotImplementedError
    
    def symbol(self):
        raise NotImplementedError

    # デバック用
    def __repr__(self):
        return f"{self.__class__.__name__}({self.sente_gote}, x={self.x}, y={self.y}, 成り={self.nari})"
