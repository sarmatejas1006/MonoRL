from Classes.card import Card


class CommandCard(Card):
    # ###### Region Fields ############
    typeOfCard = None  # int
    text = None  # string
    fixedMove = None  # string
    relativeMove = None  # string
    collect = None  # int
    moneyTransaction = None  # int
    playerInteraction = None  # int
    houseMultFactor = None  # int
    hotelMultFactor = None  # int

    def __init__(self, pType, pText, pFixedMove, pRelativeMove, pCollect, pMoneyTransaction, pPlayerInteraction, pHouseMult, pHotelMult):
        self.typeOfCard = pType  # int
        self.text = pText  # string
        self.fixedMove = pFixedMove  # string
        self.relativeMove = pRelativeMove  # string
        self.collect = pCollect  # int
        self.moneyTransaction = pMoneyTransaction  # int
        self.playerInteraction = pPlayerInteraction  # int
        self.houseMultFactor = pHouseMult  # int
        self.hotelMultFactor = pHotelMult  # int

    # Get Type of card ( 0 - Community Chest, 1 - Chance )
    def getType(self):
        return self.typeOfCard

    # Return value of card
    @staticmethod
    def getValue(self):
        return 0
