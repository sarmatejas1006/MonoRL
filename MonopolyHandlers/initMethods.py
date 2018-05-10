import os
import xml.etree.ElementTree as ET
from Classes.card import Card
from Classes.specialPositonCard import SpecialPositionCard
from Classes.commandCard import CommandCard
from Classes.propertyCard import PropertyCard
from RLHandlers.rlEnvironment import RLEnvironment
#from HelperUtils.applicaiton_context import ApplicationContext
from Classes.board import Board


class InitMethods(object):

    # ######### Region SetMethods #########

    def __init__(self):

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
                    RLEnvironment().get_instance().addCommandCard(p_card)
                    #ApplicationContext().get_instance().addCommandCard(p_card)
                    #ApplicationContext().get_instance().setCommandCards()

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

                    #ApplicationContext().get_instance().addPropertyCard(p_card)
                    #ApplicationContext().get_instance().setPropertyCards()

        except Exception as e:
            print('Exception encountered: ', str(e))
            return False

        return True

    def setBoard(self):

        b = [] # Card[]
        t = []

        for i in range(40):
            t.append(-1)

        # Add PropertyCards

       # for i in range(len(ApplicationContext().get_instance().getCards())):
           # b[ApplicationContext().get_instance().getCards()[i].getPosition()] = ApplicationContext().get_instance().getCards()[i]
           # t[ApplicationContext().get_instance().getCards()[i].getPosition()] = 0

        # Add CommunityChestCards

       # for i in range(len(ApplicationContext().get_instance().getCommunityCardPositions())):
            #b[ApplicationContext().get_instance().getCommunityCardPositions()[i]] = CommandCard()
            #t[ApplicationContext().get_instance().getCommunityCardPositions()[i]] = 1

        # Add ChanceCards
       # for i in range(len(ApplicationContext().get_instance().getChanceCardPositions())):
         #   b[ApplicationContext().get_instance().getChanceCardPositions()[i]] = CommandCard()
          #  t[ApplicationContext().get_instance().getChanceCardPositions()[i]] = 2

        b = [Card() for i in range(40)]  # empty card array
        t = [-1] * 40  # int array of -1

        # Specify that every position left on board is a special position ( GO, Jail, etc... )
        # We'll take care of what occurs on every case in a different method
        for i in range(len(b)):
            if t[i] < 0:
                t[i] = 3
                b[i] = SpecialPositionCard()

        # Set the global board parameter
        #ApplicationContext().get_instance().setBoard(Board(b, t))

