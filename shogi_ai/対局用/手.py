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
        if player_sente_or_gote == '先手':
            int2kanji_map = {
                0: '一', 1: '二', 2: '三', 3: '四', 4: '五', 5: '六', 6: '七', 7: '八', 8: '九'
            }
            int2zenkaku_map = {
                0: '１', 1: '２', 2: '３', 3: '４', 4: '５', 5: '６', 6: '７', 7: '８', 8: '９'
            }
        else:
            int2kanji_map = {
                0: '九', 1: '八', 2: '七', 3: '六', 4: '五', 5: '四', 6: '三', 7: '二', 8: '一'
            }
            int2zenkaku_map = {
                0: '９', 1: '８', 2: '７', 3: '６', 4: '５', 5: '４', 6: '３', 7: '２', 8: '１'
            }
        if self.uchite:
            return (int2zenkaku_map[self.to_pos[0]] + int2kanji_map[self.to_pos[1]] + self.koma.symbol(player_sente_or_gote)[1] + "打")
        else:
            if self.nari:
                return (int2zenkaku_map[self.to_pos[0]] + int2kanji_map[self.to_pos[1]] + self.koma.symbol(player_sente_or_gote)[1] + "成 （" + int2zenkaku_map[self.from_pos[0]] + int2kanji_map[self.from_pos[1]] + "）")
            else:
                return (int2zenkaku_map[self.to_pos[0]] + int2kanji_map[self.to_pos[1]] + self.koma.symbol(player_sente_or_gote)[1] + " （" + int2zenkaku_map[self.from_pos[0]] + int2kanji_map[self.from_pos[1]] + "）")