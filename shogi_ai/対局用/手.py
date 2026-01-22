from dataclasses import dataclass

@dataclass
class 手:
    koma: object
    from_pos: tuple | None
    to_pos: tuple
    nari: bool=False
    uchite: bool=False
    komadori: object | None = None

    def to_string(self):
        int2kanji_map = {
            0: '一', 1: '二', 2: '三', 3: '四', 4: '五', 5: '六', 6: '七', 7: '八', 8: '九'
        }
        int2zenkaku_map = {
            0: '１', 1: '２', 2: '３', 3: '４', 4: '５', 5: '６', 6: '７', 7: '８', 8: '９'
        }
        if self.uchite:
            return (int2zenkaku_map[self.to_pos[0]] + int2kanji_map[self.to_pos[1]] + self.koma.symbol()[1] + "打")
        else:
            if self.nari:
                return (int2zenkaku_map[self.from_pos[0]] + int2kanji_map[self.from_pos[1]] + int2zenkaku_map[self.to_pos[0]] + int2kanji_map[self.to_pos[1]] + self.koma.symbol()[1] + "成")
            else:
                return (int2zenkaku_map[self.from_pos[0]] + int2kanji_map[self.from_pos[1]] + int2zenkaku_map[self.to_pos[0]] + int2kanji_map[self.to_pos[1]] + self.koma.symbol()[1])