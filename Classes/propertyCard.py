from Classes.card import Card


class PropertyCard(Card):
    # ###### Region Fields ############
    cardName = None  # string
    position = None  # int
    price = None  # int
    rent = None  # int list
    mortgage = None  # int
    houseCost = None  # int
    hotelCost = None  # int
    group = None  # int

    def __init__(self, pName, pPosition, pPrice, pRent, pMortgage, pHouseCost, pHotelCost, pGroup):
        self.cardName = pName  # string
        self.position = pPosition  # int
        self.price = pPrice  # int
        self.rent = pRent  # int list
        self.mortgage = pMortgage  # int
        self.houseCost = pHouseCost  # int
        self.hotelCost = pHotelCost  # int
        self.group = pGroup  # int

    # ###### Region GetMethods ############

    # Return the position of the current card on the board
    def getPosition(self):
        return self.position

    # Return the name of the current card
    def getName(self):
        return self.cardName

    # Return the group that the current card belongs to
    def getGroup(self):
        return self.group

    # Return the value of the current card
    def getValue(self):
        return self.price

    # Return the cost to build a house for the specific card
    def getHouseCost(self):
        return self.houseCost

    # Return the cost to build a hotel for the specific card
    def getHotelCost(self):
        return self.hotelCost

    # Return the mortgage value of the current card on the board
    def getMortgageValue(self):
        return self.mortgage
