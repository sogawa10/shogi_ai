from dataclasses import dataclass

@dataclass
class 手:
    koma: object
    from_pos: tuple | None
    to_pos: tuple
    nari: bool=False
    uchite: bool=False
    komadori: object | None = None

    def to_string(self, player_sente_or_gote):
        if self.koma.sente_or_gote() == "先手":
            turn = "▲"
        else:
            turn = "△"
        if self.uchite:
            return (turn + str(self.to_pos[0] + 1) + str(self.to_pos[1] + 1) + self.koma.symbol(player_sente_or_gote)[1] + "打")
        else:
            if self.nari:
                return (turn + str(self.to_pos[0] + 1) + str(self.to_pos[1] + 1) + self.koma.symbol(player_sente_or_gote)[1] + "成(" + str(self.from_pos[0] + 1) + str(self.from_pos[1] + 1) + ")")
            else:
                return (turn + str(self.to_pos[0] + 1) + str(self.to_pos[1] + 1) + self.koma.symbol(player_sente_or_gote)[1] + "(" + str(self.from_pos[0] + 1) + str(self.from_pos[1] + 1) + ")")