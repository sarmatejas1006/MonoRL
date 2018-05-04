class MonopolyActions(object):
    # Try to buy a property on board
    def buyProperty(self, player, prop):
        # If the specific position isn't a property ( Command Card or Special Position) then don't do anything
        # If the player already has this property to his possession then return -1;
        # If the property isn't currently owned by anyone
        # Then assign this property to the player ( both on his fields and on the global public variables
        # Check whether with this buy he has just completed the form of a group.
        pass

    # Unmortgage a property
    def unmortgageProperty(self, player, prop):
        # If the current position on the board refers to a property card
        # Then check whether the user has mortgaged this property,if not then return with an error code (-1).
        # Otherwise mark this area as unmortgaged
        # Check whether with this buy he has just completed the form of a group.
        pass

    # Build on an area
    def buildOnArea(self, player, group):
        # If the group is smaller than 8 ( not Railways or Electric/Water Works ) and the player has completed this group
        # Try to find the property in that specific group with the fewest buildings on it
        # If the minimum number of buildings that we found are less than 5 ( so that we can build a hotel at least ) procceed with the build
        # Check whether we can build another house
        # Check whether we can build another hotel
        pass

    # Mortgage a property
    def mortgageProperty(self, player, prop):
        # If the current position refers to a property card then procceed
        # If the user has already mortgaged this area then return an error code (-1)
        # If the player has this property under his possesion procceed with the mortgage
        # Mark this property as mortgaged
        # Add the money to his balance
        # Update the completed groups
        pass

    # Sell on an area
    def sellOnArea(self, player, group):
        # If the group is smaller than 8 ( not Railways or Electric/Water Works ) and the player has completed this group
        # We'll try to find the property with the maximum number of buildings built on it
        # If there are buildings available to sell then procceed
        # Update the variable
        # Check whether it was a hotel or a house to add the proper amount of money to the player's balance
        # Update player's personal fields
        # Else try to mortgage the most expensive
        pass

    # Helper method to check whether a group is completed or not
    def checkIfCompleted(self, player, cp):
        # If the position refers to a property card
        # We firstly identify the group
        # boolean variable to determine whether the group is completed
        # If we find at least one property where it doesn't belong to the current player then the group isn't complete.
        # Update the specified info
        pass

    # Pay to either the bank or to another player
    def payMoney(self, pFrom, pTo, amount):
        # If pTo = -1 then it is the bank
        # Check whether the current player has the required amount of money to pay
        # If he can't pay then return -1
        # Else proceed with the payment
        pass

    # Sell a property ( or a building ) from player in order to generate more cash
    def sellProperty(self, player):
        # Here we'll use the selloOnArea method created above in order to get more cash by either
        # selling buildings or mortgaging properties starting from the most expensive group
        pass

    # Check whether the user can pay the amount
    def checkPayment(self, player, amount):
        pass

    # Calculate value of all the player's assets
    def calculateAllAssets(self, player):
        # Start by adding the player's cash to the total amount
        # Add all the value of all the buildings and the potential mortgages he has
        pass
