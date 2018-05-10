from MonopolyHandlers.monopolyActions import MonopolyActions



class ActionMethods(object):

    def __init__(self, rl_env_obj):
        self.mActions = MonopolyActions(rl_env_obj)
        self.rl_env_obj = rl_env_obj


    # Receive observation and an action array
    def receiveAction(self, actions):

        # Current position of the current player
        cp = self.rl_env_obj.currentPosition
        action = actions[0]
        group = actions[1]

        # Spend Money to specified group
        if action > 0:
            # If the current position of the user refer to a property card
            if self.rl_env_obj.board.typeId[cp] == 0:
                # If his current position is in one of the selected groups then act on this specific position of the group
                if self.rl_env_obj.getCardFromPosition(cp).getGroup() == group:
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
        if self.mActions.buyProperty(self.rl_env_obj.currentPlayer, cp) < 0:
            # After we unmortgage the property, then to buy it and final to build on the selected area
            if self.mActions.unmortgageProperty(self.rl_env_obj.currentPlayer, cp) < 0:
                self.mActions.buildOnArea(self.rl_env_obj.currentPlayer, self.rl_env_obj.getCards()[self.rl_env_obj.getIndexFromPosition(cp)].getGroup())

    # Spend money on a specific area
    def spendMoneyOnArea(self, area):
        # Spend money on area based on a priority list ( potential rent)
        done = False
        for i in range(len(self.rl_env_obj.gameCardsGroup[area].split(','))):
            pos = int(str(self.rl_env_obj.gameCardsGroup[area].Split(',')[i]))
            if self.mActions.unmortgageProperty(self.rl_env_obj.currentPlayer, pos) > 0:
                done = True
                break
        if not done:
            self.mActions.buildOnArea(self.rl_env_obj.currentPlayer, area)

    # # ######### Region GetMethods #######

    # Get money from specific area
    def getMoneyFromArea(self, area):
        # Get money from area based on a priority list (maximum earning)
        if self.mActions.sellOnArea(self.rl_env_obj.currentPlayer, area) < 0:
            # If we can't sell on the specific group then try to mortgage an area of the group
            tmp = self.rl_env_obj.gameCardsGroup[area].split(',')
            for j in range(len(tmp)):
                if self.rl_env_obj.getPlayers()[self.rl_env_obj.currentPlayer].propertiesPurchased[self.rl_env_obj.getIndexFromPosition(int(tmp[j]))] == 1:
                    if self.rl_env_obj.getPlayers()[self.rl_env_obj.currentPlayer].mortgagedProperties[self.rl_env_obj.getIndexFromPosition(int(tmp[j]))] == 0:
                        if self.mActions.mortgageProperty(self.rl_env_obj.currentPlayer, int(tmp[j])) > 0:
                            break
