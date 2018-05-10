from HelperUtils.applicaiton_context import ApplicationContext


class MonopolyActions(object):
    # Try to buy a property on board
    def buyProperty(self, player, prop):
        # If the specific position isn't a property ( Command Card or Special Position) then don't do anything
        if ApplicationContext().get_instance().board.typeId[prop] == 0:
            # If the player already has this property to his possession then return -1;
            if ApplicationContext().get_instance().getPlayers()[player].propertiesPurchased[ApplicationContext().get_instance().getIndexFromPosition(prop)] == 1:
                return -1
            # If the property isn't currently owned by anyone
            if ApplicationContext().get_instance().properties[prop] < 0:
                if ApplicationContext().get_instance().gamePlayers[player].money >= ApplicationContext().get_instance().gameCards[ApplicationContext().get_instance().getIndexFromPosition(prop)].getValue():
                    # Then assign this property to the player ( both on his fields and on the global public variables
                    ApplicationContext().get_instance().properties[prop] = player
                    ApplicationContext().get_instance().gamePlayers[player].money -= ApplicationContext().get_instance().gameCards[ApplicationContext().get_instance().getIndexFromPosition(prop)].getValue()

                    # Check whether with this buy he has just completed the form of a group.
                    self.checkIfCompleted(player, prop)

                    # Success
                    return 1
            else:
                return -1

        return -1

    # Unmortgage a property
    def unmortgageProperty(self, player, prop):
        # If the current position on the board refers to a property card
        if ApplicationContext().get_instance().board.typeId[prop] == 0:
            if not ApplicationContext().get_instance().properties[prop] == player:
                return -1

            # Then check whether the user has mortgaged this property,if not then return with an error code (-1).
            if ApplicationContext().get_instance().getPlayers()[player].money >= int(1.1 * ApplicationContext().get_instance().getCards()[ApplicationContext().get_instance().getIndexFromPosition(prop)].getMortgageValue()):
                # Otherwise mark this area as unmortgaged
                ApplicationContext().get_instance().getPlayers()[player].mortgagedProperties[ApplicationContext().get_instance().getIndexFromPosition(prop)] = 0

                # Check whether with this buy he has just completed the form of a group.
                self.checkIfCompleted()

                ApplicationContext().get_instance().gamePlayers[player].money -= int(1.1 * ApplicationContext().get_instance().getCards()[ApplicationContext().get_instance().getIndexFromPosition(prop)].getMortgageValue())

                # Success
                return 1

        return -1

    # Build on an area
    def buildOnArea(self, player, group):
        # If the group is smaller than 8 ( not Railways or Electric/Water Works ) and the player has completed this group
        if group > 1 and ApplicationContext().get_instance().completedGroups[group] == player:
            # Try to find the property in that specific group with the fewest buildings on it
            minBuilding = 6
            propertyToBuild = -1

            temp = ApplicationContext().get_instance().gameCardsGroup[group].split(",")
            for i in range(len(temp)):
                if ApplicationContext().get_instance().gamePlayers[player].mortgagedProperties[ApplicationContext().get_instance().getIndexFromPosition(int(temp[i]))] == 1:
                    return -1

                if ApplicationContext().get_instance().buildings[int(temp[i])] <= minBuilding:
                    minBuilding = ApplicationContext().get_instance().buildings[int(temp[i])]
                    propertyToBuild = int(temp[i])

            # If the minimum number of buildings that we found are less than 5 ( so that we can build a hotel at least ) procceed with the build
            if minBuilding < 5:
                # Check whether we can build another house
                if ApplicationContext().get_instance().currentHouses == ApplicationContext().get_instance().getMaxHouses():
                    return -1

                # Check whether we can build another hotel or a house
                if ApplicationContext().get_instance().buildings[propertyToBuild] < 5:
                    if ApplicationContext().get_instance().gamePlayers[player].money >= ApplicationContext().get_instance().getCards()[ApplicationContext().get_instance().getIndexFromPosition(propertyToBuild)].getHouseCost():
                        ApplicationContext().get_instance().currentHouses += 1

                        # Add the info to the player's private fields
                        ApplicationContext().get_instance().getPlayers()[player].buildingsBuilt[ApplicationContext().get_instance().getIndexFromPosition(propertyToBuild)] += 1
                        ApplicationContext().get_instance().buildings[propertyToBuild] += 1

                        ApplicationContext().get_instance().gamePlayers[player].money -= ApplicationContext().get_instance().getCards()[ApplicationContext().get_instance().getIndexFromPosition(propertyToBuild)].getHouseCost()
                else:
                    # Check whether we can build another hotel
                    if ApplicationContext().get_instance().currentHouses == ApplicationContext().get_instance().getMaxHotels():
                        return -1

                    if ApplicationContext().get_instance().gamePlayers[player].money >= ApplicationContext().get_instance().getCards()[ApplicationContext().get_instance().getIndexFromPosition(propertyToBuild)].getHotelCost():
                        ApplicationContext().get_instance().currentHotels += 1
                        ApplicationContext().get_instance().currentHouses -= 4

                        # Add the info to the player's private fields
                        ApplicationContext().get_instance().getPlayers()[player].buildingsBuilt[ApplicationContext().get_instance().getIndexFromPosition(propertyToBuild)] += 1
                        ApplicationContext().get_instance().buildings[propertyToBuild] += 1

                        ApplicationContext().get_instance().gamePlayers[player].money -= ApplicationContext().get_instance().getCards()[ApplicationContext().get_instance().getIndexFromPosition(propertyToBuild)].getHotelCost()

                return 1

        return -1

    # Mortgage a property
    def mortgageProperty(self, player, prop):
        # If the current position refers to a property card then proceed
        if ApplicationContext().get_instance().board.typeId[prop] == 0:
            if not ApplicationContext().get_instance().properties[prop] == player:
                return -1

            group = ApplicationContext().get_instance().gameCards[ApplicationContext().get_instance().getIndexFromPosition(prop)].getGroup()
            for i in range(len(ApplicationContext().get_instance().gameCardsGroup[group].split(","))):
                tmpProp = int(ApplicationContext().get_instance().gameCardsGroup[group].split(",")[i])
                if ApplicationContext().get_instance().buildings[tmpProp] > 0:
                    return -1

            # If the user has already mortgaged this area then return an error code (-1)
            if ApplicationContext().get_instance().getPlayers()[player].mortgagedProperties[ApplicationContext().get_instance().getIndexFromPosition(prop)] == 1:
                return -1

            # If the player has this property under his possesion procceed with the mortgage
            if ApplicationContext().get_instance().getPlayers()[player].propertiesPurchased[ApplicationContext().get_instance().getIndexFromPosition(prop)] == 1:
                # Mark this property as mortgaged
                ApplicationContext().get_instance().getPlayers()[player].mortgagedProperties[ApplicationContext().get_instance().getIndexFromPosition(prop)] = 1

                # Add the money to his balance
                ApplicationContext().get_instance().getPlayers()[player].money += ApplicationContext().get_instance().getCardFromPosition(prop).getMortgageValue()

                # Update the completed groups
                self.checkIfCompleted(player, prop)

                # Success
                return 1

            return -1

        return -1

    # Sell on an area
    def sellOnArea(self, player, group):
        # If the group is smaller than 8 ( not Railways or Electric/Water Works ) and the player has completed this group
        if group > 1 and ApplicationContext().get_instance().completedGroups[group] == player:
            # We'll try to find the property with the maximum number of buildings built on it
            maxBuilding = 0
            propertyToSell = -1

            temp = ApplicationContext().get_instance().gameCardsGroup[group].split(",")
            for i in range(len(temp)):
                if ApplicationContext().get_instance().buildings[int(temp[i])] >= maxBuilding:
                    maxBuilding = ApplicationContext().get_instance().buildings[int(temp[i])]
                    propertyToSell = int(temp[i])

            # If there are buildings available to sell then proceed
            if maxBuilding > 0:
                # Update the variable
                ApplicationContext().get_instance().buildings[propertyToSell] -= 1

                # Check whether it was a hotel or a house to add the proper amount of money to the player's balance
                if ApplicationContext().get_instance().buildings[propertyToSell] < 4:
                    ApplicationContext().get_instance().currentHouses -= 1
                    ApplicationContext().get_instance().getPlayers().money += int(0.5 * ApplicationContext().get_instance().getCardFromPosition(propertyToSell).getHouseCost())

                else:
                    ApplicationContext().get_instance().currentHotels -= 1
                    ApplicationContext().get_instance().currentHouses += 4
                    ApplicationContext().get_instance().getPlayers()[player].money += int(0.5 * ApplicationContext().get_instance().getCardFromPosition(propertyToSell).getHotelCost())

                # Update player's personal fields
                ApplicationContext().get_instance().getPlayers()[player].buildingsBuilt[ApplicationContext().get_instance().getIndexFromPosition(propertyToSell)] -= 1

                # Success
                return 1

        # Else try to mortgage the most expensive
        else:
            tmp = ApplicationContext().get_instance().gameCardsGroup[group].split(",")
            for i in range(len(tmp)):
                if ApplicationContext().get_instance().properties[int(tmp[i])] == player:
                    self.mortgageProperty(player, int(tmp[i]))

        return -1

    # Helper method to check whether a group is completed or not
    def checkIfCompleted(self, player, cp):
        # If the position refers to a property card
        if ApplicationContext().get_instance().board.typeId[cp] == 0:
            # We firstly identify the group
            group = ApplicationContext().get_instance().getCards()[ApplicationContext().get_instance().getIndexFromPosition(cp)].getGroup()

            # boolean variable to determine whether the group is completed
            isCompleted = True
            tmp = ApplicationContext().get_instance().gameCardsGroup[group].split(",")

            # If we find at least one property where it doesn't belong to the current player then the group isn't complete.
            for i in range(len(tmp)):
                if ApplicationContext().get_instance().getPlayers()[player].propertiesPurchased[ApplicationContext().get_instance().getIndexFromPosition(int(tmp[i]))] == 0:
                    isCompleted = False

            # Update the specified info
            if isCompleted:
                ApplicationContext().get_instance().completedGroups[group] = player
            else:
                ApplicationContext().get_instance().completedGroups[group] = -1

    # Pay to either the bank or to another player
    def payMoney(self, pFrom, pTo, amount):
        if not ApplicationContext().get_instance().gamePlayers[pFrom].isAlive:
            return -1

        # If pTo = -1 then it is the bank
        # Check whether the current player has the required amount of money to pay
        if not self.checkPayment(pFrom, amount):
            # If he can't pay then return -1
            return -1

        # Else proceed with the payment
        else:
            ApplicationContext().get_instance().gamePlayers[pFrom].money -= amount
            if pTo > -1:
                ApplicationContext().get_instance().gamePlayers[pTo].money += amount
            return 1

    # Sell a property ( or a building ) from player in order to generate more cash
    def sellProperty(self, player):
        # Here we'll use the selloOnArea method created above in order to get more cash by either
        # selling buildings or mortgaging properties starting from the most expensive group
        area = 9
        done = False

        while not done:
            if self.sellOnArea(player, area) > 0:
                done = True
            if not done:
                area -= 1
            if area < 2:
                done = True

        pos = 39
        done = False
        while not done:
            if self.mortgageProperty(player, pos) > 0:
                done = True

            if not done:
                pos -= 1

            if pos < 0:
                done = True

    # Check whether the user can pay the amount
    def checkPayment(self, player, amount):
        if ApplicationContext().get_instance().gamePlayers[player].money >= amount:
            return True
        else:
            return False

    # Calculate value of all the player's assets
    def calculateAllAssets(self, player):
        total = 0.0

        # Start by adding the player's cash to the total amount
        total += ApplicationContext().get_instance().gamePlayers[player].money

        # Add all the value of all the buildings and the potential mortgages he has
        for i in range(len(ApplicationContext().get_instance().gamePlayers[player].buildingsBuilt)):
            if ApplicationContext().get_instance().gamePlayers[player].buildingsBuilt[i] < 4:
                total += ApplicationContext().get_instance().gamePlayers[player].buildingsBuilt[i] * (0.5 * ApplicationContext().get_instance().gameCards[i].getHouseCost())
            else:
                total += 4 * (0.5 * ApplicationContext().get_instance().gameCards[i].getHouseCost())
                total += 0.5 * ApplicationContext().get_instance().gameCards[i].getHotelCost()

            if ApplicationContext().get_instance().gamePlayers[player].propertiesPurchased[i] == 1 and ApplicationContext().get_instance().gamePlayers[player].mortgagedProperties[i] == 0:
                total += ApplicationContext().get_instance().gameCards[i].getMortgageValue()

        return int(total)
