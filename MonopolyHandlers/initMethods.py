from Classes.card import Card
from Classes.specialPositonCard import SpecialPositionCard


class InitMethods(object):

    # ######### Region SetMethods #########

    def setCommandCards(self):
        try:
            # Create XML reader to store the commandCards
            pass
        except Exception as e:
            print('Exception encountered: ', str(e))
            return False

        return True

    def setPropertyCards(self):
        try:
            # Create XML reader to store the propertyCards
            pass
        except Exception as e:
            print('Exception encountered: ', str(e))
            return False

        return True

    def setBoard(self):
        # Add PropertyCards
        # Add CommunityChestCards
        # Add ChanceCards

        b = [Card() for i in range(40)]  # empty card array
        t = [-1] * 40  # int array of -1

        # Specify that every position left on board is a special position ( GO, Jail, etc... )
        # We'll take care of what occurs on every case in a different method
        for i in range(len(b)):
            if t[i] < 0:
                t[i] = 3
                b[i] = SpecialPositionCard()

        # Set the global board parameter

        pass
