from MonopolyHandlers.monopolyActions import MonopolyActions


class ActionMethods(object):


    def __init__(self, obj):
        self.obj = obj
        self.mActions = MonopolyActions(obj)

    # Receive observation and an action array
    def receiveAction(self, actions):

        # Current position of the current player
        # TODO
        cp = 0  # replace
        action = actions[0]
        group = actions[1]

        # Spend Money to specified group
        if action > 0:
            # If the current position of the user refer to a property card
            if 1:
                # If his current position is in one of the selected groups then act on this specific position of the group
                if 1:
                    self.spendMoneyOnPosition(cp)
                else:
                    self.spendMoneyOnArea(group)
            # Otherwise spend money on the area that has selected
            else:
                self.spendMoneyOnArea(group)
        elif action < 0:
            self.getMoneyFromArea(group)

    # ######### Region SpendMethods #######

    # Spend money on specific position on board
    def spendMoneyOnPosition(self, cp):
        # Get money from area based on a priority list (maximum earning)
        # We firstly try to unmortgage the property
        if 1:
            # After we unmortgage the property, then to buy it and final to build on the selected area
            if 1:
                self.mActions.buildOnArea(0, 0)

    # Spend money on a specific area
    def spendMoneyOnArea(self, area):
        # Spend money on area based on a priority list ( potential rent)
        done = False
        for i in range(10):
            pos = None
            if 1:
                done = True
                break
        if not done:
            self.mActions.buildOnArea(0, 0)

    # # ######### Region GetMethods #######

    # Get money from specific area
    def getMoneyFromArea(self, area):
        # Get money from area based on a priority list (maximum earning)
        if 1:
            # If we can't sell on the specific group then try to mortgage an area of the group
            tmp = []
            for i in range(len(tmp)):
                if 1:
                    if 1:
                        if 1:
                            break
