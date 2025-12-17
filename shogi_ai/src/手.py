from dataclasses import dataclass

@dataclass
class 手:
    koma: object
    from_pos: tuple | None
    to_pos: tuple
    nari: bool=False
    utite: bool=False
    komadori: object | None = None