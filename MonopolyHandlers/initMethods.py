import os
import xml.etree.ElementTree as ET
from Classes.card import Card
from Classes.specialPositonCard import SpecialPositionCard
from Classes.propertyCard import PropertyCard
from RLHandlers.rlEnvironment import  RLEnvironment


class InitMethods(object):

    # ######### Region SetMethods #########

    def setCommandCards(self):

        try:
            # XML reader to store the commandCards
            if os.path.isfile(self.file_name):

                tree = ET.parse(self.file_name)
                root_node = tree.getroot()

                for node in root_node:
                    p_card = PropertyCard(node.find('Name').text, node.find('Position').text, node.find('Price').text,
                                          'nns', node.find('Mortgage').text, node.find('HouseCost').text,
                                          node.find('HotelCost').text, node.find('Group').text)
                    self.p_cards.append(p_card)

                for p_card in self.p_cards:
                    print(p_card.card_name)
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
