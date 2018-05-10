class Board(object):
    boardCards = None  # Card
    # 0 - Property Card
    # 1 - Community Chest Card
    # 2 - Chance Card
    # 3 - SpecialPosition(Go, Jail, etc)
    typeId = None  # int

    def __init__(self, b=None, t=0):
        self.boardCards = b
        self.typeId = t
