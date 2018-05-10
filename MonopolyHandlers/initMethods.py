import os
import xml.etree.ElementTree as ET
from Classes.card import Card
from Classes.specialPositonCard import SpecialPositionCard
from Classes.commandCard import CommandCard
from Classes.propertyCard import PropertyCard
from RLHandlers.rlEnvironment import  RLEnvironment


class InitMethods(object):

    # ######### Region SetMethods #########

    def __init__(self):
        self.rlEnvironment = RLEnvironment()
        self.file_name_command = 'Data/CommandCards.xml'
        self.file_name_property = 'Data/Properties.xml'

    def setCommandCards(self):

        try:
            # XML reader to store the commandCards
            if os.path.isfile(self.file_name_command):

                tree = ET.parse(self.file_name_command)
                root_node = tree.getroot()

                for node in root_node:
                    p_card = CommandCard(node.find('TypeOfCard').text, node.find('Text').text, node.find('FixedMove').text,
                                          node.find('Collect').text, node.find('MoneyTransaction').text, node.find('PlayersInteraction').text,
                                          node.find('HouseMultFactor').text, node.find('HotelMultFactor').text)
                    self.rlEnvironment.addCommandCard(p_card)
                    self.rlEnvironment.setCommandCards()

        except Exception as e:
            print('Exception encountered: ', str(e))
            return False

        return True

    def setPropertyCards(self):
        try:
            # XML reader to store the commandCards
            if os.path.isfile(self.file_name_command):

                tree = ET.parse(self.file_name_command)
                root_node = tree.getroot()

                for node in root_node:
                    rent = []
                    rentString = node.find('Rent').text.split(',')
                    for s in rentString:
                        rent.append(int(s));

                    p_card = PropertyCard(node.find('Name').text, node.find('Position').text,
                                          node.find('Price').text,
                                          rent,
                                          node.find('Mortage').text,
                                          node.find('HouseCost').text,
                                          node.find('HotelCost').text, node.find('Group').text)

                    self.rlEnvironment.addPropertyCard(p_card)
                    self.rlEnvironment.setPropertyCards()

        except Exception as e:
            print('Exception encountered: ', str(e))
            return False

        return True

    def setBoard(self):

        Card = []
        t = []

        for i in range(40):
            t.append(-1)

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
